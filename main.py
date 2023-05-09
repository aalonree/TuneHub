
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import json

username = '9xibrpezi7iazqrgh4ufx5ubx'
client_id ='4fe326301d5842369470c275f63941c6'
client_secret = '5d953feeaed1436c9c518ae13eddf49a'
redirect_uri = 'https://lasacs.com/acp'
scope = 'user-read-recently-played'

token = spotipy.prompt_for_user_token(username=username, 
                                   scope=scope, 
                                   client_id=client_id,   
                                   client_secret=client_secret,     
                                   redirect_uri=redirect_uri)
sp = spotipy.Spotify(auth=token)

def get_id(track_name: str, token: str) -> str:
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer ' + token,
    }
    params = [
    ('q', track_name),
    ('type', 'track'),
    ]
    try:
        response = requests.get('https://api.spotify.com/v1/search', 
                    headers = headers, params = params, timeout = 5)
        json = response.json()
        first_result = json['tracks']['items'][0]
        track_id = first_result['id']
        return track_id
    except:
        return None

def get_features(track_id: str, token: str) -> dict:   
    try:
        features = sp.audio_features([track_id])
        return features[0]
    except:
        return None

def get_playlist_avg_features(playlist_id: str) -> dict:
    playlist_avg_features = dict({'danceability': 0.0, 'energy': 0.0, 'loudness': 0.0, 'acousticness': 0.0, 'instrumentalness': 0.0, 'liveness': 0.0, 'valence': 0.0, 'tempo': 0.0})
    results = sp.user_playlist(username, playlist_id)
    song_total = 0
    for i in results['tracks']['items']:
        song_total += 1
        song_features = get_features(i['track']['id'], token)
        playlist_avg_features['danceability'] += song_features['danceability']
        playlist_avg_features['energy'] += song_features['energy']
        playlist_avg_features['loudness'] += song_features['loudness']
        playlist_avg_features['acousticness'] += song_features['acousticness']
        playlist_avg_features['instrumentalness'] += song_features['instrumentalness']
        playlist_avg_features['liveness'] += song_features['liveness']
        playlist_avg_features['valence'] += song_features['valence']
        playlist_avg_features['tempo'] += song_features['tempo']
    playlist_avg_features['danceability'] = round(playlist_avg_features['danceability']/song_total, 4)
    playlist_avg_features['energy'] = round(playlist_avg_features['energy']/song_total, 4)
    playlist_avg_features['loudness'] = round(playlist_avg_features['loudness']/song_total, 4)
    playlist_avg_features['acousticness'] = round(playlist_avg_features['acousticness']/song_total, 4)
    playlist_avg_features['instrumentalness'] = round(playlist_avg_features['instrumentalness']/song_total, 4)
    playlist_avg_features['liveness'] = round(playlist_avg_features['liveness']/song_total, 4)
    playlist_avg_features['valence'] = round(playlist_avg_features['valence']/song_total, 4)
    playlist_avg_features['tempo'] = round(playlist_avg_features['tempo']/song_total, 4)
    return playlist_avg_features

def show_tracks(playlist_id, file):
    results = sp.user_playlist(username, playlist_id)
    for i in results['tracks']['items']:
        song_name = i['track']['name']
        song_artist = i['track']['artists'][0]['name']
        #print(song_name)
        file.write(f'{song_name} - {song_artist}\n')
    



#with open('playlist_genres.txt', file_mode) as f:
#playlists (dict) --> items (dict) --> id (str) --> sp.user_playlist(username, playlist_id) --> results (dict) --> tracks (dict) --> items (list) --> track (dict) --> id/name
with open('playlist_average_features.txt', 'w') as file:
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:      
        playlist_name = playlist['name']
        file.write(f'Playlist: {playlist_name}\n')
        # Get the ID of the current playlist
        playlist_id = playlist['id']
        this_features = get_playlist_avg_features(playlist_id)
        file.write(json.dumps(this_features) + '\n')
        show_tracks(playlist_id, file)