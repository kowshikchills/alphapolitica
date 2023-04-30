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
import cv2
from yt_dlp import YoutubeDL
from multiprocessing import Pool, Manager

class Video_File_Download:
    def __init__(self):
        self.ids_input_data_path = 'video_data/video_input.csv'
        self.status_data_path = 'video_data/video_status.csv'
        self.down_pack = 'ydl'

    def update_status_file(self,file=None):

        if not os.path.isfile(self.status_data_path):
            df_ids_input = pd.read_csv(self.ids_input_data_path)
            df_ids_input['video_file_created'] = 0
            df_ids_input['failed'] = 0
            df_ids_input = df_ids_input.drop_duplicates('ids')
            df_ids_input.to_csv(self.status_data_path ,index=False)
        else:
            df_status = pd.read_csv(self.status_data_path)
            df_ids_input = pd.read_csv('video_data/video_input.csv')
            to_add_ids = set(df_status['ids']) -  set(df_ids_input['ids'])
            df_add = pd.DataFrame(to_add_ids, columns=['ids'])
            df_add['video_file_created'] = 0
            df_add['failed'] = 0
            df_status = df_status.append(df_add)
            df_status = df_status.drop_duplicates(subset=['ids'], keep='first')
            df_status.to_csv(self.status_data_path ,index=False)

    def update_status(self,id_,status):
        if status =='created':
            print(id_)
            df_status = pd.read_csv(self.status_data_path)
            df_status.at[df_status.index[df_status.ids == id_].tolist()[0],'video_file_created'] =1
            df_status.to_csv(self.status_data_path ,index=False)
        else:
            df_status = pd.read_csv(self.status_data_path)
            df_status.at[df_status.index[df_status.ids == id_].tolist()[0],'failed'] =1
            df_status.to_csv(self.status_data_path ,index=False)

    def update_status_bulk(self,status_bulk):
        for i in status_bulk.keys():
            if status_bulk[i] == 1:
                self.update_status(i, status = 'created')
            else:
                self.update_status(i, status = 'failed')

    def get_id(self):
        df_status = pd.read_csv(self.status_data_path )
        df = df_status[df_status.video_file_created == 0]
        df = df[df.failed == 0]
        return(df.ids.values[0])

    def get_id_n(self,n):
        df_status = pd.read_csv(self.status_data_path )
        df = df_status[df_status.video_file_created == 0]
        df = df[df.failed == 0]
        return(df.ids.values[:n])

    def create_video_files_multi(self, n):
        self.id_n = self.get_id_n(n)
        manager = Manager()
        update_dict = manager.dict()
        with Pool(5) as p:
            p.map(self.create_video_file_id, [[i, update_dict] for i in  list(self.id_n)])
        self.update_status_bulk(update_dict)

    def download_video(self, link, id, mp4_file_download):
        try:
            youtube_dl_options = {
                "outtmpl": mp4_file_download,
                'extract_audio': False,
                'format':'133'
            }
            with YoutubeDL(youtube_dl_options) as ydl:
                return ydl.download([link])
        except:
            try:
                youtube_dl_options = {
                    "outtmpl": mp4_file_download,
                    'extract_audio': False,
                    'format':'134'
                }
                with YoutubeDL(youtube_dl_options) as ydl:
                    return ydl.download([link])
            except:
                youtube_dl_options = {
                    "outtmpl": mp4_file_download,
                    'extract_audio': False,
                    'format':'135'
                }
                with YoutubeDL(youtube_dl_options) as ydl:
                    return ydl.download([link])

    def create_video_file_id(self, input):
        self.id_ = input[0]
        update_dict_ = input[1]

        self.link = 'https://www.youtube.com/watch?v=' + self.id_
        mp4_file_download = self.id_+'.mp4'
        file = 'video_data/'+ mp4_file_download
        try:
            if self.down_pack == 'yttube':
                self.yt = YouTube(self.link)
                stream_ = self.yt.streams.filter(progressive="True").asc()[1]
                stream_.download(filename=mp4_file_download,output_path='video_data')
            else:
                self.download_video(self.link,self.id_,file )
        
            cap = cv2.VideoCapture(file)
            path = file.split('.mp4')[0]
            os.mkdir(path)
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            save_interval = 5
            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    frame_count += 1
                    if frame_count % (fps * save_interval) == 1:
                        cv2.imwrite(path + '/'+ str(frame_count) +'.png',frame)
                else:
                    break
            cap.release()
            cv2.destroyAllWindows()

            update_dict_[self.id_] = 1
            os.remove(file)
        except:
            update_dict_[self.id_] = 0
    
    def create_video_file(self):
        self.id_ = self.get_id()
        self.link = 'https://www.youtube.com/watch?v=' + self.id_
        mp4_file_download = self.id_+'.mp4'
        try:
            self.yt = YouTube(self.link)
            stream_ = self.yt.streams.filter(progressive="True").asc()[1]
            stream_.download(filename=mp4_file_download,output_path='video_data')
            file = 'video_data/'+ mp4_file_download
            cap = cv2.VideoCapture(file)
            path = file.split('.mp4')[0]
            os.mkdir(path)
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            save_interval = 5
            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    frame_count += 1
                    if frame_count % (fps * save_interval) == 1:
                        cv2.imwrite(path + '/'+ str(frame_count) +'.png',frame)
                else:
                    break
            cap.release()
            cv2.destroyAllWindows()
            self.update_status(self.id_,status = 'created')
            os.remove(file)
        except:
            self.update_status(self.id_,status = 'failed')

    def reset(self):
        to_delete = glob.glob('video_data/*.mp4') +['video_data/video_status.csv']
        for fil in to_delete:
            os.remove(fil)