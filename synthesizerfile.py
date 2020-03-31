import logging
import pandas as pd
from io import StringIO # python3; python2: BytesIO 
import boto3
from benchmark import benchmark
from data import load_dataset






from sdgym.synthesizers import (
    CLBNSynthesizer, CTGANSynthesizer, IdentitySynthesizer, IndependentSynthesizer,
    MedganSynthesizer, PrivBNSynthesizer, TableganSynthesizer, TVAESynthesizer, UniformSynthesizer,
    VEEGANSynthesizer)
import warnings
warnings.filterwarnings("ignore")
import requests

EPOCHS_SYNTHS = (
    #CTGANSynthesizer,
    #MedganSynthesizer,
    #TableganSynthesizer,
    #TVAESynthesizer,
    #VEEGANSynthesizer,
)


NO_INIT = (
    #CLBNSynthesizer,
    #IndependentSynthesizer,
    IdentitySynthesizer,
    UniformSynthesizer,
    #PrivBNSynthesizer,
)
bucket_name = 'enter bucketname'
def write_to_s3(df, fname ):
    bucket = bucket_name # already created on S3
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    client_obj = boto3.client('s3',
                        aws_access_key_id='enter access key id',
                        aws_secret_access_key='add secret access key')
    response = client_obj.put_object(
            ACL = 'private',
            Body = csv_buffer.getvalue(),
            Bucket=bucket,
            Key='{}.csv'.format(fname)
        )
        
    print(response)



def synthesis(name):
    
    result_epoch = {}
    for syn in EPOCHS_SYNTHS:
        print(syn)
        synthesizer = syn(epochs=1)

        print('----------------------EVALUATING EPOCH SYNTHESIZER: ', syn)

        data, categorical_columns, ordinal_columns = load_dataset(name)
        synthesizer.fit(data, categorical_columns, ordinal_columns)

        print('----------------------SYNTHESIZED DATA----------------------------------------')
        
        synthesized_data = pd.DataFrame(synthesizer.sample(100))  
        print(synthesized_data)  

        #writing synthesized data to CSV on S3 bucket
        print('-------Writing to S3 Bucket------------')
        
        write_to_s3(synthesized_data, 'synthesized_{}'.format(name))
    
       
        print('------------------------BENCHMARK RESULTS-------------------------------------') 
        benchmarked_data = pd.DataFrame(benchmark(synthesizer.fit_sample, datasets=[name], repeat=1))
        print(benchmarked_data)
        
        max_bench_score = pd.DataFrame(max(benchmarked_data.iloc[:,1]))
        print(max_bench_score)
    
        result_epoch.update({syn:max_bench_score.iloc[:,1]})

    print('----------------------------DONE RUNNING ALL EPOCH SYNTHESIZERS-----------------------------')
    
    result_noinit = {}
    for syn in NO_INIT:
        synthesizer = syn()
        print('----------------------EVALUATING NO_INIT SYNTHESIZER: ', syn)
        
        data, categorical_columns, ordinal_columns = load_dataset(name)
        synthesizer.fit(data, categorical_columns, ordinal_columns)
        print('----------------------SYNTHESIZED DATA----------------------------------------')
        
        synthesized_data = pd.DataFrame(synthesizer.sample(50))  
        print(synthesized_data)  

        #writing synthesized data to CSV on S3 bucket
        print('-----------------------Writing to S3 Bucket-----------------------------------')
        
        write_to_s3(synthesized_data,'synthesized_{}'.format(name))
       
        print('------------------------BENCHMARK RESULTS-------------------------------------') 
        benchmarked_data = pd.DataFrame(benchmark(synthesizer.fit_sample, datasets=[name], repeat=1))
        print(benchmarked_data)
        
        #print(max(benchmarked_data.iloc[:,1]))
        max_bench_score = max(benchmarked_data.iloc[:,1])
        print(max_bench_score)

        result_noinit.update({syn:max_bench_score})
        print(result_noinit)
     
    print('----------------------------DONE RUNNING ALL NO_INIT SYNTHESIZERS-----------------------------')
    final_res = {**result_epoch, **result_noinit}
    final_res= pd.DataFrame.from_dict(final_res, orient='index')

    print('FINAL RESULT : ', final_res)

    print('-----------------------Writing to S3 Bucket-----------------------------------')

    write_to_s3(final_res,'benchmarked_{}'.format(name))
    
