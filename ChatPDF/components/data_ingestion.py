import os
import sys
from ChatPDF.constants import Config
from ChatPDF.logger import logging
from ChatPDF.exception import RAGException
from typing import List, Optional

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter





class DataLoader:
    """
    Responsible for loading PDF documents and splitting them into chunks.
    """
    def __init__(self, data_path: Optional[str] = None, 
                 chunk_size: int = Config.CHUNK_SIZE,
                 chunk_overlap: int = Config.CHUNK_OVERLAP,
                 length_function=Config.LENGTH_FUNCTION):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.length_function = Config.LENGTH_FUNCTION
        self.folder_path = os.path.join(os.getcwd(),Config.DATA_PATH)
           
    
    def load_pdf(self, folder_path:str)-> List[Document]:
        '''
        Load all PDF files in a folder using PyPDFLoader.

    Args:
        folder_path (str): Path to the folder containing PDF files.

    Returns:
        List[Document]: List of all Document objects from all PDFs.
        '''
        try:
            if folder_path is None:
                folder_path = self.folder_path
                
            if not os.path.isdir(folder_path):
                logger.error("Invalid folder path: %s", folder_path)
                raise RAGException(f"Folder not found: {folder_path}", sys)
            
            docuemnts: List[Document] = []
            logging.info(f"Start data loading from folder{folder_path}")
            for filename in os.listdir(folder_path):
                if filename.endswith(".pdf"):
                    file_path = os.path.join(folder_path,filename)
                    print(file_path)
                    logging.info(f"loading data from file path {file_path}")
                    loader = PyPDFLoader(file_path)
                    docuemnts.extend(loader.load())
            logging.info(f"Data loaded from folder {folder_path}, total documents: {len(docuemnts)}")
        except Exception as e:
            raise RAGException(e,sys)
        return docuemnts
    
    def create_chunks(self, documents: List[Document]) -> List[Document]:
        """
        Split loaded documents into smaller chunks for indexing.

        Args:
            documents (List[Document]): List of loaded Document objects.

        Returns:
            List[Document]: List of chunked Document objects.
        """
        try:
            
            logging.info(f"Started the chunking of documents")
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size = self.chunk_size,
                chunk_overlap = self.chunk_overlap,
                length_function = self.length_function
            )
            
            chunks = text_splitter.split_documents(documents)
            logging.info(f"Completed the chunking of documents with total len {len(chunks)}")
            return chunks
        except Exception as e:
            raise RAGException(e,sys)
        
        
    
        
            
if __name__ == "__main__":
    loader = DataLoader()
    docs = loader.load_pdf()  # Uses default folder from Config
    chnk = loader.create_chunks(docs) #creating chunk of documents