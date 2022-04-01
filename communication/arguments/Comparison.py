#!/usr/bin/env python3


from communication.preferences.CriterionName import CriterionName


class Comparison:
    """Comparison class.
    This class implements a comparison object used in argument object.

    attr:
        best_criterion_name:
        worst_criterion_name:
    """

    def __init__(self, best_criterion_name: CriterionName, worst_criterion_name: CriterionName):
        """Creates a new comparison.
        """
        self.best_criterion_name = best_criterion_name
        self.worst_criterion_name = worst_criterion_name
    
    def __str__(self) -> str:
        return f"{self.best_criterion_name} > {self.worst_criterion_name}" 
