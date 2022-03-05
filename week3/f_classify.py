import fasttext
import argparse
import os
import functions

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-i", type=str, required=True)
    parser.add_argument("-n", type=int, default=1, help='Number of predictions')

    args = parser.parse_args()

    input = args.i
    number_of_predictions = args.n

    input_stemmed = functions.transform_name(input)

    print(f'input_stemmed: {input_stemmed}')

    model = fasttext.load_model('/workspace/search_with_machine_learning_course/week3/data/model.bin')

    (predictions, scores) = model.predict(input_stemmed, k=number_of_predictions)

    i=0
    for prediction in predictions:    
        lable = prediction.split('__')[2]
        #print(f'{lable}:{scores[i]}')
        grep_output = os.popen(f'grep -iRh {lable} -A 1 /workspace/datasets/product_data/categories | tail -n 1 | sed -e \'s/<[^>]*>//g\'').read()
        print(grep_output.strip())
        i = i+1

