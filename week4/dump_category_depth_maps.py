import argparse

import sys
import os
import xml.etree.ElementTree as ET
import pandas as pd

df_data = []
df_headers = ['id', 'name', 'parent_id', 'parent_name', 'depth']
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, required=True, help="")
    args = parser.parse_args()

    max_depth = 20
    output = args.output

    # Location for category data
    categoriesFilename = '/workspace/datasets/product_data/categories/categories_0001_abcat0010000_to_pcmcat99300050000.xml'

    tree = ET.parse(categoriesFilename)
    root = tree.getroot()

    catPathStrs = set()

    i=0
    for child in root:
        catPath = child.find('path')
        catPathStr = ''
        depth = 0
        stack = []
        for cat in catPath:
            if catPathStr != '':
                catPathStr = catPathStr + ' > '
            
            id = cat.find('id').text
            name = cat.find('name').text
            catPathStr = catPathStr + name + '|' + str(id)
            
            
            depth = depth + 1
            catPathStrs.add(catPathStr)

            if len(stack) == 0:
                parent_id = None
                parent_name = None
            else:
                parent = stack[-1]
                parent_id =  parent[0]
                parent_name =  parent[1]

            df_data.append([id, name, parent_id, parent_name, depth])
            
            stack.append((id, name))
            # i += 1
            # if i > 100:
            #     break

            if max_depth > 0 and depth == max_depth:
                break

    

    #Sort for readability
    #for catPathStr in sorted(catPathStrs):
    #   print(catPathStr)

    df = pd.DataFrame(df_data, columns=df_headers).set_index('id').drop_duplicates()
    #print(df)

    print(f'Number of categories: {df.shape[0]}')
    output = '/workspace/search_with_machine_learning_course/week4/data/category_parent_maps.csv'

    print(f'Writting data to {output}...')
    df.to_csv(output)