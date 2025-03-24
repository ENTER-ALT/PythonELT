from validators.impl.titanic_validator import TitanicValidator
from validators.impl.iris_validator import IrisValidator
from validators.impl.chicago_validator import CrimeValidator
from validators.impl.wine_validator import WineValidator
from validators.dataset_validator import DatasetValidator
from datatypes.dataset import DataSet
from typing import List
from validators.impl.processed_titanic_validator import ProcessedTitanicValidator
from validators.impl.processed_iris_validator import ProcessedIrisValidator
from validators.impl.processed_chicago_validator import ProcessedCrimeValidator
from validators.impl.processed_wine_validator import ProcessedWineValidator
from datatypes.dataset_type import DataSetType
from logger import Logger, LogStatus, LogType
from error import ErrorSeverity, Error


errorSeverity_logStatus_mapping = {
    ErrorSeverity.SEVERE: LogStatus.ERROR,
    ErrorSeverity.SAFE: LogStatus.WARNING,
}

datasetType_validator_mapping = {
    DataSetType.TITANIC: TitanicValidator(),
    DataSetType.IRIS: IrisValidator(),
    DataSetType.CHICAGO: CrimeValidator(),
    DataSetType.WINE: WineValidator()
}

processed_datasetType_validator_mapping = {
    DataSetType.TITANIC: ProcessedTitanicValidator(),
    DataSetType.IRIS: ProcessedIrisValidator(),
    DataSetType.CHICAGO: ProcessedCrimeValidator(),
    DataSetType.WINE: ProcessedWineValidator()
}

def validate_dataset(dataset: DataSet) -> bool:
    validator: DatasetValidator = datasetType_validator_mapping.get(dataset.dataset_type)
    if validator is None:
        raise ValueError(f'No validator found for dataset type: {dataset.dataset_type}')
    errors: List[Error] = validator.validate(dataset)
    log_errors(errors, validator.logger)
    for error in errors:
        if error.severity == ErrorSeverity.SEVERE:
            return False
    return True

def validate_processed_dataset(dataset: DataSet) -> bool:
    validator: DatasetValidator = processed_datasetType_validator_mapping.get(dataset.dataset_type)
    if validator is None:
        raise ValueError(f'No validator found for dataset type: {dataset.dataset_type}')
    errors: List[Error] = validator.validate(dataset)
    log_errors(errors, validator.logger)
    for error in errors:
        if error.severity == ErrorSeverity.SEVERE:
            return False
    return True

def log_errors(errors: List[Error], logger: Logger) -> None:
    for error in errors:
        log_status = errorSeverity_logStatus_mapping[error.severity]
        logger.log(str(error), log_status=log_status, log_type=LogType.VALIDATION)