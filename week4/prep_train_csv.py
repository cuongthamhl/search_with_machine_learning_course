import argparse
import os
import random
import xml.etree.ElementTree as ET
from pathlib import Path
from nltk.stem import SnowballStemmer
from nltk.tokenize import RegexpTokenizer
import functions
import pandas as pd
import csv
import functions


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default='/workspace/datasets/train.csv', type=str, required=False, help='CSV file to prep, default /workspace/datasets/train.csv')
    parser.add_argument("--output", default='/workspace/datasets/train_prep_week4.csv', type=str, required=False, help='Training data to generate, default /workspace/dataset/train_prep_week4.csv ')
    args = parser.parse_args()
    input = args.input
    output = args.output

    #i = 0
    df_rows = []
    df_headers = ['user', 'sku', 'category', 'query', 'query_normalized']
    with open(input) as file:
        csv_handle = csv.DictReader(file)
        for row in csv_handle:
            #print(row['sku'])
            query = functions.transform_name(row['query'])
            df_rows.append([
                row['user'],
                row['sku'],
                row['category'],
                row['query'],
                query
            ])    
            #i += 1
            #if i > 5:
            #    break

    df = pd.DataFrame(df_rows, columns = df_headers)

    df.to_csv(output)