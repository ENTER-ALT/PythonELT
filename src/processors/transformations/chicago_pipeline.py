from processors.transformations.transformation import *
import pandas as pd
from typing import List
import numpy as np
class ComputePopulation(Transformation):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df['population'] = df['ward'] * 10000 + 40000
        return df
    
    def __str__(self):
        return "ComputePopulation"

class ConvertToDatetime(Transformation):
    def __init__(self, columns: List[str]):
        self.columns = columns
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        for column in self.columns:
            df[column] = pd.to_datetime(df[column])
        return df
    
    def __str__(self):
        return f"ConvertToDatetime(columns={self.columns})"

class ComputeTimeToArrest(Transformation):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df['time_to_arrest,hours'] = np.where(
            df['arrest'], 
            (df['updated_on'] - df['date']).dt.total_seconds() / 3600, 
            np.nan
        )
        return df
    
    def __str__(self):
        return "ComputeTimeToArrest"

severity_scores: dict[str,int] = {
    'ASSAULT': 10,
    'BATTERY': 10,
    'ROBBERY': 10,
    'THEFT': 5,
    'BURGLARY': 5,
    'POSSESSION': 7,
    'TRAFFICKING': 7,
    'DECEPTIVE PRACTICE': 6,
    'CRIMINAL DAMAGE': 6,
    'ARSON': 8,
    'MOTOR VEHICLE THEFT': 6,
    'HOMICIDE': 15,  # Higher severity for the most serious crime
    'VANDALISM': 4,
    'FRAUD': 5,
}

class MapSeverityScore(Transformation):
    def __init__(self):
        self.severity_scores = severity_scores
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df['severity_score'] = df['primary_type'].map(self.severity_scores).fillna(0)
        return df
    
    def __str__(self):
        return "MapSeverityScore"

class DetermineDayOrNight(Transformation):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        def day_or_night(time):
            if time.hour >= 6 and time.hour < 18:
                return 'day'
            else:
                return 'night'
        
        df['day_or_night'] = df['date'].apply(day_or_night)
        return df
    
    def __str__(self):
        return "DetermineDayOrNight"

handleMissingAndDuplicates_pipeline: List[Transformation] = [
    DropNa(['id','case_number','date','updated_on','latitude', 'longitude','ward']),
    FillNaWithValue(['location_description','district'], 'Unknown'),
    FillNaWithValue(['arrest',], False),
    DropDuplicates()
]

featureEngineering_pipeline: List[Transformation] = [
    ComputePopulation(),
    ConvertToDatetime(['date', 'updated_on']),
    ComputeTimeToArrest(),
    MapSeverityScore(),
    DetermineDayOrNight()
]


