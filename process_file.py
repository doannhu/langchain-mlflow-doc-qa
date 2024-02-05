from langchain_community.document_loaders import PyPDFLoader, TextLoader
from chainlit.types import AskFileResponse
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
from langchain_community.vectorstores import Chroma
import chainlit as cl

"""Indexing"""

"""Step 1: Load and Split"""
def process_file(file: AskFileResponse, text_splitter: RecursiveCharacterTextSplitter) -> List[Document]:
    if file.type == "text/plain":
        Loader = TextLoader
    elif file.type == "application/pdf":
        Loader = PyPDFLoader

    loader = Loader(file.path)
    documents = loader.load()

    docs = text_splitter.split_documents(documents)
    for idx, doc in enumerate(docs):
        doc.metadata["source"] = f"source_{idx}"
    return docs

"""Step 2: Store"""
"""Create a Chroma vectorstore from a list of documents"""
def store_doc(file: AskFileResponse, text_splitter: RecursiveCharacterTextSplitter, embeddings):
    uploaded_docs = process_file(file, text_splitter)

    """hook"""
    cl.user_session.set("docs", uploaded_docs)
    embbed_doc = Chroma.from_documents(uploaded_docs, embeddings)
    return embbed_doc

            
