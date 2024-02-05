from langchain_community.chat_models import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

import os

def init():

    """Select model and params"""
    model_params = {
        "temperature": 1,
        "streaming": True
    }

    load_dotenv()
    secret_key = os.getenv('OPENAI_SECRET_KEY')
    chatmodel = ChatOpenAI(openai_api_key=secret_key, temperature=model_params["temperature"], streaming=model_params["streaming"])


    """Split text into chunks"""
    text_splitter_params = {
        "chunk_size": 1000,
        "chunk_overlap": 200,
        "leng_function": len,
        "is_separator_regrex": False,
    }

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=text_splitter_params["chunk_size"],
                        chunk_overlap=text_splitter_params["chunk_overlap"],
                        length_function=text_splitter_params["leng_function"],
                        is_separator_regex=text_splitter_params["is_separator_regrex"],)


    """Select Embeddings"""
    embeddings = OpenAIEmbeddings(openai_api_key=secret_key)

    return model_params, text_splitter_params, chatmodel, text_splitter, embeddings  