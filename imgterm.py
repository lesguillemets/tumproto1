#!/usr/bin/env python2
# coding:utf-8

from __future__ import print_function
from textwrap import dedent
import PIL.Image as img
import numpy as np
import sys
from rgbtoansi import colorize_bg

def get_termsize():
    try:
        import fcntl, termios, struct
        h, w, _, _ = struct.unpack(
            'HHHH',
            fcntl.ioctl(
                sys.stdout.fileno(),
                termios.TIOCGWINSZ,
                struct.pack('HHHH', 0, 0, 0, 0)))
    except OSError:
        import os
        h, w = map(int,os.popen('stty size', 'r').read().split())
    return w, h

def show_img(imgfile, widthratio=2.0/3, fontratio=2.5, method="upperleft"):
    '''
    imgfile : image file readable by PIL.Image.open
    widthratio : how much of terminal width the image uses
    fontratio : the ratio height/width of your font
    about 2 for monaco, 2.5 for ubuntu mono.
    '''
    w, _ = get_termsize()
    w = int(w*widthratio)
    imgary = np.array(img.open(imgfile))
    imgheight, imgwidth = len(imgary), len(imgary[0])
    marks = [int(float(i)*imgwidth/w) for i in range(w+1)]
    rowpixels = (imgwidth/w)*fontratio  # 2 for monaco, 2.5 for ubuntu mono
    yreadingstart = 0
    while yreadingstart < imgheight-1:
        for (i,m) in enumerate(marks[1:]):
            m_b = marks[i]
            if method == "upperleft":
                pixel = imgary[yreadingstart,m_b]
            elif method == "mean":
                grid = imgary[yreadingstart:yreadingstart+rowpixels,
                              m_b:m]
                pixel = np.array((0,0,0))
                for y_ in range(len(grid)):
                    for x_ in range(len(grid[0])):
                        pixel += grid[y_,x_]
                pixel = pixel//(len(grid)*len(grid[0]))
            
            sys.stdout.write(colorize_bg(' ', list(pixel)))
            sys.stdout.flush()
        yreadingstart += rowpixels
        sys.stdout.write('\n')


def test():
    testfile = 'kitten.jpg'
    show_img(testfile,1/2,2)
    print("______________________________")
    show_img(testfile,1/2,2, 'mean')


def main():
    try:
        filenames = sys.argv[1:]
    except IndexError:
        print("specify filename(s).")
        return
    
    for filename in filenames:
        try:
            show_img(filename,method='mean')
        except IOError:
            print("No file found. Or something like that.")
            continue


if __name__ == "__main__":
    main()
