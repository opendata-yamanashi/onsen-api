# 山梨県 温泉利用施設API

## 出典
- [「山梨県公共温泉利用施設一覧（H30.12.1現在）」（山梨県）](https://www.pref.yamanashi.jp/taiki-sui/documents/h3012011.pdf)

## API 仕様
- https://opendata.yamanashi.dev/api/onsen/docs を参照

## ライセンス
本ソフトウェアは、[MITライセンス](./LICENSE.txt)の元提供されています。

## 開発者向け情報

### 環境構築の手順

- 必要となるPythonバージョン: 3.6以上
- 必要となるJavaバージョン: 8以上

**pip を使う場合**
``` bash
$ pip install -r requirements.txt
$ uvicorn app.main:app --reload
```

**docker を使う場合**
```bash
$ docker pull opendata19/fastapi-tabula:latest
$ docker run --name onsen-api -p 8000:80 -v $(pwd)/app:/app -itd opendata19/fastapi-tabula:latest
```
