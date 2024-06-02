# threading for thread safety in singleton pattern
from threading import Lock

# os for env variables
import os

# chromadb imports
from app.settings import CHROMA_CLIENT
from chromadb.utils import embedding_functions

# Meta Class
class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()
    
    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

# A singleton class for ChromaDB to make sure there is one instance of the class
class ChromaDB(metaclass=SingletonMeta):
    # Private variables
    __collections= {}
    
    # Private constants
    __CHROMA_CLIENT= None
    
    # Constructor
    def __init__(self) -> None:
        self.__CHROMA_CLIENT = CHROMA_CLIENT
        self.__create_collections()
    
    # Public Functions
    # Getting the client (Need on instance of it)
    def get_client(self):
        return self.__CHROMA_CLIENT
    
    # Getting the items collection
    def get_collection(self):
        return self.__collections["docs"]
    
    
    # Private Functions
    # Creating the collections
    def __create_collections(self) -> None:
        self.__create_collection()
    
    # Creating the collection
    def __create_collection(self):
        embedding_function= self.__get_embedding_function()
        collection = self.__CHROMA_CLIENT.get_or_create_collection(
            name="collection",
            embedding_function= embedding_function,
        )
        self.__collections["docs"] = collection
    
    
    # Getting the embedding function
    def __get_embedding_function(self):
        model= "sentence-transformers/all-MiniLM-L6-v2"
        # embedding= self.__get_embedding_service(model)
        embedding= embedding_functions.DefaultEmbeddingFunction()
        return embedding


    # Getting other services embedding function
    def __get_embedding_service(self, model_name):
        
        embedding= embedding_functions.HuggingFaceEmbeddingFunction(
            api_key="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",
            model_name=model_name
        )

        return embedding