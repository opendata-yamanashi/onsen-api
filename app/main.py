from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, Field
import requests
import pandas as pd
import tabula
import json
import os

class OnsenData(BaseModel):
    town: str = Field(None, alias='市町村名')
    name: str = Field(None, alias='利用施設名称・屋号')
    address: str = Field(None, alias='利用施設所在地')
    quality: str = Field(None, alias='現在の利用状況/泉質')

target_url = "https://www.pref.yamanashi.jp/taiki-sui/documents/h3012011.pdf"

root_path = os.getenv("ROOT_PATH", "")
app = FastAPI(
    title="温泉利用施設API",
    root_path=root_path
)

@app.get("/", response_model=List[OnsenData])
def read_root():
    data = get_data(target_url)
    json_data = data.to_json(orient = 'records')
    return json.loads(json_data)

@app.get("/area/{area}", response_model=List[OnsenData])
def read_item(area: str):
    data = get_data(target_url)
    df_mask = data['市町村名'] == area
    data = data[df_mask]
    json_data = data.to_json(orient = 'records')
    return json.loads(json_data)

def get_data(url):
    path = download_file_if_needed(url)

    previous_df = pd.DataFrame()

    dfs = tabula.read_pdf(path, lattice=True, pages = 'all')

    # データ結合
    for df in dfs:
        if (check_columns(df, previous_df)):
            df = pd.concat([previous_df, df])
        previous_df = df
    
    return previous_df

def check_columns(df, previous_df):
    """前ページと現ページのデータフレーム比較"""
    diff1 = set(df.keys()) - set(previous_df.keys())
    diff2 = set(previous_df.keys()) - set(df.keys())
    return (len(diff1) == 0 and len(diff2) == 0)

def download_file_if_needed(url):
    """ローカルにデータファイルがない場合は、データファイルをダウンロードする"""
    dir = os.path.dirname(__file__)
    file_path = dir + "/data.pdf"
    if not os.path.exists(file_path):
        data = requests.get(url).content
        with open(file_path ,mode='wb') as f:
            f.write(data)

    return file_path
