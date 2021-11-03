import streamlit as st
import numpy as np
import json
import time
import glob
import pandas as pd

df = pd.read_csv("data/16_emotion_all.csv")
song_names = list(map(lambda f: int(f.split('/')[-1].split('.')[0]), glob.glob("generated/*.wav")))
print(song_names)

st.title("Chapter 16: Through The Trapdoor")
st.subheader("Paragraph/Valence/Ekman/Audio")

for i, row in df.iterrows():

    if i == 0:
        continue

    text = row['Paragraph Text']
    # print(row['Binary Emotion Class/Score'])
    binary = row['Binary Emotion Class/Score']
    ekman = row['Ekman Emotion Class']

    st_row = st.container()

    cols = st_row.columns(3)

    cols[0].write(text)

    if "positive" in binary:
        cols[1].success("Positive")
    elif "negative" in binary:
        cols[1].error("Negative")
    else:
        cols[1].info("Neutral")
    # cols[2].write(ekman)

    if i in song_names:
        print(i)
        audio_file = open(f"generated/{i}.wav", "rb")
        bytes = audio_file.read()
        cols[2].audio(bytes, format='audio/wav')

    st.markdown("<hr/>", unsafe_allow_html=True)

    # if i > 10:
        # break
