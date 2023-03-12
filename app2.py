from flask import Flask, request, render_template
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# Flask
app = Flask(__name__)

auth_manager = SpotifyOAuth(
    client_id = '74f3dd6a119c4711b8e141ff02303dde',
    client_secret = '36dc856cff2d46b3a3a920f6a80665c5',
    redirect_uri = 'http://www.localhost/',
    scope = 'user-library-read',
    cache_path='.cache')

sp = spotipy.Spotify(auth_manager=auth_manager)
try:
    sp.current_user()
except spotipy.SpotifyException as e:
    print(f"Error: {e}")
else:
    print("Token is valid.")

token = sp.auth_manager.get_cached_token()
# print(token_data['access_token'])
# Set up headers with authorization token
headers = {
    'Authorization': 'Bearer ' + token['access_token']
}
# Define route for index page
@app.route('/')
def index():
    print('Hola')
    return render_template('index.html')
# Define route for recommendations page
@app.route('/recommendations', methods=['POST'])
def recommendations():
    print('jeje')
    # Set up query parameters
    market = request.form['market']
    genre = request.form['genre']
    danceability = request.form['danceability']
    acousticness = request.form['acousticness']
    popularity = request.form['popularity']

    query_params = {
        'market' : market,
        'seed_genres': genre,
        'target_danceability': danceability,
        'target_acousticness': acousticness,
        'target_popularity': popularity,
        'limit': 10
    }

    # Make API request to get recommendations
    response = requests.get('https://api.spotify.com/v1/recommendations', headers=headers, params=query_params)

    # Parse response JSON
    response_json = response.json()


    # Get list of recommended tracks
    tracks = response_json['tracks']

    # Print track names and artists
    #for track in tracks:
    #    print(track['name'], 'by', track['artists'][0]['name'])
    track_list = []
    for track in tracks:
        track_list.append(f"{track['name']} by {track['artists'][0]['name']}")
    print(track_list)
    return render_template('index.html', track_list=track_list)
if __name__ == '__main__':
    app.run(debug=False, port=80)


