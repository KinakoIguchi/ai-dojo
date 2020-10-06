# AWS sagemakerの概要
AWS SageMaker は機械学習に特化したマネージド型のクラウドコンピューティングサービスである。 
機械学習に特化したという点が大きな特徴で、機械学習モデルの構築からデプロイまで
AWSが提供するシステム上で行うことができる。 

# Sagemakerの特徴
「インスタンス作成」、「モデル構築」、「トレーニング」、「デプロイ」までのフローを実施することが可能

# Sagemakerを使うメリット
* 機械学習プロセスの高速化
* 豊富なフレームワークとアルゴリズム
* 訓練ずみのモデルへ簡単にアクセス

# Sagemakerで使えるアルゴリズム
sagemakerは主要なアルゴリズムに対応している。
その中でもSageMakerで実装されている機械学習アルゴリズム、すなわち組み込みアルゴリズムで学習モデルを作成・使用するのが簡単である。
線形学習・k-Means・XGboostなどが組み込みアルゴリズムに該当する。

組み込みアルゴリズムについては以下も参照のこと

https://docs.aws.amazon.com/ja_jp/sagemaker/latest/dg/algos.html

# XGboostとは

* XGboostは弱学習器（決定木）を構築する際に前に構築された弱学習器の結果を使用し弱学習器を構築する手法。

* 最初の弱学習器で上手く推定できなかった部分を推定するために重みを付けて次の弱学習器で学習を行う。

* ランダムフォレストが並列的に弱学習器を用いたのに対して、XGboostは直列的に弱学習器を用いたものである。

* パラメータは多数あるが、その中でも重要なのがobjectiveである。

【objective】

最小化させるべき損失関数を指定する。

引数　

* reg:linear(線形回帰)
* reg:logistic(ロジスティック回帰)
* binary:logistic(2項分類で確率を返す)
* multi:softmax(多項分類でクラスの値を返す)
   
※multi:softmaxを指定した場合、num_class(クラス数)の指定が必要となる。


* パラメータの詳細は以下のサイトも参照

  https://xgboost.readthedocs.io/en/latest/parameter.html

* XGboostをイメージで理解したい方は以下サイトも参照

  https://qiita.com/2357gi/items/913af8b813b069617aad

# sagemakerを使うために必要なawsの情報
* ロール
* S3のprefix
* リージョン

それぞれの意味は環境構築のファイルを参照のこと。

※セルを動かす実習については別ファイルを参照のこと
