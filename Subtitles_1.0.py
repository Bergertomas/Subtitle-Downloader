# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 13:50:42 2016

@author: Tomas
"""
"""
Using parts of the amazing Subliminal module by Diaoul @ https://github.com/Diaoul/subliminal
"""
""" 
A code that when run will scan an entire folder for preset video format files
and download the appropriate and matching subtitle file for each of the video files.
"""
import glob
import os
import urllib.request
import sys
import hashlib
import shutil
import time
import babelfish
import subliminal


def loadVideos(folder):
    """
    folder: str, the path of the folder in which to search for video files.
    Returns a list consisting of the names of each video file in folder.
    """
    videoList = []
    extensions = [".avi", ".mpeg", ".mkv", ".mp4", ".mpg", ".mov", ".wmv"]
    for ext in extensions:
        filetemp = glob.glob(folder + "/" + "*" + ext)
        for name in filetemp:
            file_name, file_ext = os.path.splitext(name)
            videoList.append(os.path.basename(file_name))
    return videoList
    
def loadPath(video, folder):
    """
    video: str, the name of the video file we want to get the path to.
    folder: str, the path of the folder in which the video file resides.
    Returns videoName, a str of the complete path to the video file inc. ext.
    """
    videoName = ""
    extensions = [".avi", ".mpeg", ".mkv", ".mp4", ".mpg", ".mov", ".wmv"]
    for ext in extensions:
        filetemp = glob.glob(folder + "/" + "*" + ext)
        for name in filetemp:
            file_name, file_ext = os.path.splitext(name)
            file_name_updated = os.path.basename(file_name)
            if file_name_updated == video:
                videoName = name
    return videoName   
 
def get_hash_subDB(path):
    readsize = 64 * 1024
    with open(path, 'rb') as f:
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()
       
   
def downloadSubtitle_subDB(video, folder):
    """
    video: str, describing the name of a video file.
    folder: the path of the folder in which the video file resides.
    Returns a downloaded subtitle file to the video folder.
    """
    videoPath = loadPath(video, folder)
    user_agent = 'SubDB/1.0 (Subtitle-Downloader/0.1; https://github.com/Bergertomas/Subtitle-Downloader)'
    language = 'en'
    action = 'download'
    base_url = 'http://api.thesubdb.com/?'
    hashed = get_hash_subDB(videoPath)

    content = {
        'action': action,
        'hash': hashed,
        'language': language,
    }
    url = base_url + urllib.parse.urlencode(content)
    req = urllib.request.Request(url)
    req.add_header('User-Agent', user_agent)
    res = urllib.request.urlopen(req)
    subtitles = res.read()
    file_name = video + '.srt'
    subsCurrentPath = os.path.abspath(file_name)
    with open(file_name, 'wb') as f:
        f.write(subtitles)
    shutil.move(subsCurrentPath, folder)
    print ("Downloaded!")
               
    
def downloadSubtitle_OpenSubtitles_heb(videoname, folder):
    video = subliminal.Video.fromname(videoname)
    best_subtitles = subliminal.download_best_subtitles([video], {babelfish.Language('heb')}, providers=None)
    best_subtitle = best_subtitles[video][0]
    file_name =  folder + "/" + videoname + ".srt"
    subtitle = best_subtitle.content
    with open(file_name, 'wb') as f:
        f.write(subtitle)

def downloadSubtitle_OpenSubtitles_eng(videoname, folder):
    video = subliminal.Video.fromname(videoname)
    best_subtitles = subliminal.download_best_subtitles([video], {babelfish.Language('eng')}, providers=None)
    best_subtitle = best_subtitles[video][0]
    file_name =  folder + "/" + videoname + ".srt"
    subtitle = best_subtitle.content
    with open(file_name, 'wb') as f:
            f.write(subtitle)

def getSubtitles(folder):
    """
    folder: The folder containing the video files for which we would like to download subtitles. 
    returns a subtitle file corresponding and relevant for each video.
    """
    videoList = loadVideos(folder)
    downloadSubs = True
    if not videoList:
        print("Couldn't find any videos in the selected folder!")
        downloadSubs = False
    while downloadSubs is True:
        user_choice = input("Would you like to download subtitles in English or in Hebrew?"
        " Enter 'e' or 'א' for English, and 'h' or 'ע' for Hebrew. Enter 'q' to exit.\n"
        "You can also enter 'subDB' to search the subDB database:  ")
        if user_choice == "H" or user_choice == "h" or user_choice == "ע":
            for video in videoList:
                print("מוריד כתוביות עבור " + video)
                try:
                    downloadSubtitle_OpenSubtitles_heb(video, folder)
                except urllib.error.HTTPError as err:
                    print("לא ניתן למצוא כתוביות... :/")
            downloadSubs = False
        elif user_choice == "E" or user_choice == "e" or user_choice == "א":
            for video in videoList:
                print("Downloading subtitles for " + video + "!")
                try:
                    downloadSubtitle_OpenSubtitles_eng(video, folder)
                except urllib.error.HTTPError as err:
                    print("Couldn't find matching subtitles. Trying to search on a different site...")
                    try:
                        downloadSubtitle_subDB(video, folder)
                        time.sleep(10)
                    except urllib.error.HTTPError as err:
                        print ("Couldn't find subtitles for the video(s). Sorry...")         
            downloadSubs = False
        elif user_choice == "q" or user_choice == "Q":
            downloadSubs = False
        elif user_choice == "subDB":
            for video in videoList:
                print("Downloading subtitles for " + video + "!")
                try:
                    downloadSubtitle_subDB(video, folder)
                    time.sleep(10)
                except urllib.error.HTTPError as err:
                    print ("Couldn't find subtitles for the video(s). Sorry...")
            downloadSubs = False
        else:
            print("Couldn't understand your input. please type again!")
    if not videoList:
        pass
    else:
        print("Finished downloading subtitles for all files in " + folder + " !")
    
if __name__ == '__main__':
    directory = input("Please insert a valid folder path: ")
    getSubtitles(directory)
    another = True
    while another:
        user = input("Do you want to do anything else? press y or n: ")
        if user == "y":
            directory = input("Please insert a valid folder path: ")
            getSubtitles(directory)
        else:
            another = False

        
  
    
