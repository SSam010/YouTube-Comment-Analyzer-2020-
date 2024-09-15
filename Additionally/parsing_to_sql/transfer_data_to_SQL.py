import json
import os
import sqlite3
import pandas as pd
from youtubesearchpython import Channel

def load_channel_info(list_channel_id):
    dict_channel = {'channel_url': [], 'channel_name': [], 'channel_desc': []}
    with open(list_channel_id, 'r') as channel_ids:
        for channel_id in channel_ids:
            channel_info = Channel.get(channel_id.rstrip())
            dict_channel['channel_url'].append(channel_info['url'])
            dict_channel['channel_name'].append(channel_info['title'])
            dict_channel['channel_desc'].append(channel_info['description'])
    return dict_channel

def process_video_file(video_file_path, id_channel, id_video, dicts, dict_user_id_table_index, id_user):
    with open(video_file_path, 'r') as video_data_json:
        data_video = json.load(video_data_json)

        dicts['video']['video_url'].append(data_video['link'])
        dicts['video']['video_title'].append(data_video['title'])
        dicts['video']['load_data'].append(data_video['uploadDate'])

        dicts['video_channel']['channel_id'].append(id_channel)
        dicts['video_channel']['video_id'].append(id_video)

        dicts['video_stat']['video_id'].append(id_video)
        dicts['video_stat']['data_query'].append(data_video['Time search'])
        dicts['video_stat']['views'].append(int(data_video['viewCount']['text']))

        try:
            comments_file_path = os.path.join(os.path.dirname(video_file_path), data_video['id'], 'comments.json')
            with open(comments_file_path, 'r') as video_comm_json:
                data_video_comm = json.load(video_comm_json)
                for comment in data_video_comm:
                    if comment['channel'] not in dict_user_id_table_index:
                        id_user += 1
                        dict_user_id_table_index[comment['channel']] = id_user
                        dicts['user']['name'].append(comment['author'])
                        dicts['user']['user_id'].append(comment['channel'])
                        dicts['comment']['user_id'].append(id_user)
                    else:
                        dicts['comment']['user_id'].append(dict_user_id_table_index[comment['channel']])
                    dicts['comment']['text'].append(comment['text'])
                    dicts['comment']['data_pub'].append(comment['time'])
                    dicts['comment']['video_id'].append(id_video)
        except FileNotFoundError:
            print(f"{data_video['id']} don't have any comments")
    return id_user

def process_channel_directory(channel_directory, id_channel, dicts, dict_user_id_table_index, id_user):
    id_video = -1
    for video_file in os.listdir(channel_directory):
        if video_file.endswith('.json'):
            id_video += 1
            video_file_path = os.path.join(channel_directory, video_file)
            id_user = process_video_file(video_file_path, id_channel, id_video, dicts, dict_user_id_table_index, id_user)
    return id_user

def save_to_database(connection, dicts):
    for table_name, data_dict in dicts.items():
        table = pd.DataFrame.from_dict(data_dict)
        table.to_sql(table_name, connection, if_exists='append', index_label='id')

def transfer(list_channel_id, dir_search, db_address):
    connection = sqlite3.connect(db_address)

    dicts = {
        'video': {'video_url': [], 'video_title': [], 'load_data': []},
        'video_channel': {'channel_id': [], 'video_id': []},
        'video_stat': {'video_id': [], 'data_query': [], 'views': []},
        'comment': {'video_id': [], 'user_id': [], 'text': [], 'data_pub': []},
        'user': {'name': [], 'user_id': []},
        'channel': load_channel_info(list_channel_id)
    }
    dict_user_id_table_index = {}

    id_channel = -1
    id_user = -1

    for chan_dir in os.listdir(dir_search):
        id_channel += 1
        channel_directory = os.path.join(dir_search, chan_dir)
        id_user = process_channel_directory(channel_directory, id_channel, dicts, dict_user_id_table_index, id_user)

    save_to_database(connection, dicts)

    print('Data added to the library')

# Example
# transfer('list_channel_id.txt', '/path/to/dir_search', 'database.db')
