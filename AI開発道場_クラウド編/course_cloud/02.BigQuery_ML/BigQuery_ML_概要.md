# BigQuery

GCPで提供されるクラウドデータウェアハウス。2012年に公開された。数TB（テラバイト）あるいはPB（ペタバイト）に及ぶデータセットに対し、SQLライクのクエリを実行し、数秒あるいは数十秒程度で結果を返すことができる。他社の類似サービスとして Amazon Redshift、Azure SQL Data Warehouse がある。

公式：https://cloud.google.com/bigquery/?hl=ja

# BigQuery ML

BigQueryのデータに対して標準SQLクエリを利用して、機械学習モデルの作成と実行が可能。2018年のCloud Nextで発表された。2020年６月時点でベータ版のみの提供となっている。DWHからデータをエクスポートして別形式に変換や加工等をせず、SQLのみでそのままモデル作成の一連の流れが実行できる為、開発工数の削減が期待できる。以下のモデルが利用可能：

- 線形回帰（予測）
- 2 項ロジスティック回帰（分類）
- 多項ロジスティック回帰（分類）
- K 平均法クラスタリング（データ セグメンテーション）
- TensorFlow モデルのインポート

公式：https://cloud.google.com/bigquery-ml/docs/bigqueryml-intro?hl=ja


# AutoML Tables と BigQuery MLの使い分け

BigQuery MLはシンプルなモデルによる学習が前提であり、開発速度と効率性を重視している。よって、テストや反復を迅速に行うことを重視し、シンプルなモデルタイプを使用する場合は、BigQuery ML が向いている。一方、高品質で複雑なモデルを得る必要があり、かつ ある程度の時間を待つことができる場合は AutoML Tables が向いている。

なお、[2020年6月16日のリリース](https://cloud.google.com/bigquery-ml/docs/release-notes#June_16_2020)により、BigQuery ML から AutoML Tables によるアンサンブル学習を呼び出せるようになった。


# 参考

- [誰でも簡単に超高速なクエリができるBigQueryとは？](https://www.buildinsider.net/web/bigquery/01)
