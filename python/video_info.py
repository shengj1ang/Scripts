import json

with open("video_info.json","r") as f:
    x=f.readlines()
#print(x[0])
for t,i in enumerate(x):
    z=json.loads(i.replace("\n",""))
    print(str(t)+": "+str(z["description"]))
