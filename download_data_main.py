from src.download_wav_files import Audio_File_Download
import os

AFD = Audio_File_Download()
if not os.path.isfile('ids_data/ids_status.csv'):
    AFD.update_status_file()

def main():
    while True:
        try:
            AFD.create_audio_file()
        except:
            print('Failed')

main()
