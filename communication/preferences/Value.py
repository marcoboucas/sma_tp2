#!/usr/bin/env python3

from enum import Enum
from functools import total_ordering


@total_ordering
class Value(Enum):
    """Value enum class.
    Enumeration containing the possible Value.
    """

    VERY_BAD = 0
    BAD = 1
    # AVERAGE = 2
    GOOD = 3
    VERY_GOOD = 4

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def __str__(self) -> str:
        return self._name_


assert Value.VERY_BAD < Value.GOOD
