
# coding: utf-8

# In[ ]:


import json
import threading
import requests
import asyncio

from pythonosc import osc_message_builder
from pythonosc import osc_bundle_builder
from pythonosc import udp_client


from websocket import create_connection

import pythonosc

##### osc INIT
client = udp_client.SimpleUDPClient("127.0.0.1", 9000)

##for the sockets
ws = create_connection("wss://ws.blockchain.info/inv")
#usd = 1

#subscribe to unconfirmed transactions and to new blocks
ws.send(json.dumps({
    "op":"unconfirmed_sub"  
}))


bitcoin_api_url = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'

print("connected to blockchain.info"'\n')

def bitcoin_transactions_thread():
    threading.Timer(5.0, bitcoin_transactions_thread).start()
     
    response = requests.get(bitcoin_api_url)
    response_json = response.json()
    type(response_json) # The API returns a list
    global usd
    usd = response_json[0]['price_usd']
    print("Price Bitcoin USD:{}".format(response_json[0]['price_usd']))
    
bitcoin_transactions_thread()
    
while True:    
    result = ws.recv()
    result = json.loads(result)
    #print(result['op'])
    
    if result['op'] == 'utx':
        print('\n'"transaction")
        counter = 0
        for item in result['x']['inputs']:
            print("Input address", item['prev_out']['addr'])
            
        counter = 0
        for item in result['x']['out']:
            #print(item['value'])             #value in bitcoin
            print("Output address", item['addr'])
            global usd
            print("Output Value", (item['value']*(float(usd))/100000000))  #value in USD (value comes in satoshis)
            counter = counter + 1
            #this works
            #client.send_message("/outputvalue", (item['value']*(float(usd))/100000000))
            client.send_message("/ov"+str(counter), (item['value']*(float(usd))/100000000))
            print(counter)
            client.send_message("/btcvalue", float(usd))
            
            
        
        
        
    if result['op'] == 'block':
        print("block")
        print(result['x'])


    
#ws.close()

