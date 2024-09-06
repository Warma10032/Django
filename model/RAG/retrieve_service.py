# 该函数用于对外界提供retreive服务，调用的是retrieve_model 中的接口
from typing import List
from model.RAG.retrieve_model import INSTANCE
from langchain_core.documents import Document

def retrieve(query:str) ->List[Document]:
    doc_user = INSTANCE.get_user_retriever().invoke(query)
    doc_local = INSTANCE.retriever.invoke(query)
    doc_all = doc_user + doc_local
    return doc_all