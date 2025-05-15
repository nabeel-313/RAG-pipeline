from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Pinecone as LC_Pinecone
from typing import List, Optional
from pinecone import Pinecone
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)
import sys
import uuid
from ChatPDF.logger import logging
from ChatPDF.exception import RAGException
from ChatPDF.constants import Config
from ChatPDF.utils.main_utils import Utilities

# ex = Utilities.get_api_key("OPENWEATHERMAP_API_KEY")
# print(ex)

class DataTransformer:
    """
    Responsible for transforming chunked documents into embeddings and storing them.
    """
    def __init__(self):
        logging.info("Initializing DataTransformer...")
        # Initialize embedding model
        self.embedding_model = GoogleGenerativeAIEmbeddings(
            model = Config.EMBEDDING_MODEL,
            google_api_key = Utilities.get_api_key("GOOGLE_API_KEY")
        )
        
        
         # Initialize Pinecone
        self.pc = Pinecone(api_key=Utilities.get_api_key("PINECODE_API_KEY"))
        self.index = self.pc.Index(Config.PINECONE_INDEX_NAME)
        logging.info("DataTransformer initialized successfully.")
        
    def create_embeddings(self, documents: List[Document]):
        """
        Create vector embeddings from chunked documents using Gemini model.

        Args:
            documents (List[Document]): Chunked Document objects.

        Returns:
            List[dict]: List of documents with embedded vectors.
        """
        try:
            logging.info(f"Started Creating embeddings for documents {len(documents)}")
            embeddings = self.embedding_model.embed_documents([doc.page_content for doc in documents ])
            logging.info("Embeddings created successfully.")
            return embeddings
        except Exception as e:
            raise RAGException(e,sys)
        
    
    def store_embeddings(self, documents: List[Document]):
        """
        Store documents and their embeddings into Pinecone.

        Args:
            documents (List[Document]): Chunked documents with text content.

        Returns:
            None
        """
        try:
            logging.info(f"Started Storing embeddings to Pinecone index:-->> {self.index}")
            texts = [doc.page_content for doc in documents]
            embeddings = self.embedding_model.embed_documents(texts)
            
            vectors = []
            for i, (text, vector) in enumerate(zip(texts, embeddings)):
                vectors.append({
                    "id": str(uuid.uuid4()),
                    "values": vector,
                    "metadata": {
                        "text": text  # you can add more metadata like page number if needed
                    }
                })

            self.index.upsert(vectors=vectors)
            logging.info("Embeddings successfully stored in Pinecone.")
        except Exception as e:
            raise RAGException(e,sys)