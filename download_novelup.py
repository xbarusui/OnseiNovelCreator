# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import tempfile
from pathlib import Path
import novel_downloader


def download_novelup():

    # ヘッダ
    st.header("ノベル読込（ノベプラから取得）")

    st.write("epoch数を指定した後ノベプラから学習させたい文章をURLを入れて取得します")

    st.write("ノベプラのURLを入れてね　例：https://novelup.plus/story/942595339")

    name = st.text_input(label="URL",key="textbox")
    # バリデーション処理
    if len(name) < 1:
        st.warning('URLを指定してください')
        # 条件を満たないときは処理を停止する
        st.stop()

    name_list = []
    load_data = []

    #元々複数でリスト渡しだったので少し修正
    name_list =[name]

    df = pd.DataFrame(novel_downloader.nobera_download(name_list))
#    st.write(df.memory_usage(deep=True))
    st.subheader('ストーリーごとの本文')
    st.write(df.head(100))

#    df["text"] = df["text"].str.replace("\n","")
#    df["text"] = df["text"].str.replace("　","")
#    load_data = ''.join(df["text"])


    # Make temp file path from uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt",dir=st.secrets.content_dir) as f:

        filepath = Path(f.name)

        filepath.write_text(df.to_csv())
#        filepath.write_text(df.to_json())

        st.success("Saved File:{} to storyfile".format(f.name))

        st.session_state.story = filepath

    status_area = st.empty()
    status_area.info("ノベプラ読込開始")

    status_area.info("読込終了")


