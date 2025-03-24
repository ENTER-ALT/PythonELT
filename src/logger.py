from enum import Enum
import time
import os
from typing import List, Optional

class LogStatus(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3
    SUCCESS = 4

    def __str__(self) -> str:
        return self.name


class LogType(Enum):
    GENERAL = 0
    FILE = 1
    VALIDATION = 2
    TRANSFORMATION = 3

    def __str__(self) -> str:
        return self.name

class LogMessage:
    def __init__(self, message: str, log_status: LogStatus, log_type: LogType) -> None:
        self.message = message
        self.log_status = log_status
        self.log_type = log_type
        self.log_date = time.strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self) -> str:
        return f'{self.log_type}:{self.log_status} - {self.message}'

    def to_csv(self) -> str:
        return f'{self.log_date},{self.message},{self.log_status},{self.log_type}'

class Logger:
    def __init__(self, logs_filename: Optional[str], log_type: Optional[LogType]) -> None:
        self.logs_filename = logs_filename if logs_filename else 'logs.csv'
        self.logs: List[LogMessage] = []
        self.log_type = log_type or LogType.GENERAL
        self.init_file_headers()

    def init_file_headers(self) -> None:
        if os.path.exists(self.logs_filename) and os.path.getsize(self.logs_filename) > 0:
            return
        with open(self.logs_filename, 'w') as file:
            file.write('Date,Message,Status,Type\n')

    def log(
            self, message: str,
            log_status: LogStatus, 
            log_type: Optional[LogType] = None, 
            display_message: bool = True
            ) -> None:
        log_type = log_type or self.log_type
        log_message = LogMessage(message, log_status, log_type)
        self.logs.append(log_message)
        if display_message:
            print(log_message)
        self.save()

    def save(self) -> None:
        with open(self.logs_filename, 'a') as file:
            for log in self.logs:
                file.write(f'{log.to_csv()}\n')
        self.reset()

    def reset(self) -> None:
        self.logs = []

    @staticmethod
    def from_dotenv(filename, logtype) -> 'Logger':
        from dotenv import load_dotenv
        load_dotenv()
        logs_folder: str = os.getenv('LOG_FOLDER')
        if logs_folder is None:
            raise ValueError('LOG_FOLDER is not defined in .env file')
        filename = filename if filename else 'logs.csv'
        logs_file: str = os.path.join(logs_folder, filename)
        return Logger(logs_file, logtype)