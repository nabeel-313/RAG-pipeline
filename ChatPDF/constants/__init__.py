class Config:
    DATA_PATH = 'data'       #path of data
    CHUNK_SIZE = 1000      # Max tokens per chunk
    CHUNK_OVERLAP = 50      # Overlap size to retain context
    LENGTH_FUNCTION = len
    EMBEDDING_MODEL = 'models/embedding-001'
    PINECONE_INDEX_NAME = 'chatpdf'