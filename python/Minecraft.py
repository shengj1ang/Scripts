from mcstatus import JavaServer
import time, threading
from abc import ABC

server = JavaServer.lookup("bear.mtyxt.com:25565")
# You can pass the same address you'd enter into the address field in minecraft into the 'lookup' function
# If you know the host and port, you may skip this and use JavaServer("example.org", 1234)
def connn():
#    
    while True:
        status = server.status()
        print(f"The server has {status.players.online} player(s) online and replied in {status.latency} ms")

connn()
#i=0
#while i <9:
#    t = threading.Thread(target=connn, name=f'LoopThread{str(i)}')
#    t.start()

'''
from mcpi_e.minecraft import Minecraft

serverAddress="bear.mtyxt.com" # change to your minecraft server
pythonApiPort=25565 #default port for RaspberryJuice plugin is 4711, it could be changed in plugins\RaspberryJuice\config.yml
playerName="stoneskin" # change to your username

mc = Minecraft.create(serverAddress,pythonApiPort,playerName)
pos = mc.player.getPos()

print("pos: x:{},y:{},z:{}".format(pos.x,pos.y,pos.z))
'''