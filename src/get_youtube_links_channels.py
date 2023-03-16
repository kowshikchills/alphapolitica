import time 
from tqdm import tqdm
import pyyoutube
import pickle
import pandas as pd

#TODO COMPLETE THE CODE

class Get_Youtube_Links:

    def __init__(self, API_KEY = "AIzaSyBTj6qYk3Ms82gou0EzdAaguvF6dbZKLYo",     
                channel_id_file = 'channels_ids.csv'):

        self.API_KEY = API_KEY
        self.channel_id_file = channel_id_file
        self.link_channel_dict = {}
        
    def save_videos(self, channel_id, name, count):

        api = pyyoutube.Api(api_key=self.API_KEY)
        channel_info = api.get_channel_info(channel_id = channel_id)
        playlist_id = channel_info.items[0].contentDetails.relatedPlaylists.uploads
        uploads_playlist_items = api.get_playlist_items(
            playlist_id=playlist_id, count = count, limit=50)
        video_ids = []
        for item in tqdm(uploads_playlist_items.items):
            time.sleep(0.01)
            video_id = item.contentDetails.videoId
            video_ids.append(video_id)
        self.link_channel_dict[name] = video_ids

    def add_channel_name(self, name, channel_id):
        pass

    def download_videos_link(self, count):
        
        self.df_channel = pd.read_csv(self.channel_id_file)
        names = self.df_channel['name']
        channels_ids = self.df_channel['channel_id']
        for i in range(len(names)):
            self.save_videos(channels_ids[i], names[i], count)
        return(self.link_channel_dict)

''' 
import pandas as pd
df = pd.DataFrame()
df['name'] = ['abn','tv5','tv9','sakshi']
df['channel_id'] = ['UC_2irx_BQR7RsBKmUV9fePQ','UCAR3h_9fLV82N2FH4cE4RKw','UCPXTXMecYqnRKNdqdVOGSFg','UCQ_FATLW83q-4xJ2fsi8qAw']
df.to_csv('data_youtube/channels_ids.csv',index=False)
'''
        
