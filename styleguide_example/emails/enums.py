from enum import Enum


class EmailSendingStrategy(Enum):
    LOCAL = "local"
    MAILTRAP = "mailtrap"
