from processors.transformations.transformation import Transformation, FillNaWithMean, FillNaWithValue, RoundColumn, DropDuplicates
import pandas as pd
from typing import List

class ComputeFamilySize(Transformation):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
        return df

    def __str__(self):
        return "ComputeFamilySize"

class ComputeDateOfBirth(Transformation):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df['DateOfBirth'] = 1912 - df['Age']
        return df

    def __str__(self):
        return "ComputeDateOfBirth"

class ComputeIsMainBooker(Transformation):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df['IsMainBooker'] = df['Cabin'] != 'Unknown'
        return df

    def __str__(self):
        return "ComputeIsMainBooker"

class ExtractNameComponents(Transformation):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        pattern = r'(?P<Last_Name>[^,]+), (?P<Title>\S+)\s(?P<First_Name>.+)'
        df[['Last_Name', 'Title', 'First_Name']] = df['Name'].str.extract(pattern)
        return df

    def __str__(self):
        return "ExtractNameComponents"

class ComputeSurvivalProbabilityIndex(Transformation):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        pclass_weights = {1: 0.5, 2: 0.2, 3: -0.5}
        gender_weights = {'male': -0.5, 'female': 0.5}
        df['SurvivalProbabilityIndex'] = (
            df['Pclass'].map(pclass_weights) +
            df['Age'] * -0.02 +
            df['SibSp'] * -0.1 +
            df['Parch'] * -0.1 +
            df['Fare'] * 0.01 +
            df['Sex'].map(gender_weights)
        )
        return df

    def __str__(self):
        return "ComputeSurvivalProbabilityIndex"

handleMissingAndDuplicates_pipeline: List[Transformation] = [
    FillNaWithMean(['Age', 'Fare']),
    RoundColumn(['Age'], 0),
    RoundColumn(['Fare'], 2),
    FillNaWithValue(['Embarked'], 'S'),
    FillNaWithValue(['Cabin', 'Name', 'Ticket'], 'Unknown'),
    FillNaWithValue(['Sex'], 'Unknown'),
    FillNaWithValue(['SibSp', 'Parch', 'Survived'], 0),
    DropDuplicates()
]

featureEngineering_pipeline: List[Transformation] = [
    ComputeFamilySize(),
    ComputeDateOfBirth(),
    ComputeIsMainBooker(),
    ExtractNameComponents(),
    ComputeSurvivalProbabilityIndex()
]


