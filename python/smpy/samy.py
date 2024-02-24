import requests
import binascii
import sys

sys.set_int_max_str_digits(0)


def phare(bindata,interval):
    j=1
    e=""
    for i in str(bindata):
        if j%interval==0:
            e+=i+" "
        else:
            e+=i
        j+=1
    e=e.split(" ")
    
    return e

def step_1():#Requests Load.js
    headers={"Accept": "*/*", 
            "Accept-Encoding": "gzip, deflate, br", 
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6",
            "Connection": "keep-alive", 
            "Cookie": "adminpwd=NTk2Zjc1MjA2NjZmNzU2ZTY0MjA0NTYxNzM3NDY1NzIyMDQ1Njc2NzIwMjMzMTIx; envcookie=973610764; __utms=1; acgroupswithpersist=nada; __utmq=1; acopendivids=rest3",
            "DNT": "1",
            "Host": "samy.pl", 
            "Referer": "https://samy.pl/",
            "sec-ch-ua": "",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "", 
            "Sec-Fetch-Dest": "script",
            "Sec-Fetch-Mode": "no-cors", 
            "Sec-Fetch-Site": "same-origin", 
            "User-Agent": "Mozilla/5.0 (linux; u; android 9; zh-cn; v1816a build/pkq1.180819.001) applewebkit/537.36 (khtml, like gecko) version/4.0 chrome/57.0.2987.108 quark/4.2.1.138 mobile safari/537.36"}
    x=requests.get("https://samy.pl/load.js",headers=headers)
    print(x.content)
    with open("load.js","w") as f:
        f.write(str(x.content))

def step_2():#Decode js
    with open("load.js","r") as f:
        x=f.read()

    x=x[x.find("//")+2:x.find("/.source.repla")]
    x=x.replace(" ","0")
    x=x.replace("\\t","1")
    x=phare(x,4)


    #print(x)
    group=False
    res=[]
    for t in x:
        if group==False:
            t_1=int(t,2)
            group=True
        else:
            t_2=int(t,2)
            res.append(chr(int(str(t_1)+str(t_2))))
            group=False
    print(res)

    
    


    #list=res.split(" ")
    #for i in list:
    #    print(i.decode('ascii'))
    
    #x=hex(int(x,2)) #bin to hex
    #x=int(x,2)
    
    #n = int('0b'+x, 2)


    #g=phare_bin(n)

    #g=phare_bin(x)

    #print(g[0])
    #v=""
    #for k in g:
        #v+=(chr(eval("0b"+k)))
        #v+=binascii.a2b_uu(str(k)).decode("utf-8")

    #print(v)

    
    #binx=n.to_bytes((n.bit_length() + 7) // 8, 'little')
    #binx=binx.decode( errors='ignore')
    #binx=binx.decode("utf-16")
    #print(binx)
    #with open("bin.txt","wb") as f:
     #   f.write(binx)


def step_3():
     with open("bin.txt","rb") as f:
        f = f.read()
        c= f.decode('utf-16le', errors='ignore')
        print(c)
    

def decode_3():
    with open("load_t.js","r") as f:
        x=f.read()
        x=x[1:]
        while True:
            if len(x)<8:
                break
            t=x[:7]
            x=x[len(t):]
            print(t)
        return("")
            


print(decode_3())