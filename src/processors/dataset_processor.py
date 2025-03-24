from logger import Logger, LogStatus
from datatypes.dataset import DataSet
from typing import List
from processors.transformations.transformation import Transformation
from pandas import DataFrame

class DataSetProcessor:
    def __init__(self, transformations: List[Transformation], logger: Logger) -> None:
        self.pipeline: List[Transformation] = transformations
        self.logger: Logger = logger

    def transform(self, dataset: DataSet, verbose: bool = False) -> DataSet:
        dataframe: DataFrame = dataset.data.copy()
        try:
            self.logger.log(f'Starting transformation of dataset {dataset}', log_status=LogStatus.INFO)
            for tf in self.pipeline:
                self.logger.log(f'Applying transformation {tf} on dataset {dataset}', log_status=LogStatus.INFO, display_message=verbose)
                dataframe: DataFrame = tf.transform(dataframe)
                self.logger.log(f'Transformation {tf} applied on dataset {dataset}', log_status=LogStatus.SUCCESS, display_message=verbose)
            dataset.data = dataframe
            self.logger.log(f'Transformation of dataset {dataset} completed', log_status=LogStatus.SUCCESS)
            return dataset
        except Exception as e:
            self.logger.log(f'Transformation of dataset {dataset} failed with error {str(e)}',
                             log_status=LogStatus.ERROR)
            raise e