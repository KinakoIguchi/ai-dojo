## aws personalizeとは

* Amazon Personalize は、アプリケーションを使用するユーザー向けに個別化したレコメンデーションを簡単に追加できる、開発者向けの機械学習サービスである。

## 魅力

* ターゲッティングされたマーケティングプロモーションの強化に活用でき、カスタマーエンゲージメントの向上に貢献する。

* データの処理や統計、機械学習アルゴリズムを一から学ぶのではなく実践的な運用を行うために、モデルを最適化して運用することから始めることが可能で、タイムロスがない。

## チュートリアルの実施

* 基本的には下記のリンク内容に沿って行う。

  https://docs.aws.amazon.com/ja_jp/personalize/latest/dg/what-is-personalize.html

（開始方法はコンソールがやりやすい）

## 補足

分かりづらいところなどを以下で補足する

【Amazon S3 バケットポリシー】

バケットポリシーは以下のように置き換える

```
{

    "Version": "2012-10-17",
    
    "Id": "PersonalizeS3BucketAccessPolicy",
    
    "Statement": [
    
        {
        
            "Sid": "PersonalizeS3BucketAccessPolicy",
            
            "Effect": "Allow",
            
            "Principal": {
            
                "Service": "personalize.amazonaws.com"
                
            },
            
            "Action": [
            
                "s3:GetObject",
                
                "s3:ListBucket"
                
            ],
            
            "Resource": [
            
                "arn:aws:s3:::bucket-name",
                
                "arn:aws:s3:::bucket-name/*"
                
            ]
            
        }
        
    ]
    
}
```


※bucket-nameは自分の作ったものに置き換える

※https://docs.aws.amazon.com/ja_jp/AmazonS3/latest/user-guide/add-bucket-policy.html
も参照

【アクセス許可の設定】

IAMロールの作成

5.[このロールを使用するサービスを選択] で、[Amazon Personalize] を選択します。→ Personalizeを選択

12.〜20.は不要


【開始方法】

トレーニングデータを作成する

2.ratings.csv ファイルを開きます。

a.[評価] 列を削除します。→ 評価列は"rating"

※ratings.csvはおよそ10万件のデータが入っている。PCの動作が重くなることが予想される。10万件だと時間がかかるので1万件や5000件などにデータを絞って良い。



【ステップ 2: ソリューションを作成する】

3.[Recipe selection (レシピの選択)] で、[Automatic (AutoML) (自動 (AutoML))] を選択します。デフォルトのレシピリストのままにします。

→ そもそもRecipe selectionがない場合がある。その場合、3.の手順は無視して良い。

※ソリューションの作成に1時間以上はかかる。同様に後続のキャンペーンの作成も時間がかかる。



【ステップ 4: 推奨事項を取得する】

* 2020年からパーソナライズされたレコメンデーションごとに生成された推奨スコアも提供されている。スコアの具体的な内容は以下も参照。

  https://aws.amazon.com/jp/blogs/news/introducing-recommendation-scores-in-amazon-personalize/


* aws cliでjson形式で取得したい場合、以下で取得できる

```
aws personalize-runtime get-recommendations --<Campaign ARN> --user-id 84
```

※Campaign ARNと84は置き換える



【リソースの削除】

終わったら、必ずリソースを削除すること。
