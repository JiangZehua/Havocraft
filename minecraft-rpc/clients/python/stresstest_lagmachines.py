from __future__ import print_function

import time

import grpc

from delegator_pb2 import *
import delegator_pb2_grpc

import minecraft_pb2_grpc
from minecraft_pb2 import *

servers = []
ip = "3.122.95.204"

#The lag machine itself
def getListOfLagMachinesOnY(x, y, z):
    lagmachines = []
    i = x
    while i < (x+15):
        for u in range(4):
            lagmachines.append(Block(position=Point(x=i, y=y, z=z+3+(u-1)*4), type=PISTON, orientation=NORTH))
            lagmachines.append(Block(position=Point(x=i, y=y, z=z+1+(u-1)*4), type=WOOL, orientation=NORTH))
            lagmachines.append(Block(position=Point(x=i, y=y, z=z+0+(u-1)*4), type=PISTON, orientation=SOUTH))
            lagmachines.append(Block(position=Point(x=i, y=y+1, z=z+2+(u-1)*4), type=OBSERVER, orientation=NORTH))
            lagmachines.append(Block(position=Point(x=i, y=y+1, z=z+1+(u-1)*4), type=OBSERVER, orientation=SOUTH))
        i+=1
    return lagmachines

#Spawn the lag machine in a chunk (16x16)
def spawnLagMachineChunk(x, y, z, height):
    lagmachines = []
    i = y
    while i < y+height:
        temp = getListOfLagMachinesOnY(x, i, z)
        for u in range(len(temp)):
            lagmachines.append(temp[u])
        i+=2
    return lagmachines

#Waits for all futures in a list to be done
def wait_for_futures(futures):
    b = True
    while(b):
        b = False
        for i in futures:
            if(not i.done()): b = True
    return futures

#Async calls the spawning of servers
def spawnServers(client, amount):
    futures = []
    servers = []

    for i in range(amount):
        call_future = client.SpawnNewServer.future(ServerConfig(worldType=FLAT, maxHeapSize=3000))
        futures.append(call_future)

    futures = wait_for_futures(futures)

    for i in range(len(futures)):
        servers.append(futures[i].result())

    return servers

def spawnLagMachineChunkOnServer(servers, posX, posY, posZ):
    i = 0
    while i < len(servers):
        #Establish connection to spawned server
        server_channel = grpc.insecure_channel(ip+':'+str(servers[i].rpcPort))
        server_client = minecraft_pb2_grpc.MinecraftServiceStub(server_channel)

        #Spawn lag machine on server
        blocks = spawnLagMachineChunk(posX, posY, posZ, height)
        server_client.spawnBlocks(Blocks(blocks=blocks))
        i +=1
    
def sendCommand(server, cmd):
    server_channel = grpc.insecure_channel(ip+':'+str(server.rpcPort))
    server_client = minecraft_pb2_grpc.MinecraftServiceStub(server_channel)

    server_client.executeCommands(Commands(commands=[
        Command(command=cmd)
    ]))


#---------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------#

posX = int(input("Where do you want your lag machine chunk? format: x ENTER y ENTER z ENTER\n"))
posY = int(input())
posZ = int(input())
height = int(input("How many layers of lag machine do you want? format: h\n"))
amountOfServers = int(input("How many servers do you want duplicated with these lag machines? format: c\n"))

print("Processing ...")

#Make docker
channel = grpc.insecure_channel(ip+':5001')
client = delegator_pb2_grpc.DelegatorStub(channel)

servers = []
servers = spawnServers(client, amountOfServers)

#for server in servers:
#    sendCommand(server, "spark ")

spawnLagMachineChunkOnServer(servers, posX, posY, posZ)


while 1:
    time.sleep(5)
    for server in servers:
        sendCommand(server, "sponge tps")