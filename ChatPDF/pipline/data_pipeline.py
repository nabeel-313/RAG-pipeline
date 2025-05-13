from ChatPDF.components.data_ingestion import DataLoader
from langchain_core.documents import Document
from typing import List
from ChatPDF.logger import logging
from ChatPDF.exception import RAGException

class RAGPipeLine:
    def __init__(self):
        self.data_loader = DataLoader()
    
    
    def start_data_loading(self, folder_path: str = None) -> List[Document]:
        """
        Starts the data loading step of the pipeline.

        Args:
            folder_path (str, optional): Path to PDF folder. If not provided, uses default.

        Returns:
            List[Document]: Loaded documents from PDFs.
        """
        logging.info("Entered the start_data_loading method of RAGPipeLine class")
        documents = self.data_loader.load_pdf(folder_path)
        print(f"✅ Loaded {len(documents)} pages from PDF files.")
        return documents
    
    def run_pipeline(self,) -> None:
        data_loading = self.start_data_loading()

if __name__ == "__main__":
    pipeline = RAGPipeLine()
    docs = pipeline.start_data_loading()  # Uses default path from Config
