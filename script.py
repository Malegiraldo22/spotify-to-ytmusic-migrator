import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic
import ytmusicapi
import json
import os
import time

def spotify_login():
    """
    Configure the connection with Spotify
    """
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'),
        redirect_uri='http://localhost:8888/callback',
        scope='playlist-read-private'
    ))

def ytmusic_login():
    """Configure the connection with YouTube Music"""
    ytmusicapi.setup('browser.json')
    return YTMusic('browser.json')

def get_spotify_playlists(sp):
    """Get all the user's playlists"""
    playlists = []
    results = sp.current_user_playlists()

    while results:
        playlists.extend(results['items'])
        if results['next']:
            results = sp.next(results)
        else:
            break
    return playlists

def get_playlist_tracks(sp, playlist_id):
    """Get all the songs from a Spotify playlist"""
    tracks = []
    results = sp.playlist_tracks(playlist_id)

    while results:
        for item in results['items']:
            track = item['track']
            artist = track['artists'][0]['name']
            title = track['name']
            tracks.append({
                'artist':artist,
                'title':title
            })
        
        if results['next']:
            results = sp.next(results)
        else:
            break
    
    return tracks

def search_add_ytmusic(ytmusic, tracks, playlist_name):
    """Search for the songs on YouTube Music and add them to a new playlist"""
    playlist_id = ytmusic.create_playlist(playlist_name, "")

    added_tracks = 0
    failed_tracks = []

    for track in tracks:
        try:
            search_query = f"{track['artist']} {track['title']}"
            search_results = ytmusic.search(search_query, filter='songs')

            if search_results:
                #Añadir primera coincidencia a la playlist
                video_id = search_results[0]['videoId']

                try:
                    ytmusic.add_playlist_items(playlist_id, [video_id])
                    added_tracks += 1
                    print(f"Added: {track['artist']} - {track['title']}")
                    time.sleep(0.5)

                except Exception as e:
                    print(f"EError adding: {track['artist']} - {track['title']}: {e}")
                    failed_tracks.append(track)
            else:
                print(f"Not found: {track['artist']} - {track['title']}")
                failed_tracks.append(track)
        
        except Exception as e:
            print(f"Error searching: {track['artist']} - {track['title']}: {e}")
            failed_tracks.append(track)

    print("\n--- Migration Summary ---")
    print(f"Total songs: {len(tracks)}")
    print(f"Songs added: {added_tracks}")
    print(f"Failed songs: {len(failed_tracks)}")

    if failed_tracks:
        with open('failed_tracks.json', 'w', encoding='utf-8') as f:
            json.dump(failed_tracks, f, ensure_ascii=False, indent=2)
        print("Failed songs saved in 'failed_tracks.json'")

    return added_tracks, failed_tracks

def main():
    #Setting up connections to Spotify and YouTube Music
    sp = spotify_login()
    ytmusic = ytmusic_login()

    #Getting and showing all playlists available
    playlists = get_spotify_playlists(sp)
    print("Available playlists: ")
    for i, playlist in enumerate(playlists):
        print(f"{i+1}. {playlist['name']} ({playlist['tracks']['total']} songs)")

    #Selecting playlist to migrate
    playlist_index = int(input("\nEnter the number of the playlist to migrate: ")) - 1
    selected_playlist = playlists[playlist_index]

    #Getting songs to migrate
    print(f"\nGetting songs from {selected_playlist['name']}...")
    tracks = get_playlist_tracks(sp, selected_playlist['id'])

    #Migrate to Youtube Music
    print("\nMigrating songs to Youtube Music...")
    added_tracks, failed_tracks = search_add_ytmusic(ytmusic, tracks, selected_playlist['name'])

    print("\nMigration completed")

if __name__ == "__main__":
    main()