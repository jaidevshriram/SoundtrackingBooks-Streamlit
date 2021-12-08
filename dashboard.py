import streamlit as st
import os
import numpy as np
import json
import time
import glob
import pandas as pd

chapterNum = st.sidebar.selectbox(
    "Select the Chapter",
    [i for i in range(len(os.listdir("data/HP/chapters")))]
)

chapterNames = sorted(os.listdir("data/HP/chapters/"), key=lambda x: int(x.split('-')[0].strip()))
print(chapterNames[:5])

df = pd.read_csv(f"data/HP/sheets/{chapterNum+1:02}_emotion_ekman.csv")

try:
    song_names = list(map(lambda f: int(f.split('/')[-1].split('.')[0]), glob.glob(f"generated/{chapterNum}/*.wav")))
except:
    song_names = []

print(song_names)

st.title("Chapter " + str(chapterNum + 1) + ": " + chapterNames[chapterNum].split('-')[1].replace('_', ' ').split('.')[0])
st.subheader("Paragraph/Valence/Ekman/Audio")

print(df)

for i, row in df.iterrows():

    if i == 0:
        continue

    try:
        text = row['Paragraph Text']
    except:
        text = row['paragraph']

    num = 4
    try:
        # print(row['Binary Emotion Class/Score'])
        binary = row['Binary Emotion Class/Score']
        # ekman = row['Ekman Emotion Class']
    except:
        num = 3

    st_row = st.container()

    cols = st_row.columns(num)

    cols[0].write(str(i))
    cols[1].write(text)

    if num == 4:

        if "positive" in binary:
            cols[2].success("Positive")
        elif "negative" in binary:
            cols[2].error("Negative")
        else:
            cols[2].info("Neutral")
        # cols[2].write(ekman)

    if i in song_names:
        print(i)
        audio_file = open(f"generated/{chapterNum}/{i}.wav", "rb")
        bytes = audio_file.read()
        cols[num-1].audio(bytes, format='audio/wav')

    st.markdown("<hr/>", unsafe_allow_html=True)

    # if i > 10:
        # break
