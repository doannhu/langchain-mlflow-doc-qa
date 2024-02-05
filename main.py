from langchain.chains import RetrievalQAWithSourcesChain


from process_file import store_doc
from process_source import process_source
from fine_tuning_model import init
from mlflow_tracking import tracking_model

import chainlit as cl


"""Get model_params, text_splitter_params, chatmodel, text_splitter, embeddings"""
model_params, text_splitter_params, chatmodel, text_splitter, embeddings = init()


import mlflow
mlflow.set_experiment("document_qa")



"""A new chat session is created"""
@cl.on_chat_start
async def on_chat_start():
    """
    Greeting
    """
    contents = "You can now chat with your pdf"
    welcome = "welcome! Please upload a pdf or text file"
    await cl.Message(content=contents).send()

    """
    Wait for users to upload text/pdf file
    """
    files = None
    while files is None:
        files = await cl.AskFileMessage(content=welcome, accept=["text/plain", "application/pdf"], max_size_mb=100, timeout=180).send()
    file = files[0]

    """
    Process file: load, split and store
    """
    msg = cl.Message(content=f"Processing `{file.name}` !")
    await msg.send()
    doc_from_vectordb = await cl.make_async(store_doc)(file, text_splitter, embeddings)

    """Retrieve from storage and Create Rag Chain"""
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        chatmodel, chain_type="stuff", retriever=doc_from_vectordb.as_retriever(max_token_limit=4097)
    )

    msg.content = f" `{file.name}` processed. You can now ask questions!"
    await msg.update()

    """hook"""
    cl.user_session.set("chain", chain)

"""Start chatting"""
@cl.on_message
async def on_message(message: cl.Message):
    """hook"""
    chain = cl.user_session.get("chain")

    """Streaming from LLM"""
    cb = cl.LangchainCallbackHandler(stream_final_answer=True, answer_prefix_tokens=["FINAL", "ANSWER"])
    cb.answer_reached = True

    """Respond to the user's message"""
    response = await chain.acall(message.content, callbacks=[cb])
    answer = response["answer"]
    src = response["sources"].strip()
    

    """hook"""
    docs = cl.user_session.get("docs")
    metadatas = [doc.metadata for doc in docs]
    all_sources = [m["source"] for m in metadatas]

    """When query exists in uploaded doc"""
    if src:

        answer, src_elements = process_source(answer, src, all_sources, docs)

        if cb.has_streamed_final_answer:
            cb.final_stream.elements = src_elements
            await cb.final_stream.update()
        else:
            await cl.Message(content=answer, elements=src_elements).send()    

    
    """Tracking model"""
    tracking_model(question=message.content,answer=answer, model_params=model_params, text_splitter_params=text_splitter_params)