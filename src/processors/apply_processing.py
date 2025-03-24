from datatypes.dataset_type import DataSetType
from datatypes.dataset import DataSet
from processors.impl.titanic_processor import TitanicProcessor
from processors.impl.iris_processor import IrisProcessor
from processors.impl.chicago_processor import ChicagoProcessor
from processors.impl.wine_processor import WineProcessor
from processors.dataset_processor import DataSetProcessor

datasetType_processor_mapping = {
    DataSetType.TITANIC: TitanicProcessor(),
    DataSetType.IRIS: IrisProcessor(),
    DataSetType.CHICAGO: ChicagoProcessor(),
    DataSetType.WINE: WineProcessor()
}

def apply_processing(dataset: DataSet, verbose: bool = False) -> DataSet:
    processor: DataSetProcessor = datasetType_processor_mapping.get(dataset.dataset_type)
    if processor is None:
        raise ValueError(f'No processor found for dataset type: {dataset.dataset_type}')
    return processor.transform(dataset, verbose=verbose)