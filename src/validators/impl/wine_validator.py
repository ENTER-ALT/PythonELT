from logger import Logger, LogType
from validators.rules.column_rule import ColumnRules
from validators.rules.rules import *
from error import ErrorSeverity
from validators.dataset_validator import DatasetValidator

notNull_safe = NotNullRule(error_severity=ErrorSeverity.SAFE)

floatType = DataTypeRule(dtype=float)
intType = DataTypeRule(dtype=int)

minValue_0 = MinValueRule(min_value=0)
maxValue_14 = MaxValueRule(max_value=15)  # Wine alcohol values generally range up to 15%

allowedValues_Quality = AllowedValuesRule(allowed_values={3, 4, 5, 6, 7, 8, 9})  # Common wine quality scores

wine_rules = [
    ColumnRules("fixed acidity", rules=[floatType, notNull_safe, minValue_0]),
    ColumnRules("volatile acidity", rules=[floatType, notNull_safe, minValue_0]),
    ColumnRules("citric acid", rules=[floatType, notNull_safe, minValue_0]),
    ColumnRules("residual sugar", rules=[floatType, notNull_safe, minValue_0]),
    ColumnRules("chlorides", rules=[floatType, notNull_safe, minValue_0]),
    ColumnRules("free sulfur dioxide", rules=[floatType, notNull_safe, minValue_0]),
    ColumnRules("total sulfur dioxide", rules=[floatType, notNull_safe, minValue_0]),
    ColumnRules("density", rules=[floatType, notNull_safe, minValue_0]),
    ColumnRules("pH", rules=[floatType, notNull_safe, MinValueRule(min_value=2.5), MaxValueRule(max_value=4.5)]),
    ColumnRules("sulphates", rules=[floatType, notNull_safe, minValue_0]),
    ColumnRules("alcohol", rules=[floatType, notNull_safe, minValue_0, maxValue_14]),
    ColumnRules("quality", rules=[intType, notNull_safe, allowedValues_Quality]),
]

class WineValidator(DatasetValidator):
    def __init__(self) -> None:
        logger = Logger.from_dotenv('wine_validator.csv', LogType.VALIDATION)
        super().__init__(wine_rules, logger)