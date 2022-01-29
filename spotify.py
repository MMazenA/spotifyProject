
from os import access
from re import S
from urllib import response
import requests
from pprint import pprint
import base64
from urllib.parse import urlencode
import time

while(True):    
    client_id='aa1826bc005040e98502bf7d9e6d5ba2'
    secret_id=''

    token_url="https://accounts.spotify.com/api/token"

    token_data={
        "grant_type": "client_credentials"
    }
    client_creds = f"{client_id}:{secret_id}"
    client_creds_b64 =base64.b64encode(client_creds.encode())

    token_headers={ 
        "Authorization": f"Basic {client_creds_b64.decode()}"
    }

    r=requests.post(token_url,data=token_data,headers=token_headers)
    print(r.json())
    clientresponse=r.json()
    p_access_token=clientresponse['access_token']

    expiresIn=clientresponse['expires_in']

    headers = {
        "Authorization": f"Bearer {p_access_token}"
    }
    endpoint = 'https://api.spotify.com/v1/users/eggzimic'
    #data = urlencode({"q": "Time", "type": "track"})
    #print(data)

    current_track_url='https://api.spotify.com/v1/me/player'
    r = requests.get(
        endpoint, 
        headers={
            "Authorization": f"Bearer {p_access_token}"
        }
        )
    #print(r.json())

    userauthenticate={
    "auth_endpoint":'https://accounts.spotify.com/authorize',
    "response_type":'code',
    "redirect_uri":'http://localhost:7800/',
    "scope" : 'user-read-currently-playing',
    }

    #test=requests.get(
    #   userauthenticate
    #)
    #print(test.json())

    s_access_token= 'BQAYMENsDrgIZ7l9Egtwh59yNlAqkMbafX7QoWYH3eKGo_o7n2BL6pR-Jtz2xWSM7EOG-7EMbW8dFu4ANmybAxSfvIHb9qA0EZVOAp1nKTpID1iNl8x7NI5Gicie30BQZLa0rnPgOa-SeYrIvtCnC9iKhnJjR2sXILk-odmvCVyXaypr84I0NA'
    current_track_url='https://api.spotify.com/v1/me/player'


    #print(s_access_token)
    #print("")
    #print(p_access_token)

    def current_track(access_token):
        response=requests.get(
            current_track_url,
            headers={
                "Authorization": f"Bearer {access_token}"
                }
        )
        resp_json=response.json()

        #print(resp_json)

        
        #if(resp_json['error']['status']==401):
            #return "Error 401: The access token expired"
        
        track_id=resp_json['item']['id']
        track_name=resp_json['item']['name']
        artists=resp_json['item']['artists']
        artists_name = ', '.join([artist['name'] for artist in artists])
        time=[0,0]
        position=resp_json['progress_ms']  #miliseconds int 
        time[0]=(int((position/1000)/60))
        time[1]=(int((position/1000)%60))
        pic=resp_json['item']['album']['images'][0]['url']
        current_track_info = {
            "id":track_id,
            "name":track_name,
            "artists":artists_name,
            "position":time,
            "picture":pic,
        }
        return current_track_info
            

        
                
            



    def main():
        #print('hi')

        current_track_info=current_track(s_access_token)

        pprint(current_track_info, indent=4)

    main()
    time.sleep(1)
