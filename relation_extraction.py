from allennlp.predictors.predictor import Predictor
predictor = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/srl-model-2018.05.25.tar.gz")
from datetime import datetime

def relExtra(Passage):
    t0 = datetime.now()
    a = predictor.predict(
        sentence="Jack and John are good friends."
    )
    t1 = datetime.now()
    #print(a)
    #print((t1 - t0))
    b = predictor.predict(
        sentence="Jack and John are good friends."
    )
    dummy_data = {

        'nodes': [
            {'name': "Adam"},
            {'name': "Bob"},
            {'name': "Carrie"},
            {'name': "Donovan"},
            {'name': "Edward"},
            {'name': "Felicity"},
            {'name': "George"},
            {'name': "Hannah"},
            {'name': "Iris"},
            {'name': "Jerry"}
        ],
        'edges': [
            {'source': 0, 'target': 1, 'label': "friend"},
            {'source': 0, 'target': 2, 'label': "student"},
            {'source': 0, 'target': 3, 'label': "lover"},
            {'source': 0, 'target': 4, 'label': "old friend"},
            {'source': 1, 'target': 5, 'label': "killed by"},
            {'source': 2, 'target': 5, 'label': "classmates"},
            {'source': 3, 'target': 4, 'label': "teacher"},
            {'source': 5, 'target': 8, 'label': "teacher"},
            {'source': 5, 'target': 9, 'label': "teacher"},
            {'source': 6, 'target': 7, 'label': "teacher"},
            {'source': 7, 'target': 8, 'label': "teacher"},
            {'source': 8, 'target': 9, 'label': "teacher"}
        ]
    }
    print(Passage)
    return dummy_data