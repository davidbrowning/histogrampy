#!/usr/bin/python

import argparse
import cv2
import sys
import os
import re
import cPickle as pickle

################################
# module: hist_image_index.py
# author:  your name and A-number
# description: persistent image histogram indexer
# to run:
#
# $ python hist_image_index.py -imgdir images/ -clr rgb -hist rgb_hist16.pck -bin 16
# $ python hist_image_index.py -imgdir images/ -clr hsv -hist hsv_hist16.pck -bin 16
#
# the output will look as follows:
# ...
# indexing images/16_07_02_14_50_48_orig.png
# images/16_07_02_14_50_48_orig.png indexed
# images/16_07_02_14_37_38_orig.png
# images/16_07_02_14_37_38_orig.png indexed
# images/123473019.JPG
# images/123473019.JPG indexed
# indexing finished
#
# when indexing is finished, the persisted index object is
# saved in rgb_hist16.pck and hst_hist16.pck
################################

ap = argparse.ArgumentParser()
ap.add_argument('-imgdir', '--imgdir', required = True, help = 'image directory')
ap.add_argument('-hist', '--hist', required = True, help = 'histogram index file')
ap.add_argument('-bin', '--bin', required=True, help='histogram bin size')
ap.add_argument('-clr', '--clr', required=True, help='color space')
args = vars(ap.parse_args())

HIST_INDEX = {}

def generate_file_names(fnpat, rootdir):
    for path,dirlist, filelist in os.walk(rootdir):
        for file_name in filelist:
            if(re.match(fnpat, file_name)):
                yield (os.path.join(path, file_name))

def hist_index_img(imgp, color_space, bin_size=8):
  im = cv2.imread(imgp)
  global HIST_INDEX
  if(color_space == 'rgb'):
    HIST_INDEX[imgp] = cv2.calcHist([im], [0,1,2], None, [bin_size,bin_size,bin_size], [0,256,0,256,0,256])
  elif(color_space == 'hsv'):
    hsv_im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    HIST_INDEX[imgp] = cv2.calcHist([hsv_im], [0,1,2], None, [bin_size,bin_size,bin_size], [0,256,0,256,0,256])

def hist_index_img_dir(imgdir, color_space, bin_size):
    for img in generate_file_names(r'.+\.(jpg|png|JPG)', imgdir):
        hist_index_img(img, color_space, bin_size)

if __name__ == '__main__':
  hist_index_img_dir(args['imgdir'], args['clr'], int(args['bin']))
  with open(args['hist'], 'wb') as histpick:
    pickle.dump(HIST_INDEX, histpick)
  print('indexing finished')


