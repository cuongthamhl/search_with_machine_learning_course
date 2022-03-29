import fasttext
import functions
import ast 

# don't do this in production, please
with open('/workspace/search_with_machine_learning_course/week4/data/cat_nodes.py') as f:
    cat_nodes = ast.literal_eval(f.read())

model = fasttext.load_model('/workspace/search_with_machine_learning_course/week4/data/query-classifier-model.bin')

def predict(input, number_of_predictions: int = 5, threshold=.5):
    input_stemmed = functions.transform_name(input)

    print(f"predition for {input} / stemmed: {input_stemmed}:")
    (predictions, scores) = model.predict(input_stemmed, k=number_of_predictions)

    i=0
    results = []
    for prediction in predictions:    
        label = prediction.split('__')[2]

        node = cat_nodes[label]
        print(f"    label: {label}, score: {scores[i]}, name: {node['name']}")

        if scores[i] >= threshold:
            results.append({'label': label, 'score': scores[i], 'name': node['name']})

        i = i+1
    
    print('Labels are chosen:')
    for r in results:
        print(f"    [X] label: {r['label']}, score: {r['score']}, name: {r['name']}")

    return results