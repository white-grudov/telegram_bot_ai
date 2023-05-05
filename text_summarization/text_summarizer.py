from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

async def summarize_text(text: str, num_sentences=2) -> str:
    sentences = sent_tokenize(text)

    stop_words = set(stopwords.words('english'))
    word_tokens = [word_tokenize(sentence.lower()) for sentence in sentences]
    filtered_words = [[word for word in words if word not in stop_words] for words in word_tokens]

    vectorizer = TfidfVectorizer(use_idf=True)
    X = vectorizer.fit_transform([' '.join(words) for words in filtered_words])

    scores = np.sum(X, axis=1)
    scores = np.squeeze(np.asarray(scores))

    sorted_indices = np.argsort(scores)[::-1]

    summary = ' '.join([sentences[i] for i in sorted_indices[:num_sentences]])
    return summary