from src.download_wav_files import Audio_File_Download
import os
import time

VFD = Audio_File_Download()
if not os.path.isfile('ids_data/ids_status.csv'):
    VFD.update_status_file()

def main():
    while True:
        try:
            VFD.create_audio_file()
        except:
            print('Failed')

main()
