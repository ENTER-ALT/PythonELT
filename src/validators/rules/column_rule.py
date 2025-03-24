from typing import List
import pandas as pd
from error import Error, ErrorSeverity
from validators.rules.rules import Rule

class ColumnRules:
    def __init__(self, column_name: str, rules: List[Rule]) -> None:
        self.column_name = column_name
        self.rules = rules

    def validate(self, dataframe: pd.DataFrame) -> List[Error]:
        errors: List[Error] = []
        for rule in self.rules:
            if self.column_name not in dataframe.columns:
                errors.append(Error(f"Column {self.column_name} not found in dataset", error_severity=ErrorSeverity.SEVERE))
                continue
            errors.extend(rule.validate(dataframe, self.column_name))
        return errors