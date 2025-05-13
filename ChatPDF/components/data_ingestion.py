import os
import sys
from ChatPDF.constants import Config
from ChatPDF.logger import logging
from ChatPDF.exception import RAGException
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader





class DataLoader:
    def __init__(self):
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
            docuemnts = []
            logging.info(f"Start data loading from folder{folder_path}")
            for filename in os.listdir(folder_path):
                if filename.endswith(".pdf"):
                    file_path = os.path.join(folder_path,filename)
                    print(file_path)
                    logging.info(f"loading data from file path {file_path}")
                    loader = PyPDFLoader(file_path)
                    docuemnts.extend(loader.load())
            logging.info(f"Data loaded from folder {folder_path}")
        except Exception as e:
            raise RAGException(e,sys)
        return docuemnts
    
            
if __name__ == "__main__":
    loader = DataLoader()
    docs = loader.load_pdf()  # Uses default folder from Config
    #print(f"Loaded {len(docs)} pages in total.")
