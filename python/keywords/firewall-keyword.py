# -*- coding: UTF-8 -*-
import requests
import base64
import urllib.parse
from random import choice
import threading
import time
import sys
out_file = "proxy.txt"
def check_list(socks_file):
	print("> Checking list")
	temp = open(socks_file).readlines()
	temp_list = []
	for i in temp:
		if i not in temp_list:
			if ':' in i and '#' not in i:
				try:
					socket.inet_pton(socket.AF_INET,i.strip().split(":")[0])#check valid ip v4
					temp_list.append(i)
				except:
					pass
	rfile = open(socks_file, "wb")
	for i in list(temp_list):
		rfile.write(bytes(i,encoding='utf-8'))
	rfile.close()
	
def DownloadProxies(proxy_ver):
	if proxy_ver == "4":
		f = open(out_file,'wb')
		socks4_api = [
			"https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4&country=all",
			"https://www.proxy-list.download/api/v1/get?type=socks4",
			"https://www.proxyscan.io/download?type=socks4",
			"https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
			'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt',
			"https://api.openproxylist.xyz/socks4.txt",
			"https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
			"https://www.freeproxychecker.com/result/socks4_proxies.txt",
			"https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
		]
		for api in socks4_api:
			try:
				r = requests.get(api,timeout=5)
				f.write(r.content)
			except:
				pass
		f.close()
		try:#credit to All3xJ
			r = requests.get("https://www.socks-proxy.net/",timeout=5)
			part = str(r.content)
			part = part.split("<tbody>")
			part = part[1].split("</tbody>")
			part = part[0].split("<tr><td>")
			proxies = ""
			for proxy in part:
				proxy = proxy.split("</td><td>")
				try:
					proxies=proxies + proxy[0] + ":" + proxy[1] + "\n"
				except:
					pass
				fd = open(out_file,"a")
				fd.write(proxies)
				fd.close()
		except:
			pass
	if proxy_ver == "5":
		f = open(out_file,'wb')
		socks5_api = [
			"https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all&simplified=true",
			"https://www.proxy-list.download/api/v1/get?type=socks5",
			"https://www.proxyscan.io/download?type=socks5",
			"https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
			"https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
			"https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
			"https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
			"https://api.openproxylist.xyz/socks5.txt",
			"https://www.freeproxychecker.com/result/socks5_proxies.txt",
			#"http://www.socks24.org/feeds/posts/default"
		]
		for api in socks5_api:
			try:
				r = requests.get(api,timeout=5)
				f.write(r.content)
			except:
				pass
		f.close()
	if proxy_ver == "http":
		f = open(out_file,'wb')
		http_api = [
			"https://api.proxyscrape.com/?request=displayproxies&proxytype=http",
			"https://www.proxy-list.download/api/v1/get?type=http",
			"https://www.proxyscan.io/download?type=http",
			#"http://spys.me/proxy.txt",
			"https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
			"https://api.openproxylist.xyz/http.txt",
			"https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt",
			"http://alexa.lr2b.com/proxylist.txt",
			"http://rootjazz.com/proxies/proxies.txt",
			"https://www.freeproxychecker.com/result/http_proxies.txt",
			"http://proxysearcher.sourceforge.net/Proxy%20List.php?type=http",
			"https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
			"https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
			"https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
			"https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt"
			"https://proxy-spider.com/api/proxies.example.txt",
			"https://multiproxy.org/txt_all/proxy.txt",
			"https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
			"https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/http.txt",
			"https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/https.txt",
		]
		for api in http_api:
			try:
				r = requests.get(api,timeout=5)
				f.write(r.content)
			except:
				pass
		f.close()
	print("> Have already downloaded proxies list as "+out_file)


url_base=["http://bear.mtyxt.com:32060/","http://bear.mtyxt.com:32075/","http://bear.mtyxt.com:9005/","http://bear.mtyxt.com:32070/","http://bear.mtyxt.com:10000/","http://bear.mtyxt.com:32072/","http://bear.mtyxt.com:5000/","http://bear.mtyxt.com:32071/","http://bear.mtyxt.com:5005/","http://bear.mtyxt.com:32073/","http://bear.mtyxt.com:8096/"]
url_proxy=["https://api-fetcher.deno.dev/","https://kkkplus.000webhostapp.com/fetch/?key=WKPjMZ9BtpHUwAV&target="]

with open("keywords.txt","r") as f:
    keywords=f.readlines()

with open("proxy.txt","r") as f:
    proxylist=f.readlines()
def get_keyword():
    return choice(keywords).replace("\n","")
def get_url_base():
    return choice(url_base)
def get_url_proxy():
    return choice(url_proxy)
def get_proxy():
    return choice(proxylist).replace("\n","")
def thread_req_kkk(threadname):
    err=0
    while True:
        try:
            if err>99:
                break
            keyword=get_keyword()
            print("[Thread_{}] {}".format(str(threadname),keyword))
            keyword=urllib.parse.quote(keyword)
            url_req=get_url_base()+keyword
            url_req=url_req.encode()
            url_req_proxy=get_url_proxy()+base64.b64encode(url_req).decode()
            #print(url_req_proxy)
            r=requests.get(url_req_proxy,timeout=3)
            print("[Thread_{}] {}".format(str(threadname),r))
            #print(r.content.decode())
            
        except Exception as ex:
            print(ex)
            err+=1

def thread_req_proxylist(threadname):
    err=0
    while True:
        try:
            if err>99:
                break
            keyword=get_keyword()
            print("[Thread_{}] {}".format(str(threadname),keyword))
            keyword=urllib.parse.quote(keyword)
            #url_req=get_url_base()+keyword
            #url_req=url_req.encode()
            #url_req_proxy=get_url_proxy()+base64.b64encode(url_req).decode()
            #print(url_req_proxy)
            r=requests.get("https://ip.kkk.plus/ip",timeout=3,proxies={'sockns5':get_proxy()})
            print("[Thread_{}] {}".format(str(threadname),r))
            print(r.content.decode())
            
        except Exception as ex:
            print(ex)
            err+=1

            
if len(sys.argv)<2:
    print("Argument Required")
elif sys.argv[1]=="kkk":
    n=1
    while n<=10:
        x=threading.Thread(target=thread_req_kkk, args=(n,))
        x.start()
        n+=1
elif sys.argv[1]=="thread_req_proxylist":
    n=1
    while n<=10:
        x=threading.Thread(target=thread_req_proxylist, args=(n,))
        x.start()
        n+=1
elif sys.argv[1]=="DownloadProxies":
    DownloadProxies("http")
elif  sys.argv[1]=="check_list":
    check_list("proxy.txt")
else:
    print("Invaild Argument")
