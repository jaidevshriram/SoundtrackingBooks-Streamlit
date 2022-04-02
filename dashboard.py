import streamlit as st
import os
import numpy as np
import json
import time
import glob
import pandas as pd

version = st.sidebar.selectbox(
    "Select version of soundtrack",
    ["generated_chunked"]
)

chapterNum = st.sidebar.selectbox(
    "Select the Chapter",
    [i for i in range(len(os.listdir("data/HP/chapters")))]
)

chapterNames = sorted(os.listdir("data/HP/chapters/"), key=lambda x: int(x.split('-')[0].strip()))
# print(chapterNames[:5])

with open(os.path.join("./data/HP/chunks/", f"{chapterNames[chapterNum].replace('txt', 'json')}")) as f:
    chunked = json.load(f)

try:
    song_names = list(map(lambda f: int(f.split('/')[-1].split('.')[0]),  glob.glob(f"{version}/{chapterNum}/*.mp3")))
except:
    song_names = []

st.title("Chapter " + str(chapterNum) + ": " + chapterNames[chapterNum].split('-')[1].replace('_', ' ').split('.')[0])
st.subheader("Chunk / Paragraph / Audio")

for i, chunk in enumerate(chunked['segmented']):

    paras = chunk.splitlines()

    for j, row in enumerate(paras):

        row = row.strip()

        if len(row) == 0:
            continue

        st_row = st.container()

        cols = st_row.columns(4)

        cols[0].write(str(i))
        cols[1].write(str(j//2))
        cols[2].write(row)

        if i in song_names and j == 0:
            audio_file = open(f"{version}/{chapterNum}/{i}.mp3", "rb")
            bytes = audio_file.read()
            cols[3].audio(bytes, format='audio/mp3')

        st.markdown("<hr/>", unsafe_allow_html=True)

        # if i > 10:
            # break
