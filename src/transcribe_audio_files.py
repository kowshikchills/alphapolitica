import torch
from transformers import pipeline
from datasets import load_dataset
import torchaudio
import pandas as pd
import glob
import os

class Transcribe:
    def __init__(self):
        self.status_data_path = 'ids_data/ids_status.csv'
        self.data_path = 'ids_data'
        self.pipe = pipeline(
        "automatic-speech-recognition",
        model="vasista22/whisper-telugu-base",
        chunk_length_s=60,device=0)

    def get_id(self):
        files = glob.glob(self.data_path +'/*.wav')
        id_ = files[0].split('/')[1].split('.wav')[0]
        return(files[0],id_)

    def transcribe(self):
        self.audio_url,id_ = self.get_id()
        try: 
            print(self.audio_url)
            speech, org_sr = torchaudio.load(self.audio_url)
            new_sample_rate = 16000
            speech = torchaudio.functional.resample(speech, orig_freq=org_sr, new_freq=new_sample_rate)
            sample = speech[0].numpy()
            self.output = self.pipe(sample)
            text_file = open(self.audio_url.replace('.wav','.txt'), "w")
            n = text_file.write(self.output['text'])
            os.remove(self.audio_url)
            text_file.close()
        except:
            print(self.audio_url,'failed')
            text_file = open(self.audio_url.replace('.wav','.::failed.txt'), "w")
            n = text_file.write(self.output['text'])
            os.remove(self.audio_url)
            text_file.close()
