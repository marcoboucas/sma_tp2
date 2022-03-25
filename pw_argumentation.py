import logging
from multiprocessing import get_context
from random import choice, shuffle
from re import M
from typing import List, Optional, Tuple

from mesa import Model
import mesa
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.agent.preferences_agent import PreferencesAgent
from communication.arguments.Argument import Argument
from communication.arguments.CoupleValue import CoupleValue
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative
from communication.message.MessageService import MessageService
from communication.preferences.CriterionName import CriterionName
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.Item import Item
from communication.preferences.Preferences import Preferences
from communication.preferences.Value import Value


class ArgumentAgent(CommunicatingAgent, PreferencesAgent):
    """ArgumentAgent."""

    def __init__(self, unique_id, model, name):
        CommunicatingAgent.__init__(self, unique_id, model, name)
        self.preference = Preferences()

    def step(self):
        """Init."""
        self.step_q9()

    def step_q9(self):
        """Q8. Selecting arguments."""

        proposition_messages = self.get_messages_from_performative(
            MessagePerformative.PROPOSE
        )
        if self.has_unread_message_with_performative(MessagePerformative.ARGUE):
            argue_message = self.get_last_unread_message_with_performative(
                MessagePerformative.ARGUE
            )
            if self.is_argument_attackable(argue_message.get_content()):
                # We attack !
                argument = self.select_argument_from_item(ask_why_message.get_content())
                # answer an argument
                self.argue(to_agent=argue_message.get_exp(), argument=argument)
            else:
                self.accept(
                    proposer_agent_id=argue_message.get_exp(),
                    item=argue_message.get_content().get_item(),
                )

        if self.name == "Agent1":
            # if  the agent's mailbox contains an ASK_WHY message
            if self.has_unread_message_with_performative(MessagePerformative.ASK_WHY):
                ask_why_message = self.get_last_unread_message_with_performative(
                    MessagePerformative.ASK_WHY
                )
                argument = self.select_argument_from_item(ask_why_message.get_content())
                # answer an argument
                self.argue(ask_why_message.get_exp(), argument)
            else:
                chosen_item = choice(self.model.items)
                all_agents = self.get_all_agents_except_me()
                for agent in all_agents:
                    self.propose(chosen_item, agent)

        elif self.name == "Agent2":
            # check if has an unread PROPOSE message
            if self.has_unread_message_with_performative(MessagePerformative.PROPOSE):
                # if so, retrieve this message
                last_message = self.get_last_unread_message_with_performative(
                    MessagePerformative.PROPOSE
                )
                self.ask_why(last_message)

    def is_argument_attackable(self, argument: Argument) -> bool:
        """Check if we can attack argument."""
        # Check if the criterion is not important for him
        if not argument.is_important_for_user:
            return True
        if argument.has_criterion_not_respected(self.preference):
            return True
        return False

    def get_all_agents_except_me(self) -> List[CommunicatingAgent]:
        """Return all agents except me."""
        return [
            agent
            for agent in self.model.schedule.agents
            if agent.unique_id != self.unique_id
        ]

    def select_argument_from_item(self, item: Item) -> Argument:
        """Generate the argument for an agent and an item."""
        argument = Argument(True, item)

        # Get positives premisses
        premisses = argument.list_supporting_proposals(item, self.preference)
        # sort by preference
        order_criterion = self.preference.get_criterion_name_list()
        premisses = list(
            sorted(
                premisses, key=lambda prem: order_criterion.index(prem.criterion_name)
            )
        )
        selected_premiss = premisses[0]
        argument.add_premiss_couple_values(
            criterion_name=selected_premiss.criterion_name, value=selected_premiss.value
        )
        return argument


class ArgumentModel(Model):
    """ArgumentModel."""

    def __init__(self) -> None:
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)

        # Define Items
        self.items = [Item("E", "Elec"), Item("D", "Diesel"), *[]]

        a1 = ArgumentAgent(0, self, "Agent1")
        a1.generate_preferences()
        self.schedule.add(a1)

        a2 = ArgumentAgent(1, self, "Agent2")
        a2.generate_preferences()
        self.schedule.add(a2)
        self.running = True

    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()


if __name__ == "__main__":
    argument_model = ArgumentModel()
    for _ in range(5):
        argument_model.step()
