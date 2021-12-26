# auto-invoice
請求書を自動生成するツール

## 各種サービスのversion

| サービス | version |
| ------------- | ------------- |
| Python  | 3.9.7  |

## zipをダウンロードしてから動作確認する

1. https://github.com/kuroroblog/auto-invoice へアクセスする。
2. 緑色の「Code」と書かれたボタンを選択
3. 「Download ZIP」を選択
4. ダウンロードされたzipファイルをデスクトップへ移動
5. zipファイルをダブルクリック
6. ターミナルを開く。
7. ターミナルを活用して、zipを展開して生成されたフォルダへ移動する。(`$ cd Desktop/auto-invoice-master`)
8. `$ pip install -r requirements.txt`を実行する。
9. `$ cp example.json env.json`を実行する。
10. env.jsonの内容を書き換える。
11. スプレットシートとの接続を行うための準備を行う。(こちらの記事の「2. スプレッドシートの設定」まで対応する。https://tanuhack.com/operate-spreadsheet/ 。ファイル名をservice-account.jsonとしてルートディレクトリに配置する。)
12. cv2.imwrite関数の第一引数のパスを変更する。(cv2.imwriteは画像を保存する関数。なので、画像を保存したい場所を、絶対パス指定などして対応する。デスクトップのパスをあてると無難。)
13. `$ python main.py`を実行する。

## 参考文献
- https://note.nkmk.me/python-pip-install-requirements/
- https://tanuhack.com/operate-spreadsheet/
