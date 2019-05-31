from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
from pandas import DataFrame, Series
import time
import pychromecast


#===============================================================
# . Studio Ghibli Chromecast Movie Player .
#  Chromecast various Ghibli movies via video link. If links
#  are active, this controller and script will work. See notes
#  for more information.
#===============================================================


# File where the video links are saved.
mov = pd.read_csv('ghiblimovies.csv', encoding='latin1')


# Script that grabs the download URLs from the embedded videos.
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


# Script that takes the download URL and sends it to the Chromecast.
# NOTE: You must input the device you want to cast to under "device_friendly_name".
def chromecast(url):
    print("\nCasting to Chromecast....\nPlease wait.....")

    ### Input the name of the Chromecast you want to cast to. ###
    device_friendly_name = "Kitchen TV"
    
    chromecasts = pychromecast.get_chromecasts()
    cast = next(cc for cc in chromecasts if cc.device.friendly_name == device_friendly_name)

    cast.wait()

    mc = cast.media_controller
    play = mc.play_media(url, 'video/mp4')
    
    mc.block_until_active()

    mc.pause()
    time.sleep(5)
    mc.play()

    
        
# Do not alter, entire program will not work.
def main():
    movtitle = str(input('Please enter the movie title. \n Title: '))
    movres = str(input('Please enter one of the following viewing resolutions, 360p, 480p, 720p. \n Resolution: '))

    print("\nPreparing to cast", movtitle,',', movres,'...\n')
    chromecast(getVideoURL(movtitle,movres))
    

main()

    
