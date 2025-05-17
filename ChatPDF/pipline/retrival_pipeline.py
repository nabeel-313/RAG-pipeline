from typing import List
import sys
from pinecone import Pinecone
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_pinecone import PineconeVectorStore
from ChatPDF.logger import logging
from ChatPDF.exception import RAGException
from ChatPDF.constants import Config
from ChatPDF.utils.main_utils import Utilities

class RetrievalPipeline:
    def __init__(self):
        logging.info("Initializing RetrievalPipeline with history and source support...")
        
        self.embedding_model = GoogleGenerativeAIEmbeddings(
            model=Config.EMBEDDING_MODEL,
            google_api_key=Utilities.get_api_key("GOOGLE_API_KEY")
        )

        self.pinecone = Pinecone(api_key=Utilities.get_api_key("PINECODE_API_KEY"))
        self.index = self.pinecone.Index(Config.PINECONE_INDEX_NAME)

        self.vectorstore = PineconeVectorStore(
            index=self.index,
            embedding=self.embedding_model,
            text_key="text"
        )

        self.llm = Utilities.load_LLM()

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )

        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 5}),
            memory=self.memory,
            return_source_documents=True
        )

        logging.info("RetrievalPipeline ready with ConversationalRetrievalChain.")

    def chat(self, query: str) -> dict:
        """
        Query the LLM with retrieval-augmented context.
        """
        try:
            logging.info(f"User query received: {query}")
            response = self.qa_chain.invoke({"question": query})

            answer = response["answer"]
            sources = response["source_documents"]

            source_texts = [
                {
                    "source": doc.metadata.get("source", "unknown"),
                    "content": doc.page_content
                }
                for doc in sources
            ]

            return {
                "answer": answer,
                "sources": source_texts
            }

        except Exception as e:
            raise RAGException(e, sys)

if __name__ == "__main__":
    retrival = RetrievalPipeline()
    retrival.chat()
                
        