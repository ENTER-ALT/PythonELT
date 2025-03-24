import os
from dotenv import load_dotenv
from logger import Logger, LogStatus, LogType
from datatypes.dataset import DataSet
from typing import List
from validators.validate_dataset import validate_dataset


class Reader:
    def __init__(self) -> None:
        load_dotenv()
        self.folder: str = os.getenv('INPUT_FOLDER') 
        if self.folder is None:
            raise ValueError('INPUT_FOLDER is not defined in .env file')
        self.logger = Logger.from_dotenv('reader.csv', LogType.FILE)
        
    def read_from_folder(self) -> List[DataSet]:
        self.logger.log('Reading input files', LogStatus.INFO, LogType.FILE)
        result: List[DataSet] = []
        try:
            for file in os.listdir(self.folder):
                if file.endswith('.xlsx'):
                    dataset: DataSet = self.read_dataset(file)
                    result.append(dataset)

        except Exception as e:
            self.logger.log(f'Error reading files: {str(e)}', LogStatus.ERROR, LogType.FILE)
            raise e
        self.logger.log('Finished reading input files', LogStatus.SUCCESS, LogType.FILE)
        return result
    
    def read_dataset(self, file: str) -> DataSet:
        self.logger.log(f'Reading {file}', LogStatus.INFO, LogType.FILE)
        dataset: DataSet = DataSet.from_excel_file(file, self.folder)
        self.logger.log(f'Read {len(dataset.data)} rows from {file}', LogStatus.SUCCESS, LogType.FILE)

        self.logger.log(f'Validating {dataset}', LogStatus.INFO, LogType.FILE)
        validate_dataset(dataset)
        self.logger.log(f'Validation successful for {dataset}', LogStatus.SUCCESS, LogType.FILE)
                    
        return dataset

if __name__ == '__main__':
    reader = Reader()
    result = reader.read_from_folder()