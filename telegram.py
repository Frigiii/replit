from apikey import frigi_channel_id
from apikey import frigi_chat_id
from apikey import API_KEY
import requests

async def request(method, param) -> dict:
    url = 'https://api.telegram.org/bot{API_KEY}/{method}'.format(API_KEY = API_KEY, method = method)
#    print('Making request to : {} {}'.format(url, param))

    r = requests.get(url, params=param)
    #print(r.headers['Content-Type'])
    r_dic = r.json() 
    if (len(r_dic['result'])):
    #    print ('Response of request: {}'.format(r_dic['result']))
        return r_dic['result']
    else:
        return None
