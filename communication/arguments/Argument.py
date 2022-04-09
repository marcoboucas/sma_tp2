#!/usr/bin/env python3

from sys import prefix
from typing import List, Union

from communication.arguments.Comparison import Comparison
from communication.arguments.CoupleValue import CoupleValue
from communication.preferences.CriterionName import CriterionName
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.Item import Item
from communication.preferences.Preferences import Preferences
from communication.preferences.Value import Value


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
        """Creates a new Argument."""
        self.decision: bool = boolean_decision
        self.item = item
        self.comparison_list: List[Comparison] = []
        self.couple_values_list: List[CoupleValue] = []

    def is_positive(self) -> bool:
        return self.decision

    def get_item(self):
        return self.item

    def __eq__(self, __o: object) -> bool:
        return (
            self.decision == __o.decision
            and self.item == __o.item
            and str(self.comparison_list) == str(__o.comparision_list)
            and str(self.couple_values_list) == str(__o.couple_values_list)
        )

    def add_premiss_comparison(
        self, best_criterion_name: CriterionName, worst_criterion_name: CriterionName
    ):
        """Adds a premiss comparison in the comparison list."""
        self.comparison_list.append(
            Comparison(best_criterion_name, worst_criterion_name)
        )

    def add_premiss_couple_values(self, criterion_name: CriterionName, value: Value):
        """Add a premiss couple values in the couple values list."""
        self.couple_values_list.append(CoupleValue(criterion_name, value))

    def list_supporting_proposals(
        self, item: Item, preferences: Preferences
    ) -> List[CoupleValue]:
        """List a list of supporting (positive) premises for a given item (in order of importance)."""
        corresponding_preferences = preferences.get_criterion_for_item(item)
        supporting_premises = []
        for pref in corresponding_preferences:
            if pref.get_value() in {Value.GOOD, Value.VERY_GOOD}:
                supporting_premises.append(
                    CoupleValue(pref.get_criterion_name(), pref.get_value())
                )

        # Sort the premises by order of preference
        order_criterion = preferences.get_criterion_name_list()
        supporting_premises = list(
            sorted(
                supporting_premises,
                key=lambda prem: order_criterion.index(prem.criterion_name),
            )
        )
        return supporting_premises

    def list_attacking_proposal(
        self, item: Item, preferences: Preferences
    ) -> List[CoupleValue]:
        """Generates a list of negative premises that can be used to attack an item"""
        corresponding_preferences = preferences.get_criterion_for_item(item)
        attacking_premises = []
        for pref in corresponding_preferences:
            if pref.get_value() in {Value.BAD, Value.VERY_BAD}:
                attacking_premises.append(
                    CoupleValue(pref.get_criterion_name(), pref.get_value())
                )

        # Sort the premises by order of preference
        order_criterion = preferences.get_criterion_name_list()
        attacking_premises = list(
            sorted(
                attacking_premises,
                key=lambda prem: order_criterion.index(prem.criterion_name),
            )
        )
        return attacking_premises

    def __str__(self) -> str:
        return f"Argument Decision: {self.decision}, Item: {self.item}, comparision_list: {'|'.join(list(map(str, self.comparison_list)))}, couple_list: {'|'.join(list(map(str, self.couple_values_list)))}"

    def is_important_for_user(self, preferences: Preferences) -> bool:
        """Is important for user. (not in"""
        # If not in the top preferences, then Not
        important_criterion_names = set(preferences.get_criterion_name_list()[:2])
        for couple_value in self.couple_values_list:
            if couple_value.criterion_name not in important_criterion_names:
                return False
        return True

    def has_criterion_not_respected(self, preferences: Preferences) -> bool:
        """Boolean function that returns
        wether or not one couple value premise does not respect the corresponding criterion
        """
        corresponding_preferences = {
            pref.get_criterion_name(): pref.get_value()
            for pref in preferences.get_criterion_for_item(self.item)
        }
        for couple_value in self.couple_values_list:
            if (
                corresponding_preferences[couple_value.criterion_name]
                > couple_value.value
            ):
                return True
        return False


if __name__ == "__main__":
    # Generate preferences
    from communication.agent.preferences_agent import PreferencesAgent
    from communication.preferences.Preferences import Preferences

    items = [Item("D", ""), Item("E", "")]
    agent = PreferencesAgent()
    agent.preference = Preferences()
    agent._generate_preferences_agent1(items)
    pref: Preferences = agent.preference

    # Tests for the different functions
    argument = Argument(True, item=items[0])
    supporting_proposals = argument.list_supporting_proposals(items[0], pref)
    assert all(x.value in {Value.GOOD, Value.VERY_GOOD} for x in supporting_proposals)
    attacking_proposals = argument.list_attacking_proposal(items[0], pref)
    assert all(x.value in {Value.BAD, Value.VERY_BAD} for x in attacking_proposals)
