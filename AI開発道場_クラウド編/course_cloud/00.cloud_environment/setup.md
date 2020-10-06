# クラウド編環境構築

* クラウド編ではGoogle Cloud PlatformとAmazon Web Serviceというクラウドサービスを利用する。 

# Google Cloud Platform（GCP）とは
* Google Cloud Platform（GCP） とは、Google がクラウド上で提供するサービス群の総称である。

* 公式ドキュメントは以下

  https://cloud.google.com/docs?hl=ja
  
# Amazon Web Service(AWS)とは
* Amazon Web Services(AWS)はAmazonが提供している100以上のクラウドコンピューティングサービスの総称である。

* 公式ドキュメントは以下

  https://docs.aws.amazon.com/index.html
  
# GCPを使うにあたって
* GCPを使うには、いくつかの準備が必要となる。

## Gsuiteとは
* G Suiteとは、 Google社が提供している各サービスのアプリケーションをビジネス向けにまとめて利用できる有料サービスである。
* 管理者機能があり、G SuiteサービスのすべてをGoogle管理コンソールで一元的に管理できる。この管理機能を使って、ユーザーの追加や削除、支払いの管理、モバイルデバイスの設定などを行うことができる。
* シングルサインオンや2段階認証の仕組みでセキュリティ面で安心である。

GCPを使う際にはG Suiteのアカウントを使用する。

## Google Compute Engine（GCE）
* AWS の EC2 に相当するサービスとなっており、時間あたりの課金で仮想マシンをレンタルすることができるサービス
* 高いネットワーク性能が期待でき、セキュリティ的に安全である。
* 以下も参照のこと

  https://cloud.google.com/compute?hl=ja

## GCEでインスタンスを立ち上げる
* GCPコンソールでログインして、Compute Engine>Create Instanceを選択
* Nameにインスタンスの名前を指定。
* Zoneはasia-northeast1-a、
* Machine typeは試しにやるならmicro
* boot diskはUbuntu 16.04 LTS
* firewallはAllow HTTP traffic
上記を設定したらcreateするとインスタンスの設定が完了する。

### View gcloud command

”Connect” ボタンについている下向きの三角形をクリックすると、インスタンスに接続する方法の選択肢が表示される。この中から、 ”View gcloud command” をクリック。gcloud を使用してインスタンスに接続するためのコマンドが表示される。

### Google Cloud SDKのインストール

* apt-getを使用するインストール
  以下を参照のこと
  
  https://github.com/dcs-aidojo/contents/blob/master/getting_started/usage/gcp.md#google-cloud-sdkgcloud%E5%B0%8E%E5%85%A5

* インストーラの使用でインストールする場合

ターミナルで以下コマンドを打つ
```
curl https://sdk.cloud.google.com | bash
```
```
exec -l $SHELL
```
```
gcloud init
```
* gcloud initがうまくいかない場合は.bash_profileにパスを書く、以下を実行
```
cd ~
ls -a
vi .bash_profile
```
以下を追記
```
source <sdkを入れたディレクトリ>/google-cloud-sdk/completion.bash.inc
source <sdkを入れたディレクトリ>/google-cloud-sdk/path.bash.inc
```
### インスタンスの接続
* 設定が開始される。Google アカウントへのログインを求められるので、ログインを行う。
* ブラウザが開くので、アカウントへのログインを行い、 OAuth の認証画面で許可を行う。
* ターミナル画面に戻ると、プロジェクトの選択を求められるので、プロジェクトを選択する。GCP研修で利用するプロジェクトは「aidojoPJ」。
* View gcloud commandのところで表示されたコマンドを打つ。

鍵がないときwarningが出るが、そのまま作成すれば良い。

【注意】
2回目以降ssh接続する際は、cloud SDKの承認が必要である。
以下のコマンドを実行する。
```
gcloud auth login
```
URLが表示されるので、アクセスしてgoogleアカウントでログインして許可。
コードが表示されるので、ターミナルに貼り付ける。
これで承認され、gcloudコマンド（後述）が使えるようになる。


### ポートの接続
* GCPのコンソールページのナビゲーションメニューから、VPCネットワーク→ファイアウォール　ルールに移動して、
ファイアウォール　ルールを作成をクリック。

    名前→任意の名前

    ターゲットタグ→任意のタグ

    ソース IP の範囲→0.0.0.0/0

    指定したプロトコルとポート→tcpにチェックしてポート番号を適当に

    他は初期設定のままでOK。

* GCPのコンソールページのナビゲーションメニューから、Compute Engine→VMインスタンスに移動。

