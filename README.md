# Q&A application



## 概要

・簡単な質問投稿アプリケーションです。質問に対して回答、その回答に対して返答ができます。
・質問者は回答からベストアンサーを１つ選べます。



## 確認した環境
---

:docker: 19.03.12
:docker-compose: 1.27.2



## 手順
---
1.リポジトリをクローン

```
git clone https://github.com/selfsryo/QandA
```

2.マイグレート

```
cd QandA
docker-compose run --rm web python3 manage.py migrate
```

3.コンテナ起動

```
docker-compose up
```

 以下URLからトップページ遷移

```
http://127.0.0.1:8000/
```

4.管理者作成

```
docker-compose run --rm web python3 manage.py createsuperuser
```

 以下URLからアドミンページ遷移

```
http://127.0.0.1:8000/admin/
```

