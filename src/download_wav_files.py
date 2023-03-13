''' 
Create audio file

'''
import pandas as pd
import os.path
from pytube import YouTube
from scrapetube import scrapetube
import moviepy.config as mpy_conf
import moviepy.editor as mp
import os
import glob

class Audio_File_Download:
    def __init__(self):
        self.ids_input_data_path = 'ids_data/ids_input.csv'
        self.status_data_path = 'ids_data/ids_status.csv'

    def update_status_file(self,file=None):

        if not os.path.isfile(self.status_data_path):
            df_ids_input = pd.read_csv(self.ids_input_data_path)
            df_ids_input['audio_file_created'] = 0
            df_ids_input['failed'] = 0
            df_ids_input = df_ids_input.drop_duplicates('ids')
            df_ids_input.to_csv(self.status_data_path ,index=False)
        else:
            df_status = pd.read_csv(self.status_data_path)
            df_ids_input = pd.read_csv('ids_data/ids_input.csv')
            to_add_ids = set(df_status['ids']) -  set(df_ids_input['ids'])
            df_add = pd.DataFrame(to_add_ids, columns=['ids'])
            df_add['audio_file_created'] = 0
            df_add['failed'] = 0
            df_status = df_status.append(df_add)
            df_status = df_status.drop_duplicates(subset=['ids'], keep='first')
            df_status.to_csv(self.status_data_path ,index=False)

    def update_status(self,id_,status):
        if status =='created':
            df_status = pd.read_csv(self.status_data_path)
            df_status.at[df_status.index[df_status.ids == id_].tolist()[0],'audio_file_created'] =1
            df_status.to_csv(self.status_data_path ,index=False)
        else:
            df_status = pd.read_csv(self.status_data_path)
            df_status.at[df_status.index[df_status.ids == id_].tolist()[0],'failed'] =1
            df_status.to_csv(self.status_data_path ,index=False)

    def get_id(self):
        df_status = pd.read_csv(self.status_data_path )
        df = df_status[df_status.audio_file_created == 0]
        df = df[df.failed == 0]
        return(df.ids.values[0])
    
    def create_audio_file(self):
        self.id_ = self.get_id()
        self.link = 'https://www.youtube.com/watch?v=' + self.id_
        mp4_file_download = self.id_+'.mp4'
        wav_file_download = self.id_+'.wav'
        try:
            self.yt = YouTube(self.link)
            stream_ = self.yt.streams.filter(progressive="True").asc()[1]
            stream_.download(filename=mp4_file_download,output_path='ids_data')
            #mpy_conf.change_settings({'FFMPEG_BINARY': '/opt/homebrew/Cellar/ffmpeg'})
            my_clip = mp.VideoFileClip('ids_data/' + mp4_file_download)
            my_clip.audio.write_audiofile('ids_data/' + wav_file_download)
            os.remove('ids_data/' + mp4_file_download)
            self.update_status(self.id_,status = 'created')
        except:
            self.update_status(self.id_,status = 'failed')

    def reset(self):
        to_delete = glob.glob('ids_data/*.wav') + glob.glob('ids_data/*.mp4')+['ids_data/ids_status.csv']
        for fil in to_delete:
            os.remove(fil)