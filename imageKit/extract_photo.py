#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  extract photo-rent-XX.tar.bz2
#
#  usage: ./extract_photo.py dataset_path
#
import tarfile
import sys
import os
import re
import argparse

## parsing arguments
parser = argparse.ArgumentParser()
parser.add_argument('dataset_path', help='the dataset directory path')
parser.add_argument('id_prefix_list', metavar='ID_PREFIX', nargs='*',
                    help='the prefix(s) of the property IDs')
parser.add_argument('-t', '--target-path', help='the target directory path to be extracted. (default=[dataset_path]/photo)')
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()
dataset_path = args.dataset_path
target_path = args.target_path
if target_path is None:
    target_path = os.path.join(dataset_path, 'photo')

## 展開するIDリスト
path_prefix_list = []
for id_prefix in args.id_prefix_list:
    if len(id_prefix) <= 2:
        path_prefix = id_prefix
    elif len(id_prefix) <= 4:
        path_prefix = id_prefix[:2] + '/' + id_prefix[2:4]
    else:
        path_prefix = id_prefix[:2] + '/' + id_prefix[2:4] + '/' + id_prefix[4:]
    path_prefix_list.append(path_prefix)

## check whether 'dataset_path' is a directory
if not os.path.isdir(dataset_path):
    sys.stderr.write('"%s" must be a directory.\n' % dataset_path)
    sys.exit(1)

## 解凍対象ファイルの取得
pattern_photo = re.compile('^photo-rent-\d\d\.tar\.bz2$')
bz2_list = [os.path.join(dataset_path, x) for x in sorted(os.listdir(dataset_path))
            if pattern_photo.match(x)]
if len(bz2_list) == 0:
    sys.stderr.write('"%s" has no photo archive files.\n' % dataset_path)
    sys.exit(1)

# 解凍先ディレクトリの作成
if not os.path.exists(target_path):
    os.mkdir(target_path)

## tar.bz2ファイルを読み、条件にマッチするファイルのみを書き出す
def _match_conditions(m):
    if len(path_prefix_list) > 0:
        for p in path_prefix_list:
            if m.name.startswith(p):
                return True
        return False
    else:
        return True

for bz2 in bz2_list:
    tf = tarfile.open(bz2, 'r')
    sys.stderr.write("extracting %s\n" % bz2)
    for m in tf:
        if not _match_conditions(m): 
            tf.members = []
            continue
        if args.verbose:
            sys.stderr.write(m.name + "\n")
        tf.extract(m, target_path)
        tf.members = []
    tf.close()
