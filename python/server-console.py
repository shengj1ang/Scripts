import time, sys, os, platform, threading, random, subprocess, socket
from flask import Flask, request, send_from_directory, redirect, jsonify, session, send_file, abort
from flask_basicauth import BasicAuth #pip install Flask-BasicAuth
import psutil
import queue 

app = Flask(__name__)
app.secret_key = 'your_secret_key' 
app_port=8000
app_debug=False
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'
basic_auth = BasicAuth(app)

def get_system_info():
    os_info = {
        "OS Type": platform.system(),
        "OS Release": platform.release(),
        "OS Version": platform.version()
    }
    cpu_info = {
        "Physical Cores": psutil.cpu_count(logical=False),
        "Total Cores": psutil.cpu_count(logical=True),
        "Max Frequency": psutil.cpu_freq().max if psutil.cpu_freq() else None,
        "Current Frequency": psutil.cpu_freq().current if psutil.cpu_freq() else None,
        "CPU Usage": psutil.cpu_percent(interval=1)
    }
    memory_info = psutil.virtual_memory()
    ram_info = {
        "Total Memory": memory_info.total,
        "Available Memory": memory_info.available,
        "Used Memory": memory_info.used,
        "Memory Usage": memory_info.percent
    }
    disk_info = {}
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info[partition.device] = {
                "Mountpoint": partition.mountpoint,
                "Total Size": usage.total,
                "Used": usage.used,
                "Free": usage.free,
                "Percent Used": usage.percent
            }
        except PermissionError:
            # 无法访问某些分区（如系统保留分区）时，忽略这些分区
            continue

    # NetWork
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    network_info = {
        "Hostname": hostname,
        "IP Address": ip_address
    }

    return {
        "Operating System": os_info,
        "CPU": cpu_info,
        "RAM": ram_info,
        "Disk": disk_info,
        "Network": network_info
    }
    
def get_basic_info():
    try:
        return(f"{platform.system()} {platform.release()} ({socket.gethostname()}, {socket.gethostbyname(socket.gethostname())}) ")
    except Exception as ex:
        return(f"{platform.system()} {platform.release()}")

def reboot_system():
    os_type = platform.system().lower()
    try:
        if os_type == 'windows':
            subprocess.run(["shutdown", "/r", "/t", "0"], check=True)
        elif os_type in ['linux', 'darwin']:  # darwin is for MacOS
            subprocess.run(["sudo", "reboot"], check=True)
        else:
            print(f"Unsupported operating system: {os_type}")
    except Exception as e:
        print(f"Error rebooting system: {e}")

def shutdown_system():
    os_type = platform.system().lower()
    try:
        if os_type == 'windows':
            subprocess.run(["shutdown", "/s", "/t", "0"], check=True)
        elif os_type in ['linux', 'darwin']:  # darwin is for MacOS
            subprocess.run(["sudo", "shutdown", "-h", "now"], check=True)
        else:
            print(f"Unsupported operating system: {os_type}")
    except Exception as e:
        print(f"Error shutting down system: {e}")
        
def run_command(command, output_queue):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    for line in iter(process.stdout.readline, ''):
        output_queue.put(line)
    process.stdout.close()
    process.wait()

basic_info=get_basic_info()

