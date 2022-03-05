import os
import argparse
from pathlib import Path
import functions

def transform_training_data(title, comment):
    # IMPLEMENT
    #return functions.transform_name(title + ' ' + comment)
    return (title + ' ' + comment).lower()
    #return title
    #return title + ' ' + comment


# Directory for review data
directory = r'/workspace/datasets/product_data/reviews/'
parser = argparse.ArgumentParser(description='Process some integers.')
general = parser.add_argument_group("general")
general.add_argument("--input", default=directory,  help="The directory containing reviews")
general.add_argument("--output", default="/workspace/search_with_machine_learning_course/week3/data/output-reviews.fasttext", help="the file to output to")
general.add_argument("--use-3-tier", action='store_true')


args = parser.parse_args()
output_file = args.output
use_3_tier = args.use_3_tier
path = Path(output_file)
output_dir = path.parent
if os.path.isdir(output_dir) == False:
        os.mkdir(output_dir)

if args.input:
    directory = args.input

print(f'use_3_tier: {use_3_tier}')
print("Writing results to %s" % output_file)
with open(output_file, 'w') as output:
    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            with open(os.path.join(directory, filename)) as xml_file:
                for line in xml_file:
                    if '<rating>'in line:
                        rating = line[12:15]
                    elif '<title>' in line:
                        title = line[11:len(line) - 9]
                    elif '<comment>' in line:
                        comment = line[13:len(line) - 11]
                    elif '</review>'in line:   
                      rating_float = float(rating)                   
                      tiered_ratings = 0
                      if rating_float >= 3.3:
                          tiered_ratings = 1
                      elif rating_float <= 2.7:
                          tiered_ratings = -1
                      
                      if use_3_tier:
                          final_rating = tiered_ratings
                      else:
                          final_rating = rating
                      #print(f'final_rating:{final_rating}, rating_float:{rating_float}')
                      output.write("__label__%s %s\n" % (final_rating, transform_training_data(title, comment)))
