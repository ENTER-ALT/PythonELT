import os
from typing import List
from dotenv import load_dotenv
from logger import Logger, LogStatus, LogType
from reader import Reader
from datatypes.dataset import DataSet

class Writer:
    def __init__(self) -> None:
        load_dotenv()
        self.folder: str = os.getenv('OUTPUT_FOLDER') 
        if self.folder is None:
            raise ValueError('OUTPUT_FOLDER is not defined in .env file')
        self.logger = Logger.from_dotenv('writer.csv', LogType.FILE)

    def write_to_folder(self, datasets: List[DataSet]) -> None:
        self.logger.log(f'Writing data to output folder {self.folder}', LogStatus.INFO, LogType.FILE)
        try:
            for dataset in datasets:
                self.logger.log(f'Writing {dataset.name}', LogStatus.INFO, LogType.FILE)
                dataset.save_to_folder(self.folder)
                self.logger.log(f'Finished writing {dataset.name}', LogStatus.SUCCESS, LogType.FILE)
        except Exception as e:
            self.logger.log(f'Error writing files: {str(e)}', LogStatus.ERROR, LogType.FILE)
            raise e
        self.logger.log(f'Finished writing data to output folder {self.folder}', LogStatus.SUCCESS, LogType.FILE)

if __name__ == '__main__':
    reader: Reader = Reader()
    datasets: List[DataSet] = reader.read_from_folder()
    writer: Writer = Writer()
    writer.write_to_folder(datasets)