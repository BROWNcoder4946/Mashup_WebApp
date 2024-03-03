from youtubesearchpython import VideosSearch
import yt_dlp
from pydub import AudioSegment
import os
import sys

# To get urls from yt
def get_youtube_urls(search_query, n=5):
    try:
        videos_search = VideosSearch(search_query, limit=n)
        results = videos_search.result()

        # Check if results list is empty
        if not results['result']:
            raise Exception("No results found")

        urls = [result['link'] for result in results['result']]
        return urls
    except Exception as e:
        print(f"Error: {e}")
        return []

# To download audios from url's
def download_audio_ytdlp(url, download_location):

    if not os.path.exists(download_location):
        os.makedirs(download_location)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': download_location + '/%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except yt_dlp.DownloadError as e:
        print(f"Download error: {e}")

# To crop mp3 files
def crop_and_merge_audio(input_folder, end_ms , output_filename="final.mp3"):

    if end_ms < 10000:
        raise ValueError("Time must be greater than or equal 10 seconds")

    # List all files in the input folder
    input_files = [file for file in os.listdir(input_folder) if file.endswith(".mp3")]

    # List to store cropped audio segments
    cropped_audios = []

    # Crop each audio file and append to the list
    for input_file in input_files:
        input_path = os.path.join(input_folder, input_file)
        audio = AudioSegment.from_file(input_path, format="mp3")
        cropped_audio = audio[0:end_ms]
        cropped_audios.append(cropped_audio)

    # Merge the cropped audio segments
    merged_audio = sum(cropped_audios)

    # Export the merged audio to a new file in the output folder
    output_path = os.path.join(output_filename)
    merged_audio.export(output_path, format="mp3")

    return output_path


def main(singer , nov , nos , output_file = 'final.mp3'):

    # Get the url's
    query = f"{singer}'s latest song"
    url = get_youtube_urls(query,nov)

    # Downloading mp3 files to raw_mp3 folder
    for i in range(nov):
        download_audio_ytdlp(url[i],'raw_mp3')

    # Croppping audio from downloaded mp3 files
    crop_and_merge_audio('raw_mp3', nos , output_file)


# singer = str(input("Enter Singer's Name:"))
# no_of_videos = int(input("Enter number of videos to extract:"))
# no_of_seconds = int(input("Enter number of seconds of audio to extract from each song:"))*1000
# output_file = 'final.mp3'


# Making this file executable from command line
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py singer nov nos output_file")
    else:
        singer = sys.argv[1]
        no_of_videos = int(sys.argv[2])
        no_of_seconds = int(sys.argv[3]) * 1000
        output_file = sys.argv[4]
        main(singer, no_of_videos, no_of_seconds, output_file)
