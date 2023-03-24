from src.download_mp_files import Video_File_Download
import os
import time

VFD = Video_File_Download()
if not os.path.isfile('video_data/video_status.csv'):
    VFD.update_status_file()

def main():
    while True:
        try:
            VFD.create_video_files_multi(10)
        except:
            print('failed')

main()
