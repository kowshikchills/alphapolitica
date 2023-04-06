from src.create_faces_video import CreateFaces
import time
import glob
CF = CreateFaces()

def main():
    while True:
        if len(glob.glob('video_data/*')) > 2:
            try:
                CF.get_all_faces_from_folder()
            except:
                print('failed')
                time.sleep(120)
        else:
            print('waiting for video files')
            time.sleep(120)

main()