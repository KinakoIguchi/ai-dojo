# 前提

* 本演習は、Chromebookの仮想Linux上で実施すること。
* 演習の成果物（python、シェルスクリプト、API-KEY）は、各自のGitHubプライベートリポジトリの course_cloud/AutoML_Tables にすべてアップロードすること。
  * GitHub へのアップロードは、Linuxコンソールからコミット、プッシュ もしくは GitHub のウェブ画面から GUIでアップロード のどちらでもかまいません。GitHub のウェブ画面からアップロードする場合は、対象のディレクトリに移動した後、[Add file] > [Upload Files] > (アップロードするファイルを選択) > [Commit Changes] を実行します。（下図参照）

  <img src="https://github.com/dcs-aidojo/public-data/blob/master/course_cloud/automl_tables/cat_git_upload.png?raw=true" width="750">

# 演習

実習2のデータを利用して、Pythonおよびシェルスクリプトを実装し、データセット作成〜バッチ予測までの一覧の流れを実行する。

＜全体イメージ＞

 <img src="https://github.com/dcs-aidojo/public-data/blob/master/course_cloud/automl_tables/cat_exercise_overview.png?raw=true" width="750">

## 1-1. データセット作成 の実装

実習2を参考に、AutoML Tablesのデータセットを作成するPythonとシェルスクリプトを実装してください。

* シェルスクリプトが先に実行され、シェルスクリプトからPythonが呼ばれる形にしてください
* サービスアカウントとAPIキーは、実習2で作成したものを再使用してください。
* バケットは有無を確認し、無ければ作成する実装としてください。バケット名とデータセット名は実習2で設定したものと同名としてください。
* ファイル名およびディレクトリ構成は以下のとおりとしてください。
```
AutoML_Tables
  ├── api-key
  │    └── aidojoPJ-XXXXXXXXXX.json：各自が作成したAPIキーファイル
  └── src
       ├── create_dataset.py：データセット作成（Python）
       └── create_dataset.sh：データセット作成（シェル）
```

## 1-2. データインポート〜バッチ予測 の実装

実習2の「census」のデータを再度使って、データインポート、データセットの更新、モデル作成、バッチ予測 の各処理について、それぞれPyhonとシェルスクリプトを実装してください。なお、実装する上で以下の点にご注意ください。

* データインポート
  * インポート元のデータは実習2で使用したものを再使用してください。
* データセット更新
  * 全ての特徴量について、Null非許容とし、かつ データ型を個別に定義してください。個別定義するデータ型は[こちら](https://drive.google.com/drive/folders/16paR6WBlreDVhYbSOe7xS_wiEuWNNeUn)の「dataset_code.json」のとおりとしてください。
  
 【注】実装する際は、`json.load` メソッドを利用して「dataset_code.json」を Pythonの辞書形式として読み取り、全てのデータ型を個別に設定してください。
* モデル作成
  * モデル名は実習2で設定したものと同名としてください。
* バッチ予測
  * バッチ予測対象のデータは実習2で使用したものを再使用してください。（自身で作成したバケットにコピーしてから予測する形としてください）
* 全体
  * 変数は別ファイルとして作成し、ファイルを読み込んで変数を取得する形としてください。（変数定義のPythonファイルを作成し、importする）
  * ファイル名およびディレクトリ構成は以下のとおりとしてください。
```
AutoML_Tables
  ├── api-key
  │    └── aidojoPJ-XXXXXXXXXX.json：各自が作成したAPI-KEY
  ├── data
  │    └── dataset_code.json
  └── src
       ├── batch_prediction.py：バッチ予測（Python）
       ├── batch_prediction.sh：バッチ予測（シェル）
       ├── constants.py：変数用（Python）
       ├── constants.sh：変数用（シェル）
       ├── create_dataset.py：データセット作成（Python）
       ├── create_dataset.sh：データセット作成（シェル）
       ├── create_model.py：モデル作成（Python）
       ├── create_model.sh：モデル作成（シェル）
       ├── import_data.py：データインポート（Python）
       ├── import_data.sh：データインポート（シェル）
       ├── update_dataset.py：データセット更新（Python）
       └── update_dataset.sh：データセット更新（シェル）
```
