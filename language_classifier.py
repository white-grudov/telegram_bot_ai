import pandas as pd
import joblib
import asyncio

from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

class LanguageClassifier:
    def __init__(self):
        self.__pipeline = None

    async def train_model(self, dataset_filename: str):
        data = pd.read_csv(dataset_filename)

        X_train, X_test, y_train, y_test = train_test_split(data['text'], data['language'], test_size=0.2, random_state=42)

        self.__pipeline = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', MultinomialNB())
        ])

        self.__pipeline.fit(X_train, y_train)
        y_pred = self.__pipeline.predict(X_test)

        print(classification_report(y_test, y_pred))
        print(confusion_matrix(y_test, y_pred))

    async def predict_language(self, text: str, threshold=0.5) -> str:
        predicted_language = self.__pipeline.predict([text])[0]
        confidence = max(self.__pipeline.predict_proba([text])[0])

        if confidence < threshold:
            return "unknown"
        else:
            return predicted_language
    
    async def save_model(self, model_filename: str):
        joblib.dump(self.__pipeline, model_filename)

    def load_model_from_file(self, model_filename: str):
        self.__pipeline = joblib.load(model_filename)

async def test_model(model_filename):
    classifier = LanguageClassifier()
    classifier.load_model_from_file(model_filename)

    while True:
        message = input('Enter: ')
        predicted_intent = classifier.predict_language(message)
        print("Predicted language:", predicted_intent)

async def create_model(dataset_filename, model_filename):
    classifier = LanguageClassifier()
    await classifier.train_model(dataset_filename)
    await classifier.save_model(model_filename)

async def main():
    dataset_filename = './files/languages.csv'
    model_filename = './files/language_classifier.pkl'

    await create_model(dataset_filename, model_filename)
    # await test_model(model_filename)

if __name__ == '__main__':
    asyncio.run(main())