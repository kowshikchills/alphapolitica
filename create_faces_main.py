from src.create_faces_video import CreateFaces

CF = CreateFaces()

def main():
    while True:
        try:
            CF.create_screenshots()
        except:
            print('Failed')
main()