from youtube_transcript_api import YouTubeTranscriptApi
import os
from pytube import YouTube

def sanitize_filename(filename):
    # Sanitize the filename by removing or replacing characters that are illegal in filenames...
    return "".join([c if c.isalnum() or c in " .-_()" else "_" for c in filename])


def seconds_to_min(seconds):
    """Convert seconds to minutes:seconds format."""
    minutes = int(seconds // 60)
    seconds_remainder = int(seconds % 60)
    return f"{minutes}:{str(seconds_remainder).zfill(2)}"  # zfill(2) ensures the seconds are always two digits

def fetch_transcript_and_save(video_url, directory="Transcripts"):
    try:
        # Use pytube to get the video's title
        yt = YouTube(video_url)
        video_title = sanitize_filename(yt.title)
    except Exception as e:
        print(f"Failed to fetch video title: {e}")
        return None

    # Check if the specified directory exists; if not, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Use the sanitized video title as the filename
    filename = os.path.join(directory, f"{video_title}.txt")

    try:
        # Fetching the transcript
        transcript = YouTubeTranscriptApi.get_transcript(yt.video_id)
        
        # Open a file to write in the specified directory
        with open(filename, 'w', encoding='utf-8') as file:
            for entry in transcript:
                timestamp_in_minutes = seconds_to_min(entry['start'])
                line = f"Timestamp: {timestamp_in_minutes} - Text: {entry['text']}\n"
                file.write(line)
                
        print(f"Transcript saved to '{filename}'")
    except Exception as e:
        print(f"An error occurred while fetching the transcript: {e}")
        return None

    return filename

# Youtube link input function...
def yt_input():
    video_url = input("youtube link: ")
    return fetch_transcript_and_save(video_url)


