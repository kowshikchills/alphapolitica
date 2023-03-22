
import pandas as pd
import glob
import cv2
import os
from PIL import Image
import face_recognition
import time

class CreateFaces:
    def __init__(self,):
        self.faces_path = 'faces'

    def get_video_file(self):
        files = [i for i in glob.glob('video_data/*') if ('.csv' not in i) and ('.mp4' not in i)]
        id_ = files[0].split('/')[1]
        return(files[0],id_)

    def get_faces_file(self, img_loc):
        image = face_recognition.load_image_file(img_loc)
        face_locations = face_recognition.face_locations(image)
        face_pil_images = []
        for face_location in face_locations:
            top, right, bottom, left = face_location
            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            face_pil_images.append(pil_image)
        return(face_pil_images)
    
    def get_all_faces_from_folder(self):
        self.folder, id_ = self.get_video_file()
        self.png_files = glob.glob(self.folder + '/*png')
        for img_loc in self.png_files:
            frame = img_loc.split('/')[-1].split('.png')[0]
            self.face_pil_images = self.get_faces_file(img_loc)
            if len(self.face_pil_images) != 0:
                for i in range(len(self.face_pil_images)):
                    pil_image = self.face_pil_images[i]
                    pil_image.save(self.faces_path + '/'+id_+'_'+frame+ '_face_'+ str(i) +'.png')
        os.remove(self.folder)

    

    


        