from src.create_faces_video import CreateFaces

CF = CreateFaces()

def main():
    while True:
        try:
            CF.get_all_faces_from_folder()
        except:
            print('Failed')
main()