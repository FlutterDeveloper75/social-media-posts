# Narration and sound

Voice: Kokoro `af_heart` (Heart) for every video. kokoro-onnx is MIT, Kokoro-82M weights are Apache 2.0.

Setup (each fresh session):
    pip install --break-system-packages kokoro-onnx soundfile scipy
    mkdir -p ~/kokoro && cd ~/kokoro
    curl -sLO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
    curl -sLO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin

Use: write a cue file like example-cues-f5.json (each cue = start, end, exact caption text; sfx = time, whoosh|pop|click|tick|chime), then
    python3 tools/narrate.py cues.json audio.wav
    ffmpeg -i video.mp4 -i audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k -af loudnorm=I=-16:TP=-1.5:LRA=11 -shortest -movflags +faststart out.mp4
Narration reads the on-screen caption word for word and ends with "The link is in the caption."

Writing for the voice: spell times and dates the way a person says them ("Monday night, November thirtieth, at eleven fifty-nine, Central time"). Avoid abbreviations such as p.m., a.m., CT or $ in narration text; they cause stalls. Keep the abbreviations on screen only.
