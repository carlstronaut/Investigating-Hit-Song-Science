import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials('9dfa3290211549deadedcc32beb9b2c7','b24bcf2780f9478f88bfe5ba13094fb4')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
markets = ['AD', 'AE', 'AR', 'AT', 'AU', 'BE', 'BG', 'BH', 'BO', 'BR', 'CA', 'CH', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DE', 'DK',
           'DO', 'EC', 'EE', 'EG', 'ES', 'FI', 'FR', 'GB', 'GR', 'GT', 'HK', 'HN', 'HU', 'ID', 'IE', 'IL', 'IN', 'IS', 'IT',
           'JO', 'JP', 'KW', 'LB', 'LI', 'LT', 'LU', 'LV', 'MC', 'MT', 'MX', 'MY', 'NI', 'NL', 'NO', 'NZ', 'OM', 'PA', 'PE',
           'PH', 'PL', 'PT', 'PY', 'QA', 'RO', 'SA', 'SE', 'SG', 'SK', 'SV', 'TH', 'TN', 'TR', 'TW', 'US', 'VN', 'ZA']

billboard = pd.read_csv('updated_billboard.csv')
billboard_including_features = pd.DataFrame()
found = [False for row in billboard.iterrows()]

for market in markets:
    for index, row in billboard.iterrows():
        if not found[index]:
            while True:
                try:
                    artist = row['artist'].replace(" ft ", " ").replace(" & ", " ").replace("/", " ").replace(" vs ", " ").replace("'", "")
                    title = row['title'].replace("'", "")
                    q = "artist:%s track:%s" % (artist, title)
                    track = sp.search(q=q, type="track", market=market, limit=1)

                    if len(track["tracks"]["items"]) > 0:
                        trackURI = track["tracks"]["items"][0]["uri"]
                        features = sp.audio_features([trackURI])[0]
                        if (features):
                            audio_analysis = sp.audio_analysis(trackURI)
                            data = {'position': row['position'],
                                    'title': row['title'],
                                    'artist': row['artist'],
                                    'year': row['year'],
                                    'month': row['month'],
                                    'day': row['day'],
                                    'duration_ms': features['duration_ms'],
                                    'key': features['key'],
                                    'mode': features['mode'],
                                    'time_signature': features['time_signature'],
                                    'acousticness': features['acousticness'],
                                    'danceability': features['danceability'],
                                    'energy': features['energy'],
                                    'instrumentalness': features['instrumentalness'],
                                    'liveness': features['liveness'],
                                    'loudness': features['loudness'],
                                    'speechiness': features['speechiness'],
                                    'valence': features['valence'],
                                    'tempo': features['tempo'],
                                    'audio_analysis' : audio_analysis
                                    }
                            billboard_including_features = billboard_including_features.append(data, ignore_index=True)
                            found[index] = True
                            print('[%s %s%%] %s/%d found: "%s" by: %s' %
                                    (market, str((index*100//len(billboard.index))).rjust(3), str(len(billboard_including_features.index)).zfill(4), len(billboard.index), row['title'], row['artist']))
                    else:
                        print('[%s %s%%] Searching...' % (market,
                            str((index*100//len(billboard.index))).rjust(3)), end='\r')
                except ConnectionError:
                    continue
                break

billboard_including_features.to_csv('billboard_including_features_and_analysis.csv', index=False)
print('Done', ' ' * 40, '\n' * 2)
print(billboard_including_features.info())
