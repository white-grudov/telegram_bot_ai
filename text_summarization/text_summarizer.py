import spacy
import re
import heapq

from transformers import pipeline
from nltk.tokenize import sent_tokenize, word_tokenize

class TextSummarizer:
    def __init__(self):
        self.__summarizer = pipeline(
                "summarization",
                model="sshleifer/distilbart-cnn-12-6",
                revision="a4f8f3e"
            )
        self.__nlp = spacy.load('en_core_web_sm')

    async def __extractive_summary(self, text):
        summary = self.__summarizer(text, max_length=150, min_length=50, do_sample=False)
        summary_sentences = re.findall(r'([^.]*\.)', summary[0]['summary_text'])[:2]
        final_summary = ' '.join(summary_sentences).replace(" .", ".").replace(". ", ".")

        return final_summary

    async def __abstractive_summary(self, text):
        doc = self.__nlp(text)

        keywords = []
        for token in doc:
            if not token.is_stop and not token.is_punct and token.pos_ != 'PRON':
                keywords.append(token.lemma_)
        
        freq_table = {}
        for word in keywords:
            if word in freq_table:
                freq_table[word] += 1
            else:
                freq_table[word] = 1

        max_freq = max(freq_table.values())
        for word in freq_table.keys():
            freq_table[word] = freq_table[word] / max_freq

        sent_list = sent_tokenize(text)
        sent_scores = {}
        for sent in sent_list:
            for word in word_tokenize(sent.lower()):
                if word in freq_table.keys():
                    if sent in sent_scores:
                        sent_scores[sent] += freq_table[word]
                    else:
                        sent_scores[sent] = freq_table[word]

        summary_sentences = heapq.nlargest(len(sent_scores) // 2, sent_scores, key=sent_scores.get)
        summary = ' '.join(summary_sentences)
        return summary

    async def summarize_text(self, text):
        result = await self.__abstractive_summary(text)
        result = await self.__extractive_summary(result)
        
        return result
