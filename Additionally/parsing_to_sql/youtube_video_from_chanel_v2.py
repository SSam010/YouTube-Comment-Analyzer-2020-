import json
import os
from youtubesearchpython import Playlist, Video, ResultMode

def create_directory(path):
    os.makedirs(path, exist_ok=True)

def get_channel_name(playlist):
    return playlist.videos[0]['channel']['name']

def fetch_all_videos(playlist):
    while playlist.hasMoreVideos:
        playlist.getNextVideos()

def save_video_info(video, channel_dir, time_now):
    video_info = Video.getInfo(video['link'], mode=ResultMode.json)
    video_info['Time search'] = str(time_now)
    video_file_path = os.path.join(channel_dir, f"{video['id']}.json")
    with open(video_file_path, 'w') as file:
        json.dump(video_info, file, indent=4)

def process_channel(channel_id, dir_search, time_now):
    playlist = Playlist(playlist_from_channel_id(channel_id.rstrip()))
    channel_name = get_channel_name(playlist)
    channel_dir = os.path.join(dir_search, channel_name)
    create_directory(channel_dir)
    fetch_all_videos(playlist)
    for video in playlist.videos:
        save_video_info(video, channel_dir, time_now)
    print(f'Parsing video results are saved in the directory "{channel_name}"')

def start_parsing_video(channel_id_file, dir_search, time_now):
    create_directory(dir_search)
    with open(channel_id_file, "r") as file:
        for channel_id in file:
            process_channel(channel_id, dir_search, time_now)

# example
# start_parsing_video('channel_id_file.txt', '/path/to/dir_search', '2023-10-01')
