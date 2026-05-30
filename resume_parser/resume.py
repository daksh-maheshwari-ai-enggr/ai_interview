from langchain_community.document_loaders import PyPDFLoader

def load_pdf(path: str):

    loader = PyPDFLoader(path)

    docs = loader.load()

    text = ""

    for doc in docs:
        text += doc.page_content + "\n"

    return text

import re

def clean_resume(text: str):

    text = re.sub(r"\n+", "\n", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


