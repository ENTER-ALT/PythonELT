from logger import Logger, LogType
from validators.rules.column_rule import ColumnRules
from validators.rules.rules import *
from error import ErrorSeverity
from validators.dataset_validator import DatasetValidator

notNull_safe = NotNullRule(error_severity=ErrorSeverity.SAFE)

notNull = NotNullRule()
unique = UniqueRule()

intType = DataTypeRule(dtype=int)
floatType = DataTypeRule(dtype=float)
strType = DataTypeRule(dtype=str)

minValue_0 = MinValueRule(min_value=0)
maxValue_120 = MaxValueRule(max_value=120)

allowedValues_Survived = AllowedValuesRule(allowed_values={0, 1})
allowedValues_Pclass = AllowedValuesRule(allowed_values={1, 2, 3})
allowedValues_Embarked = AllowedValuesRule(allowed_values={"C", "Q", "S"})
allowedValues_Sex = AllowedValuesRule(allowed_values={"male", "female"})

name_pattern = r'(?P<Last_Name>[^,]+), (?P<Title>\S+)\s(?P<First_Name>.+)'
regex_Name = RegexRule(pattern=name_pattern, error_severity=ErrorSeverity.SEVERE)
cabin_pattern = r'([A-Za-z]\d+( \d+)*)'
regex_Cabin = RegexRule(pattern=cabin_pattern, error_severity=ErrorSeverity.SEVERE)


titanic_rules = [
    ColumnRules("PassengerId", rules=[intType, notNull, unique, minValue_0]),
    ColumnRules("Survived", rules=[intType, notNull_safe, allowedValues_Survived]),
    ColumnRules("Pclass", rules=[intType, notNull_safe, allowedValues_Pclass]),
    ColumnRules("Name", rules=[strType, notNull_safe, regex_Name]),
    ColumnRules("Sex", rules=[strType, notNull_safe, allowedValues_Sex]),
    ColumnRules("Age", rules=[floatType, notNull_safe, minValue_0, maxValue_120]),
    ColumnRules("SibSp", rules=[intType, minValue_0]),
    ColumnRules("Parch", rules=[intType, minValue_0]),
    ColumnRules("Ticket", rules=[notNull_safe]),
    ColumnRules("Fare", rules=[floatType, notNull_safe, minValue_0]),
    ColumnRules("Cabin", rules=[strType, notNull_safe, regex_Cabin]),
    ColumnRules("Embarked", rules=[strType, notNull_safe, allowedValues_Embarked]),
]

class TitanicValidator(DatasetValidator):
    def __init__(self) -> None:
        logger = Logger.from_dotenv('titanic_validator.csv', LogType.VALIDATION)
        super().__init__(titanic_rules, logger)
