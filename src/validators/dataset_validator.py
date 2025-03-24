from error import Error
from datatypes.dataset import DataSet
from validators.rules.column_rule import ColumnRules
from typing import List
from logger import Logger

class DatasetValidator:
    def __init__(self, rules: List[ColumnRules], logger: Logger) -> None:
        self.rules = rules
        self.logger = logger

    def validate(self, dataset: DataSet) -> List[Error]:
        dataframe = dataset.data
        errors: List[Error] = []
        for rule in self.rules:
            rule_errors = rule.validate(dataframe)
            errors.extend(rule_errors)
        return errors