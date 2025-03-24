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

            self.validate_datasets(result)
        except Exception as e:
            self.logger.log(f'Error reading files: {str(e)}', LogStatus.ERROR, LogType.FILE)
            raise e
        self.logger.log('Finished reading input files', LogStatus.SUCCESS, LogType.FILE)
        return result
    
    def read_dataset(self, file: str) -> DataSet:
        self.logger.log(f'Reading {file}', LogStatus.INFO, LogType.FILE)
        dataset: DataSet = DataSet.from_excel_file(file, self.folder)
        self.logger.log(f'Read {len(dataset.data)} rows from {file}', LogStatus.SUCCESS, LogType.FILE)
                    
        return dataset
    
    def validate_datasets(self, datasets: List[DataSet]) -> bool:
        invalid_datasets = []
        for dataset in datasets:
            self.logger.log(f'Validating dataset {dataset}', LogStatus.INFO, LogType.VALIDATION, new_line=True)
            is_valid = validate_dataset(dataset)
            if not is_valid:
                invalid_datasets.append(dataset)
        if invalid_datasets:
            string_datasets = ', '.join([str(dataset) for dataset in invalid_datasets])
            self.logger.log(f'There are severe errors in datasets: {string_datasets}', LogStatus.ERROR, LogType.VALIDATION)
            raise ValueError(f'There are severe errors in datasets: {string_datasets}')
        self.logger.log('All datasets are valid', LogStatus.SUCCESS, LogType.VALIDATION)



if __name__ == '__main__':
    reader = Reader()
    result = reader.read_from_folder()