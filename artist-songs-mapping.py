from urllib.request import Request, urlopen
import urllib.error, urllib.parse
from bs4 import  BeautifulSoup
import json, ssl
from time import  sleep
import sys

#Ignoring the https certificates security errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#the base url where songs name of each artist will be scrapped
songs_url = "http://www.song-list.net/{}/songs"
artists = ["coldplay", "hozier", "samsmith", "rihanna"]
artist_mapping = dict()

#requesting each artist songs url and scrapping the html page to get the songs
for artist in artists:
    song_artist_url = songs_url.format(artist)
    print("retreving", song_artist_url)
    
    # must use Request to avoid security modes errors
    req = Request( song_artist_url , headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find('table', attrs={'class':'songs'}).find_all('td', attrs={'id':'songname'})
    
    artist_mapping[artist]= []
    
    for tag in tags:
        song_name = tag.text.strip()
        artist_mapping[artist].append(song_name)
        
    print("artist", artist)
    print(artist_mapping[artist][:5])
    sleep (10)
    
for k, v in artist_mapping.items():
    print(k,len(v))
    


json_file = "Artists-Songs.json"
with open(json_file, 'w') as file:
    json.dump(artist_mapping, file)

with open(json_file) as f:
    a = json.load(f)
    print(a)
    


       
     
        