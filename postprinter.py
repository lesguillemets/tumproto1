#!/usr/bin/env python2
# coding:utf-8
from textwrap import dedent
from colors import prettify
from colors import bold, underlined
from postimage import PostImage
import imgterm
import os

"""
pretty prints posts.
"""

def textpost(post):
    return dedent(
        """\
        ==={}===
        {}
        """).format(
            prettify(post['title'].encode('utf-8') if post['title'] else '',
                     'green', None, 'bold', 'underlined'),
            bold(post['body'].encode('utf-8'))
        )

def photopost(post):
    photostr = dedent(
        """\
        {}
        \t{}
        """).format(
            bold(post['caption'].encode('utf-8')),
            '\n\t'.join(
                ('* {}\n\t{}\n\t\t({} : {}x{})'.format(
                    bold(photo['caption'].encode('utf-8')),
                    '\n\t'.join(
                        imgterm.show_img(
                        PostImage.id_and_num_to_file(post['id'],
                                                     photo['alt_sizes'][0]['url'],
                                                     i),
                            method='mean'  # better at letters.
                        )
                    ),
                    prettify(photo['alt_sizes'][0]['url'],'dark gray',None),
                    prettify(photo['alt_sizes'][0]['width'],'dark gray',None),
                    prettify(photo['alt_sizes'][0]['height'],'dark gray',None)
                )
                    for (i,photo) in enumerate(post['photos']))
            )
        )
    return photostr

def quotepost(post):
    quotestr = dedent(
        """\
        {}
        \t---{}
        """).format(
            post['text'].encode('utf-8'),
            prettify(post['source'].encode('utf-8'),
                     'light gray',None),
        )
    return quotestr

def linkpost(post):
    linkstr = "{} ({})\n".format(
        post['title'].encode('utf-8'),
        prettify(post['url'].encode('utf-8'),
        'blue',None))
    linkstr += '\n'.join(
        ('\t'+line.encode('utf-8'))
             for line in post['description'].split())
    return linkstr + '\n'

def chatpost(post):
    return ("CHAT!\n")

def audiopost(post):
    return("audio!\n")

def videopost(post):
    return("video!\n")

def answerpost(post):
    return("answer!\n")

class PostPrinter(object):
    def __init__(self):
        pass
    
    printer = {
        'text' : textpost,
        'photo' : photopost,
        'quote' : quotepost,
        'link' : linkpost,
        'chat' : chatpost,
        'audio' : audiopost,
        'video' : videopost,
        'answer' : answerpost,
    }
    
    @classmethod
    def show(cls, post):
        rows, columns = map(int,os.popen('stty size', 'r').read().split())
        printstr = dedent(
            """\
            {}
            {}
            {} at {} from {}, id is {}
            {} : [{}]
            """).format(
                prettify(' '*columns,'dark gray',None,'underlined'),
                prettify(' '*columns,None,None),
                prettify(post['type'], 'white', 'blue'),
                bold(post['date']),
                prettify(post['blog_name'],None, None,'bold'),
                post['id'],
                prettify('tagged','green',None,'bold'),
                ','.join(
                    list(map(lambda t: underlined(t.encode('utf-8')),
                             post['tags']))
                )
            )
        if 'source_url' in post:
            printstr += "source : {} ({})\n".format(
                post['source_title'].encode('utf-8'),
                post['source_url'].encode('utf-8'))
        printstr += cls.printer[post['type']](post)
        printstr += prettify('({})'.format(post['post_url']).rjust(columns),
                             'dark gray', None)
        printstr += prettify(' '*columns+'\n', 'dark gray',None,'underlined')
        return printstr


