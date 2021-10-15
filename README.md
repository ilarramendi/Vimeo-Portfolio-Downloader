# Vimeo-Portfolio-Downloader
Python script to find MP4 links from password protected Vimeo-PRO collection (portfolios) and download them using WGET since the direct download of the vimeopro.com page (not mp4) with youtube-dl only downloaded the audio most of the times and had problems with password protection.

This script can also be used to generate direct links to Vimeo-PRO videos that can be played on any browser without a password or be easily downloaded with WGET.

This was developed to automaticaly download new videos from a certain institution 👀 (no names given) but should work with any Vimeo-Pro portfolio that is password protected, it can be easily modified (not implemented) to download videos from collections without password or from vimeo.com insted of vimeopro.com, the video file selected is the highest resolution available.

## USAGE
1) Clone repository (`git clone https://github.com/ilarramendi/Vimeo-Portfolio-Downloader`)
2) install requests `pip3 install requests`
3) Install WGET `sudo apt install wget`
4) Edit `config.json`:  
&nbsp;&nbsp;&nbsp;&nbsp;`WGET_BIN`: Path to wget binary (`whereis wget`)  
&nbsp;&nbsp;&nbsp;&nbsp;`OUTPUT_DIR`: Output directory (file names explained later)  
&nbsp;&nbsp;&nbsp;&nbsp;`DOWNLOAD`: Array with multiple collections to download:  
&nbsp;&nbsp;&nbsp;&nbsp;> `NAME`: Name to save the collection  
&nbsp;&nbsp;&nbsp;&nbsp;> `URL`: Collection URL: `/USER/COLLECTION_NAME` (NOT `vimeopro.com/USER/COLLECTION_NAME`)  
&nbsp;&nbsp;&nbsp;&nbsp;> `PASSWORD`: Collection password  
4) RUN: `python3 Vimeo-Portfolio-Downloader.py`

## Output
Videos will be saved in the sub-directory: `OUTPUT_DIR/NAME`  
Video titles are taken from vimeo, if a date was found in the title it will be stored as: `NAME_YYYY-MM-DD.mp4`  
If no date was found it will be stored as: `NAME_TITLE.mp4`  

## Parameters
`--dry`: Performs a dry run only printing the mp4 url to STDOUT
