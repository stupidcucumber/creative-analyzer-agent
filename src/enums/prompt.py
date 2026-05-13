from enum import Enum


class DatabasePromptPartEnum(str, Enum):

    def __new__(cls, value, definition, example):
        # This creates the actual string member
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.definition = definition
        obj.example = example
        return obj

    def prompt(self) -> dict:
        return {
            "value": self._value_,
            "definition": self.definition,
            "example": self.example
        }
