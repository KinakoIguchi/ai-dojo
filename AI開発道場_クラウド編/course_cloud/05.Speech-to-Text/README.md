## Speech-to-Text実習・演習

### 目標
- Speech-to-Textが提供する機能について理解し、利用、実装できること。

### 提出課題
- [APIを試す](#APIを試す)を実施し、音声文字変換API呼び出しのHTTP通信ログを提出
- [クイックスタート](#クイックスタート)を実施し、実行ログを提出
- [入門ガイド](#入門ガイド)を実施し、Pythonプログラムと実行ログを提出
- PythonプログラムはGitHubのプライベートリポジトリ上に登録して提出(git pushやGitHubリポジトリページから直接コミット等)
- 最終日までに実施が終わらなかった場合、実施したところまでを提出


### 参照URL
- [公式ドキュメント](https://cloud.google.com/speech-to-text/docs?hl=ja)
- [Python用GitHubリポジトリ](https://github.com/googleapis/python-speech)
  - [Python用サンプルコード(v1.3.2)](https://github.com/googleapis/python-speech/tree/v1.3.2/samples/v1)
  
### サービス概要
- [料金](https://cloud.google.com/speech-to-text/pricing?hl=ja)
  - 毎月60分までは無料（１つの請求単位）
  - 各リクエストの音声の長さは15秒単位で切り上げとなるため、短い音声のリクエストが多く発生する使い方場合、注意が必要
  - データロギングを有効にすると割安になるが、送信された音声データをGoogleが機械学習モデル改善のため使用することになるため注意が必要
- [サポートされている音声エンコード形式](https://cloud.google.com/speech-to-text/docs/encoding?hl=ja)
  - MP3(ベータ),FLAC,LINEAR16(wav)など
- [音声認識精度向上ベストプラクティス](https://cloud.google.com/speech-to-text/docs/best-practices?hl=ja)
  - サンプリングレードは16 kHz 以上でキャプチャ。電話通話の場合は8 kHz
  - ユーザの近くにマイクを置く（ノイズキャンセルといった変換処理は不要）
  - 名前や用語など認識しづらい語句のヒントをリクエスト呼び出し時に加える
- [割当上限](https://cloud.google.com/speech-to-text/quotas?hl=ja)
  - 音声の長さ上限
    - 同期リクエスト：約１分
    - 非同期リクエスト：約480分
    - ストリーミングリクエスト：約5分
  
### 環境準備
- 前提
  - GCPプロジェクトでSpeech-to-Textが有効化されている（今回はすでに設定済み）
  - ChromebookにLinuxのターミナルが導入されていること（環境構築で実施済みの想定）
    - 以降のコマンド系の作業はLinuxのターミナル上で実施する
  - Cloud SDKが導入・初期設定済み（環境構築で実施済みの想定）
  - [Text](https://chrome.google.com/webstore/detail/text/mmfbcljfglbokpmkimbfghdkjmjhdgbg?hl=ja)が導入済み（環境構築で実施済みの想定）
- サービスアカウントファイル（JSONファイル）ダウンロード
  - [Google共用ドライブ](https://drive.google.com/drive/folders/1JM13tzI1WMg-hPL1p0srIywlljp0IIBH)からダウンロード(aidojopj-speech2text.json)
  - Pythonのプログラムから実行する場合に使用。
  - gcloudコマンド経由の実行の場合は不要
    - Cloud SDK初期設定(gcloud init)時の情報からアクセスに必要な情報を自動で取得するため
- ChromebookのLinuxコンテン環境で音声サポートを有効化
  - Chromebook上のコンソール画面上で音声の録音、再生処理をするために必要
  - ChromeOSのバージョンが79以上であること（2020/1リリース）
  - Chromeブラウザ上でCtrl-Alt-TでChromeシェル画面を開き、下記を実行
  - 以下はLinux環境の再起動が入る場合や一定時間たったあとなどで無効になるため音声録音、再生がうまくいかない場合は都度実施すること
  - stopコマンドを実行すると既存で開いていたLinuxアプリ(ターミナルやVSCodeなど）が停止されるため注意
  - [参考URL](https://chromium.googlesource.com/chromiumos/docs/+/master/containers_and_vms.md#Is-audio-capture-e_g_microphone_supported)
  ```
  crosh> vmc stop termina
  crosh> vmc start termina --enable-audio-capture
  ```
- Sox導入
  - 音声ファイルの録音、変換、再生処理で利用
  - rec(音声録音),play(音声再生),sox(音声変換)コマンドが利用可能となる
  - Linuxターミナル画面より以下を実行しインストール
  ```
  sudo apt-get install sox
  sudo apt-get install libsox-fmt-mp3
  ```
- Soxの使い方
  - [コマンドリファレンス](http://sox.sourceforge.net/sox.html)
  - [soxコマンドで音声ファイルを編集する10の例](https://blog.asial.co.jp/885)
  - 音声録音
    - 入力の音声ファイルのエンコードはファイル拡張子によって自動判定されて出力される
    ```
    #録音停止はCtrl+C
    rec test.mp3
    ```
  - 音声再生
    ```
    play test.mp3
    ```
  - 音声情報出力
    ```
    soxi test.mp3
    ```
  - 音声編集
    ```
    #MP3形式をサンプリングレート16ｋHz,16bit精度,チャンネル数1(モノラル)のwav形式に変換
    sox test.mp3 --rate 16k --bits 16 --channels 1 test.wav
    soxi test.wav
    ```
- 検証用音声ファイルダウンロード
  - 検証で使いたい音声ファイル(mp3)をダウンロードする
  - LinuxからChromebook上のファイルを参照する場合は、ファイルアプリのマイファイルを右クリック（ダブルタップ）でLinuxとの共有を選択すると`/mnt/chromeos/MyFiles/Downloads`からアクセス可能
  - 音声再生はファイルアプリから音声ファイルをダブルクリックやスペースキー（プレビュー）で確認
  - [サンプルナレーション音声](http://pro-video.jp/voice/announce/)
  - [青空朗読](https://aozoraroudoku.jp/index.html)
  - [NHKラジオニュース](https://www.nhk.or.jp/radionews/)：再生中にsoxで音声録音
  - [ラジオNIKKEIポッドキャスト AIのすゝめ](http://www.radionikkei.jp/podcasting/aino/archive.html):長い音声ファイルの文字変換を試す際の音源。聴くのリンクからMP3をダウンロード。
  - [文化放送ポットキャスト](http://www.joqr.co.jp/podcast/index.php):複数人の会話の話者分離機能を試す際の音源。MP3でダウンロードできるものを選択。
- 音声ファイル格納用GCSバケット作成
  ```
  # xxxには名前(ローマ字）を入れる
  gsutil mb gs://speech_to_text_xxx
  ```

### [APIを試す](https://cloud.google.com/speech-to-text?hl=ja)
- 課題1
  - MP3の音声ファイルをアップロードして音声文字変換API呼び出し時のHTTP通信ログ(リクエストBodyとレスポンスBody)をテキストファイルで提出(api-1-req.log,api-1-res.log)
  - 音声コンテンツ部分は除外する
  - 上記通信を含むHTTP通信ログをHAR形式で課題に提出(api-1.har)
- 課題2
  - マイクを使った音声文字変換API呼び出し時のHTTP通信ログ(WebSocketの送受信Message)をテキストファイルで提出(api-2-send.log,api-2-recv.log)
  - 音声途中と判断している受信メッセージ（[isFinal](https://cloud.google.com/speech-to-text/docs/reference/rpc/google.cloud.speech.v1#streamingrecognitionresult)がTrueとなっているもののみ）は除外
  - 音声のバイナリコンテンツ部分は除外する
  - 上記通信を含むHTTP通信ログをHAR形式で課題に提出(api-2.har)

- 実施概要
  - 「Speech-to-Text を有効に活用する」の下の部分にある入力フォームを使ってAPIを試す。
  - Input TypeにMicrophoneとあるのは、ブラウザのマイク機能からリアルタイムに音声をテキスト化する。File Uploadは、音声ファイルをアップロードして認識した文字列が画面に出力される。
  - Langageには音声の言語を選択します。日本語の音声ファイルの場合、下の方の「日本語(日本)」を選択
  - Speaker diarizationをOnにすると音声に含まれる複数の話者を識別して結果を返します。Onにした場合、話者の人数もあわせて指定。
  - Punctuationを有効にすると句読点の挿入が行われる
  - Show JSONをクリックするとSpeech-to-TextのAPIを呼び出すURLとリクエストするJSONデータを確認できる（このデモでは実際にAPI呼び出しの通信先とは異なる点に注意）
  - Microphoneでのリアルタイム文字認識の場合はストリームでの音声認識APIの呼び出しはgRPCとなっているが、このブラウザベースのデモの仕組みではWebSocketのエンドポイントをプロキシを経由してデータ送受信を行っている。
    - API設計時のRESTやgRPCについては[こちら](https://cloud.google.com/blog/ja/products/api-management/understanding-grpc-openapi-and-rest-and-when-to-use-them)を参照。
  - ファイルアップロードによる方式では、音声ファイルは１分以内のものを指定する。それ以上はこのAPIではエラーとなる
  - マイクを使った方式では、実行直後、ロボットでないことを確認するチェックボックスが表示されるのでチェックする


  - ChromeのDeveloper Toolsを使ったHTTP通信ログの確認・取得方法
    - URLバーがある右端の３点ボタン（︙）より「その他ツール」＞「ディベロッパーツール」を選択
    - Networkのタブを選択し、ブラウザとの通信のURLのName部分のリストが表示される
    - このウィンドウを表示している状態で、上記の音声テキスト変換処理の実行を行う
    - ファイルアップロードによる音声文字変換のURL（Name部分）
      - `proxy?url=https%3A%2F%2Fspeech.googleapis.com...`
    - マイクによる音声文字変換URL(Name)
      - `ws`
    - 効率的に探すには、フィルタ（Networkタブの直下のツールバーの左から３番目）を選択してURLの部分文字列（上記の場合は「proxy」や「ws」）を入力する
    - リクエストBodyはHeaderタブの一番下「Request Payload」で「view source」を選択
      - audioのcontent部分は音声データをBASE64エンコードした文字列のため長い文字列となり、スプレッドシートに貼り付けると１行の最大文字列を超える場合があるため、content部分の文字列は除外して貼り付ける
      - Payload選択して全体が青くなったあと、スクロールで"content":までをコピーする
    - レスポンスBodyはResponseタブを選択
    - WebSocketの送信メッセージは、Messagesタブ（wss://xxxのURLの場合に表示される）を選択し、FilterでALLからSendに変更する。Binary Message以外のものを選択して、下部のウィンドウに表示されたJSONメッセージを選択（トリプルクリックでメッセージ全体を選択できる）してコピーする
    - WebSocketの受信メッセージは、FilterをReceiveにして、isFinalがtrueとなっているものを１つ選択してコピー。[isFinal](https://cloud.google.com/speech-to-text/docs/reference/rpc/google.cloud.speech.v1#streamingrecognitionresult)がFalseのものは、音声途中のものとして判断しているもの。
    - 通信ログをファイルとして保存する場合は、ログのURLを１つ選択して右クリック>「Save all as HAR with content」でhar形式（HTTPアーカイブ）で保存する
    - もしくはDeveloper Toolsのツールバーから[HARエクスポート](https://developers.google.com/web/updates/2019/05/devtools#HAR)


### [クイックスタート](https://cloud.google.com/speech-to-text/docs/quickstart)
- 課題1
  - [gcloudツール](https://cloud.google.com/speech-to-text/docs/quickstart-gcloud)を使って以下の音声文字変換を行い、実行ログを提出(qs-1.log)
    - GCS上にある短い音声ファイルを使った音声文字変換
    - ローカル上にある短いwav形式の音声ファイルを音声文字変換
    - HTTP通信ログを有効にして音声文字変換
    - ベータ版コマンドを使ってMP3音声ファイルを直接、音声文字変換
- 課題2
  - [curlコマンド](https://cloud.google.com/speech-to-text/docs/quickstart-protocol)を使って以下の音声文字変換を行い、実行ログを提出(qs-2.log)
    - GCS上にある短い音声ファイルを使った音声文字変換
    - GCS上にある長い音声ファイルを使った音声文字変換
    - 句読点の自動挿入による音声文字変換
    - 話者分離による音声文字変換


- 実施概要
  - 音声文字変換の３つのやり方があり、gcloudとcurlを使ったやり方について実施
  - Pythonを使った実装方法は次の「入門ガイド」のところで実施する
  - リンク先は適宜参照し実施。一部リンク先にないものを実施する箇所もある。
  - 実行ログはscriptコマンドを使いターミナルに出力した内容をファイルに出力する。[参考URL](https://dev.classmethod.jp/articles/scriptcommand/)
    ```
    script ログファイル名
    # 終了時はexitで抜ける
    ```
  - 課題１：gcloudを使ったやり方
    - 準備
      - gcloudが導入・初期設定済み
      - 1分以内の短い音声ファイル(short.mp3)をrecコマンドやダウンロードサイトからダウンロードして準備
    - 音声文字変換リクエスト
      - GCS上の音声ファイルに対する音声文字変換
      - 音声ファイルの場所はGCS上にあるファイルパスかローカル上のファイルパスを指定
      - 音声ファイル形式によって、指定必須のオプションが変わる
      - 音声変換したい[言語コード](https://cloud.google.com/speech-to-text/docs/languages?hl=ja)は指定必須
      - [コマンドリファレンス](https://cloud.google.com/sdk/gcloud/reference/ml/speech/recognize?hl=ja)
      - [コマンドリファレンス(beta版)](https://cloud.google.com/sdk/gcloud/reference/beta/ml/speech/recognize?hl=ja)
      ```
      #GCS上にある音声ファイルを指定して実行
      gcloud ml speech recognize gs://cloud-samples-tests/speech/brooklyn.flac --language-code=en-US

      #ローカル上のMP3ファイルをsoxを使いチャンネル数1でwav形式変換して実行
      sox xxx.mp3 --rate 16k --bits 16 --channels 1 xxx.wav
      soxi xxx.wav
      #日本語で音声文字変換リクエストを呼び出す
      gcloud ml speech recognize xxx.wav --language-code=ja-JP

      #GCS上にコピーしてHTTP通信ログを有効にして実行(--log-httpオプションを付ける)
      gsutil cp xxx.wav gs://speech_to_text_xxx/
      gsutil ls gs://speech_to_text_xxx/
      gcloud ml speech recognize gs://speech_to_text_xxx/xxx.wav --language-code=ja-JP --log-http

      #MP3形式に対応したbeta版コマンドで実行
      #gcloud betaコマンド初めて実行する場合
      gcloud components install beta
      #MP3ファイル情報を確認
      soxi xxx.mp3
      #GCSにコピー
      gsutil cp xxx.mp3 gs://speech-to-text_xxxx/
      gsutil ls gs://speech_to_text_xxxx/
      #sample-rateはsoxiで確認したサンプリングレートにあわせて指定して実行
      gcloud beta ml speech recognize gs://speech_to_text_xxx/xxx.mp3 --encoding=mp3 --sample-rate=xxxx --language-code=ja-JP
      ```

  - 課題２：curlコマンドを使って音声文字変換を行う
    - [GCS上にある短い音声ファイルを使った音声文字変換](https://cloud.google.com/speech-to-text/docs/quickstart-protocol#make_an_audio_transcription_request)
      - 使用する音声ファイルを確認する場合、GCSからダウンロードして再生
        ```
        gsutil ls gs://cloud-samples-tests/speech/
        gsutil cp gs://cloud-samples-tests/speech/brooklyn.flac .
        soxi brooklyn.flac
        play brooklyn.flac
        ```
      - [ヒアドキュメント](https://qiita.com/take4s5i/items/e207cee4fb04385a9952)でJSONリクエストファイル作成
        ```
        cat <<EOS >sync-request.json
        {
          "config": {
              "encoding":"FLAC",
              "sampleRateHertz": 16000,
              "languageCode": "en-US",
              "enableWordTimeOffsets": false
          },
          "audio": {
              "uri":"gs://cloud-samples-tests/speech/brooklyn.flac"
          }
        }
        EOS
        cat sync-request.json
        ```
      - 呼び出し
        ```
        #APIに呼び出しに必要なアクセストークンが取得可能か確認。うまくいかない場合、gcloud initで初期設定
        gcloud auth application-default print-access-token
        #音声文字変換処理呼び出し
        curl -s -H "Content-Type: application/json" \
        -H "Authorization: Bearer "$(gcloud auth application-default print-access-token) \
        https://speech.googleapis.com/v1/speech:recognize \
        -d @sync-request.json
        ```
      - 日本語音声で試す
        ```
        #日本語音声MP3ファイルの情報を確認
        soxi xxx.mp3
        #flac形式に変換
        sox xxx.mp3 --rate 16000 --channels 1 xxx.flac
        #GCSにコピー
        gsutil cp xxx.flac gs://speech_to_text_xxxx/
        #sync-request-jp.jsonとして作成
        cat <<EOS >sync-request-jp.json
        {
          "config": {
              "encoding":"FLAC",
              "sampleRateHertz": 16000,
              "languageCode": "ja-JP",
              "enableWordTimeOffsets": false
          },
          "audio": {
              "uri":"gs://speech_to_text_xxxx/xxx.flac"
          }
        }
        EOS
        cat sync-request-jp.json
        #音声文字変換処理呼び出し
        curl -s -H "Content-Type: application/json" \
        -H "Authorization: Bearer "$(gcloud auth application-default print-access-token) \
        https://speech.googleapis.com/v1/speech:recognize \
        -d @sync-request-jp.json
        ```

    - [GCS上にある長い音声ファイルを使った音声文字変換](https://cloud.google.com/speech-to-text/docs/async-recognize#speech_transcribe_async_gcs-protocol)
      - 長い音声ファイル場合、オペレーション名(nameの値）が返却後、その値を使って結果を呼び出す
        ```
        curl -X POST \
             -H "Authorization: Bearer "$(gcloud auth application-default print-access-token) \
             -H "Content-Type: application/json; charset=utf-8" \
             --data "{
               'config': {
                 'language_code': 'en-US'
                },
                'audio':{
                  'uri':'gs://cloud-samples-tests/speech/vr.flac'
                }
              }" "https://speech.googleapis.com/v1/speech:longrunningrecognize"
        curl -H "Authorization: Bearer "$(gcloud auth application-default print-access-token) \
             -H "Content-Type: application/json; charset=utf-8" \
        "https://speech.googleapis.com/v1/operations/xxxx"

        # 上記に加えて日本語の１分以上のMP3音声ファイルで試す。コマンドは各自これまでの内容を踏まえ考えて実施
        # MP3ファイルの音声情報出力
        # flac形式（チャンネル数1,サンプリングレート16000)に変換
        # flac形式の音声情報確認
        # GCSにアップロード
        # リクエストJSONをカスタマイズして実行
        ```
    - [句読点の自動挿入による音声文字変換](https://cloud.google.com/speech-to-text/docs/automatic-punctuation#speech_transcribe_auto_punctuation-protocol)
      - 上記のリンクの内容のコマンド実行に加え日本語による句読点の自動挿入による音声文字変換を実施する。
      - 日本語音声内容により句読点がうまく入らない場合もある。
    - [話者分離による音声文字変換](https://cloud.google.com/speech-to-text/docs/multiple-voices#speech_transcribe_diarization_beta-protocol)
      - 上記リンクのcurlコマンドによるコマンド実行後、出力結果ファイルはcatで表示して実行ログに出力す。
      - 上記コマンド実行に加え日本語の会話音声ファイルを使って話者分離による音声文字変換も実施する。
 
### [入門ガイド](https://cloud.google.com/speech-to-text/docs/how-to)
- 課題1
  - [短い音声ファイルの音声文字変換](https://cloud.google.com/speech-to-text/docs/sync-recognize)を行い、Pythonプログラムと実行ログを提出(howto-1.log)
    - ローカル ファイルでの同期音声認識の実行
      - [speech_transcribe_sync.py](https://github.com/googleapis/python-speech/blob/v1.3.2/samples/v1/speech_transcribe_sync.py)
    - リモート ファイルでの同期音声認識の実行
      - [speech_transcribe_sync_gcs.py](https://github.com/googleapis/python-speech/blob/v1.3.2/samples/v1/speech_transcribe_sync_gcs.py)
- 課題2
  - [長い音声ファイルの音声文字変換](https://cloud.google.com/speech-to-text/docs/async-recognize)を行い、Pythonプログラムと実行ログを提出(howto-2.log)
    - Google Cloud Storage ファイルを使用した長い音声ファイルの文字変換
      - [speech_transcribe_async_gcs.py](https://github.com/googleapis/python-speech/blob/v1.3.2/samples/v1/speech_transcribe_async_gcs.py)
    - ローカル ファイルを使用した長い音声ファイルの変換
      - [speech_transcribe_async.py](https://github.com/googleapis/python-speech/blob/v1.3.2/samples/v1/speech_transcribe_async.py)
- 課題3
  - [ストリーミング入力の音声文字変換](https://cloud.google.com/speech-to-text/docs/streaming-recognize)を行い、Pythonプログラムと実行ログを提出(howto-3.log)
    - ローカル ファイルでのストリーミング音声認識の実行
      - [transcribe_streaming.py](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/speech/cloud-client/transcribe_streaming.py)
    - 音声ストリームでのストリーミング音声認識の実行
      - [transcribe_streaming_mic.py](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/speech/microphone/transcribe_streaming_mic.py)
- 課題4
  - [音声適応による認識リクエストの送信](https://cloud.google.com/speech-to-text/docs/context-strength)を行い、Pythonプログラムと実行ログを提出(howto-4.log)
    - [transcribe_context_classes.py](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/speech/cloud-client/transcribe_context_classes.py)

- 課題5
  - [異なる話者の分離](https://cloud.google.com/speech-to-text/docs/multiple-voices)を行い、Pythonプログラムと実行ログを提出(howto-5.log)
    - [speech_transcribe_diarization_beta.py](https://github.com/googleapis/python-speech/blob/v1.3.2/samples/v1p1beta1/speech_transcribe_diarization_beta.py)
- 課題6
  - [認識メタデータの追加](https://cloud.google.com/speech-to-text/docs/recognition-metadata)を行い、Pythonプログラムと実行ログを提出(howto-6.log)
    - [speech_transcribe_recognition_metadata_beta.py](https://github.com/googleapis/python-speech/blob/v1.3.2/samples/v1p1beta1/speech_transcribe_recognition_metadata_beta.py)
- 課題7
  - [句読点挿入の自動化](https://cloud.google.com/speech-to-text/docs/automatic-punctuation)を行い、Pythonプログラムと実行ログを提出(howto-7.log)
    - [transcribe_auto_punctuation.py](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/speech/cloud-client/transcribe_auto_punctuation.py)
- 課題8
  - [単語のタイムスタンプの取得](https://cloud.google.com/speech-to-text/docs/async-time-offsets)を行い、Pythonプログラムと実行ログを提出(howto-8.log)
    - [speech_transcribe_async_word_time_offsets_gcs.py](https://github.com/googleapis/python-speech/blob/v1.3.2/samples/v1/speech_transcribe_async_word_time_offsets_gcs.py)


- 実施概要
  - 提供される機能のPythonでの実装方法について学ぶ
  - リンクの内容に従ってPythonプログラムを作成、修正し、実行
  - GitHubのリンクが一部404となっているものは、上記Pythonのソース（v1.3.2)のリンクからアクセスする
  - 日本語音声に対応するためにlanguage_codeはja-JPに差し替える
  - プログラムの実行方法は、ソースコードに記載のものを参照する
  - 音声ファイルが入力に必要なものは、soxを使った変換やgcsへのコピーを適宜行う。
  - 事前準備
    - サービスアカウントファイル(aidojopj-speech2text.json)
    - [認証設定](https://cloud.google.com/docs/authentication/getting-started#cloud-console)
      - Google Cloudが提供するAPIにアクセスするために必要な認証設定を行う
      - サービスアカウントは事前に準備したファイルをコピーして利用する
      ```
      cp /mnt/chromeos/GoogleDrive/SharedDrives/AI開発道場/クラウド編/Speech-to-Text/aidojopj-speech2text.json ~/
      #export GOOGLE_APPLICATION_CREDENTIALS={JSONファイルのパス}
      export GOOGLE_APPLICATION_CREDENTIALS=~/aidojopj-speech2text.json
      ls -l $GOOGLE_APPLICATION_CREDENTIALS
      ```
    - ライブラリインストール
      ```
      pip install --upgrade google-cloud-speech
    - ストリーム呼び出し時に必要なライブラリインストール
      ```
      sudo apt install portaudio19-dev
      pip install pyaudio
      ```
  - Pythonプログラム作成・修正
    - GitHubからソースをコピーして作成。リポジトリをまるごとgit cloneしてもよい
    - 編集はターミナルからviか、VSCodeやTEXTなど好きなものを使う
  - 実行
    ```
    python xxx.py [プログラムによってはオプション指定]
    ```
