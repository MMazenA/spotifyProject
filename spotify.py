
from os import access
from re import S
from urllib import response
import requests
from pprint import pprint
import base64
from urllib.parse import urlencode
import time


#provides accesstoken through refreshtoken recieved from manualuserAuth
def getAccessToken():
    client_id='aa1826bc005040e98502bf7d9e6d5ba2'
    secret_id='.'

    token_url="https://accounts.spotify.com/api/token"

    token_data={
        "grant_type": "authorization_code",
        "code":".",                                 
        "redirect_uri":"http://127.0.0.1:5000/home/"
    }

    token_data_refresh={
        "grant_type": "refresh_token",
        "refresh_token":".",                        
        "redirect_uri":"http://127.0.0.1:5000/home/"
        }
    client_creds = f"{client_id}:{secret_id}"
    client_creds_b64 =base64.b64encode(client_creds.encode())

    token_headers={ 
            "Authorization": f"Basic {client_creds_b64.decode()}"
        }

    r=requests.post(token_url,data=token_data_refresh,headers=token_headers)
    resp_json=r.json()
    requested_access_token=resp_json['access_token']
    #print(r.json())
    #s_access_token=s_access_token= 'BQCsGhfymKzbYVXf_dP8M4OaUooU5DDQiS5Eqec7RPGGuBMBUxiqewQlWFKLS-8ygf4-4x1hBPkHvCIMmdQ_6GfJISdpbPOtSdUPSezFSxmOUvSkmD3ZcU8MZJhTC8kVAAE4zzxVCsVrZF6WHnYpkieoMw'
    return requested_access_token
    
    

def current_track(access_token):
    current_track_url='https://api.spotify.com/v1/me/player'
    response=requests.get(
    current_track_url,
    headers={
            "Authorization": f"Bearer {access_token}"
            }
    )
    resp_json=response.json()

   #print(resp_json)

        
   # if(resp_json['error']['status']==401):
     #   return "Error 401: The access token expired"
        
    track_id=resp_json['item']['id']
    track_name=resp_json['item']['name']
    artists=resp_json['item']['artists']
    artists_name = ', '.join([artist['name'] for artist in artists])
    time=[0,0]
    position=resp_json['progress_ms']  #miliseconds int 
    time[0]=(int((position/1000)/60))
    time[1]=(int((position/1000)%60))
    pic=resp_json['item']['album']['images'][0]['url']
    playing=resp_json['is_playing']
    current_track_info = {
            "id":track_id,
            "name":track_name,
            "artists":artists_name,
            "position":time,
            "picture":pic,
            "is_playing":playing,
        }
    return current_track_info
            

        
                
            
#print(getAccessToken())
#pprint(current_track('BQC5pBPma_7nzd9wjWBH8xqltAZag8hqTtXgqBydj6aWmm5EVVxegOczMlltrfmzc7QrJGYYD9GU2GAw8jC7gs_ZBvb-6IQeL-PzSiVNOHgELK2kOpUhImHpoTINvoCR0YQBEN-Lzg1eGIE2EywPnmBE4w'))

def main():
    token=getAccessToken()
    listining_info=current_track(token)
    pprint(listining_info,indent=4)
    


main()
    