* 使用するインスタンス内の画面上部にある編集をクリックして、ネットワークタグにファイアウォールルールで作成したターゲットタグを入力してenterキー。

* 画面下部の保存で設定の保存。

```
sudo systemctl disable firewalld
Removed symlink /etc/systemd/system/multi-user.target.wants/firewalld.service.
Removed symlink /etc/systemd/system/dbus-org.fedoraproject.FirewallD1.service.
```

* 続いて、 /etc/selinux/config を編集

```
$ sudo vi /etc/selinux/config
```

下記のように変更。
```
SELINUX=disabled
```
```
$ sudo vi /etc/ssh/sshd_config
```
* sshdの設定を以下のように編集

```
#Port 22
Port XXXXXX # 新しいポート番号
```
```
$ sudo systemctl restart sshd
```

* コンソールからSSHでブラウザウィンドウで開くをクリック。ポート22で接続できないことを確認

* ブラウザ ウィンドウでカスタムポートを開くをクリック。ポート番号を入力して接続できればポート番号の変更は成功。

# gcloudコマンド

* gcloud コマンドは、Google Cloud Platform (GCP) のサービスについて表示・管理・更新を行うコマンドラインツールで、Google が作成している Cloud SDK の中の一部である。
* gcloud で GCP の全サービスを操作できるわけではなく、BigQuery は bq コマンド、Google Cloud Storage (GCS) は gsutil コマンド、GKE (≒Kubernetes) は kubectl コマンドをそれぞれ使用する

## gcloud コマンドの基本的な使い方

* gcloud の後には「グループ」を指定する。

* 例:
  * gcloud compute … Compute Engine に関する表示・設定
  * gcloud sql … Cloud SQL に関する表示・設定

## よく使われるコマンド

【全体】

* 自分のプロジェクト一覧を表示

```
gcloud projects list
```

* cloud sdkのプロパティを見る

```
gcloud config list
```

* プロジェクト切り替え

```
gcloud config set project <your-project-id>
```

【GCE】

* インスタンス一覧を見る

```
gcloud compute instances list
```

* インスタンスの作成

```
gcloud compute instances create <your-instance-name> --project <your-project-name> --image-family centos-7
```

* 使用可能なimage一覧を見る

```
gcloud compute images list
```

* インスタンスの起動・停止

```
gcloud compute instances start <your-instance-name>
gcloud compute instances stop <your-instance-name>
```

* インスタンスにssh

```
gcloud compute ssh <your-instance-name>
```

* 通常のsshコマンドで接続できるように設定

```
gcloud compute config-ssh
```

~/.ssh/configに稼働中のインスタンスへの接続設定が作られる。

```
ssh <your-instance-name>.<zone>.<your-project-id>
```

ssh [tab]で

* インスタンスへローカルのファイルをコピーする

```
gcloud compute copy-files <local-path> <your-instance-name>:<remote-path> --zone <zone>
```

* インスタンスにあるファイルをローカルにコピーする

```
gcloud compute copy-files <your-instance-name>:<remote-path> <local-path> --zone <zone>
```

## Google Cloud Storage

* Google Cloud Storage（以下、GCS）は、オブジェクトストレージである。
* 管理がシンプルで、高耐久性、高可用性のストレージを提供している。
* リンクは以下
  
  https://cloud.google.com/storage/docs?hl=ja

### gsutilコマンド

* gsutilコマンドとは、GCS(Google Cloud Storage)をコマンドラインから操作できるPythonアプリケーションのこと

#### よく使われるコマンド

* gsutilのバージョンを確認する場合
```
gsutil version
```
* バケットの一覧を出力する場合
```
gsutil ls
```
* バケット内のオブジェクト一覧を出力する場合
```
gsutil ls <bucket-name>
```
* オブジェクトの内容を出力する場合
```
gsutil cat <object-name>
```

## big queryとは
GCPで提供されるクラウドデータウェアハウス。2012年に公開された。数TB（テラバイト）あるいはPB（ペタバイト）に及ぶデータセットに対し、SQLライクのクエリを実行し、数秒あるいは数十秒程度で結果を返すことができる。他社の類似サービスとして Amazon Redshift、Azure SQL Data Warehouse がある。

公式は以下
  https://cloud.google.com/bigquery/?hl=ja

