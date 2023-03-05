from src.transcribe_audio_files import Transcribe

TB = Transcribe()

def main():
    while True:
        try:
            TB.transcribe()
        except:
            print('Failed')
main()