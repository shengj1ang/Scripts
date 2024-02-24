from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
   return 'Invalid Requests'

@app.route('/upload', methods=["GET"])
def web_page_upload():
   return('''<html>
<head>
  <title>File Upload</title>
</head>
<body>
    <form action="/upload" method="POST" enctype="multipart/form-data">
        <input type="file" name="file"  />
        <input type="submit" value="提交" />
    </form>
</body>
</html>''')


@app.route("/upload", methods=["POST"])
def save_file():
    data = request.files
    #print("start...")
    #print(type(data))
    #print(data)
    file = data['file']
    print(file.filename)
    #print(request.headers)
    file.save("files/"+file.filename)
    #print("end...")
    return('''<html>
<head>
  <title>File Upload</title>
</head>
<body>
    <form action="/upload" method="POST" enctype="multipart/form-data">
        <input type="file" name="file"  />
        <input type="submit" value="提交" />
    </form>
<h1>上传成功</h1>
</body>
</html>''')

if __name__ == '__main__':
   #app.run(port=37000,  debug=True)
   app.run('0.0.0.0',port=37000, ssl_context=('tls/server.crt', 'tls/server.key'), debug=False)
