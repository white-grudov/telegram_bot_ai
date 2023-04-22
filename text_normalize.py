from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def normalize(nlp, text):
    doc = nlp(text.lower())

    tokens = [token.text for token in doc if token.is_alpha]
    normalized_tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]

    normalized_text = " ".join(normalized_tokens)
    return normalized_text