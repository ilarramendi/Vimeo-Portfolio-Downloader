from requests import Session, get
from re import findall, search
from os import path, mkdir
from subprocess import call
import datetime
import json
from html.entities import entitydefs
from sys import argv
from shutil import move

BASE_URL = "https://vimeopro.com"
VIDEO_BASE_URL = "https://player.vimeo.com/video"
CONFIG_PATH = './config.json'
TMP_FILE = './tmp.mp4'

DRY_RUN = '--dry' in argv

DOWNLOAD = []
WGET_BIN = ''
OUTPUT_DIR = ""

# Load config.json
with open(CONFIG_PATH, 'r') as f:
    js = json.loads(f.read())
    DOWNLOAD = js['download']
    WGET_BIN = js['WGET_BIN']
    OUTPUT_DIR = js['OUTPUT_DIR']

# Check if paths exist
if not(path.exists(OUTPUT_DIR)):
    print(OUTPUT_DIR, 'directory dosnt exist!')
    quit()
if not(path.exists(WGET_BIN)):
    print('No binary for wget found in:', WGET_BIN)
    quit()

for portfolio in DOWNLOAD:
    print('Downloading: ', portfolio['name'])
    session = Session() # Session needed in this case to get response cookies
    page = session.post(
        BASE_URL + portfolio['url'],
        headers={'User-Agent': 'Mozilla/5.0'},
        data={'password': portfolio['password']})
    if page.status_code == 200 and len(session.cookies) > 0:
        cookies = {}
        for cookie in session.cookies:
            # Save response cookie for later (also can be made only using session but meh)
            if 'portfolio' in cookie.name: cookies = {cookie.name: cookie.value} 

        if cookies == {}: 
            print('Response cookie not found.')
            break

        pageNumber = 1
        while page.status_code == 200:
            videos = findall(
                '"(' + portfolio['url'].replace('/', '\/') + '\/video\/(\d+))"[^>]+ title="([^"]+)"',
                str(page.content))
            for video in videos: # video => [URL, ID, TITLE]
                title = video[2] 
                for k,v in entitydefs.items():  # Replace HTML Special character codes with the actual character
                    title = title.replace('&' + k + ';', v)
                
                # Create output subdirectory if missing
                out_dir = path.join(OUTPUT_DIR, portfolio['name'])
                if not (path.exists(out_dir) or DRY_RUN): mkdir(out_dir)

                # If no date was found save as video title (SEARCHES FOR DATE FORMAT: DD-MM-YYYY)
                tmp = search("(\d{2})-(\d{2})-(\d{4})", str(title))
                out = ''
                if tmp:
                    date = tmp.group(3) + '-' + tmp.group(2) + '-' + tmp.group(1)
                    # SAVE WITH DATE FORMAT YYYY-MM-DD FOR BETTER SORTING
                    out = path.join(out_dir, portfolio['name'] + '_' + date + '.mp4')
                else: out = path.join(out_dir, portfolio['name'] + '_' + title + '.mp4')
                
                # Only download if file dosnt exist
                if not path.exists(out) or DRY_RUN:
                    print('Downloading:', out.rpartition('/')[2])
                    videoPage = get(
                        # Get porfolio_id (needed) from cookies
                        VIDEO_BASE_URL + '/' + video[1] + "?portfolio_id=" + list(cookies.keys())[0].partition('_')[2],
                        cookies=cookies,
                        headers={'referer': BASE_URL} # Referer here is needed to work
                    ) 
                    
                    # Get direct link (mp4) to video
                    js = json.loads(search('"progressive":(\[[^]]+])}', str(videoPage.content)).group(1))
                    if len(js) > 0:
                        maxRes = js[0]['height']
                        url = js[0]['url']
                        for stream in js: # Find highest resolution video available
                            if stream['height'] > maxRes: 
                                url = stream['url']
                                maxRes = stream['height']
                        if DRY_RUN: print(url)
                        elif call([WGET_BIN, url, '-O', TMP_FILE, '-q', '--show-progress']) != 0: # Download with WGET
                            print('Error downloading video from url:', url)
                        else: move(TMP_FILE, out)
                    else: print('No video tracks found!')
           
            # Stop if no videos found
            if len(videos) == 0:
                print('No videos found in page')
                break
            
            # Check if more pages exist
            pageNumber += 1
            if (portfolio['url'] + '/page/' + str(pageNumber)) in str(page.content): 
                # Request next page and repeat
                page = get(BASE_URL + portfolio['url'] + '/page/' + str(pageNumber), cookies=cookies)
            else: break
        else: print('Error accessing:', page.url)    
    else: print('Wrong password or cant get cookie')    

print('DONE!')
