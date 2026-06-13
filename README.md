# 📒 アルゴリズム学習ノート

BFS・二分探索・DPなどを、解説＋インタラクティブ迷路＋コード実行で学べるサイト。

## ローカルで動かす

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Cloud にデプロイ

1. このリポジトリを GitHub に push
2. [share.streamlit.io](https://share.streamlit.io) でリポジトリを選択
3. Main file: `app.py`
4. Deploy!

## 新しいアルゴリズムを追加する方法

`pages/` にファイルを追加するだけ。

```
pages/2_二分探索.py
pages/3_DP入門.py
```

自動でサイドバーに追加されます。
