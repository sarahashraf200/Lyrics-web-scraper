from urllib.request import Request, urlopen
import urllib.error, urllib.parse
from bs4 import  BeautifulSoup
import json, ssl
from time import  sleep
import sys
import re

#Ignoring the "https" certificates security errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

song_list = "Artists-Songs.json"
songs_dict = dict()
#returning a dictionary which includes the artist and its songs
with open(song_list) as file:
    songs_dict = json.load(file)
    
artist = input("choose the artist, please")  

songs = songs_dict[artist]  
song_name = []

#applying regular expression on each song to clear it before using it in scraping
for song in songs:
    brackets_removed = re.sub(r'\(.*\)',"",song)
    clear_song = re.sub(r'\W+', '', brackets_removed).lower()
    song_name.append(clear_song)
# put the list as a set to avoid any duplication    
song_name = list(set(song_name))
print(song_name) 

A_Z_url = "https://www.azlyrics.com/lyrics/{}/{}.html"
lyrics_file = "song-lyrics.txt"
with open(lyrics_file, "w") as file:
    
    for songs in song_name:
        final_url = A_Z_url.format(artist,songs)

        try:
            req = Request(final_url , headers={'User-Agent': 'Mozilla/5.0'})
            html_page = urlopen(req, context = ctx).read()
            soup = BeautifulSoup(html_page, 'html.parser')

            class_name = soup.find('div', attrs={'class':'ringtone'})
            _name = class_name.find_next('b').contents[0].strip()
            lyrics = class_name.find_next('div').text.strip()

            file.write("Song name: ", _name )
            file.write("============================================================")
            file.write(lyrics)
            file.write("============================================================")
            
            print("Lyrics was found for  : " + _name)
            
        except:
            print("Lyrics not found for : " + songs)
            
            
        finally:
            sleep(10)

