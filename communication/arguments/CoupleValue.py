#!/usr/bin/env python3


from communication.preferences.CriterionName import CriterionName
from communication.preferences.CriterionValue import CriterionValue


class CoupleValue:
    """CoupleValue class.
    This class implements a couple value used in argument object.

    attr:
        criterion_name:
        value:
    """

    def __init__(self, criterion_name: CriterionName, value: CriterionValue):
        """Creates a new couple value.
        """
        self.__criterion_name = criterion_name
        self.__value = value

    @property
    def criterion_name(self):
        """Get criterion name."""
        return self.__criterion_name
    
    @property
    def value(self):
        """Get value."""
        return self.__value

    def __str__(self) -> str:
        return f"Criterion '{self.__criterion_name}' with value '{self.__value}'"

    def __repr__(self) -> str:
        return self.__str__()