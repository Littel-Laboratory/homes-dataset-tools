# HOME'Sデータセット ツールキット

## 説明

[国立情報学研究所データリポジトリ](http://www.nii.ac.jp/dsc/idr/)経由で提供を行っている[HOME'Sデータセット](http://www.nii.ac.jp/dsc/idr/next/homes.html)を対象とした支援ツールキットです。本ツールキットを用いることで、物件画像に付けられているタグをもとに、ディープラーニングのフレームワークであるChainerを用いて畳み込みニューラルネットワークでの分類器学習を行ったり、テキストマイニングを試したりすることができます。

## imageKit

賃貸物件画像と、それに付加された部屋の種類の情報から、画像の種類のクラス分類を行う学習を行わせるツールキットです。

chainerのサンプルに含まれるImageNetのNetwork in Networkモデルの実装を改良しています。また学習を行わせるのに必要な形式、画像サイズへの変換ツールが含まれます。

## nlpKit

(公開準備中です)