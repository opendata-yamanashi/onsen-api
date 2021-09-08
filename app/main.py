from typing import Optional
from fastapi import FastAPI
import pandas as pd
import tabula
import json

app = FastAPI(root_path="/api/onsen")

@app.get("/")
def read_root():
    data = get_data()
    json_data = data.to_json(orient = 'records')
    return json.loads(json_data)

@app.get("/area/{area}")
def read_item(area: str):
    data = get_data()
    df_mask = data['市町村名'] == area
    data = data[df_mask]
    json_data = data.to_json(orient = 'records')
    return json.loads(json_data)

def check_columns(df, previous_df):
    """前ページと現ページのデータフレーム比較"""
    diff1 = set(df.keys()) - set(previous_df.keys())
    diff2 = set(previous_df.keys()) - set(df.keys())
    return (len(diff1) == 0 and len(diff2) == 0)

def get_data():
    previous_df = pd.DataFrame()

    # dfs = tabula.read_pdf("https://www.pref.yamanashi.jp/taiki-sui/documents/h3012012.pdf", lattice=True, pages = 'all')
    dfs = tabula.read_pdf("h3012011.pdf", lattice=True, pages = 'all')

    # データ結合
    for df in dfs:
        if (check_columns(df, previous_df)):
            df = pd.concat([previous_df, df])
        previous_df = df
    
    return previous_df

if __name__ == '__main__':
    data = get_data()
    print(data)