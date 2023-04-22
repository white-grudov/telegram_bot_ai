import json
import joblib
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

from text_normalize import normalize

class IntentClassifier:
    def __init__(self):
        self.__nlp = spacy.load('en_core_web_sm')
        self.__pipeline = None

    def __load_data(self, dataset_filename):
        dataset = []

        with open(dataset_filename, "r") as f:
            loaded_data: dict = json.load(f)

        for k, v in loaded_data.items():
            intent_class = k
            for sentence in v:
                dataset.append((sentence, intent_class))

        return dataset

    def train_model(self, dataset_filename: str):
        data = self.__load_data(dataset_filename)

        X = [normalize(self.__nlp, text) for text, _ in data]
        y = [intent for _, intent in data]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        self.__pipeline = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', LinearSVC())
        ])

        self.__pipeline.fit(X_train, y_train)
        y_pred = self.__pipeline.predict(X_test)

        print(classification_report(y_test, y_pred))
        print(confusion_matrix(y_test, y_pred))

    def predict_intent(self, text, threshold=0.5):
        preprocessed_input = normalize(self.__nlp, text)
        predicted_intent = self.__pipeline.predict([preprocessed_input])[0]
        confidence = max(self.__pipeline.decision_function([preprocessed_input])[0])

        if confidence < threshold:
            return "unknown"
        else:
            return predicted_intent

    def save_model(self, model_filename):
        joblib.dump(self.__pipeline, model_filename)

    def load_model_from_file(self, model_filename: str):
        self.__pipeline = joblib.load(model_filename)


def test_model(model_filename):
    classifier = IntentClassifier()
    classifier.load_model_from_file(model_filename)

    while True:
        message = input('Enter: ')
        predicted_intent = classifier.predict_intent(message)
        print("Predicted intent:", predicted_intent)

def create_model(dataset_filename, model_filename):
    classifier = IntentClassifier()
    classifier.train_model(dataset_filename)
    classifier.save_model(model_filename)

def main():
    dataset_filename = './files/intent_classifier_dataset.json'
    model_filename = './files/intent_classifier.pkl'

    create_model(dataset_filename, model_filename)
    test_model(model_filename)

if __name__ == '__main__':
    main()
