from processors.transformations.transformation import * 
import pandas as pd
from typing import List 

class ComputeArea(Transformation):
    def __init__(self, new_column: str, col1: str, col2: str):
        self.new_column = new_column
        self.col1 = col1
        self.col2 = col2

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df[self.new_column] = df[self.col1] * df[self.col2]
        return df
    
    def __str__(self):
        return f"ComputeArea({self.new_column}, {self.col1}, {self.col2})"

class ComputeFlowerComplexityScore(Transformation):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df['Flower Complexity Score'] = df['Sepal Area'] / df['Petal Area']
        return df
    
    def __str__(self):
        return "ComputeFlowerComplexityScore"

handleMissingAndDuplicates_pipeline: List[Transformation] = [
    FillNaWithMean(['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width']),
    DropNa(['Species']),
    DropDuplicates()
]

species_data = pd.DataFrame({
    'Species': ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'],
    'Average_Height': [25.4, 28.0, 30.0],  
    'Color': ['Blue', 'Purple', 'Red'] 
})

featureEngineering_pipeline: List[Transformation] = [
    ComputeArea('Sepal Area', 'Sepal Length', 'Sepal Width'),
    ComputeArea('Petal Area', 'Petal Length', 'Petal Width'),
    RoundColumn(['Sepal Area', 'Petal Area'], 2),
    ComputeFlowerComplexityScore(),
    RoundColumn(['Flower Complexity Score'], 2),
    MergeDataFrame(species_data, 'Species'),
    CastColumnType(['Species'], 'category'),
    CastColumnType(['Average_Height'], float),
    CastColumnType(['Color'], 'category'),
    SplitColumn('Species', ['Genus', 'Species_Name'], '-')
]
