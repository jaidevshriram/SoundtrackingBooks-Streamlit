import streamlit as st
import numpy as np
import cv2
import json
import pysrt
import time
import requests
from io import BytesIO
from PIL import Image

from voiceResult import Result
# import SessionState

# from streamlit_autorefresh import st_autorefresh
# st_autorefresh(interval=5 * 60 * 1000, key="dataframerefresh")

sub = pysrt.open("data/HP/new_chapter_subtitles.srt")

def getSubtitle(ms):
    for subtitle in sub:
        start = subtitle.start.to_time()
        end = subtitle.end.to_time()

        startms = start.hour * 60 * 60 * 1000 + start.minute * 60 * 1000 + start.second * 1000 + start.microsecond * 0.001
        endms = end.hour * 60 * 60 * 1000 + end.minute * 60 * 1000 + end.second * 1000 + end.microsecond  * 0.001

        if ms >= startms and ms <= endms:
            return subtitle
    return None

def getCurSong(songList, s):
    for song in songList:
        # print(song.time, s)
        if song.result['matches'] and song.time < s and s < (song.time + 8):
            return song.result
    return None

st.write("""
# Harry Potter
*Movie/Subtitle/Character/Music Alignment*
""")

cap = cv2.VideoCapture("data/videos/HP1.mp4")
raw_vid = open('data/videos/HP1.mp4', 'rb').read()

total_frames = cap.get(7)
fps = cap.get(cv2.CAP_PROP_FPS)
duration = total_frames/fps

# st.write(f"{fps} framerate")

frameIdx = st.slider("Slide to the window", 0, int(duration))

st.write(f"{frameIdx} under consideration, {total_frames} total")

frameNum = int(frameIdx * fps)
# print(frameNum)

# Get frame from video
cap.set(1, frameNum)
ret, frame = cap.read()
# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

st.image(frame, channels="BGR")

chapterName = None

# Show Subtitle
subtitle = getSubtitle(frameNum/fps * 1000)

if subtitle is not None:
    if len(subtitle.text.split(':')) > 1:

        if len(subtitle.text.split(':')) == 2:

            character = subtitle.text.split(':')[0]
            text = ' '.join(subtitle.text.split(':')[1:])

            st.markdown(f"## Character: {character}")
            st.markdown(f""":page_with_curl: - <strong>{text}</strong>""", unsafe_allow_html=True)
        else:
            chapterName = subtitle.text.split(':')[0]
            character = subtitle.text.split(':')[1]
            text = ' '.join(subtitle.text.split(':')[2:])
            st.markdown(f"## Character: {character}")
            st.markdown(f""":page_with_curl: - <strong>{text}</strong>""", unsafe_allow_html=True)
    else:
        st.markdown(f""":page_with_curl: - <strong>{subtitle.text}</strong>""", unsafe_allow_html=True)
else:
    st.markdown(f":x: No Subtitle Here")

col1, col2 = st.columns(2)

# Show song info

songInfo = np.load("data/HP/HPsongInfo.npy", allow_pickle=True)
curSong = getCurSong(songInfo, frameNum/fps)

col1.markdown("## Shazam API")
if curSong is None:
    col1.write("**No song information!**")
else:
    trackName = curSong['track']['title']
    subtitle = curSong['track']['subtitle']
    imageURL = curSong['track']['images']['coverart']

    response = requests.get(imageURL)
    img = Image.open(BytesIO(response.content))

    col1.markdown(f"{curSong['track']['title']}")
    col1.image(img, width=200)

# Column Two

col2.write("## Corresponding Chapter")

if chapterName is not None:
    col2.write(f"**{chapterName}**")
else:
    col2.write(f":x: No Matches!")
