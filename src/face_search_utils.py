import face_recognition
from PIL import Image, ImageDraw
import numpy as np
from tqdm import tqdm
import glob
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams,PointStruct


def get_face_encoding(face_loc):
    image_ = face_recognition.load_image_file(face_loc)
    face_locations = face_recognition.face_locations(image_)
    face_encoding = face_recognition.face_encodings(image_ , model= 'small')[0]
    return(face_encoding)

def get_matching_ids(face_encoding):
    query_vector = face_encoding
    client = QdrantClient(path="/home/ubuntu/alphapolitica/db") 
    hits = client.search(
        collection_name="alphapolitica_face_db",
        query_vector=query_vector,
        score_threshold=0.94, limit=100000 )
    return([dict(i)['payload']['location'] for i in hits])

def matching_ids(face_loc):
    face_encoding = get_face_encoding(face_loc)
    face_ids = get_matching_ids(face_encoding)
    return(face_ids)