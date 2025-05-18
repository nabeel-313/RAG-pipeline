from dotenv import find_dotenv, load_dotenv
from pinecone import Pinecone

from ChatPDF.utils.main_utils import Utilities

load_dotenv(find_dotenv(), override=True)

ex = Utilities.get_api_key("PINECODE_API_KEY")
print(ex)
# Replace with your actual API key and index name
PINECONE_API_KEY = ex
INDEX_NAME = "chatpdf"  # The index you created from the dashboard

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Get list of all available indexes
index_names = [index.name for index in pc.list_indexes()]
print("index_names :-->>",index_names)

if INDEX_NAME in index_names:
    print(f"✅ Index '{INDEX_NAME}' exists.")
    index = pc.Index(INDEX_NAME)
    print(f"🔗 Successfully connected to index '{INDEX_NAME}'")
else:
    print(f"❌ Index '{INDEX_NAME}' does NOT exist. Please check the name.")