## bqコマンド
* データセット・テーブル・ビューの作成
```
bq mk 
```
* テーブル作成
```
bq load
```
* データ読み込み
```
bq ls
```
* データセットの権限やテーブルのスキーマ情報等を表示
```
bq show
```
* コマンド一覧やオプションなどを確認する
```
bq help
```
* データセット・テーブルの削除
```
bq rm
```
* クエリ実行
```
bq query
```
* データセットやテーブル情報を更新する 
```
bq update
```
* テーブル内容の確認
```
bq head 
```
* テーブルのエクスポート
```
bq extract
```
* テーブルのコピー
```
bq cp
```

# サービスアカウント
個々のユーザではなく、アプリケーションに属するアカウント。使いたい数だけ発行し、アプリに組み込んで使う。
サービスアカウントは0以上のサービスアカウントのキーペアを持ち、Googleの認証に使用する。

## サービスアカウントの付与
* GCPのダッシュボードからサービスアカウントを選択。

* 「サービスアカウントを作成」からロールを割り当てて作る。

* サービスアカウント作成後は該当のサービスアカウントの操作>鍵を作成を選択し、JSONを選択すると鍵作成後、認証ファイルがダウンロードされる。  

## AWSの基本的情報

### Region
AWSサービスのバックボーンは、「リージョン」と呼ばれる地理的に離れた領域のデータセンター群がそれぞれ接続されることで構成されている。
各リージョンではAWSのサービスがそれぞれ独立して提供されている。
東日本では基本的に東京リージョンを使うが、たまに東京リージョンで使えないサービスがあり、その際は別のリージョンを使う。
AWSコンソールで初めてログインした際には、リージョンを東京に変えるのが最初にやることの1つである。

### IAM
AWS上のサービスを操作するユーザーとアクセス権限を管理するのがIAM（AWS Identity and Access Management）である。
ユーザーがアクセスするための認証情報やAWSリソースを制御するための権限を集中管理することができる。

### S3
ストレージサービスで、バケットと呼ばれる入れ物にデータを保存する。容量は無制限。

### EC2
「仮想サーバー」を立てるサービス。LinuxやWindowsなどさまざまなOSの仮想サーバーをすぐに実行できる環境を用意することができる。
立てたサーバーのことはインスタンスと呼ぶ。

## AWSでEC2インスタンスを作成

* シングルサインオンでAWSにログイン

* 上の「サービス」からEC2を選択

* 左のメニューから「インスタンス」を選択して、上の「インスタンスを作成」をクリック。

* AMIは（こだわりが無ければ）一番上のAmazon Linux 2 AMI (HVM), SSD Volume Type>(64 ビット x86)を選択

* インスタンスタイプはt2.microを選択

* ストレージはデフォルト

* タグはキーがName、値は適当なもの

* セキュリティグループ→タイプ:SSH、プロトコル:TCP、ポート:初期値は22、ソース:マイAP

* キーが作成されるので保管

* 確認と作成をクリック>起動をクリック

* インスタンスの状態とステータスチェックの項目が緑色になったら接続可能

### AWSインスタンスの起動

* 接続をクリック

* 保存したキーをlinuxで共有管理するようにする。

* 以下コマンドを実行
```
sudo chmod 400 key_name
```
```
ssh -i key_name ec2-user@public-dns-name
```
※key_name、ec2-user、public-dns-nameは各自置き換えること

これでログインできる。

【ログイン後にやること】

* インストール済みのパッケージをアップデートする
```
sudo yum update
```

* 時間を日本時間にする

```
sudo mv /etc/localtime /etc/localtime.org
sudo ln -s /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
sudo vi /etc/sysconfig/clock
```

* viで「ZONE="UTC"　UTC=true」を「ZONE="Asia/Tokyo"　UTC=true」に修正。再起動する。

```
sudo reboot
```

### AWS CLI

AWS CLIは、AWSのサービスをコマンドラインから操作し、管理するためのツールである。
このツールはプラットフォームや開発言語の制限がなく、Linux、Mac、Windowsなど様々なOSで利用できる。

【使う準備】（アクセスキーIDとキーが分かっている人はcurlコマンドまで飛ばして良い）

* サービスからIAMを選択

* 左のタブからユーザを選択

* 右のタブから認証情報を選択

* アクセスキーを作成して情報をメモするか情報の入ったcsvをダウンロードする

【インストール】
```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

* 確認

```
aws --version
```

* AWS CLIのコンフィグを設定

```
aws configure
```

* 下記のようなものが出るので埋める。

    AWS Access Key ID : アクセスキーの作成時にメモしたもの

    AWS Secret Access Key : アクセスキーの作成時にメモしたもの

    Default region name :ap-northeast-1 

    Default output format :json 

* 動作確認

```
aws ec2 describe-vpcs
```
