from src.download_wav_files import Video_File_Download
import os
import time

VFD = Video_File_Download()
if not os.path.isfile('video_data/video_status.csv'):
    VFD.update_status_file()

def main():
    while True:
        try:
            VFD.create_audio_file()
            time.sleep(5)
        except:
            print('Failed')

main()
