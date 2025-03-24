from processors.dataset_processor import DataSetProcessor
from logger import Logger, LogType
from processors.transformations.titanic_pipeline import handleMissingAndDuplicates_pipeline, featureEngineering_pipeline
from typing import List
from processors.transformations.transformation import Transformation

class TitanicProcessor(DataSetProcessor):
    def __init__(self):
        logger: Logger = Logger.from_dotenv('titanic_processor.csv', LogType.TRANSFORMATION)
        pipeline: List[Transformation] = handleMissingAndDuplicates_pipeline + featureEngineering_pipeline
        super().__init__(pipeline, logger)
