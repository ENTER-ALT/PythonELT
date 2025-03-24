from enum import Enum
import regex as re


class DataSetType(Enum):
    TITANIC = 1
    IRIS = 2
    WINE = 3
    CHICAGO = 4
    
    def get_from_filename(filename):
        patterns = {
            DataSetType.TITANIC: re.compile(r'titanic', re.IGNORECASE),
            DataSetType.IRIS: re.compile(r'iris', re.IGNORECASE),
            DataSetType.WINE: re.compile(r'wine', re.IGNORECASE),
            DataSetType.CHICAGO: re.compile(r'chicago', re.IGNORECASE)
        }
        
        for dataset_type, pattern in patterns.items():
            if pattern.search(filename):
                return dataset_type
        return None