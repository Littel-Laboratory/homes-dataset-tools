# imageKitについて

物件画像の種類の分類器を作成するためのツールキットです。

## 動作環境

* Linux (推奨: Ubuntu 14.04 LTS 64bit または CentOS 7 64bit)
* [Chainer](http://chainer.org/) 1.5.1
* (推奨) GPU利用環境 (CUDA 6.5, 7.0, 7.5)

## HOME'Sデータセットの利用申請

HOME'Sデータセットは国立情報学研究所(NII)のご協力を得て研究資源として提供させていただいております。研究の用途に限定させていただいているため、[情報学研究データリポジトリ(IDR)](http://www.nii.ac.jp/dsc/idr/)より申請をお願いいたします。1～2週間でデータセット提供用ページよりダウンロードしていただけます。

## Chainerのインストール

Linux環境での[Chainer](http://chainer.org/) v1.5のインストールをお願いします。画像枚数が大変多いため、GPUの利用を強くお勧めします。

Chainer自体のインストールは容易ですが、GPU演算のためのCUDAのインストールは、多くの方がよくつまづかれる部分です。[公式ドキュメント](http://developer.download.nvidia.com/compute/cuda/7_0/Prod/doc/CUDA_Getting_Started_Linux.pdf)通りにしていただければよいかと思いますが、よろしければ[こちら](http://qiita.com/bohemian916/items/a48e6496b04bbbf09fb3)も参考にしてください。

Chainerのインストールが終わったら、MNISTのチュートリアルを実行することをお勧めします。

## ツールキットの入手

HOME'Sデータセットから、Chainerに含まれるImageNet用の分類サンプルソースを用いて分類器を学習できるよう、ツールキットを用意しています。下記の通り、GitHubリポジトリからcloneまたはダウンロードしてください。場所はどこでもよいのですが、本文書では、データセットディレクトリ配下にcloneする前提で進めます。

(cloneする場合)
```
cd /path/to/dataset/directory
git clone https://github.com/Littel-Laboratory/homes-dataset-tools.git
```

(ダウンロードする場合)  
https://github.com/Littel-Laboratory/homes-dataset-tools/archive/master.zip


## データセットの展開

本データセットに含まれる物件画像データファイル (photo-rent-NN.tar.bz2) は、tar.bz2形式で圧縮されているので、展開作業が必要です。展開用のツールを用意していますのでご利用ください。

```
cd /path/to/dataset/directory
./homes-dataset-tools/imageKit/extract_photo.py ./
```

* 物件画像の展開にはかなり長い時間がかかります
* 全画像ファイルを展開する場合は、概ね1TBytes以上のディスク領域が必要となります。
* 画像のファイル数がかなり多い (約8300万枚) ため、ディスクの容量とともにinode数をかなり消費します。inode数を多めに確保してフォーマットしてください。

上記を実行すると、データセットディレクトリ内のphotoディレクトリ (/path/to/dataset/directory/photo) に物件画像ファイルが展開されます。
物件画像ファイルは物件と対応づけられています。物件IDは16進数32桁の数字です。物件IDを元に画像ディレクトリが生成されます。画像は0001.jpgから順に番号が振られています。

例: 物件IDが0123456789abcdef0123456789abcdef の場合、この物件IDの画像は photo/01/23/456789abcdef0123456789abcdef に格納されています。
  
画像は、  
0001.jpg  0004.jpg  0007.jpg  0010.jpg  0014.jpg  0017.jpg  
0002.jpg  0005.jpg  0008.jpg  0011.jpg  0015.jpg  0018.jpg  
0003.jpg  0006.jpg  0009.jpg  0013.jpg  0016.jpg  
といった形です。  

また、本ツールキットでは物件画像のメタデータ (画像種類タグ) を学習に用います。
photo_rent.tsv.bz2を展開してください。

```sh
cd /path/to/dataset/directory
bunzip2 photo_rent.tsv.bz2
```

## 訓練データの準備

ImageNetのソースを利用して学習させるために、データセットを加工します。

具体的には、

* 画像のパスとタグ（種類）のリストの作成 
* 画像のリサイズ
* 平均画像生成

を行います。

### 画像パスとタグのリスト作成

リストは、以下のようにスペース区切りで画像パスとタグを記述したものです。今回使用するタグは、画像に付けられた画像タイプです。 (例: 1=間取り, 11=居間, 12=キッチン)

```
00/00/03d67c168129876425c22a106dae/0003.jpg 1
00/00/180a3c6848b723749e1dc9cd4b12/0030.jpg 3
00/00/11fe05aa3585e929b34d887b2dbe/0007.jpg 10
00/00/081549d99cf1e3f5be593e560799/0004.jpg 11
00/00/081549d99cf1e3f5be593e560799/0005.jpg 12
00/00/081549d99cf1e3f5be593e560799/0006.jpg 15
00/00/11fe05aa3585e929b34d887b2dbe/0009.jpg 16
00/00/11fe05aa3585e929b34d887b2dbe/0010.jpg 17
00/00/11fe05aa3585e929b34d887b2dbe/0011.jpg 18
00/00/03d67c168129876425c22a106dae/0014.jpg 19
```

学習には、以下の２つの独立したリストファイルが必要となります。

* train.txt: 訓練用データ
* test.txt: テスト用データ

これを作成するには、ツールキットのmake_train_lists.pyを実行します

```sh
cd /path/to/dataset/directory/homes-dataset-tools/imageKit
./make_train_lists.py ../../photo_rent.tsv
```

すると、各タグの写真のパスがtrain.txt, test.txtにそれぞれ10,000枚、1,000枚づつ含まれたリストが生成されます。また同時にリサイズすべき画像リストresize.txtが生成されます。

make_train_lists.py のオプションで枚数を変更したり、写真をピックアップする際のオフセットやインターバルを変えて、異なる訓練セットを生成することもできます。この枚数で大きく学習時間が変わってきますので、もう少し早く結果を見たい方は、--trainphotos, --testphotosオプションで枚数を減らしてください。詳しくは、
```sh
./make_train_lists.py --help
```
でヘルプを参照してください。


### 画像のリサイズ

ImageNetのインプット画像サイズは256*256であるので、先ほどリストに追加された画像のリサイズを行います。

```
./resize_photo.py resize.txt ../../resized_photo/
```

### 平均画像生成

最後に、訓練データから平均画像を生成します。

```
./compute_mean.py train.txt --root ../../resized_photo/
```
  
こちらを実行すると、 mean.npy というファイルが生成されます。

これでImageNetでの学習に必要なデータ一式の準備は終了です。


## ImageNetで学習

### 学習

ツールキットの train_imagenet.py で学習を始めます。

Chainer附属のImageNetと少しだけコードを変えてあります。変更点としては、保存する形式をCPUでも読み込めるようにしているだけです。

```
$ ./train_imagenet.py train.txt test.txt -g 0 --batchsize 32 --val_batchsize 100 --epoch 300 --root ../../resized_photo/ | tee log
```

こちらを実行すると学習が始まります。((見やすくするためにログを多少加工しています。))

```
{"iteration":100,"loss":2.735,"type":"train","error": 0.846875}
{"iteration":200,"loss":2.167,"type":"train","error": 0.7709375}
{"iteration":300,"loss":1.963,"type":"train","error": 0.719062499}
{"iteration":400,"loss":1.898,"type":"train","error": 0.6765625}
{"iteration":500,"loss":1.880,"type":"train","error": 0.664374999}
{"iteration":600,"loss":1.814,"type":"train","error": 0.6396875}
{"iteration":700,"loss":1.770,"type":"train","error": 0.61687500}
{"iteration":800,"loss":1.781,"type":"train","error": 0.620937499}
{"iteration":900,"loss":1.754,"type":"train","error": 0.60375}
{"iteration":1000,"loss":1.740,"type":"train","error": 0.60187499}
・
・
```

枚数が多いので、AWSのGPUインスタンスを利用した場合でも、初期設定の13万枚の学習データで300epochの学習で丸2日かかります。
結果を早く試したい場合は、epochを減らすか、学習データ枚数を減らしてください。

## 学習済みモデルでテスト

学習が終わった後は、modelというファイルが生成されています。use_model.pyを用いて作成したモデルにてクラス分類を行います。

```sh
./use_model.py /path/to/bukken/photo
トイレ           98.312% 
風呂             1.218% 
洗面             0.401% 
収納             0.057% 
設備             0.011% 
キッチン         0.000% 
駐車場           0.000% 
バルコニー       0.000% 
居間             0.000% 
玄関             0.000% 
```
