from asciimatics.screen import Screen
from time import sleep
import time
from asciimatics.renderers import BarChart
import sys
import math
from random import randint
from asciimatics.effects import Print
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene

import os
import mido
import socket
import json
import hashlib
import binascii
from pprint import pprint
import random
from multiprocessing import Process
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import threading
import requests
import asyncio
from websocket import create_connection
import pythonosc
import curses, traceback
from playsound import playsound

#time counter
lastsave = 0
lastsave2 = 0
#note counter
notecounter = 0
notecounterFinal = 0

blockCount = ' '
MIDImsg = ' '

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start': '1',
    'limit': '1',
    'convert': 'EUR',
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '2b1ec842-3d92-4c24-b257-7ad649a8c333',
}


counter = 0
texto = 'hola'

delayRate = 0.001

COLOUR_BLACK = 0
COLOUR_RED = 1
COLOUR_GREEN = 2
COLOUR_YELLOW = 3
COLOUR_BLUE = 4
COLOUR_MAGENTA = 5
COLOUR_CYAN = 6
COLOUR_WHITE = 7

A_BOLD = 1
A_NORMAL = 2
A_REVERSE = 3
A_UNDERLINE = 4

bitcoinInfoData = ' '
nonceInfo = ' '
targetInfo = ' '
blockHeaderInfo = ' '
hashInfo = ' '
mineResultInfo = 0
payloadInfo = ' '

co2 = 0
kwh = 0
footTime = 0

paintMine = False

######################
#### AUDIO PLAYER
######################
def audio():
    os.system("aplay /home/warholiano/1.wav")



##################################
##### MINER ~~~############
##################################

def mine():

    global nonceInfo
    global targetInfo
    global blockHeaderInfo
    global mineResultInfo
    global hashInfo
    global payloadInfo

    address = '1GvSP13YjQAu9VAa8J1Hvbc4n3N8kUE3Ch'
    nonce   = hex(random.randint(0,2**32-1))[2:].zfill(8)
    nonceInfo ='{}'.format(nonce)

    #print("nonce: ", nonce)
    #print("\033[1;32;40m nonce \n")

    host    = 'solo.ckpool.org'
    port    = 3333

    #print("address:{} nonce:{}".format(address,nonce))
    #print("host:{} port:{}".format(host,port))

    sock    = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host,port))

    #server connection
    sock.sendall(b'{"id": 1, "method": "mining.subscribe", "params": []}\n')
    lines = sock.recv(1024).decode().split('\n')
    response = json.loads(lines[0])
    sub_details,extranonce1,extranonce2_size = response['result']

    #authorize workers
    sock.sendall(b'{"params": ["'+address.encode()+b'", "password"], "id": 2, "method": "mining.authorize"}\n')

    #we read until 'mining.notify' is reached
    response = b''
    while response.count(b'\n') < 4 and not(b'mining.notify' in response):
        response += sock.recv(1024)


    #get rid of empty lines
    responses = [json.loads(res) for res in response.decode().split('\n') if len(res.strip())>0 and 'mining.notify' in res]

    #pprint(responses)

    #welcome message
    #print responses[0]['params'][0]+'\n'


    job_id,prevhash,coinb1,coinb2,merkle_branch,version,nbits,ntime,clean_jobs \
        = responses[0]['params']

    #target http://stackoverflow.com/a/22161019
    target = (nbits[2:]+'00'*(int(nbits[:2],16))).zfill(64)
    targetInfo = '{}'.format(target)
    #print('target:{}\n'.format(target))

    extranonce2 = '00'*extranonce2_size

    coinbase = coinb1 + extranonce1 + extranonce2 + coinb2
    coinbase_hash_bin = hashlib.sha256(hashlib.sha256(binascii.unhexlify(coinbase)).digest()).digest()

    #print('coinbase:\n{}\n\ncoinbase hash:{}\n'.format(coinbase,binascii.hexlify(coinbase_hash_bin)))
    merkle_root = coinbase_hash_bin
    for h in merkle_branch:
        merkle_root = hashlib.sha256(hashlib.sha256(merkle_root + binascii.unhexlify(h)).digest()).digest()

    merkle_root = binascii.hexlify(merkle_root).decode()

    #little endian
    merkle_root = ''.join([merkle_root[i]+merkle_root[i+1] for i in range(0,len(merkle_root),2)][::-1])

    #print('merkle_root:{}\n'.format(merkle_root))

    blockheader = version + prevhash + merkle_root + nbits + ntime + nonce +\
        '000000800000000000000000000000000000000000000000000000000000000000000000000000000000000080020000'

    #print('blockheader:\n{}\n'.format(blockheader))
    blockHeaderInfo = '{}'.format(blockheader)

    hash = hashlib.sha256(hashlib.sha256(binascii.unhexlify(blockheader)).digest()).digest()
    hash = binascii.hexlify(hash).decode()
    #print('hash: {}'.format(hash))
    hashInfo = '{}'.format(hash)

    if hash < target :
        mineResultInfo = 1
        #print('success!!')
        payload = '{"params": ["'+address+'", "'+job_id+'", "'+extranonce2 \
            +'", "'+ntime+'", "'+nonce+'"], "id": 1, "method": "mining.submit"}\n'
        sock.sendall(payload)
        #print(sock.recv(1024))
        payloadInfo = '{}'.format(sock.recv(1024))

    else:
        mineResultInfo = 0
        #print(CRED + 'failed mine, hash is greater than target\n\n' + CEND)

    sock.close()

