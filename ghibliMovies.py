from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
from pandas import DataFrame, Series
import time
import pychromecast

mov = pd.read_csv('ghiblimovies.csv', encoding='latin1')

def getVideoURL(movtitle, movres):
    search = mov[mov['TITLE'].str.contains(movtitle)]
    url = search['VIDEO URL'].values[0]
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    
    if movres == '720p':
        p720 = soup.find('source', label="720p")
        url = p720.get('src')
        return url

    elif movres == '480p':
        p480 = soup.find('source', label="480p")
        url = p480.get('src')
        return url

    elif movres == '360p':
        p360 = soup.find('source', label="360p")
        url = p360.get('src')
        return url

def chromecast(url):
    print("\nCasting to Chromecast....\nPlease wait.....")
    device_friendly_name = True
    chromecasts = pychromecast.get_chromecasts()
    cast = next(cc for cc in chromecasts if cc.device.friendly_name == device_friendly_name)

    cast.wait()

    mc = cast.media_controller
    mc.play_media(url, 'video/mp4')

    mc.block_until_active()

    mc.pause()
    time.sleep(5)
    mc.play()

def main():
    movtitle = str(input('Please enter the movie title. \n Title: '))
    movres = str(input('Please enter one of the following viewing resolutions, 360p, 480p, 720p. \n Resolution: '))

    print(" ", movtitle,', ', movres)
    chromecast(getVideoURL(movtitle,movres))

main()

    
