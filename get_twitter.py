# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 15:10:33 2017

@author: Hp
"""

#CRAWLING TWITTER OFFLINE


from bs4 import BeautifulSoup, NavigableString
import datetime
import pandas as pd
import json
import time

#fungsi untuk menghapus tags yang di list saja, hanya tags bukan konten
def strip_tags(html, invalid_tags):
    soup = BeautifulSoup(html, 'html.parser')

    for tag in soup.findAll(True):
        if tag.name in invalid_tags:
            s = ""

            for c in tag.contents:
                if not isinstance(c, NavigableString):
                    c = strip_tags(str(c), invalid_tags)
                s += str(c)

            tag.replaceWith(s)

    return soup

#fungsi untuk menghapus konten dari tags yang di list    
def remove_tags_contents(html, invalid_tags):
    soup = BeautifulSoup(html, 'html.parser')
    
    for tag in soup.findAll(True):
        if tag.name in invalid_tags:
            for script in soup(tag.name):
                script.decompose()
    return soup

#fungsi untuk menyimpan konten dari tags yang di list, berdasarkan class yang dipakai    
def keep_contents(html, keep_tag, keep_class):
    soup = BeautifulSoup(html, 'html.parser')
    
    for tag in soup.find_all(keep_tag):
        if not bool(set(tag['class']).intersection(keep_class)):
            soup.find(class_=tag['class']).decompose()
    return soup


def get_tweets(soup):
    outputtweet = soup.find_all("li", class_="js-stream-item")
    df = []
    i = 1
    for item in outputtweet:
        if item.find("div", {"class": "tweet"}) != None:
            datauser = item.find("div", {"class": "tweet"})
            tweets = item.find("p", {"class" : "TweetTextSize"})
            tweetid = (datauser['data-item-id'])
            userid = (datauser['data-user-id'])
            twitterid = (datauser['data-screen-name'])
            twittername = (datauser['data-name'])
            datatweet = item.find("span", {"class": "_timestamp"})
            date = datatweet['data-time']
            date = time.strftime("%d-%m-%Y", time.localtime(int(date)))
            count_retweet = item.find("span", {"class": "ProfileTweet-action--retweet"}).find("span", {"class": "ProfileTweet-actionCount"})['data-tweet-stat-count']
            count_favorite = item.find("span", {"class": "ProfileTweet-action--favorite"}).find("span", {"class": "ProfileTweet-actionCount"})['data-tweet-stat-count']
            count_reply = item.find("span", {"class": "ProfileTweet-action--reply"}).find("span", {"class": "ProfileTweet-actionCount"})['data-tweet-stat-count']
             
            tweet = tweets.getText(separator=' ')
            tweet = tweet.replace('@ ','@')
            tweet = tweet.replace('# ','#')
            tweet = str(tweet).replace('\n','')
            print(i)
            i = i + 1
            df.append({'tweet_id' : str(tweetid), 'user_id' : str(userid), 'twitter_screen': str(twitterid),
                       'twitter_name' : str(twittername), 'tweet_date' : str(date), 'retweet' : count_retweet,
                       'favorite' : count_favorite, 'reply' : count_reply , 'tweet' : tweet
                       })
    dffinal = pd.DataFrame(df)
    return dffinal


    
## end of function


##-main

html_doc = open('E:/IDXP/FWD/New folder/fwdlife_id - Pencarian Twitter.html', encoding='utf8')
soup = BeautifulSoup(html_doc, 'html.parser')
dffinal = get_tweets(soup)

outfileurl = "E:/IDXP/FWD/twitter_post.csv"    
dffinal.to_csv(outfileurl, sep='`', encoding='utf-8', index=False)
df2 = pd.read_csv(outfileurl, sep="`")

#print(soup.prettify())

invalid_tags = ['span', 'img', 'strong', 's', 'b', 'p','a']
remove_tags = ['a', 'strong']
keep_class = ['twitter-hashtag', 'js-nav']


    
n = int(len(outputtweet))
i = 0
#print(outputtweet[0].prettify())
print(n)
mylist = list(range(1,n+1))
print(mylist)
df = pd.DataFrame(index=mylist,columns=('tweetid', 'userid', 'twitterid', 'twittername', 'tweets', 'datetimetweets'))

while n > 0:
    datauser = outputtweet[i].find("div", {"class": "tweet"})
    tweets = outputtweet[i].find("p", class_="TweetTextSize")
    
    #print('NO :', i + 1 ,' \n')
    #get tweetid
    df.tweetid[i+1] = (datauser['data-item-id'])
    #print('tweetid = ', tweetid)
    #get userid
    df.userid[i+1] = (datauser['data-user-id'])
    #print('userid = ', userid)
    #get twitterid
    df.twitterid[i+1] = (datauser['data-screen-name'])
    #print('twitterid = ', twitterid)
    #get twittername
    df.twittername[i+1] = (datauser['data-name'])
    #print('twittername = ', twittername)
    
    
    #get tweets
    
    tweets = keep_contents(str(tweets), 'a', keep_class)
    tweets = str(strip_tags(str(tweets), invalid_tags)).replace('\n','')
    tweets = str(strip_tags(str(tweets), invalid_tags)).replace('[pic]','')
    tweets = str(strip_tags(str(tweets), invalid_tags)).replace('—','')
    tweets = str(strip_tags(str(tweets), invalid_tags)).replace('&amp;','&')
    tweets = str(strip_tags(str(tweets), invalid_tags)).replace('&amp','&')

    df.tweets[i+1] = tweets
    #print('isi tweet = \n', tweets ,'\n')

    #get date time
    datatweet = outputtweet[i].find("span", {"class": "_timestamp"})
    datetweets = datatweet['data-time']
    df.datetimetweets[i+1] = datetime.datetime.fromtimestamp(int(datetweets)).strftime('%d-%m-%Y %H:%M:%S')
    #print('Tanggal Tweet = \n', datetweets)
    
    #['data-time']
    i = i + 1
    n = n - 1    
print(df)

df.to_csv('C:/Users/Hp/Documents/idxp/html/test3.csv', sep=';')