##################################
##### TRANSACTIONS ~~~############
##################################

def transactions():
    #sockets for transactions and block
    ws = create_connection("wss://ws.blockchain.info/inv")
    ws1 = create_connection("wss://ws.blockchain.info/inv")

    #subscribe to unconfirmed transactions and to new blocks
    ws.send(json.dumps({
        "op":"unconfirmed_sub"
    }))

    ws1.send(json.dumps({
        "op":"blocks_sub"
    }))

    print("connected to blockchain.info"'\n')

    while True:
        result = ws.recv()      #new transactions
        result = json.loads(result)

        if result['op'] == 'utx':
            print('\n'"transaction")
            counter = 0
            for item in result['x']['inputs']:
                counter = 0
                print("Input address", item['prev_out']['addr'])

            counter = 0
            for item in result['x']['out']:
                #print(item['value'])             #value in bitcoin
                #print("Output address", item['addr'])
                #global usd
                usd = 3000
                print("Output Value", (item['value']*(float(usd))/100000000))  #value in USD (value comes in satoshis)
                counter = counter + 1
                #print(counter)


        if result['op'] == 'block':
            print("block")
            print(result['x'])


#################
### midi setup
#################

def print_ports(heading, port_names):
    print(heading)
    for name in port_names:
        print("    '{}'".format(name))
    print()


#########################
##### MIDI PLAYER #######
#########################
def playm():
    #play the MIDI file and start action
    global notecounter
    global lastsave
    global lastsave2
    global MIDImsg

    mid = mido.MidiFile('samba.mid')
    for msg in mid.play():
        port.send(msg)      #para que no se retrase hay que hacer lo siguiente en paralelo
        if msg.type == 'note_on':
            #MINE!
            threading.Thread(target=mine).start()

            #print(msg)
            MIDImsg = '{}'.format(msg)

            #add a counter notes per second to check this works
            if time.time() - lastsave > 2:
                # this is in seconds, so 5 minutes = 300 seconds
                lastsave = time.time()
                notecounter = 0
            else:
                notecounter = notecounter + 1

            if time.time() - lastsave2 > 15:
                lastsave2 = time.time()
                #print("UDATE")
                #UPDATE BITCOIN INFO!
                threading.Thread(target=updateBitcoin).start()
            #print("note-on nr: ", notecounter)


#########################
##### FOOTPRINT #######
#########################
def footprintCalculator():
    #play the MIDI file and start action
    global co2
    global kwh
    global footTime
    global paintMine

    while True:
        if time.time() - footTime > 1:
            footTime = time.time()
            co2 = co2 + 0.32
            kwh = kwh + 0.675
            paintMine = True
        else:
            paintMine = False
        sleep(0.5)


