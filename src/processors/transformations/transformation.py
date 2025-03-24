import pandas as pd
from abc import ABC, abstractmethod

class Transformation(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def transform(self, df):
        pass

    @abstractmethod
    def __str__(self):
        pass

class DropNa(Transformation):
    def __init__(self, column_names: list[str]):
        self.column_names = column_names

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        for column in self.column_names:
            df[column] = df[column].dropna()
        return df

    def __str__(self):
        return f"DropNa(columns={self.column_names})"

class FillNaWithMean(Transformation):
    def __init__(self, column_names: list[str]):
        self.column_names = column_names

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        for column in self.column_names:
            df[column] = df[column].fillna(df[column].mean())
        return df

    def __str__(self):
        return f"FillNaWithMean(columns={self.column_names})"

class FillNaWithValue(Transformation):
    def __init__(self, column_names: list[str], value):
        self.column_names = column_names
        self.value = value

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        for column in self.column_names:
            df[column] = df[column].fillna(self.value)
        return df

    def __str__(self):
        return f"FillNaWithValue(columns={self.column_names}, value={self.value})"

class RoundColumn(Transformation):
    def __init__(self, column_names: list[str], decimals: int):
        self.column_names = column_names
        self.decimals = decimals

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        for column in self.column_names:
            df[column] = df[column].round(self.decimals)
        return df

    def __str__(self):
        return f"RoundColumn(columns={self.column_names}, decimals={self.decimals})"

class DropDuplicates(Transformation):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.drop_duplicates()

    def __str__(self):
        return "DropDuplicates()"

class CastColumnType(Transformation):
    def __init__(self, column_names: list[str], dtype):
        self.column_names = column_names
        self.dtype = dtype

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        for column in self.column_names:
            df[column] = df[column].astype(self.dtype)
        return df

    def __str__(self):
        return f"CastColumnType(columns={self.column_names}, dtype={self.dtype})"

class MergeDataFrame(Transformation):
    def __init__(self, merge_df: pd.DataFrame, on_column: str):
        self.merge_df = merge_df
        self.on_column = on_column

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return pd.merge(df, self.merge_df, on=self.on_column, how='left')

    def __str__(self):
        return f"MergeDataFrame(on_column={self.on_column})"

class SplitColumn(Transformation):
    def __init__(self, column_name: str, new_columns: list[str], delimiter: str):
        self.column_name = column_name
        self.new_columns = new_columns
        self.delimiter = delimiter

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df[self.new_columns] = df[self.column_name].str.split(self.delimiter, expand=True)
        return df

    def __str__(self):
        return f"SplitColumn(column={self.column_name}, new_columns={self.new_columns}, delimiter={self.delimiter})"

class MultiplyInto(Transformation):
    def __init__(self, column1: str, column2: str, result_column: str):
        self.column1 = column1
        self.column2 = column2
        self.result_column = result_column

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df[self.result_column] = df[self.column1] * df[self.column2]
        return df

    def __str__(self):
        return f"MultiplyInto(column1={self.column1}, column2={self.column2}, result_column={self.result_column})"

class AddInto(Transformation):
    def __init__(self, column1: str, column2: str, result_column: str):
        self.column1 = column1
        self.column2 = column2
        self.result_column = result_column

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df[self.result_column] = df[self.column1] + df[self.column2]
        return df

    def __str__(self):
        return f"AddInto(column1={self.column1}, column2={self.column2}, result_column={self.result_column})"

class DivideInto(Transformation):
    def __init__(self, column1: str, column2: str, result_column: str):
        self.column1 = column1
        self.column2 = column2
        self.result_column = result_column

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df[self.result_column] = df[self.column1] / df[self.column2]
        return df

    def __str__(self):
        return f"DivideInto(column1={self.column1}, column2={self.column2}, result_column={self.result_column})"

class CutIntoCategories(Transformation):
    def __init__(self, column: str, bins: list, labels: list, result_column: str):
        self.column = column
        self.bins = bins
        self.labels = labels
        self.result_column = result_column

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df[self.result_column] = pd.cut(df[self.column], bins=self.bins, labels=self.labels)
        return df

    def __str__(self):
        return f"CutIntoCategories(column={self.column}, bins={self.bins}, labels={self.labels}, result_column={self.result_column})"