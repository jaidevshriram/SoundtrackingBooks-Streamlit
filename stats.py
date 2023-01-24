from pathlib import Path

from pydub import AudioSegment

song_paths = Path('generated_chunked_low_arousal').rglob('*.mp3')

lengths = []
for song_path in song_paths:
    song = AudioSegment.from_mp3(song_path)
    lengths.append(len(song))

print(max(lengths), min(lengths), len(lengths))
print(sum(lengths)/len(lengths))
