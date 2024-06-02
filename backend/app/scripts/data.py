# threading for thread safety in singleton pattern
from threading import Lock
import pandas as pd
import numpy as np

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

# Singleton pattern is implemented to make sure the data is read once by pandas lib
class Data(metaclass=SingletonMeta):
    __df = None
    # Constructor
    def __init__(self) -> None:
        self.__set_df()
    
    # Setting up the data
    def __set_df(self) -> None:
        self.__df = pd.read_pickle("./scripts/extracted_texts.pkl")

    def get_df(self):
        return self.__df