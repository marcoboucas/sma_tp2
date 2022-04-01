"""Preferences."""

import logging
from random import choice, shuffle
from typing import List, Optional

from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.arguments.Argument import Argument
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative
from communication.message.MessageService import MessageService
from communication.preferences.CriterionName import CriterionName
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.Item import Item
from communication.preferences.Preferences import Preferences
from communication.preferences.Value import Value

class PreferencesAgent():
    def get_preference(self):
        return self.preference

    def generate_preferences(self):
        """Generate the preferences (order and threshold) of the agent."""
        # Add the list in order of preference
        if self.name == "Agent1":
            self._generate_preferences_agent1(self.model.items)
        elif self.name == "Agent2":
            self._generate_preferences_agent2(self.model.items)
        else:
            raise ValueError(f"Problem agent name, {self.name}")

    def _generate_preferences_agent1(self, items: List[Item]):
        """Generate agent1 pref."""
        self.preference.set_criterion_name_list(
            [
                CriterionName.PRODUCTION_COST,  # C1
                CriterionName.ENVIRONMENT_IMPACT,  # C4
                CriterionName.CONSUMPTION,  # C2
                CriterionName.DURABILITY,  # C3
                CriterionName.NOISE,  # C5
            ]
        )
        iced_pref = {
            CriterionName.PRODUCTION_COST: Value.VERY_GOOD,
            CriterionName.CONSUMPTION: Value.GOOD,
            CriterionName.DURABILITY: Value.VERY_GOOD,
            CriterionName.ENVIRONMENT_IMPACT: Value.VERY_BAD,
            CriterionName.NOISE: Value.BAD,
        }
        e_pref = {
            CriterionName.PRODUCTION_COST: Value.BAD,
            CriterionName.CONSUMPTION: Value.VERY_BAD,
            CriterionName.DURABILITY: Value.AVERAGE,
            CriterionName.ENVIRONMENT_IMPACT: Value.VERY_GOOD,
            CriterionName.NOISE: Value.VERY_GOOD,
        }
        for item in items:
            if item.get_name() == "E":
                for k, v in e_pref.items():
                    self.preference.add_criterion_value(CriterionValue(item, k, v))
            elif item.get_name() == "D":
                for k, v in iced_pref.items():
                    self.preference.add_criterion_value(CriterionValue(item, k, v))
            else:
                raise ValueError(f"Name of the item incrroect {item.get_name()}")

    def _generate_preferences_agent2(self, items: List[Item]):
        """Generate agent2 pref."""
        self.preference.set_criterion_name_list(
            [
                CriterionName.ENVIRONMENT_IMPACT,  # C4
                CriterionName.NOISE,  # C5
                CriterionName.PRODUCTION_COST,  # C1
                CriterionName.CONSUMPTION,  # C2
                CriterionName.DURABILITY,  # C3
            ]
        )
        iced_pref = {
            CriterionName.PRODUCTION_COST: Value.AVERAGE,
            CriterionName.CONSUMPTION: Value.BAD,
            CriterionName.DURABILITY: Value.AVERAGE,
            CriterionName.ENVIRONMENT_IMPACT: Value.VERY_BAD,
            CriterionName.NOISE: Value.VERY_BAD,
        }
        e_pref = {
            CriterionName.PRODUCTION_COST: Value.AVERAGE,
            CriterionName.CONSUMPTION: Value.BAD,
            CriterionName.DURABILITY: Value.BAD,
            CriterionName.ENVIRONMENT_IMPACT: Value.VERY_GOOD,
            CriterionName.NOISE: Value.VERY_GOOD,
        }
        for item in items:
            if item.get_name() == "E":
                for k, v in e_pref.items():
                    self.preference.add_criterion_value(CriterionValue(item, k, v))
            elif item.get_name() == "D":
                for k, v in iced_pref.items():
                    self.preference.add_criterion_value(CriterionValue(item, k, v))
            else:
                raise ValueError(f"Name of the item incrroect {item.get_name()}")

    def __generate_random_preferences(self):
        """Generate the preferences (order and threshold) of the agent."""
        list_criterions = list(CriterionName)
        shuffle(list_criterions)
        self.preference.set_criterion_name_list(list_criterions)

        # Set the thresholds for each criterion
        for item in self.model.items:
            for criterion_name in CriterionName:
                # generate random value
                self.preference.add_criterion_value(
                    CriterionValue(item, criterion_name, choice(list(Value)))
                )