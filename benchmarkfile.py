import os
import unittest
import synthesizerfile
from benchmark import benchmark
from sdgym.synthesizers import (
    CLBNSynthesizer, CTGANSynthesizer, IdentitySynthesizer, IndependentSynthesizer,
    MedganSynthesizer, PrivBNSynthesizer, TableganSynthesizer, TVAESynthesizer, UniformSynthesizer,
    VEEGANSynthesizer)

import warnings
warnings.filterwarnings("ignore")
import dask

'''DEFAULT_DATASETS = [
   # "adult",
    "autompg"
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
'''
def synthesise(name):
    print('------------------------EVALUATING DATASET: ', name)
    synthesizerfile.synthesis(name)
    print('------------------DONE RUNNING ALL DATASETS-----------------')


#synthesizer = syn()

#code.compute()


def run(name):  
    code = synthesise(name)
    code.compute()
#code.visualise(filename = 'graph.svg')
#for name in DEFAULT_DATASETS: