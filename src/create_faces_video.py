
import pandas as pd
import glob
import os
import cv2
import os

class CreateFaces:
    def __init__(self):
        self.status_data_path = 'video_data/video_status.csv'
        self.data_path = 'video_data'

    def get_video(self):
        files = glob.glob(self.data_path +'/*.mp4')
        id_ = files[0].split('/')[1].split('.mp4')[0]
        return(files[0],id_)

    def create_failed_file(self):
        pass

    def get_screenshots(self, file, id):
        try:
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
        except:
            print(id,'failed')

    def create_screenshots(self):
        self.video_url,id_ = self.get_video()
        self.get_screenshots(self, self.video_url, id_)
        print(self.video_url)
        os.remove(self.video_url)
        