import streamlit as st
import glob 
import numpy as np
import pandas as pd


st.metric(label="Total Videos In folder", value=str(len(glob.glob('video_data/*'))))

st.header('Total files created')

df = pd.read_csv('video_data/video_status.csv')
created = df['video_file_created'].sum()
total = len(df)
st.metric(label="Total videos created", value= str(created),delta=str(np.round(created/total,2)) )



import glob
import numpy as np
faces_id = np.unique([i.split('faces/')[1].split('_face')[0][:11] for i in (glob.glob('faces/*'))])
created = len(faces_id)
st.metric(label="Total faces created", value= str(created),delta=str(np.round(created/total,2)) )