import face_recognition
from PIL import Image, ImageDraw
import numpy as np
import glob
import pickle
from multiprocessing import Pool, Manager
def update_data_with_trans(A):
    translated_dict =  A[0]
    face_loc =  A[1]
    image_ = face_recognition.load_image_file(face_loc)
    x = image_.shape[0]
    y = image_.shape[1]
    loc = [(0,0,x,y)]
    translated_dict[face_loc] = face_recognition.face_encodings(image_, loc)[0]

manager = Manager()
translated_dict = manager.dict()
list_face_loc = glob.glob('../faces/*png')
with Pool(20) as p:
    p.map(update_data_with_trans, [[translated_dict,i] for i in list_face_loc])
translated_dict  = dict(translated_dict)

with open('filename.pickle', 'wb') as handle:
    pickle.dump(dict(translated_dict), handle, protocol=pickle.HIGHEST_PROTOCOL)