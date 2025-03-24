from logger import Logger, LogType
from validators.rules.column_rule import ColumnRules
from validators.rules.rules import *
from error import ErrorSeverity
from validators.dataset_validator import DatasetValidator

notNull_safe = NotNullRule(error_severity=ErrorSeverity.SAFE)

notNull = NotNullRule()

floatType = DataTypeRule(dtype=float)
intType = DataTypeRule(dtype=int)
strType = DataTypeRule(dtype=str)

minValue_0 = MinValueRule(min_value=0)
maxValue_14 = MaxValueRule(max_value=15)  # Wine alcohol values generally range up to 15%

allowedValues_LowMediumHigh = AllowedValuesRule(allowed_values={'Low', 'Medium', 'High'})
allowedValues_DryMediumSweet = AllowedValuesRule(allowed_values={'Dry', 'Medium', 'Sweet'})

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

    # alcohol per liter,total acidity,acid ratio,normalized residual sugar,sweetness level,WQI
    ColumnRules("quality", rules=[strType, notNull, allowedValues_LowMediumHigh]),
    ColumnRules("sweetness level", rules=[strType, notNull, allowedValues_DryMediumSweet]),
    ColumnRules("total acidity", rules=[strType, notNull, allowedValues_LowMediumHigh]),
    ColumnRules("alcohol per liter", rules=[floatType, notNull, minValue_0]),
    ColumnRules("acid ratio", rules=[floatType, notNull, minValue_0]),
    ColumnRules("normalized residual sugar", rules=[floatType, notNull, minValue_0]),
    ColumnRules("WQI", rules=[floatType, notNull, minValue_0]),
]

class ProcessedWineValidator(DatasetValidator):
    def __init__(self) -> None:
        logger = Logger.from_dotenv('processed_wine_validator.csv', LogType.VALIDATION)
        super().__init__(wine_rules, logger)