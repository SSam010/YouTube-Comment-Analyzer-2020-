from datetime import datetime

from parsing_to_sql import comments_below_video as cbv
from parsing_to_sql import transfer_data_to_SQL as tds
from parsing_to_sql import youtube_video_from_chanel_v2 as yvc

time_str = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")

SETTINGS = {
    'file_txt_address': 'channel_id.txt',
    'search_directory': f'search_result {time_str}',
    'db_address': 'db.sqlite3'
}

yvc.start_parsing_video(list_channel_id=SETTINGS['file_txt_address'],
                        dir_search=SETTINGS['search_directory'],
                        time_now=time_now
                        )

cbv.get_comments_from_directory(search_dir=SETTINGS['search_directory'])

tds.transfer(list_channel_id=SETTINGS['file_txt_address'],
             dir_search=SETTINGS['search_directory'],
             db_address=SETTINGS['db_address']
             )
