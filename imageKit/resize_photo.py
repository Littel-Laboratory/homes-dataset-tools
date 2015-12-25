#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  crop pistures from imagenet style list (eg. hoge/hoge/test.jpg 2)
#
#  usage: ./crop_csv.py list_path destination_directory_path
#
import cv2
import argparse
import os
import numpy
import csv
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("list_file")
parser.add_argument("target_dir")
parser.add_argument('--root', '-r', default='./photo/',
                            help='Root directory path of image files')
args = parser.parse_args()

target_shape = (256, 256)

# ファイルパスを配列に入れて返す
def load_image_list(path):
    file_list = []
    for line in open(path, 'r'):
        vals = line.strip().split(' ')
        file_list.append(vals[0])
    return file_list

image_list = load_image_list(args.list_file)

for image in image_list:
    source_imgpath = image
    src = cv2.imread(args.root + source_imgpath)
    if (src == None) :
	print "fail"
	continue
    # mirror image
    while src.shape[0] < target_shape[0] or src.shape[1] < target_shape[1]:
        print src.shape
        src = numpy.concatenate((numpy.fliplr(src), src), axis=1)
        src = numpy.concatenate((numpy.flipud(src), src), axis=0)
    src = src[:target_shape[0], :target_shape[1]]
    print src.shape
    dir_name, file_name = os.path.split(args.target_dir+"/"+source_imgpath)
    print dir_name
    if os.path.isdir(dir_name) == False :
	os.makedirs(dir_name)
    cv2.imwrite(args.target_dir+"/"+source_imgpath, src)
