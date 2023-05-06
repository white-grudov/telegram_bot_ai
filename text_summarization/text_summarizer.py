import spacy
import re

from transformers import pipeline

nlp = spacy.load('en_core_web_sm')

async def summarize_text(text):
    summarizer = pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6",
        revision="a4f8f3e"
    )
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    summary_sentences = re.findall(r'([^.]*\.)', summary[0]['summary_text'])[:2]
    final_summary = ' '.join(summary_sentences).replace(" .", ".")

    return final_summary
