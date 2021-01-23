# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 12:51:10 2017

@author: OPTUS-81
"""

import subprocess
import os
import urllib.request as urlreq
import urllib.parse as urlparse
import simplejson as json
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as req
import pandas as pd
from collections import defaultdict

titles = []
getcomments = []
comments = []

def getTitles():
    df = pd.DataFrame()
    titles = []
    
    data = {}
    data['channelId'] = 'UCUajjhNQ7CPitfLepxoHdtg' # Put the channelId of channel you want to Sync to.
    data['part'] = 'snippet, contentDetails'
    data['key'] =   'AIzaSyCvPpEsRXK_C-M6_MBQBB4jidWdPyGrmf0'
    
    no = 1
    while True:
        requestValues = urlparse.urlencode(data)
        request = "https://www.googleapis.com/youtube/v3/activities?" + requestValues
        print(request)
        string = urlreq.urlopen(request).read().decode('utf-8')
        items = json.loads(string)['items']
        
        for item in items:
            videoId = item['contentDetails']['upload']['videoId']
            title = item['snippet']['title']
            description = item['snippet']['description']
            print(no)
            no = no + 1            
            titles.append({'id' : videoId, 'title' : title, 'description' : description})
        
        test = json.loads(string)
        if not test.get('nextPageToken'):
            break
        
        nextpagetoken = json.loads(string)['nextPageToken']
        print(nextpagetoken)        
        data['pageToken'] = str(nextpagetoken)
        
    return titles

    getTitles()
    df_titles = getTitles()
    df = df.append(df_titles)
    return df

def getAllComments():
    df = pd.DataFrame()
    allcomments = []
    
    
    data = {}
    data['part'] = 'snippet'
    data['allThreadsRelatedToChannelId'] = 'UCUajjhNQ7CPitfLepxoHdtg' # Put the channelId of channel you want to Sync to.
    data['key'] =   'AIzaSyCvPpEsRXK_C-M6_MBQBB4jidWdPyGrmf0'
        
    while True:
        requestValues = urlparse.urlencode(data)
        request = "https://www.googleapis.com/youtube/v3/commentThreads?" + requestValues
        string = urlreq.urlopen(request).read().decode('utf-8')
        items = json.loads(string)['items']
        for item in items:
            videoId = item['snippet']['videoId']
            author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            comment = item['snippet']['topLevelComment']['snippet']['textOriginal']
      
            allcomments.append({'videoId' : videoId, 'Name' : author,'comment' : comment})
        test = json.loads(string)
        if not test.get('nextPageToken'):
            break
        nextpagetoken = json.loads(string)['nextPageToken']
        data['pageToken'] = str(nextpagetoken)
        
    return allcomments

    getAllComments()
    df_allcomment = getAllComments()
    df = df.append(df_allcomment)
    df.to_csv('D:\Pekerjaan\Python\Crawl\FWD Comments.csv', sep='`', encoding='utf-8')
  

def getCount(titles):
    df3 = pd.DataFrame()
    counts = []
    i = 1
    for title in titles:
        i = i + 1
        videoid = title['id']
    
        data = {}
        data['id'] = videoid
        data['part'] = 'snippet, statistics'
        data['key'] =   'AIzaSyCvPpEsRXK_C-M6_MBQBB4jidWdPyGrmf0'
        requestValues = urlparse.urlencode(data)
        request = "https://www.googleapis.com/youtube/v3/videos?" + requestValues
        string = urlreq.urlopen(request).read().decode('utf-8')
        items = json.loads(string)['items']
        
        for item in items:
            ids = item['id']
            title = item['snippet']['title']
            description = item['snippet']['description']
            date = item['snippet']['publishedAt']
            view = item['statistics']['viewCount']
            like = item['statistics']['likeCount']
            dislike = item['statistics']['dislikeCount']
            comment = item['statistics']['commentCount']
            counts.append({'videoId' : ids, 'Title' : title, 'Description' : description, 'Date' : date,'View' : view, 'Like' : like, 'Dislike' : dislike, 'commentCount' : comment})
        
    return counts

    getCount(df_titles)
    asa = getCount(df_titles)
    df3 = df3.append(asa)
    df3.to_csv('D:\Pekerjaan\Python\Crawl\FWD Video desc.csv', sep='`', encoding='utf-8')
    
    df5= pd.read_csv('D:\Pekerjaan\Python\Crawl\FWD Video desc.csv', sep='`')
