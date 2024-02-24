import sys
if len(sys.argv)<2:
    print("Argument Required")
    sys.exit()
with open("keywords.txt","r") as f:
    list_init=f.readlines()
keywords=[]
for i in list_init:
    keyword=i.replace("\n","").replace(" ","")
    if keyword not in keywords:
        keywords.append(keyword)
#print(len(keywords))
res=[]
if sys.argv[1]=="f":
    with open("passage.txt","r") as f:
        list_passage=f.readlines()
    text=""
    for i in list_passage:
        text+=i.replace("\n","").replace(" ","")
    for i in keywords:
        if i in text and i!="":
            res.append(i)  
elif sys.argv[1]=="clean":
    with open("keywords.txt","r") as f:
        list_init=f.readlines()
    keywords=[]
    res=""
    for i in list_init:
        keyword=i.replace("\n","").replace(" ","")
        if keyword not in keywords and len(keyword)>1:
            keywords.append(keyword)
    for i in keywords:
        res+=i+"\n"
    with open("keywords.txt","w") as f:
        f.write(res)
else:
    for i in keywords:
        if i in sys.argv[1].replace("\n","").replace(" ","") and i!="":
            res.append(i)
print(res)