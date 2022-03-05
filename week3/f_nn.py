import fasttext
import argparse
import os
import functions


model = fasttext.load_model('/workspace/search_with_machine_learning_course/week3/data/title_model.bin')
    
def predict(input: str, number_of_predictions=10):
    input_stemmed = functions.transform_name(input)
    predictions = model.get_nearest_neighbors(input_stemmed, k=number_of_predictions)
    return predictions

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-i", type=str, required=True)
    parser.add_argument("-n", type=int, default=1, help='Number of predictions')

    args = parser.parse_args()

    input = args.i
    number_of_predictions = args.n

    predictions = predict(input, number_of_predictions)

    for (score, r) in predictions:    
        print(f'{r}    ({score})')

