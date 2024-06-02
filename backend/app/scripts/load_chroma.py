import time
# import the data singleton class
from .data import Data

# import chromadb singelton class
from vectorDB.chroma_db import ChromaDB

# instantiating ChromaDB
chromadb = ChromaDB()

# instantiating Data
data = Data()

def run():
    start = time.time()
    
    # getting the data
    df = data.get_df()
    
    
    # Getting the chromadb collection
    collection = chromadb.get_collection()

    for i, row in df.iterrows():
        # Insert item to chromadb
        collection.upsert(
            ids= str(i + 1),
            documents= row['text'],
        )
        
    
    print("Chromadb Loading finished")

    end = time.time()
    print(f"Time taken for chromadb: {end-start} seconds")