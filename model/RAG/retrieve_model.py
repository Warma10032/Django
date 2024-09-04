from model.model_base import Modelbase
from model.model_base import ModelStatus

import os
from env import get_app_root

from langchain_community.embeddings import ModelScopeEmbeddings

from langchain_core.vectorstores import VectorStoreRetriever,VST
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.faiss import FAISS

from config.config import Config

#r'C:/Users/16013/.cache/modelscope/hub/iic/nlp_corom_sentence-embedding_chinese-base'

# 检索模型
class Retrievemodel(Modelbase):
    
    _retriever: VectorStoreRetriever

    def __init__(self,*args,**krgs):
        super().__init__(*args,**krgs)

        # 此处请自行改成下载embedding模型的位置
        self._embedding_model_path = Config.get_instance().get_with_nested_params("model", "embedding", "model-name")
        self._loader = PyPDFDirectoryLoader # 先做成本地pdf加载，后续添加网页加载功能
        self._text_splitter = RecursiveCharacterTextSplitter
        #self._embedding = OpenAIEmbeddings()
        self._embedding = ModelScopeEmbeddings(model_id=self._embedding_model_path)
        self._pdf_data_path = os.path.join(get_app_root(), "data/retriever/pdf")  
        
        #self._logger: Logger = Logger("rag_retriever")

    # 建立向量库
    def build(self):
        
        # 设置模型状态为 BUILDING
        self._model_status = ModelStatus.BUILDING
        
        # 加载pdf文档
        loader = PyPDFDirectoryLoader(path=self._pdf_data_path)
        docs = loader.load()
        
        # 创建一个 RecursiveCharacterTextSplitter 对象，用于将文档分割成块，chunk_size为最大块大小，chunk_overlap块之间可以重叠的大小
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        splits = text_splitter.split_documents(docs)
        
        # 使用 FAISS 创建一个向量数据库，存储分割后的文档及其嵌入向量
        vectorstore = FAISS.from_documents(documents=splits, embedding=self._embedding)
        # 将向量存储转换为检索器，设置检索参数 k 为 6，即返回最相似的 6 个文档
        self._retriever = vectorstore.as_retriever(search_kwargs={"k": 6})
        
    @property
    def retriever(self)-> VectorStoreRetriever:
        if self._model_status == ModelStatus.FAILED :
            self.build()
            return self._retriever
        else:
            return self._retriever

INSTANCE = Retrievemodel()