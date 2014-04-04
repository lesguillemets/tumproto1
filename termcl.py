#!/usr/bin/env python2
# coding:utf-8
from __future__ import print_function
#from __future__ import unicode_literals # can't just data ="path/to/my/file"
import keys
import pytumblr
import urllib2
import Queue
import threading
from postprinter import PostPrinter
from textwrap import dedent
from colors import prettify

client = pytumblr.TumblrRestClient(
    keys.consumer_key,
    keys.consumer_secret,
    keys.oauth_tokens['oauth_token'],
    keys.oauth_tokens['oauth_token_secret']
)


class Myapp(object):
    """ base class."""
    
    def __init__(self, tracked_tags, workernum=5, client=client):
        self.tracked_tags = tracked_tags
        self.client = client
        self.freshqueue()
        self.workernum = workernum
    
    def freshqueue(self):
        self.readqueue = Queue.Queue()
        for tag in self.tracked_tags:
            self.readqueue.put(tag)
        self.readqueue.put(None)
        self.tlqueue = Queue.Queue()
    
    def readworker(self,**args):
        while not self.readqueue.empty():
            tag = self.readqueue.get()
            if tag is None:
                self.readdashboard()
                continue
            print(" {} {}".format(
                prettify('reading','green','blue'),tag.encode("utf-8")))
            if not args:
                posts = self.client.tagged(tag.encode('utf-8'))
            else:
                posts = self.client.tagged(tag.encode('utf-8'), **args)
            print(" {} : {}".format(tag.encode('utf-8'),len(posts)))
            for post in posts:
                self.tlqueue.put(post)
            self.readqueue.task_done()
            print(" {}: {}".format(
                prettify('Job done','magenta','cyan'),
                tag.encode('utf-8')))
    
    def readdashboard(self, **args):
        print(" {} dashboard".format(
            prettify('reading','green','blue')))
        posts = self.client.dashboard()['posts']
        for post in posts:
            #print(post)
            self.tlqueue.put(post)
        self.readqueue.task_done()
        print(" dashboard has been read")
    
    def read(self):
        for i in range(self.workernum):
            t = threading.Thread(target=self.readworker)
            t.start()
        self.readqueue.join()
    
    def showtl(self,n=15):
        tl = []
        while not self.tlqueue.empty():
            tl.append(self.tlqueue.get())
        tl.sort(key=lambda x:x['timestamp'])
        for post in reversed(tl[-n:]):
            self.printpost(post)
    @staticmethod
    def printpost(post):
        print(PostPrinter().show(post))
    
    def tryme(self):
        self.read()
        self.showtl()


tracked_tags = ["chat",'ask',"firefox",] #"monospaced", "programming", 'Georgia',
#                'Georgian language', 'tbilisi', 'kartveli', 'sakartvelo',
#                'linux','bash','bashrc','vimrc','vim','monospace',
#                'processing','regex','typography','typesetting',
#                'typeface','font', 'train','cityscape','ruby rose']
a = Myapp(tracked_tags)
a.tryme()
