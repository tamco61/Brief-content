from transformers import pipeline

SUMMARIZER = pipeline("summarization", model="Falconsai/text_summarization")


def create_sum(text):
    return SUMMARIZER(text, do_sample=False)