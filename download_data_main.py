from src.download_wav_files import Audio_File_Download
import os
import time

AFD = Audio_File_Download()
if not os.path.isfile('ids_data/ids_status.csv'):
    AFD.update_status_file()

def main():
    while True:
        try:
            AFD.create_audio_file()
            time.sleep(5)
        except:
            print('Failed')

main()
