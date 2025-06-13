import os
import requests

CLIENT_ID =  YOUR_CLIENT_ID
CLIENT_SECRET = YOUR_CLIENT_SECRECT
REFRESH_TOKEN = YOUR_REFRESH_TOKEN

TOKEN_URL = "https://accounts.spotify.com/api/token"
LIKED_SONGS_URL = "https://api.spotify.com/v1/me/tracks"

def get_access_token(client_id, client_secret, refresh_token):
    auth = (client_id, client_secret)
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(TOKEN_URL, data=data, headers=headers, auth=auth)
    print("Status Code:", response.status_code)
    print("Response Headers:", response.headers)
    print("Response Text:", response.text)

    response.raise_for_status()
    return response.json()['access_token']

def get_all_liked_songs(access_token):
    songs = []
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'limit': 50, 'offset': 0}  # Spotify max limit per request is 50

    while True:
        response = requests.get(LIKED_SONGS_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        for item in data['items']:
            track = item['track']
            song_name = track['name']
            artists = ", ".join(artist['name'] for artist in track['artists'])
            songs.append(f"{song_name} - {artists}")

        if data['next']:
            params['offset'] += params['limit']
        else:
            break
    return songs

def save_songs_to_file(songs, filename='liked_songs.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        for song in songs:
            f.write(song + '\n')

def main():
    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)
    songs = get_all_liked_songs(access_token)
    save_songs_to_file(songs)
    print(f"Saved {len(songs)} songs to liked_songs.txt")

if __name__ == "__main__":
    main()
