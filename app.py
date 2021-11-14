# -*- coding: utf-8 -*-

import streamlit as st
import download_novelup as download
import onsei_select as onseisel

##google colab
#st.session_state.content_dir = "/content/"
##streamlit sharing
st.session_state.content_dir = "/home/appuser/"

def main():

    # タイトル
    st.title('音声ノベルクリエイター')

    # アプリケーション名と対応する関数のマッピング
    apps = {
        "-": None,
        "ノベル読込(ノベプラ)": download_novelup,
        "ノベル音声選択": onsei_select,
        "音声ノベルダウンロード": download_onseinovel
    }
    selected_app_name = st.sidebar.selectbox(label="apps",
                                             options=list(apps.keys()))

    if selected_app_name == "-":
        st.info("左のメニューから選んでください")
        st.stop()

    # 選択されたアプリケーションを処理する関数を呼び出す
    render_func = apps[selected_app_name]
    render_func()


def download_novelup():
    download.download_novelup()

def onsei_select():
    onseisel.onsei_select()

def download_onseinovel():
    st.write("工事中")


if __name__ == "__main__":
    main()


