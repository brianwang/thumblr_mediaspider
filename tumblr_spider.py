#!/usr/bin/python

import requests
from pyquery import PyQuery as pq
import feedparser
import urllib2
from threading import Thread
import os

def crawl(url):
    proxies = {
        'http': '127.0.0.1:1080',
        'https': '127.0.0.1:1080',
    }
    rss = requests.get(url, proxies= proxies)
    feed = feedparser.parse(rss.content)
    items = feed["items"]
    if len(items) == 0:
        return
    allmedias = []
    for item in items:
        content = item['description'].encode('utf-8').replace('_500','_1280')
        imgs = pq(content)('img')
        for img in imgs:
            imgurl = pq(img).attr('src')
            t= Thread(target=download,args=(imgurl, imgurl.split('/')[-1],'img'))
            t.start()
        videos = pq(content)('video source').attr('src')
        if videos is not None:
            t=  Thread(target=download,args=(videos, videos.split('/')[-1]+'.mp4','video'))
            t.start()

def download(url, name,type='img'):
    proxies = {
        'http': '127.0.0.1:1080',
        'https': '127.0.0.1:1080',
    }
    if type == 'img':
        path = './imgs/'+name
    elif type == 'video':
        path = './videos/'+name
    rsp = requests.get(url,proxies= proxies)
    if not os.path.exists(path):
        with open(path,'wb') as f:
            for chunk in rsp.iter_content(chunk_size=10240): 
                f.write(chunk)
        f.close()
    print url+' complete!!!'

def spider(username):
    urls = []
    urls.append('https://'+username +'.tumblr.com/rss')
   
    for p in range(2,20):
        urls.append('https://'+username+'.tumblr.com/page/'+str(p)+'/rss')


    for url in urls:
        crawl(url)

#crawl('http://p66.tumblr.com/rss')
#crawl('http://davidtz8886.tumblr.com/rss')
#url ='https://78.media.tumblr.com/0ae99c6db393f5467ed0022ca19347ea/tumblr_oyr2djieBe1upugcqo6_1280.jpg'
#download(url, url.split('/')[-1],'img')
#crawl('http://fish1025559.tumblr.com/rss')
#download('p66')
#download('davidtz8886')
spider('davidtz8886')