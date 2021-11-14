# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import re
import os
import text2speech as t2s

def onsei_select():

    # ヘッダ
    st.header("ノベル音声選択")

    st.write("まずは章を選択した後に文章の区切りを指定して声を割り当ててください")

    st.write("区切る文字列を指定したら、選択できます")

    df = pd.read_csv(st.session_state.story)
    col1,col2 = st.columns(2)

    with col1:
        chapter = st.selectbox("章を選択してください",df["No"])

        seps = st.multiselect(
        "区切り文字列を指定してください",["「」", "！", "。"],["「」"])

        #上記を元にセパレータ作る。3つ以上、2つ以上、1つ以上で固定
        story_sep = ""
        if len(seps)==3:
            story_sep="「|」|！|。"
        elif len(seps)==2:
            if "「」" in seps and "！" in seps:
                story_sep="「|」|！"
            elif "「」" in seps and "。" in seps:
                story_sep="「|」|。"
            else:
                story_sep="！|。"
        else:
            if "「」" in seps:
                story_sep = "「|」"
            if "！" in seps:
                story_sep = "！"
            if "。" in seps:
                story_sep = "。"

        #ここでchapterからデータ抽出
        df2 = df.filter(items=["No", "text"]).query("No=="+str(chapter))

        st.write("You selected:" + str(seps))

        list_story=[]

        #"列を全部くっつける"
        list_string = df2["text"].str.cat(sep="")
        #先に\nとか\rとかスペースとか取っちゃう
        list_string = list_string.replace("\n","")
        list_string = list_string.replace("\r","")
        list_string = list_string.replace("　","")
        list_string = list_string.replace(" ","")
        # text を"。""」"で、分割
        list_story += re.split(story_sep, list_string)
        list_story.remove("")

        df_story = pd.DataFrame(list_story)
        df_story.assign(voice="default") 


    with col2:
#        st.write(df.filter(items=['No', 'text']).query("No=="+str(chapter))) 

        st.dataframe(df_story) 

        onsei_text = st.text_input("しゃべらせたいtextを入れてね")
        speaker_name = st.selectbox("声をいれてね",("男1","女1","女2"))

        speaker = {"男1": "2b174967-1a8a-42e4-b1ae-5f6548cfa05d", "女1": "c28adf78-d67d-4588-a9a5-970a76ca6b07", "女2": "46a81787-af54-4a91-8c5b-3b597066294e"}

        if st.button("準備ができたらボタンを押してね"):
#            os.remove(str(st.session_state.content_dir)+"/response.wav")
            with open(str(st.secret.content.content_dir)+"response.wav", "wb") as f:
                f.write(t2s.text2speech(speaker[speaker_name],onsei_text))
                st.audio(f.name)