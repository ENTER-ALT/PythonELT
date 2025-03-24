import pandas as pd
import os
from datatypes.dataset_type import DataSetType

class DataSet:
    def __init__(self, data: pd.DataFrame, dataset_type: DataSetType, name: str) -> None:
        self.data: pd.DataFrame = data
        self.dataset_type: DataSetType = dataset_type
        self.name: str = name

    @staticmethod
    def from_excel_file(file: str, folder: str) -> 'DataSet':
        filename = os.path.join(folder, file)
        data = pd.read_excel(filename)
        dataset_type = DataSetType.get_from_filename(file)
        name = f'{file}-{dataset_type.name}'

        if dataset_type == DataSetType.IRIS:
            data.columns = ["Sepal Length", "Sepal Width", "Petal Length", "Petal Width", "Species"]

        return DataSet(data, dataset_type, name)
    
    def save_to_folder(self, folder: str) -> None:
        filename = os.path.join(folder, f'{self.name}.csv')
        self.data.to_csv(filename, index=False)

    def __str__(self) -> str: 
        return f'{self.name}'