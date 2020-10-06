# AutoML

AutoML(Automated Machine Learning)とは、機械学習モデルの設計・構築を自動化するための手法全般、またはその概念を指す。機械学習の専門的な知識がなくても素早く、そして簡単に機械学習モデルを構築できることを目標としている。

# Google Cloud AutoML

Google Cloud AutoMLは、2018年1月に公開されたGoogleが提供するクラウド型のAutoMLサービス。GCPコンソールのGUI操作で、データに基づいたモデルのトレーニング、評価、改善、デプロイを実行し、独自の機械学習モデルを作成できる。現在ベータ版も含めて以下５種類のサービスが提供されている。
- [AutoML Vision](https://cloud.google.com/vision/automl/docs?hl=ja)
- [AutoML Video Intelligence](https://cloud.google.com/video-intelligence/automl/docs?hl=ja)
- [AutoML Natural Language](https://cloud.google.com/natural-language/automl/docs?hl=ja)
- [AutoML Translation](https://cloud.google.com/translate/automl/docs?hl=ja)
- [AutoML Tables](https://cloud.google.com/automl-tables/docs?hl=ja)

＜AutoML サービス一覧と概要＞

<img src="https://cdn-xtech.nikkei.com/atcl/learning/lecture/19/00091/00001/hyo2.jpg?__scale=w:800,h:545,q:100&_sh=0560d80fe0" width="500">

公式：https://cloud.google.com/automl?hl=ja

# Google AutoML Tables

2019年4月に公開されたCloud AutoMLサービスの１つで、構造化データ（表形式のデータやデータベース）の解析・予測を自動で行う。2020年6月時点でベータ版のみの提供となっている。AutoML Tablesは教師付きの学習サービスで二項分類、多項分類、回帰分析をサポートしており、データの種類によって最適なモデルを複数選び、アンサンブル学習（複数のモデルの組み合わせ）を行い、モデルをビルドできる。

＜AutoML Tables 概要図＞

<img src="https://github.com/dcs-aidojo/public-data/blob/master/course_cloud/automl_tables/cat_automltables_overview.png?raw=true" width="700">

# 参考

- [[Cloud OnAir] Next ’19 サンフランシスコ最新情報 GCP 特集 2019年4月11日 放送](https://www.slideshare.net/GoogleCloudPlatformJP/cloud-onair-next-19-gcp-2019411)
- [Cloud AutoML](https://cloud.google.com/automl?hl=ja)
- [AutoML Tables の特徴と機能](https://cloud.google.com/automl-tables/docs/features?hl=ja)
- [GCPのAI・機械学習サービス](https://xtech.nikkei.com/atcl/learning/lecture/19/00091/00001/)
