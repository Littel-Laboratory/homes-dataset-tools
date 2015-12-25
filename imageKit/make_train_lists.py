#!/usr/bin/env python
# -*- coding:utf-8 -*-

###
### make train.txt and test.txt for training by chainer and caffe from photo_rent.tsv
###
### usage: 
###	./generate_custom_list.py photo.tsv 
###
### example
###	./make_train_lists.py ../photo_rent.tsv --root /media/homes_dasaset/photo/ --trainphotos 20000 --testphotos 2000 -a /test/ -i 1000 -o 1000

import sys
import argparse
import shutil
import os.path
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('photo_list')
parser.add_argument('--root', '-r', default='./photo/', 
                            help='Absolute path to photo_rent directory')
parser.add_argument('--trainphotos',  default=10000, type=int, 
                            help='Number of photos of each type for train')
parser.add_argument('--testphotos',  default=1000, type=int,
                                    help='Number of photos of each type for test')
parser.add_argument('--interval', '-i', default=10, type=int,
                            help='Interval of photos when picking photos up')
parser.add_argument('--offset', '-o', default=1, type=int,
                                    help='Offset of photos when picking photos up')
args = parser.parse_args()

IMG_PATH_POS = 2
TYPE_POS = 3

# 学習させる画像タイプのリスト　
# デフォルトでは、間取り、地図、玄関、居間、キッチン、風呂、トイレ、洗面、収納
# 設備、バルコニー、エントランス、駐車場
valid_type = [1,3,10,11,12,15,16,17,18,19,20,21,22]

# 有効タイプの画像辞書を作成
def load_image_list(path):
    type_dict = {}
    for i in valid_type :
        type_dict[i] = []

    count = 0
    for line in open(path):
        vals = line.strip().split('\t')
        if len(vals) >= TYPE_POS +1 and vals[TYPE_POS] != '' and np.int32(vals[TYPE_POS]) in valid_type :
            photo_type = np.int32(vals[TYPE_POS])
            photo_path = vals[IMG_PATH_POS]
            type_dict[photo_type].append((photo_path, photo_type))

        count += 1
        sys.stderr.write('\r{}'.format(count))
        sys.stderr.flush()
        #print('filename:%s type: %d' %(photo_path, photo_type))

    return type_dict

# 画像枚数の確認
print("loadning {0}".format(args.photo_list))
data_dict = load_image_list(args.photo_list)

required_photo_count = args.trainphotos + args.testphotos
for i in valid_type:
    if len(data_dict[i]) < required_photo_count:
        print 'type: %d shortage! required count: %d exist count: %d \n prease decrease trainphoto and testphoto' %(i, required_photo_count, len(data_dict[i]))
        sys.exit()

picked_data = {} 

# インターバルとオフセットを元に使用画像を取得
print("generating lists")
for x in valid_type:
    interval = args.interval 
    offset   = args.offset
    picked_data[x] = []
    count = 0
    while(1):
        for pos in range(offset, len(data_dict[x]), interval) :
            file_path = args.root + data_dict[x][pos][0] 
            if os.path.exists(file_path) and os.path.getsize(file_path)!=0 :
                picked_data[x].append(data_dict[x][pos])
                count += 1
                sys.stderr.write('\r{}'.format(count))
                sys.stderr.flush()
                if count >= required_photo_count:
                    break
        offset += 1
        if offset >= interval:
            offset = 0
        if count >= required_photo_count:
            break  

# 各タイプが順に並ぶようにリスト作成
train_list  = ""
test_list   = ""   
resize_list = ""
for x in range(required_photo_count) :
    for photo_type in valid_type:
        if x < args.trainphotos:
            train_list += picked_data[photo_type][x][0] + " "  + str(photo_type) + "\n"
        else:
            test_list += picked_data[photo_type][x][0] + " " + str(photo_type) + "\n"
        resize_list += picked_data[photo_type][x][0] + "\n"

# ファイル書き込み
f = open('train.txt', 'w')
f.write(train_list)
f.close()

f2 = open('test.txt', 'w')
f2.write(test_list)
f2.close()

f3 = open('resize.txt', 'w')
f3.write(resize_list)
f3.close()
