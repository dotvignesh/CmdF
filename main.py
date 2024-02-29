import time
from pynput import keyboard
from pynput.keyboard import Key, Controller
import pyperclip
import youtube_dl
import subprocess
import os
import re
from thefuzz import process
from fuzzywuzzy import fuzz
import sys
import webbrowser

whisper_path = "" #TODO set this to your whisper path

controller = Controller()
url = None
cwd = None
transcript = []

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'temp/out.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

def grep(pattern, transcript):
    expr = re.compile(pattern)
    return [line for line in transcript if expr.match(line)]

def getVideo():

    global cwd, url, transcript

    with controller.pressed(Key.cmd):
        controller.tap("l")
        controller.tap("a")
        controller.tap("c")

    time.sleep(0.1)

    url = pyperclip.paste()

    if not url: return
    print("Video:", url)

    cwd = os.getcwd()
    os.chdir(whisper_path)

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)

    ffmpeg_command = [
    'ffmpeg',
    '-i', 'temp/out.mp3',   # Input file
    '-ar', '16000',         # Set sample rate to 16kHz
    '-ac', '1',             # Set number of audio channels to 1 (mono)
    '-c:a', 'pcm_s16le',    # Set audio codec to PCM 16-bit little-endian
    'temp/out.wav'          # Output file
    ]

    try:
        subprocess.run(ffmpeg_command, check=True)
        print("Conversion completed successfully.")
    except subprocess.CalledProcessError as e:
        print("Conversion failed:", e)

    output = subprocess.check_output("./main -f temp/out.wav", shell=True).decode("utf-8")

    transcript = output.split("\n")


def time_to_seconds(time_str):

    pattern = r'\[(\d+):(\d+):(\d+)\.\d+'

    match = re.match(pattern, time_str)
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2))
        seconds = int(match.group(3))

        # Convert the time to seconds
        total_seconds = hours * 3600 + minutes * 60 + seconds
        return str(total_seconds)
    else:
        return None


def getQuery():

    global url, transcript

    if "&" in url:
        url = url[:url.index("&")]

    with controller.pressed(Key.cmd):
        controller.tap("a")
        controller.tap("c")

    time.sleep(0.1)

    query = pyperclip.paste()

    if not query: return
    print("Query:", query)

    matches = process.extract(query, transcript, scorer=fuzz.ratio)
    seconds = time_to_seconds(matches[0][0])

    print("Top Matched URL: ", url + "&t=" + seconds)

    webbrowser.open(url + "&t=" + seconds, new=2, autoraise=True)
    


def f9():
    try:
        getVideo()
    except Exception as e:
        print(e)
    
def f10():
    try:
        getQuery()
    except Exception as e:
        print(e)


def exit_handler():
    try:
        subprocess.call(["rm", "temp/out.wav"])
        subprocess.call(["rm", "temp/out.mp3"])
        os.chdir(cwd)
    except:
        print("---Error---")
    finally:
        print("---Exit---")
    sys.exit(0)


if __name__ == "__main__":
   try:
    with keyboard.GlobalHotKeys({"<109>": f10, "<101>": f9}) as h:
        h.join()
   except KeyboardInterrupt:
      exit_handler()