@app.route('/')
@basic_auth.required
def page_index():
    return(f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>Console</title>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <link rel="icon" href="https://static.kkk.plus/favicon/favicon.png" sizes="23x23" type="image/x-icon">
    </head>
    <body>
    <h1>控制台</h1>
    <h3>{basic_info}</h3>
    <h5>详细解释：<br>
        sysinfo（获取详细的系统信息）<br>
        shutdown（关机）<br>
        reboot（重启）<br>
        shell（进入控制台模式，使用exit退出）<br>
        download [filename]（下载文件，需要在shell命令内使用）<br>
        upload（上传文件，需要在shell命令内使用）<br>
        clear（清空Terminal）</h5>
    <div id="tab_1">
        <iframe src="/terminal"
                height="500"
                width=100%
                frameborder="0"
                scrolling="0"
        ></iframe>
    </div>
    </body>
    </html> 
    """)
    
@app.route('/terminal')
@basic_auth.required
def page_terminal():
    return(f"""
        <!DOCTYPE html>
        <html>
        <head>
        <title>Terminal</title>

        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <link rel="icon" href="https://static.kkk.plus/favicon/favicon.png" sizes="23x23" type="image/x-icon">
        <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/jquery.terminal/js/jquery.terminal.min.js"></script>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/jquery.terminal/css/jquery.terminal.min.css"/>
        </head>
        <body>
            <input type="file" id="fileInput" style="display: none;">
        </body>
        
      
    <script>
        $(function() {{
            var fileInput = $('#fileInput');
            fileInput.on('change', function(e) {{
                var file = e.target.files[0];
                if (!file) {{
                    return;
                }}

                var formData = new FormData();
                formData.append('file', file);

                $.ajax({{
                    url: '/api/upload',
                    type: 'POST',
                    data: formData,
                    processData: false,
                    contentType: false,
                    success: function(response) {{
                        terminal.echo(response);
                    }},
                    error: function() {{
                        terminal.error("Error during file upload.");
                    }}
                }});
            }});

            var terminal = $('body').terminal({{
                sysinfo: function() {{
                    return fetch("/api/get_system_info")
                    .then(r => r.text());
                }},
                reboot: function() {{
                    return fetch('/api/reboot')
                    .then(r => r.text());
                }},
                status: function() {{
                    return fetch('/status')
                    .then(r => r.text());
                }},
                statistics: function() {{
                    return fetch('/statistics')
                    .then(r => r.text());
                }},
                help: function() {{
                    return fetch('/help')
                    .then(r => r.text());
                }},
                appinfo: function() {{
                    return fetch('/appinfo')
                    .then(r => r.text());
                }},
                shell: function() {{
                    this.push(function(command) {{
                        if (command.toLowerCase() === 'exit') {{
                            this.pop();
                        }} else if (command.toLowerCase().startsWith('download ')) {{
                            const filename = command.split(' ')[1];
                            window.open(`/api/download?file=${{filename}}`);
                        }} else if (command.toLowerCase() === 'upload') {{
                            fileInput.click();
                        }} else {{
                            fetch('/api/execute', {{
                                method: 'POST',
                                headers: {{ 'Content-Type': 'application/json' }},
                                body: JSON.stringify({{ command: command }})
                            }})
                            .then(r => r.text())
                            .then(r => this.echo(r));
                        }}
                    }}, {{
                        prompt: 'shell> '
                    }});
                }}  
            }}, {{
                greetings: '一个在线命令行，你可以在以下输入命令'
            }});
        }});
    </script>
        </html>


    """)
@app.route('/api/get_system_info')
@basic_auth.required
def api_get_system_info():
    return(str(get_system_info()))

@app.route('/api/reboot')
@basic_auth.required
def api_reboot():
    reboot_system()
                
@app.route('/api/shutdown')
@basic_auth.required
def api_shutdown():
    shutdown_system()


@app.route("/api/execute", methods=['POST'])
@basic_auth.required
def api_execute():
    data = request.get_json()
    command = data.get("command")
    timeout = data.get("timeout", 30)  # 默认超时时间为30秒
    if 'cwd' not in session:
        session['cwd'] = os.getcwd()

    if command.startswith('cd'):
        try:
            if 'cwd' in session:
                os.chdir(session['cwd'])
            # 获取新目录路径
            new_dir = command.split(maxsplit=1)[1]
            # 更新session中的当前工作目录
            os.chdir(new_dir)
            session['cwd'] = os.getcwd()
            return f"Changed directory to {session['cwd']}"
        except Exception as e:
            return f"Error changing directory: {e}"
    elif command.startswith('download '):
        file_path = command.split(maxsplit=1)[1]
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        if os.path.exists(file_path):
            return send_from_directory(directory, filename, as_attachment=True)
        else:
            return f"File not found: {filename}"
    try:
        if command.startswith("ls") and platform.system().lower()=="windows":
            command="dir"
        elif command.startswith("ll") and platform.system().lower()=="windows":
            command="dir"
        # 执行其他命令
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, cwd=session['cwd'])
        return output.decode()
    except subprocess.CalledProcessError as e:
        return e.output.decode()

    return f"No command provided"

    '''
    if command:
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            output = e.output
        return output.decode()
    return f"No command provided"
    '''
    '''
    if command:
        output_queue = queue.Queue()
        command_thread = threading.Thread(target=run_command, args=(command, output_queue))
        command_thread.start()

        output = []
        start_time = time.time()

        # 收集输出，直到线程结束或超时
        while command_thread.is_alive():
            try:
                line = output_queue.get_nowait()
                output.append(line)
            except queue.Empty:
                if time.time() - start_time > timeout:
                    process.terminate()
                    output.append("\nCommand terminated due to timeout.")
                    break
                time.sleep(0.1)  # 短暂等待，以减少CPU使用

        return jsonify(output)
    return "No command provided"
    '''


@app.route('/api/download')
@basic_auth.required
def api_download():
    file=request.args.get('file')
    if 'cwd' not in session:
        session['cwd'] = os.getcwd()
    full_path=session['cwd']+"/"+file
    if os.path.isfile(full_path):
        return send_file(full_path, as_attachment=True)
    else:
        # 如果文件不存在或不是一个文件，则返回404错误
        abort(404, description="File not found or is not a file")


@app.route('/api/upload',methods=['POST'])
@basic_auth.required
def api_upload():
    if 'cwd' not in session:
        session['cwd'] = os.getcwd()
    
    if 'file' not in request.files:
        return 'No file part in the request', 400
    file = request.files['file']
    if file.filename == '':
        return 'No file selected for uploading', 400
    if file:
        filename = file.filename
        save_path = os.path.join(session['cwd'], filename)
        file.save(save_path)
        return f'File {filename} uploaded successfully'
    return 'Error during file upload', 500
    
    if os.path.isfile(full_path):
        return send_file(full_path, as_attachment=True)
    else:
        # 如果文件不存在或不是一个文件，则返回404错误
        abort(404, description="File not found or is not a file")
        
        
if __name__ == '__main__':
   
    app.run('0.0.0.0', port=app_port, debug=app_debug)