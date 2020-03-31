import streamlit as st
import pandas as pd
import numpy as np
import s3fs
import time
import json
import csv
from io import StringIO 
import boto3
import os
import sys
import tempfile
import threading
import traceback
import requests
import boto3
import numpy
import six
s3 = s3fs.S3FileSystem(anon=False, requester_pays=True)
s3 = boto3.resource('s3')
bucket_name = 'enter bucket name'
def write_to_s3(df, fname):
    bucket = bucket_name # already created on S3
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    client_obj = boto3.client('s3')
    response = client_obj.put_object(
            ACL = 'private',
            Body = csv_buffer.getvalue(),
            Bucket=bucket,
            Key='{}.csv'.format(fname)
        )




uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
file_name = st.text_input("Enter filename ")
GENERATED_CSV_URL = bucket_name + '.s3.amazonaws.com/datasets/' + file_name + '.csv'
GENERATED_RESPONSE_CSV_URL = bucket_name + '.s3.amazonaws.com/datasets/' + 'synthesized_' +file_name + '.csv'
GENERATED_RESPONSE_CSV_URL = bucket_name + '.s3.amazonaws.com/datasets/' + 'benchmarked_' +file_name + '.csv'
ordinal_dict = {}
cont_dict = {} 
categorical_dict = {} 
if uploaded_file is not None and file_name:
    data = pd.read_csv(uploaded_file,index_col=False)
    data = data.select_dtypes(exclude=['object','datetime','timedelta'])
    data = data.fillna(data.mean())
    data =data.astype(str).astype(float)
    st.write(data) 
    write_to_s3(data,file_name)   
    cat_unique_dict = {} #categorical dicitonary <====================
    col_names = {} 
    ord_hier_dict = {} 
    target = st.multiselect("Enter the target column", data.columns)
    if target:
        for col in data.columns: 
            col_names.update({col:"continuous"})
        for col in data.columns:
            if col == target[0]:
                col_names.pop(target[0])
                col_names.update({"label":"continuous"})
                data = data.rename(columns={col: "label"})
    regression = st.text_input("Enter the type of problem") #<======== 
    cat_agree = st.checkbox('Yes, I have a categorical features')
    if cat_agree:
        categorical = st.multiselect("Please select the categorical columns",list(col_names))
        cat_unique_colvalues = []
        categorical_keys = list(categorical)
        if len(categorical_keys) > 0:
            for cat_key in categorical_keys:
                col_names.update({cat_key:"categorical"})
                unique_val = data[cat_key].unique()
                for mx2 in unique_val:
                    cat_unique_colvalues.append(str(mx2))
                cat_unique_dict.update({cat_key:cat_unique_colvalues})
                

    ord_agree = st.checkbox('Yes, I have a ordinal features')
    if ord_agree:
        ordinal = st.multiselect("Please select the ordinal columns",list(col_names))
        for col_name in ordinal:
            ord_array = []
            o_key = 'ordinal_key'+col_name
            o_key = st.text_input(label="enter the heirarcy for "+col_name)
            x1m = [str(i) for i in o_key.replace(',',"")]
            ordinal_dict.update({col_name:x1m})
        

    submit = st.button("Submit",key="ord_submit")
    if submit:
        if len(ordinal_dict) > 0:
            for col_name in ordinal_dict.keys():
                ord_hier_dict.update({col_name:ordinal_dict.get(col_name)})
                col_names.update({col_name:"ordinal"})
        minmax = []
        cont_minmax_dict = {}
        for key in col_names.keys():
            if col_names.get(key) == 'continuous':
                minmax = [data[key].min(), data[key].max()]
                cont_minmax_dict.update({key:minmax})
        counter_a = 0
        counter_b = 0
        counter_c = 0

        ordinal_dict = {}
        for key1 in col_names.keys():
            if col_names.get(key1) == 'ordinal':
                counter_c = counter_c+1
                i2s = (ord_hier_dict.get(key1))
                size = len(i2s)
                name = key1
                ordinal_dict.update({counter_c:[i2s,name,size,"ordinal"]})
            
            elif col_names.get(key1) == 'categorical':
                counter_b = counter_b+1
                i2s = (cat_unique_dict.get(key1))
                size = len(i2s)
                name = key1
                categorical_dict.update({counter_b:[i2s, name, size,"categorical"]})
            else:
                counter_a = counter_a+1
                value = cont_minmax_dict.get(key1)
                min_v = value[0].tolist()
                max_v = value[1].tolist()
                name = key1
                cont_dict.update({counter_a:[max_v,min_v,name,"continuous"]})
            
            
    
        cont_column = ['max', 'min', 'name','type']
        df = pd.DataFrame.from_dict(cont_dict,orient='index',columns=cont_column)
        continuos_jsn = df.to_json(orient='records')

        categor_column = ['i2s','name','size','type']
        dfcat = pd.DataFrame.from_dict(categorical_dict,orient='index',columns=categor_column)
        categor_json = dfcat.to_json(orient='records')
        
        ordinal_column = ['i2s','name','size','type']
        dford = pd.DataFrame.from_dict(ordinal_dict,orient='index',columns=ordinal_column)
        ordinal_json = dford.to_json(orient='records')
        
        dictA = json.loads(continuos_jsn)
        dictB = json.loads(categor_json)
        dictC = json.loads(ordinal_json)
        dictD = dictA+dictB+dictC
        base_dict = {"columns":dictD,"problem_type":regression}
        filename = file_name + '.json'
        s3.Object(bucket_name,filename).put(Body=json.dumps(base_dict,indent=4))
        GENERATED_JSON_URL = bucket_name + '.s3.amazonaws.com/datasets/' + filename 

        r = requests.post('http:// enter kubernetes ip /synthesise', json = {"filename": file_name})
        print(r.status_code)
        my_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.1)
            my_bar.progress(percent_complete + 1)  
    syn_button = st.button("Get Synthesised data")
    if syn_button:
        syn_data = pd.read_csv('s3://' + bucket_name + '/synthesized_' + file_name + '.csv' )
        st.write(syn_data)

    bench_button = st.button("Get Benchmark Result")
    
    if bench_button:
        try:
            bench_data = pd.read_csv('s3://' + bucket_name  + '/benchmarked_'  + file_name + '.csv' )
            st.write(bench_data)
        except FileNotFoundError as e:
            st.write("Still Processing! Try Again After Sometime")



