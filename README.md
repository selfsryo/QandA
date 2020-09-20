# Q&A application


## 概要

・簡単な質問投稿アプリケーションです。質問に対して回答、その回答に対して返答ができます。<br>
・質問者は回答からベストアンサーを１つ選べます。<br>
・タグはアドミンページから追加できます。


## 確認バージョン

| docker | docker-compose |
:---:|:---:
| 19.03.12 | 1.27.2 |


## 環境構築
1.リポジトリをクローン

```
git clone https://github.com/selfsryo/QandA
cd QandA
```

2.マイグレート

```
docker-compose run --rm web python3 manage.py migrate
```

3.コンテナ起動

```
docker-compose up
```

 以下URLからトップページ遷移可能

```
http://127.0.0.1:8000/
```

4.管理者作成

```
docker-compose run --rm web python3 manage.py createsuperuser
```

 以下URLからアドミンページ遷移可能

```
http://127.0.0.1:8000/admin/
```

