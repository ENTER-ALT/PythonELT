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
booleanType = DataTypeRule(dtype=bool)
dateType = DataTypeRule(dtype=pd.Timestamp)
dateFormat = DateFormatRule(date_format="%Y-%m-%dT%H:%M:%S.%f")
minValue_0 = MinValueRule(min_value=0)

allowedValues_day_or_night = AllowedValuesRule(allowed_values={"day", "night"})

crime_rules = [
    ColumnRules("id", rules=[intType, notNull, unique, minValue_0]),
    ColumnRules("case_number", rules=[strType, notNull, unique]),
    ColumnRules("date", rules=[dateType, notNull, dateFormat]),
    ColumnRules("block", rules=[strType, notNull_safe]),
    ColumnRules("iucr", rules=[notNull_safe]),
    ColumnRules("primary_type", rules=[strType, notNull_safe]),
    ColumnRules("description", rules=[strType, notNull_safe]),
    ColumnRules("location_description", rules=[strType, notNull_safe]),
    ColumnRules("arrest", rules=[booleanType, notNull_safe]),
    ColumnRules("domestic", rules=[booleanType, notNull_safe]),
    ColumnRules("beat", rules=[intType, notNull_safe, minValue_0]),
    ColumnRules("district", rules=[intType, notNull_safe, minValue_0]),
    ColumnRules("ward", rules=[intType, notNull_safe, minValue_0]),
    ColumnRules("community_area", rules=[intType, notNull_safe, minValue_0]),
    ColumnRules("fbi_code", rules=[notNull_safe]),
    ColumnRules("x_coordinate", rules=[floatType, minValue_0]),
    ColumnRules("y_coordinate", rules=[floatType, minValue_0]),
    ColumnRules("year", rules=[intType, notNull_safe, minValue_0]),
    ColumnRules("updated_on", rules=[dateType, notNull, dateFormat]),
    ColumnRules("latitude", rules=[floatType]),
    ColumnRules("longitude", rules=[floatType]),
    ColumnRules("location", rules=[strType]),

    # population,"time_to_arrest,hours",severity_score,day_or_night
    ColumnRules("population", rules=[intType, notNull, minValue_0]),
    ColumnRules("time_to_arrest,hours", rules=[floatType]),
    ColumnRules("severity_score", rules=[floatType, notNull]),
    ColumnRules("day_or_night", rules=[strType, notNull, allowedValues_day_or_night]),
]

class ProcessedCrimeValidator(DatasetValidator):
    def __init__(self) -> None:
        logger = Logger.from_dotenv('processed_crime_validator.csv', LogType.VALIDATION)
        super().__init__(crime_rules, logger)