###########################
##### BITCOIN INFO ########
###########################
def updateBitcoin():
    global bitcoinInfoData
    try:
        response = session.get(url, params=parameters)
        bitcoinInfoData = json.loads(response.text)
        data = json.loads(response.text) #this works, it is for printing only
        #print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)



def cambia():
    return 'El texto es {} '.format(time.time())

###########################
##### GET-ERS
#############################

bitcoinInfoData

def getNrNotes():
    ast = ' '
    ast = '*' * notecounter
    return 'Musical notes played per second ({})'.format(notecounter) + '   ' + ast

def getMIDImsg():
    return 'Musician played: ' + MIDImsg[17:38]

def getBlockCount():
    return 'Block Count: ' + blockCount

def getBitcoinInfoData1():
    t = '{}'.format(bitcoinInfoData)
    t2= t[:93]
    #print('t vale:' + t)
    return 'Bitcoin Realtime info: {}'.format(t2)

def getBitcoinInfoData2():
    t = '{}'.format(bitcoinInfoData)
    t2= t[93:]
    #print('t vale:' + t)
    return '{}'.format(t2[:108])
    #return '{}'.format(t2[189:313])

def getBitcoinInfoData3():
    t = '{}'.format(bitcoinInfoData)
    t2= t[200:]
    #print('t vale:' + t)
    return '{}'.format(t2[:125])

def getBitcoinInfoData4():
    t = '{}'.format(bitcoinInfoData)
    t2= t[325:]
    #print('t vale:' + t)
    return '{}'.format(t2[:125])

def getBitcoinInfoData5():
    t = '{}'.format(bitcoinInfoData)
    t2= t[450:]
    #print('t vale:' + t)
    return '{}'.format(t2[:125])

def getBitcoinInfoData6():
    t = '{}'.format(bitcoinInfoData)
    t2= t[575:]
    #print('t vale:' + t)
    return '{}'.format(t2[:125])


def getNonce():
    return 'Mining Nonce: ' + nonceInfo

def getHash():
    return 'Mining Hash: ' + hashInfo

def getTarget():
    return 'Mining Target: ' + targetInfo

def getBlockHeader1():
    return 'Block Header: ' + blockHeaderInfo[:100]

def getBlockHeader2():
    b = blockHeaderInfo[100:200]
    return b

def getBlockHeader3():
    b = blockHeaderInfo[200:]
    return b

def getMiningResult():
    r= ' '
    if(mineResultInfo == 1):
        r = 'RESULT : SUCCESS!!!!!!!!'
    else:
        r = 'RESULT: LOSE, hash is greater than target!!!!'
    return r

def getCO2():
    return 'Bitcoin miners have emitted {0:.2f} Kg of CO2 since we play'.format(co2)

def getKWh():
    return 'Bitcoin miners have consumed {0:.2f} KWh of electricity since we play'.format(kwh)

def drawTitle(x,y, screen):

    #text
    screen.print_at('', x, y+1, COLOUR_GREEN, A_BOLD)
    screen.print_at('  _____ _          __  __ _                 ', x, y+2, COLOUR_GREEN, A_BOLD)
    screen.print_at(' |_   _| |_  ___  |  \/  (_)_ _  ___ _ _ ___', x, y+3, COLOUR_GREEN, A_BOLD)
    screen.print_at("   | | | ' \/ -_) | |\/| | | ' \/ -_) '_(_-< ", x, y+4, COLOUR_GREEN, A_BOLD)
    screen.print_at('   |_| |_||_\___| |_|  |_|_|_||_\___|_| /__/', x, y+5, COLOUR_GREEN, A_BOLD)

def drawMine1(x,y, screen):

    #text
    screen.print_at('', x, y+1, COLOUR_GREEN, A_BOLD)
    screen.print_at(" ._ _  o ._   _    |_  o _|_  _  _  o ._   _   | ", x, y+2, COLOUR_GREEN, A_BOLD)
    screen.print_at(' | | | | | | (/_   |_) |  |_ (_ (_) | | | _>   o ', x, y+3, COLOUR_GREEN, A_BOLD)

