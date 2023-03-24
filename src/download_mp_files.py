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
from multiprocessing import Pool

class Video_File_Download:
    def __init__(self):
        self.ids_input_data_path = 'video_data/video_input.csv'
        self.status_data_path = 'video_data/video_status.csv'

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
        with Pool(5) as p:
            p.map(self.create_video_file_id, list(self.id_n))

    
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

    def create_video_file_id(self, id_):
        self.id_ = id_
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