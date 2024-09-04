from model.model_base import Modelbase
from model.model_base import ModelStatus

import os
import markdown
import unstructured
import docx
from env import get_app_root

from langchain_community.embeddings import ModelScopeEmbeddings

from langchain_core.vectorstores import VectorStoreRetriever
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, JSONLoader, MHTMLLoader, TextLoader, CSVLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader, UnstructuredHTMLLoader, UnstructuredMarkdownLoader

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
        self._data_path = os.path.join(get_app_root(), "data/retriever")
        
        #self._logger: Logger = Logger("rag_retriever")

    # 建立向量库
    def build(self):
        
        # 加载PDF文件
        pdf_loader = DirectoryLoader(self._data_path, glob="**/*.pdf", loader_cls=PyPDFLoader, silent_errors=True)
        pdf_docs = pdf_loader.load()
        
        # 加载Word文件
        docx_loader = DirectoryLoader(self._data_path, glob="**/*.docx", loader_cls=UnstructuredWordDocumentLoader, silent_errors=True)
        docx_docs = docx_loader.load()
        
        
        # 加载txt文件
        txt_loader = DirectoryLoader(self._data_path, glob="**/*.txt", loader_cls=TextLoader, silent_errors=True, loader_kwargs={'autodetect_encoding': True})
        txt_docs = txt_loader.load()
        
        # 加载csv文件
        csv_loader = DirectoryLoader(self._data_path, glob="**/*.csv", loader_cls=CSVLoader, silent_errors=True, loader_kwargs={'autodetect_encoding': True})
        csv_docs = csv_loader.load()
        
        # 加载html文件
        html_loader = DirectoryLoader(self._data_path, glob="**/*.html", loader_cls=UnstructuredHTMLLoader, silent_errors=True)
        html_docs = html_loader.load()
        
        mhtml_loader = DirectoryLoader(self._data_path, glob="**/*.mhtml", loader_cls=MHTMLLoader, silent_errors=True)
        mhtml_docs = mhtml_loader.load()
        
        # 加载markdown文件
        markdown_loader = DirectoryLoader(self._data_path, glob="**/*.md", loader_cls=UnstructuredMarkdownLoader, silent_errors=True)
        markdown_docs = markdown_loader.load()
        
        # 要利用json数据要设置jq语句和content_key提取特定字段，这在不同json数据结构中有所不同，较为繁琐。
        # 官方文档：https://api.python.langchain.com/en/latest/document_loaders/langchain_community.document_loaders.json_loader.JSONLoader.html
        # json_loader = DirectoryLoader(self._data_path, glob="**/*.json", loader_kwargs={"jq_schema": ".","text_content":False},loader_cls=JSONLoader, silent_errors=True)
        # json_docs = json_loader.load()
        
        
        #合并文档
        docs = pdf_docs + docx_docs  + txt_docs + csv_docs + html_docs + mhtml_docs + markdown_docs
        
        # 创建一个 RecursiveCharacterTextSplitter 对象，用于将文档分割成块，chunk_size为最大块大小，chunk_overlap块之间可以重叠的大小
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        splits = text_splitter.split_documents(docs)
        
        # 使用 FAISS 创建一个向量数据库，存储分割后的文档及其嵌入向量
        vectorstore = FAISS.from_documents(documents=splits, embedding=self._embedding)
        # 将向量存储转换为检索器，设置检索参数 k 为 6，即返回最相似的 6 个文档
        self._retriever = vectorstore.as_retriever(search_kwargs={"k": 6})
        
        # 设置模型状态为 BUILDING
        self._model_status = ModelStatus.BUILDING
        
    @property
    def retriever(self)-> VectorStoreRetriever:
        if self._model_status == ModelStatus.FAILED :
            self.build()
            return self._retriever
        else:
            return self._retriever

INSTANCE = Retrievemodel()