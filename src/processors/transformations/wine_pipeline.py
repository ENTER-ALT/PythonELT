from processors.transformations.transformation import Transformation, FillNaWithMean, DropNa, MultiplyInto, AddInto, RoundColumn, DivideInto, CutIntoCategories
import pandas as pd
from typing import List

class ComputeWQI(Transformation):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df['WQI'] = (
            (df['density'] / (df['alcohol'] * 0.3)) +
            (df['pH'] / (df['fixed acidity'] * 0.2 + df['volatile acidity'] * 0.1)) +
            (df['total sulfur dioxide'] / (df['free sulfur dioxide'] * 0.2)) +
            (df['chlorides'] / (df['residual sugar'] * 0.2))
        )
        return df
    
    def __str__(self):
        return "ComputeWQI"

handleMissingAndDuplicates_pipeline: List[Transformation] = [
    FillNaWithMean([
        'fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar', 
        'chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'density', 
        'pH', 'sulphates', 'alcohol'
    ]),
    DropNa(['quality']),
]

featureEngineering_pipeline: List[Transformation] = [
    MultiplyInto('alcohol', 'density', 'alcohol per liter'),
    AddInto('fixed acidity', 'volatile acidity', 'total acidity'),
    RoundColumn(['total acidity'], 0),
    DivideInto('citric acid', 'total acidity', 'acid ratio'),
    CutIntoCategories('quality', bins=[0, 5, 7, 10], labels=['Low', 'Medium', 'High'], result_column='quality'),
    CutIntoCategories('total acidity', bins=[0, 5, 10, 17], labels=['Low', 'Medium', 'High'], result_column='total acidity'),
    DivideInto('residual sugar', 'density', 'normalized residual sugar'),
    CutIntoCategories('residual sugar', bins=[0, 4, 12, 50], labels=['Dry', 'Medium', 'Sweet'], result_column='sweetness level'),
    ComputeWQI()
]