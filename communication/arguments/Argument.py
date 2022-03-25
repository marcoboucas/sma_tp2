#!/usr/bin/env python3

from typing import List, Union

from communication.arguments.Comparison import Comparison
from communication.arguments.CoupleValue import CoupleValue
from communication.preferences.CriterionName import CriterionName
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.Item import Item
from communication.preferences.Value import Value
from communication.preferences.Preferences import Preferences

class Argument:
    """Argument class.
    This class implements an argument used in the negotiation.

    attr:
        decision:
        item:
        comparison_list:
        couple_values_list:
    """

    def __init__(self, boolean_decision: bool, item: Item):
        """Creates a new Argument.
        """
        self.__decision: bool = boolean_decision
        self.__item = item
        self.__comparison_list: List[Comparison] = []
        self.__couple_values_list: List[CoupleValue] = []

    def get_item(self):
        return self.__item

    def add_premiss_comparison(self, criterion_name_1: CriterionName, criterion_name_2: CriterionName):
        """Adds a premiss comparison in the comparison list.
        """
        self.__comparison_list.append(Comparison(criterion_name_1, criterion_name_2))

    def add_premiss_couple_values(self, criterion_name: CriterionName, value: Value):
        """Add a premiss couple values in the couple values list.
        """
        self.__couple_values_list.append(CoupleValue(criterion_name, value))

    def list_supporting_proposals(self, item: Item, preferences: Preferences) -> List[CoupleValue]:
        """List a list of supporting (positive) premises for a given item."""
        corresponding_preferences = preferences.get_criterion_for_item(item)
        supporting_premises = []
        for pref in corresponding_preferences:
            if pref.get_value() in {Value.GOOD, Value.VERY_GOOD}:
                supporting_premises.append(CoupleValue(pref.get_criterion_name(), pref.get_value()))
        return supporting_premises


    def list_attacking_proposal(self, item: Item, preferences: Preferences) -> List[CoupleValue]:
        """Generates a list of negative premises that can be used to attack an item"""
        corresponding_preferences = preferences.get_criterion_for_item(item)
        supporting_premises = []
        for pref in corresponding_preferences:
            if pref.get_value() in {Value.BAD, Value.VERY_BAD}:
                supporting_premises.append(CoupleValue(pref.get_criterion_name(), pref.get_value()))
        return supporting_premises
        
    def __str__(self) -> str:
        return f"Argument Decision: {self.__decision}, Item: {self.__item}, comparision_list: {'|'.join(list(map(str, self.__comparison_list)))}, couple_list: {'|'.join(list(map(str, self.__couple_values_list)))}"
    
    def is_important_for_user(self, preferences: Preferences) -> bool:
        """Is important for user."""
        # If not in the top preferences, then Not
        important_criterion_names = set(preferences.get_criterion_name_list()[:-2])
        for couple_value in self.__couple_values_list:
            if couple_value.criterion_name not in important_criterion_names:
                return False
        return True

    def has_criterion_not_respected(self, preferences: Preferences) -> bool:
        """Boolean function that returns 
            wether or not one couple value premise does not respect the corresponding criterion
        """
        corresponding_preferences = {
            pref.get_criterion_name(): pref.get_value()
            for pref in preferences.get_criterion_for_item(self.__item)
        }
        for couple_value in self.__couple_values_list:
            if corresponding_preferences[couple_value.criterion_name] > couple_value.value:
                return True
        return False