def drawMine2(x,y, screen):

    #text
    screen.print_at('', x, y+1, COLOUR_GREEN, A_BOLD)
    screen.print_at("                                                  ", x, y+2, COLOUR_GREEN, A_BOLD)
    screen.print_at('                                                  ', x, y+3, COLOUR_GREEN, A_BOLD)


def drawChart(x,y, screen):
    #top decorator
    screen.print_at('%---------------------------------------------%', x, y, COLOUR_GREEN, A_BOLD)

    #bottom decorator
    screen.print_at('%---------------------------------------------%', x, y+10, COLOUR_GREEN, A_BOLD)



#####################################################
#################### SCREEN MANAGEMENT ##############
#####################################################
def demo(screen):
    while(True):

        screen.clear()

        # Draw a diagonal line from the top-left of the screen.
        #screen.move(23, 13)
        #screen.draw(10, 10)

        drawTitle(0,0,screen)
        #drawMine1(65,17,screen)

        if(paintMine):
            drawMine1(65,17,screen)
        else:
            drawMine2(65,17,screen)

        screen.print_at(getBlockCount(), 50, 2, COLOUR_GREEN, A_BOLD)
        screen.print_at(getCO2(), 50, 4, COLOUR_GREEN, A_BOLD)
        screen.print_at(getKWh(), 50, 6, COLOUR_GREEN, A_BOLD)

        #bitcoin data
        screen.print_at(getBitcoinInfoData1(), 2, 10, COLOUR_GREEN, A_REVERSE)
        screen.print_at(getBitcoinInfoData2(), 2, 11, COLOUR_GREEN, A_REVERSE)
        screen.print_at(getBitcoinInfoData3(), 2, 12, COLOUR_GREEN, A_REVERSE)
        screen.print_at(getBitcoinInfoData4(), 2, 13, COLOUR_GREEN, A_REVERSE)
        screen.print_at(getBitcoinInfoData5(), 2, 14, COLOUR_GREEN, A_REVERSE)
        screen.print_at(getBitcoinInfoData6(), 2, 15, COLOUR_GREEN, A_REVERSE)

        #screen.print_at(getTime(), 80, 32, COLOUR_GREEN, A_BOLD)

        screen.print_at(getNrNotes(), 8, 20, COLOUR_GREEN, A_BOLD)
        screen.print_at(getMIDImsg(), 8, 22, COLOUR_GREEN, A_BOLD)

        screen.print_at(getNonce(), 8, 24, COLOUR_GREEN, A_BOLD)
        screen.print_at(getBlockHeader1(), 8, 26, COLOUR_GREEN, A_BOLD)
        screen.print_at(getBlockHeader2(), 22, 27, COLOUR_GREEN, A_BOLD)
        screen.print_at(getBlockHeader3(), 22, 28, COLOUR_GREEN, A_BOLD)
        screen.print_at(getTarget(), 8, 30, COLOUR_GREEN, A_BOLD)
        screen.print_at(getHash(), 8, 32, COLOUR_GREEN, A_BOLD)
        screen.print_at(getMiningResult(), 8, 36, COLOUR_GREEN, A_BOLD)

        #drawChart(0,100, screen)

        screen.refresh()

        #sleep(delayRate)





### MAIN PROGRAM ######

#MIDI output print_ports
print_ports('Output Ports:', mido.get_output_names())
names = mido.get_output_names()
print(names[1])
port = mido.open_output(names[1])

#COINMARKET credentials
session = Session()
session.headers.update(headers)

#block count
r = requests.get("https://blockchain.info/q/getblockcount")
#print("Block Count: ", r.content.decode("utf-8"))
blockCount = r.content.decode("utf-8") # global variable for displaying

#get Bitcoin info at the beginning
threading.Thread(target=updateBitcoin).start()

#parallel processes
#threading.Thread(target=transactions).start()
threading.Thread(target=footprintCalculator).start()
threading.Thread(target=playm).start()
threading.Thread(target=audio).start()

##screen management
Screen.wrapper(demo)
