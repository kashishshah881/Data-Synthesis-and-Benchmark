import json
import os
import urllib
import ssl
import numpy as np
import pandas as pd
from numpy import load
ssl._create_default_https_context = ssl._create_unverified_context
from sdgym.constants import CATEGORICAL, ORDINAL
bucket_name = ''
#BASE_URL = 'http://sdgym.s3.amazonaws.com/datasets/'
BASE_URL = 'https://'+ bucket_name+ '.s3.amazonaws.com/'
#DATA_PATH = os.path.join(os.path.dirname(file), 'data')
DATA_PATH = os.path.join(os.getcwd(), 'data')

def _load_json(path):
    with open(path) as json_file:
        return json.load(json_file)


def _load_file(filename, loader):
    local_path = os.path.join(DATA_PATH, filename)
    if not os.path.exists(local_path):
        os.makedirs(DATA_PATH, exist_ok=True)
        
        #urllib.request.urlretrieve(local_path)
    #print("hello")
    if(loader == np.load):
        return local_path
    else:
        urllib.request.urlretrieve(BASE_URL + filename, local_path)
        
        return loader(os.getcwd() + '/data/'+filename)


    if(loader == pd.read_csv):
        return local_path
    else:
        urllib.request.urlretrieve(BASE_URL + filename, local_path)
        return loader(os.getcwd() + filename)

        


def _get_columns(metadata):
    categorical_columns = list()
    ordinal_columns = list()
    for column_idx, column in enumerate(metadata['columns']):
        if column['type'] == CATEGORICAL:
            categorical_columns.append(column_idx)
        elif column['type'] == ORDINAL:
            ordinal_columns.append(column_idx)

    return categorical_columns, ordinal_columns


def trainFunc(filename):
    data = load(filename,allow_pickle=True)
    #for a in data.files:
    #    print(a)
    #    print(data[a])
    data1 = data['train']
    #print("WORKINGGGGGG TRAIN")
    return data1

def testFunc(filename):
    data = load(filename,allow_pickle=True)
    data2 = data['test']
    #print("WORKINGGGGGG TEST")
    return data2


DEFAULT_DATASETS = [
   #"adult",
   # "alarm",
   # "asia",
   # "census",
   # "child",
   # "covtype",
   # "credit",
   # "grid",
   # "gridr",
   # "insurance",
   # "intrusion",
   # "mnist12",
   # "mnist28",
   # "news",
   # "ring"
]
def load_dataset(name, benchmark=False):
    
    if name in DEFAULT_DATASETS:
        
        data = _load_file(name + '.npz', np.load)
        print('Loop 1')
    else:

        data = _load_file(name + '.csv', pd.read_csv)
        data = data.drop(data.columns[0],axis=1)
        print('#########################')
        data =data.astype(str).astype(float)
        msk = np.random.rand(len(data)) < 0.8
        train = data[msk]
        test = data[~msk]

        outfile = os.path.join(os.getcwd()) + '/data/' + name + '.npz'
        outfile1 = name + '.csv'
        np.savez(outfile, test = test.values, train = train.values)
        print('#########################')
        data = _load_file(outfile, np.load)
        #data = load_dataset(outfile)
        print('FOUND DATA')
    print(data)
    meta = _load_file(name + '.json', _load_json)
    print('#########################------------METAAAaaaaaaaa')
    categorical_columns, ordinal_columns = _get_columns(meta)
    print('#########################------------CATTT')


 
    train = trainFunc(data)
    test = testFunc(data)
 
    if benchmark:
        return train, test, meta, categorical_columns, ordinal_columns

    return train, categorical_columns, ordinal_columns