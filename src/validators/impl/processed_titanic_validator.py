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
boolType = DataTypeRule(dtype=bool)

minValue_0 = MinValueRule(min_value=0)
maxValue_120 = MaxValueRule(max_value=120)

allowedValues_Survived = AllowedValuesRule(allowed_values={0, 1})
allowedValues_Pclass = AllowedValuesRule(allowed_values={1, 2, 3})
allowedValues_Embarked = AllowedValuesRule(allowed_values={"C", "Q", "S"})
allowedValues_Sex = AllowedValuesRule(allowed_values={"male", "female","Unknown"})

name_pattern = r'(?P<Last_Name>[^,]+), (?P<Title>\S+)\s(?P<First_Name>.+)|(Unknown)'
regex_Name = RegexRule(pattern=name_pattern)
cabin_pattern = r'([A-Za-z]\d+( \d+)*)|(Unknown)'
regex_Cabin = RegexRule(pattern=cabin_pattern)


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

    #  FamilySize,DateOfBirth,IsMainBooker,Last_Name,Title,First_Name,SurvivalProbabilityIndex
    ColumnRules("FamilySize", rules=[intType, minValue_0, notNull]),
    ColumnRules("DateOfBirth", rules=[floatType, minValue_0, notNull]),
    ColumnRules("IsMainBooker", rules=[boolType, notNull]),
    ColumnRules("Last_Name", rules=[strType]),
    ColumnRules("Title", rules=[strType]),
    ColumnRules("First_Name", rules=[strType]),
    ColumnRules("SurvivalProbabilityIndex", rules=[floatType, notNull]),
]

class ProcessedTitanicValidator(DatasetValidator):
    def __init__(self) -> None:
        logger = Logger.from_dotenv('processed_titanic_validator.csv', LogType.VALIDATION)
        super().__init__(titanic_rules, logger)
