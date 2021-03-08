# Script I used to scrape my tracks from the now-defunct Google Play Music.  Youtube killed the radio star :(

#!python3
# run w/ /path/to/python3 gplay.py using python >3.5

# deps
from gmusicapi import Mobileclient
import urllib.request
import os
import eyed3, eyed3.mp3
import time

# create urllib opener
opener = urllib.request.FancyURLopener()

# connect and login
api = Mobileclient()
api.oauth_login('XXXXXXXXXXXXXXXX') # censored
print("Connected to gPlay")

# get library from gplay
library = api.get_all_songs()
print("Downloaded library.")

# get albums in library
albumIDs = [song['albumId'] if 'artistId' in song.keys() else print(song['artist']) for song in library]
albumIDs = list(set(albumIDs))
num_albums = len(albumIDs)

# download all albums in library
for album_count, albumID in enumerate(albumIDs):


    # get album info including track list
    album = api.get_album_info(albumID)

    # get album artist
    artist_name = album['albumArtist']

    # create album directory if missing
    # album_path = os.path.join(os.getcwd(), 'Music')
    album_path = '/cloud/Music/audio/'
    album_path = os.path.join(album_path, artist_name.replace('/',' - ').replace('  ',' '))
    album_path = os.path.join(album_path, album['name'].replace('/',' - ').replace('  ',' '))

    if(album['name'] == 'Dream'):
        continue

    if not os.path.exists(album_path):
        os.makedirs(album_path)

    # download album art
    if not os.path.exists(os.path.join(album_path, 'folder.jpg')):
        opener.retrieve(album['albumArtRef'], os.path.join(album_path, 'folder.jpg'))

    # skip album if already downloaded
    if(len(album['tracks']) + 1 == len(os.listdir(album_path))):
        print(str(album_count + 1) + '/' + str(num_albums) + ' : CHECK')
        continue

    # for each song
    for song_count, song in enumerate(album['tracks']):

        # announce yourself
        print(str(album_count + 1) + '/' + str(num_albums) + ' : ' + str(song_count + 1) + '/' + str(len(album['tracks'])) + ' ' + artist_name + ' ' + f'\r', end='')

        # check if song missing
        download_path = os.path.join(album_path, song['title'].replace('/',' - ').replace('  ',' ') + '.mp3')
        if (os.path.exists(download_path)):
            continue

        download_url = api.get_stream_url(song['nid'])
        # build paths
        #try:
        #    download_url = api.get_stream_url(song['nid'])
        #except:
        #    print("Error retrieving download URL for song " + song['nid'])
        #    continue

        # download song
        opener.retrieve(download_url, download_path)

        # write metadata
        mp3file = eyed3.load(download_path)
        mp3file.initTag()
        if('title' in song.keys()):
            mp3file.tag.title = song['title']
        if('artist' in song.keys()):
            mp3file.tag.artist = artist_name
        #if('albumArtist' in song.keys()):
        #    mp3file.tag.album_artist = song['albumArtist']
        if('album' in song.keys()):
            mp3file.tag.album = album['name']
        if('trackNumber' in song.keys()):
            mp3file.tag.track_num = song['trackNumber']
        #if('composer' in song.keys()):
        #    mp3file.tag.composer = song['composer']
        if('year' in song.keys()):
            mp3file.tag.release_date = song['year']
        if('genre' in song.keys()):
            mp3file.tag.genre = song['genre']
        mp3file.tag.save()

        time.sleep(5)

    print()
