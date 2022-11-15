import json

import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords

nltk.data.path.append("/tmp")
nltk.download('stopwords', download_dir="/tmp")
def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        songs = getLyrics(body['author'])
        return {
            "statusCode": 200,
            "body": json.dumps({
                'lyrics': songs
            }),
            "headers": {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
            }
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": "Error processing your request: "+e,
            "headers": {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
            }
        }
"""
Function to get the lyrics of certain number of songs of an artist
Arguments:
    artist: Name of the artist
    songs: Number of songs
"""
def getLyrics(artist, songs=3):
    # Web scrapping to get songs
    URL = "https://genius.com/artists/"+artist
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    #listSongsDiv = soup.find("div", class_="mini_card_grid")
    songsDiv = soup.find_all("div", class_="mini_card_grid-song")[0:songs]
    songsLyrics = []
    for song in songsDiv:
        songURL = song.find("a", class_="mini_card").get("href")
        songsLyrics.append(getLyric(songURL).replace(',', ''))
    return songsLyrics

"""
Function to get the lyrics of a songs
Arguments:
    url: url of genius.com song page
"""
def getLyric(url):
    # Web scrapping to get songs

    URL = url
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    lyrics1 = soup.find("div", class_="Lyrics__Container-sc-1ynbvzw-6 YYrds")
    
    if lyrics1:
        # Splitting text to delete the stop words
        # Combining spanish and english stop words, the most popular languages
        stop_words = stopwords.words('english') + stopwords.words('spanish')
        words = lyrics1.get_text().split()
        filtered_words = []
        for word in words:
            if word not in stop_words:
                filtered_words.append(word)
        lyrics = ' '.join(filtered_words)

    else:
        words = soup.find("div", class_="lyrics").get_text().split()

    return lyrics