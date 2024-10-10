from typing import Optional

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.sql_database import SQLDatabaseLoader
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from sqlalchemy import Select

from configs.common_config import settings
from core.databases.db import engine
from core.databases.models import Restaurant
from core.enumerate import DatabaseSchema, EmbeddingModel


class ShopeeKnowledgeBase:
    def __init__(self) -> None:
        # SQL loader
        self.sql_database = SQLDatabase(
            engine=engine,
            schema=DatabaseSchema.SHOPEE.value,
        )
        # embeddings function
        self.embeddings = OpenAIEmbeddings(
            model=EmbeddingModel.EMBEDDING_ADA_V2.value
        )
        # qdrant setting
        self.collection_name = "shopee_restaurants"
        self.qdrant_url = settings.QDRANT_URL
        self.qdrant_port = settings.QDRANT_PORT
        self.qdrant_grpc_port = settings.QDRANT_GRPC_PORT
        self.qdrant_api_key = settings.QDRANT_API_KEY
        self.qdrant_client = QdrantClient(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
            port=self.qdrant_port,
            grpc_port=self.qdrant_grpc_port,
            # prefer_grpc=True,
            # https=None
        )
        self.retriever_search_kwargs = {
            "k": 5,
        }
        self._vector_db = self.init_vector_db()

    def init_vector_db(self):
        if self.qdrant_client.collection_exists(self.collection_name):
            return QdrantVectorStore.from_existing_collection(
                collection_name=self.collection_name,
                embedding=self.embeddings,
                url=self.qdrant_url,
                port=self.qdrant_port,
                api_key=self.qdrant_api_key,
                # prefer_grpc=True,
            )
        else:
            # create new collection with empty documents
            return QdrantVectorStore.from_documents(
                documents=[],
                embedding=self.embeddings,
                url=self.qdrant_url,
                port=self.qdrant_port,
                api_key=self.qdrant_api_key,
                collection_name=self.collection_name,
                # prefer_grpc=True,
            )

    def load_data(self) -> None:
        loader = SQLDatabaseLoader(
            query=Select(Restaurant.name, Restaurant.address, Restaurant.url),
            db=self.sql_database,
        )
        loaded_documents = loader.load()
        return loaded_documents
        

    def split_documents(
        self,
        loaded_docs,
        chunk_size: Optional[int] = 500,
        chunk_overlap: Optional[int] = 20,
    ):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        chunked_docs = splitter.split_documents(loaded_docs)
        return chunked_docs

    def initiate_document_injetion_pipeline(self):
        loaded_docs = self.load_data()
        chunked_docs = self.split_documents(loaded_docs)
        self._vector_db = self._vector_db.from_documents(
            documents=chunked_docs,
            embedding=self.embeddings,
            url=self.qdrant_url,
            port=self.qdrant_port,
            api_key=self.qdrant_api_key,
            collection_name=self.collection_name,
            # prefer_grpc=True,
        )
        return self._vector_db
    
    @property
    def vector_store(self):
        return self._vector_db
    
    @property
    def retriever(self):
        return self._vector_db.as_retriever(
            search_kwargs=self.retriever_search_kwargs
        )
