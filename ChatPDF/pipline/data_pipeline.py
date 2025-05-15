from ChatPDF.components.data_ingestion import DataLoader
from ChatPDF.components.data_transformation import DataTransformer

from langchain_core.documents import Document
from typing import List, Optional
from ChatPDF.logger import logging
from ChatPDF.exception import RAGException

class RAGPipeLine:
    """
    Orchestrates the Retrieval-Augmented Generation (RAG) pipeline steps.
    """
    def __init__(self):
        self.data_loader = DataLoader()
        self.data_transformer = DataTransformer()
    
    
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
    
    def start_data_chunking(self, documents: List[Document]) -> List[Document]:
        """
        Chunk loaded documents into smaller pieces.

        Args:
            documents (List[Document]): Documents to chunk.

        Returns:
            List[Document]: Chunked Document objects.
        """
        logging.info("Entered the start_data_chunking method of RAGPipeLine class")
        chunks = self.data_loader.create_chunks(documents)
        print(f"✅ Created the chunk of documents with no of chunk is  {len(chunks)}")
        return chunks
        
    def start_data_transformation(self, chunks):
        logging.info("Entered the start_data_transformation method of RAGPipeLine class")
        self.data_transformer.store_embeddings(chunks)
        logging.info("Stored embeddings successfully.")
    
    def run_pipeline(self, folder_path: Optional[str] = None) -> None:
        """
        Execute the full RAG pipeline: loading, chunking, embedding, and indexing.

        Args:
            folder_path (str, optional): Custom PDF folder path.
        """
        data_loading = self.start_data_loading()
        chunked_data = self.start_data_chunking(data_loading)
        self.start_data_transformation(chunked_data)
        logging.info("RAG pipeline completed successfully")

if __name__ == "__main__":
    pipeline = RAGPipeLine()
    docs = pipeline.start_data_loading() 
    chncks = pipeline.start_data_chunking(docs)
