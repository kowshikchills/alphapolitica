from src.download_wav_files import Audio_File_Download

AFD = Audio_File_Download()
AFD.update_status_file()

def main():
    while True:
        try:
            AFD.create_audio_file()
        except:
            print('Failed')

main()
