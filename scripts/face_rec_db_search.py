import sys
sys.path.insert(0, '..')

import glob
from src.face_search_utils import *
import json
from tqdm import tqdm
json_dict = {}
for face_loc in tqdm(glob.glob('../alphapolitica_faces/*')):
    face_id = face_loc.split('../alphapolitica_faces/')[1]
    json_dict[face_id] = matching_ids(face_loc)

with open("../data/facerec_results.txt", "w") as fp:
    json.dump(json_dict, fp)