import requests
import base64
import time
import privateInfo  # file containing client codes
import pythonSQL


def getAccessToken():
    client_id = privateInfo.clientID()
    secret_id = privateInfo.secretID()

    token_url = "https://accounts.spotify.com/api/token"

    # token_data_refresh = {
    # "grant_type": "authorization_code",
    #  "code": "AQDbVeE5sVzaCq1PczSOZTa-5gQiTJR98FTYI5vHYlZPS5oUs7hY3Fy9eEO1IKsBjWoeGd_EfyaAJ-DUIf9JlIhUfiQi6Hr4ssUBKpCXe1Gocxq3vfoNQYbTCBHNg5jkuy31szCIQtgFreMd_MRJDtNfdkCmifXHdwqqv9RcNCY6_XMZ2rBfegjKAnlQL-eO291CEdqJuATaWo9fkZvNbKExZ4Qt6e6AAmyiZmxjqM7KQQ4M0q3dLIVs0p_CQPvoI2EOKMzsaBzOvXnisp0ssnAylw",
    #   "redirect_uri": "http://127.0.0.1:5000/home/"
    # }

    token_data_refresh = {
        "grant_type": "refresh_token",
        "refresh_token": privateInfo.refreshToken(),
        "redirect_uri": "http://127.0.0.1:5000/home/"
    }
    client_creds = f"{client_id}:{secret_id}"
    client_creds_b64 = base64.b64encode(client_creds.encode())

    token_headers = {
        "Authorization": f"Basic {client_creds_b64.decode()}"
    }

    r = requests.post(token_url, data=token_data_refresh,
                      headers=token_headers)
    resp_json = r.json()
    # print(resp_json)           #prints token ,type,scope
    requested_access_token = resp_json['access_token']
    return requested_access_token


def current_track(access_token):
    import time  # dont know why but exception is raised without this for current time
    localt = time.localtime()
    time_string = time.strftime("<%m/%d/%Y, %H:%M:%S>", localt)

    global token
    if(token == 0):
        token = getAccessToken()

    current_track_url = 'https://api.spotify.com/v1/me/player'
    response = requests.get(
        current_track_url,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    print()
    print(time_string, response)

    if(response.status_code == 401):
        print("Authorization code expired retriving new token")
        token = getAccessToken()
        return 0
    elif(response.status_code == 204):
        print("Connection made, Nothing is playing")
        return 1

    resp_json = response.json()
# response = Str(response)
# print(response.status_code)
# print(type(response))
# print(token)

    if(resp_json['currently_playing_type'] == 'track'):
        track_id = resp_json['item']['id']
        track_name = resp_json['item']['name']
        artists = resp_json['item']['artists']
        main_artist = resp_json['item']['artists'][0]['name']
        artists_name = ', '.join([artist['name'] for artist in artists])
        time = [0, 0]
        position = resp_json['progress_ms']
        time[0] = (int((position/1000)/60))
        time[1] = (int((position/1000) % 60))
        pic = resp_json['item']['album']['images'][2]['url']
        playing = resp_json['is_playing']
        length = [0, 0]
        length_raw = (resp_json['item']["duration_ms"])
        length[0] = (int((length_raw/1000)/60))
        length[1] = (int((length_raw/1000) % 60))
        # percent_complete=f"% {position*100/length_raw}"
        current_track_info = {
            "id": track_id,
            "name": track_name,
            "artists": artists_name,
            "position": position,
            "length": length_raw,
            "picture": pic,
            "is_playing": playing,
            "main_artist": main_artist,
            # "% complete":percent_complete
        }
    else:
        return '1'
    return current_track_info


# print(getAccessToken())
def main():
    global token
    token = 0
    countPrevent = True
    sleepTimer = 25

    while(True):
        try:

            listining_info = current_track(token)
            print(listining_info)

            sleepTimer = 0

            if(listining_info == 1):
                sleepTimer = 29

            # pprint(listining_info, indent=4)
            if(listining_info != 0 and listining_info != 1):  # if data is available

                sleepTimer = 5
                if(not listining_info.get('is_playing')):
                    sleepTimer = 25

                repeat = True
                lastSongDB = pythonSQL.lastRow()
                lastID = lastSongDB[0]
                lastCount = lastSongDB[5]
                count = 0

                if(lastID != listining_info.get('id')):
                    print("different song playing now")
                    countPrevent = True

                # accounts for songs on repeat
                if(lastID == listining_info.get('id') and not countPrevent and listining_info.get('position') < 30000):
                    countPrevent = True
                    print('Repeating')

                if(lastID == listining_info.get('id') and listining_info.get('position') > 30000 and countPrevent):
                    print("Adding 1 to count")
                    count = int(lastCount)
                    count += 1
                    countPrevent = False
                    repeat = False
                elif(lastID == listining_info.get('id') and repeat):
                    count = lastCount

                payload = (str(listining_info.get('id')),
                           str(listining_info.get('name')),
                           str(listining_info.get('artists')),
                           str(listining_info.get('main_artist')),
                           str(listining_info.get('length')),
                           int(count),
                           str(listining_info.get('position')),
                           str(listining_info.get('picture')))
                # print(payload)

                pythonSQL.dataInsert((payload))
                # count = 0

            time.sleep(5)
        except:
            print("Reponse not working")
            time.sleep(29)

        time.sleep(sleepTimer)

    # sql stuff

    return listining_info


main()
