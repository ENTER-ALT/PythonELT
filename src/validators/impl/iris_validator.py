from logger import Logger, LogType
from validators.rules.column_rule import ColumnRules
from validators.rules.rules import *
from error import ErrorSeverity
from validators.dataset_validator import DatasetValidator

# Define rules
notNull_safe = NotNullRule(error_severity=ErrorSeverity.SAFE)

floatType = DataTypeRule(dtype=float)
strType = DataTypeRule(dtype=str)

minValue_0 = MinValueRule(min_value=0)

allowedValues_Species = AllowedValuesRule(allowed_values={"Iris-setosa", "Iris-versicolor", "Iris-virginica"})

# Define column rules for the Iris dataset
iris_rules = [
    ColumnRules("Sepal Length", rules=[floatType, notNull_safe, minValue_0]),
    ColumnRules("Sepal Width", rules=[floatType, notNull_safe, minValue_0]),
    ColumnRules("Petal Length", rules=[floatType, notNull_safe, minValue_0]),
    ColumnRules("Petal Width", rules=[floatType, notNull_safe, minValue_0]),
    ColumnRules("Species", rules=[strType, notNull_safe, allowedValues_Species]),
]

class IrisValidator(DatasetValidator):
    def __init__(self) -> None:
        logger = Logger.from_dotenv('iris_validator.csv', LogType.VALIDATION)
        super().__init__(iris_rules, logger)

    def validate(self, dataset):
        return super().validate(dataset)
