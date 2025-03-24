import pandas as pd
from abc import ABC, abstractmethod
import re
from error import Error, ErrorSeverity

class Rule(ABC):
    def __init__(self, error_severity=ErrorSeverity.SEVERE):
        self.error_severity = error_severity

    @abstractmethod
    def validate(self, df, column_name):
        pass


class NotNullRule(Rule):
    def validate(self, df, column_name):
        series = df[column_name]
        if series.isnull().any():
            return [Error(f"Column '{column_name}' contains NULL values", self.error_severity)]
        return []


class UniqueRule(Rule):
    def validate(self, df, column_name):
        series = df[column_name]
        if series.duplicated().any():
            return [Error(f"Column '{column_name}' must have unique values but contains duplicates.", self.error_severity)]
        return []


class DataTypeRule(Rule):
    def __init__(self, dtype, error_severity=ErrorSeverity.SEVERE):
        super().__init__(error_severity)
        self.dtype = dtype

    def validate(self, df, column_name):
        series = df[column_name]
        if not series.map(lambda x: isinstance(x, self.dtype) or pd.isnull(x)).all():
            return [Error(f"Column '{column_name}' contains values that are not of type {self.dtype}.", self.error_severity)]
        return []


class AllowedValuesRule(Rule):
    def __init__(self, allowed_values, error_severity=ErrorSeverity.SEVERE):
        super().__init__(error_severity)
        self.allowed_values = set(allowed_values)

    def validate(self, df, column_name):
        series = df[column_name]
        if not series.dropna().isin(self.allowed_values).all():
            return [Error(f"Column '{column_name}' contains values outside allowed set {self.allowed_values}.", self.error_severity)]
        return []


class MinValueRule(Rule):
    def __init__(self, min_value, error_severity=ErrorSeverity.SEVERE):
        super().__init__(error_severity)
        self.min_value = min_value

    def validate(self, df, column_name):
        series = df[column_name]
        if (series.dropna() < self.min_value).any():
            return [Error(f"Column '{column_name}' contains values less than {self.min_value}.", self.error_severity)]
        return []


class MaxValueRule(Rule):
    def __init__(self, max_value, error_severity=ErrorSeverity.SEVERE):
        super().__init__(error_severity)
        self.max_value = max_value

    def validate(self, df, column_name):
        series = df[column_name]
        if (series.dropna() > self.max_value).any():
            return [Error(f"Column '{column_name}' contains values greater than {self.max_value}.", self.error_severity)]
        return []


class CustomValidatorRule(Rule):
    def __init__(self, custom_validator, error_severity=ErrorSeverity.SEVERE):
        super().__init__(error_severity)
        self.custom_validator = custom_validator

    def validate(self, df, column_name):
        series = df[column_name]
        invalid_values = series.dropna().apply(lambda x: not self.custom_validator(x))
        if invalid_values.any():
            return [Error(f"Column '{column_name}' contains values failing custom validation.", self.error_severity)]
        return []

class RegexRule(Rule):
    def __init__(self, pattern, error_severity=ErrorSeverity.SEVERE):
        super().__init__(error_severity)
        self.pattern = re.compile(pattern)

    def validate(self, df, column_name):
        series = df[column_name]
        invalid_values = series.dropna().reset_index().apply(lambda x: not bool(self.pattern.search(str(x))))

        if invalid_values.any():
            wrong_values = series[invalid_values].tolist()
            return [Error(f"Column '{column_name}' contains values that do not match the regex pattern {self.pattern.pattern}: {wrong_values}.", self.error_severity)]
        return []



class DateFormatRule(Rule):
    def __init__(self, date_format, error_severity=ErrorSeverity.SEVERE):
        super().__init__(error_severity)
        self.date_format = date_format

    def validate(self, df, column_name):
        series = df[column_name]
        def is_valid_date(date_str):
            try:
                pd.to_datetime(date_str, format=self.date_format)
                return True
            except ValueError:
                return False

        if not series.dropna().apply(is_valid_date).all():
            return [Error(f"Column '{column_name}' contains values that do not match the date format {self.date_format}.", self.error_severity)]
        return []
