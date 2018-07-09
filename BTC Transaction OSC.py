
# coding: utf-8

# In[1]:


import json
import threading
import requests
import asyncio
import aiosc

from websocket import create_connection

##### osc INIT
loop = asyncio.get_event_loop()


ws = create_connection("wss://ws.blockchain.info/inv")
usd = 1

#subscribe to unconfirmed transactions and to new blocks
ws.send(json.dumps({
    "op":"unconfirmed_sub"  
}))

#ws2.send(json.dumps({
#    "op":"blocks_sub"  
#}))

bitcoin_api_url = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'

print("connected to blockchain.info"'\n')

def bitcoin_transactions_thread():
    threading.Timer(5.0, bitcoin_transactions_thread).start()
     
    response = requests.get(bitcoin_api_url)
    response_json = response.json()
    type(response_json) # The API returns a list
    #print(response_json[0]['price_usd'])
    global usd
    usd = response_json[0]['price_usd']
    print("Price Bitcoin USD:{}".format(response_json[0]['price_usd']))
    loop.run_until_complete(
        aiosc.send(('127.0.0.1', 9000), '/btcvalue', float(usd))
    )
bitcoin_transactions_thread()
    
while True:    
    result = ws.recv()
    result = json.loads(result)
    #print(result['op'])
    
    if result['op'] == 'utx':
        print('\n'"transaction")
        
        #print(result)
        for item in result['x']['inputs']:
            #print(item['value'])             #value in bitcoin
            print("Input address", item['prev_out']['addr'])
            #print("Input value", (item['prev_out']['value']*(float(usd))/100000000))  #value in USD (value comes in satoshis)
            #global usd
            
        for item in result['x']['out']:
            #print(item['value'])             #value in bitcoin
            print("Output address", item['addr'])
            global usd
            print("Output Value", (item['value']*(float(usd))/100000000))  #value in USD (value comes in satoshis)
            loop.run_until_complete(
                aiosc.send(('127.0.0.1', 9000), '/outputvalue', (item['value']*(float(usd))/100000000))
            )
            #print(item['address'])  #value in USD (value comes in satoshis)
        
    if result['op'] == 'block':
        print("block")
        print(result['x'])


    
#ws.close()

