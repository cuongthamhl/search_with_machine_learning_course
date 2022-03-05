import argparse
import os
import random
import xml.etree.ElementTree as ET
from pathlib import Path
from nltk.stem import SnowballStemmer
from nltk.tokenize import RegexpTokenizer
from IPython.display import display
import pandas as pd  

stemmer = SnowballStemmer("english")
reg_tokenizer = RegexpTokenizer(r'\w+')

replace_dict = {
    'at&t': 'at_t'
}

def replace_by_dict(i: str) -> str:
    o = i.lower()
    for k,v in replace_dict.items():         
        o = o.replace(k, v)
    return o

def transform_name(product_name):    
    product_name_pre = replace_by_dict(product_name)       
    tokens = reg_tokenizer.tokenize(product_name_pre)
    stemmed_tokens = [stemmer.stem(token) for token in tokens]  
    text = ' '.join(stemmed_tokens)
    
    return text

def display_rows(data, rows):
    original_num_rows = pd.get_option('display.max_rows')        
    pd.set_option('display.max_rows', rows)
    display(data)
    pd.set_option('display.max_rows', original_num_rows)    