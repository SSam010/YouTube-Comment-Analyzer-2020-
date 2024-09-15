from youtube_comment_downloader import *


import os
import json
from youtube_comment_downloader import YoutubeCommentDownloader

def load_video_data(video_file_path):
    with open(video_file_path, "r") as file:
        return json.load(file)

def download_comments(video_url):
    downloader = YoutubeCommentDownloader()
    return downloader.get_comments_from_url(video_url, language='en')

def save_comments(comments, comments_dir):
    os.makedirs(comments_dir, exist_ok=True)
    comments_file_path = os.path.join(comments_dir, 'comments.json')
    with open(comments_file_path, 'w') as comments_file:
        json.dump(comments, comments_file, indent=4)

def process_video_file(channel_directory, video_file):
    if video_file.endswith(".json"):
        video_file_path = os.path.join(channel_directory, video_file)
        video_data = load_video_data(video_file_path)
        video_id = video_data['id']
        video_url = video_data['link']
        comments_dir = os.path.join(channel_directory, video_id)

        comments = download_comments(video_url)
        if comments:
            save_comments(comments, comments_dir)

def process_channel(channel_directory):
    for video_file in os.listdir(channel_directory):
        process_video_file(channel_directory, video_file)

def get_comments_from_directory(search_dir):
    for channel_name in os.listdir(search_dir):
        channel_directory = os.path.join(search_dir, channel_name)
        process_channel(channel_directory)
        print(f'Comments from the channel "{channel_name}" received.')
