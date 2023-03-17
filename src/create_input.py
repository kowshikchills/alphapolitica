import pandas as pd
import ast
import numpy as np
from tqdm import tqdm
from googletrans import Translator
from multiprocessing import Pool, Manager



#TODO: complete code 
#  
class CreateInputFile:
    def __init__(self):
        pass
    def read_merge_data(self):
        df_data = pd.read_csv('data/videos_alphapolitica_tagged.csv')
        df_channel = pd.read_csv('data/videos_alphapolitica.csv')
        df_length = pd.read_pickle('data/videos_alphapolitica_length.pkl')
        del df_channel['Unnamed: 0']
        df_tagged = pd.merge(df_channel,df_data,on='ids')
        df_tagged['sno'] =np.arange(len(df_tagged))
        del df_tagged['Unnamed: 0']
        self.df_tagged = pd.merge(df_tagged,df_length,on='ids')
        self.df_tagged = self.df_tagged.dropna()
    def translate(self):
        translator = Translator()
        def update_data_with_trans(A):
            d = A[0]
            i = A[1]
            extracted =  self.df_tagged[self.df_tagged.sno == i]['title'].values[0][:5000]
            d[i] = translator.translate(extracted, dest='en').text
        manager = Manager()
        translated_dict = manager.dict()
        with Pool(15) as p:
            p.map(update_data_with_trans, [[translated_dict,i] for i in np.arange(len(self.df_tagged))])
        self.df_tagged['translated'] = [translated_dict[i] for i in np.arange(len(self.df_tagged))]
        self.df_tagged.to_csv('data/videos_alphapolitica_tagged_translated.csv')
    def create_file_ids(self, read_file =False,):
        if self.read_file:
            df_tagged_translated = pd.read_csv('data/videos_alphapolitica_tagged_translated.csv')
        else:
            df_tagged_translated = self.df_tagged
        del df_tagged_translated['Unnamed: 0.1']
        del df_tagged_translated['Unnamed: 0']
        df_tagged_translated = pd.merge(df_tagged_translated,df_length,on='ids')
        df_tagged_translated = df_tagged_translated.dropna()
        df_tagged_translated['keywords'] = [ast.literal_eval(i) for i in df_tagged_translated['keywords']]
        df_tagged_translated['len_keywords'] = [len(i) for i in df_tagged_translated['keywords']]
        df_tagged_translated = df_tagged_translated[df_tagged_translated['length'] < 10*60]
        df_tagged_translated[['ids']].to_csv('ids_data/ids_input.csv',index=None)
        



