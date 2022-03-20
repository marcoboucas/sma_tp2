from typing import Optional, List
from mesa import Model
from mesa.time import RandomActivation
from random import choice
import logging

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative
from communication.preferences.Preferences import Preferences
from communication.preferences.CriterionName import CriterionName
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.Value import Value
from communication.preferences.Item import Item


class ArgumentAgent(CommunicatingAgent):
    """ArgumentAgent."""

    def __init__(self, unique_id, model, name):
        super().__init__(unique_id, model, name)
        self.preference = Preferences()

    def step(self):
        """Init."""
        self.step_q5()

    def get_all_agents_except_me(self) -> List[CommunicatingAgent]:
        """Return all agents except me."""
        return [
            agent
            for agent in self.model.schedule.agents
            if agent.unique_id != self.unique_id
        ]

    def propose(self, item: Item, receiver: CommunicatingAgent) -> None:
        """Propose item."""
        self.send_message(
            Message(
                from_agent=self.unique_id,
                to_agent=receiver.unique_id,
                message_performative=MessagePerformative.PROPOSE,
                content=item,
            )
        )

    def accept(self, message: Message):
        """Accept an agent proposition"""
        self.send_message(
            Message(
                from_agent=self.unique_id,
                to_agent=message.get_exp(),
                message_performative=MessagePerformative.ACCEPT,
                content=message.get_content(),
            )
        )

    def ask_why(self, message: Message):
        """Init."""
        self.send_message(
            Message(
                from_agent=self.unique_id,
                to_agent=message.get_exp(),
                message_performative=MessagePerformative.ASK_WHY,
                content=message.get_content(),
            )
        )

    def commit(self, received_message: Message):
        """Init."""
        self.send_message(
            Message(
                from_agent=self.unique_id,
                to_agent=received_message.get_exp(),
                message_performative=MessagePerformative.COMMIT,
                content=received_message.get_content(),
            )
        )

    def argue(self, *args, **kwargs):
        """Argue."""
        logging.warning("Argue not implemented")
        # TODO: We need to argue

    def step_q4(
        self,
    ):
        """Init."""

        if self.name == "Agent1":
            chosen_item = choice(self.model.items)
            all_agents = self.get_all_agents_except_me()
            for agent in all_agents:
                self.propose(chosen_item, agent)

        elif self.name == "Agent2":
            messages = self.get_messages_from_performative(MessagePerformative.PROPOSE)
            # Accept the first one if we have one
            if len(messages) > 0:
                self.accept(messages[-1])

    def step_q5(self):
        """Init."""
        if self.name == "Agent1":
            chosen_item = choice(self.model.items)
            all_agents = self.get_all_agents_except_me()
            for agent in all_agents:
                self.propose(chosen_item, agent)

        elif self.name == "Agent2":
            messages = self.get_messages_from_performative(MessagePerformative.PROPOSE)
            # Accept the first one if we have one
            if len(messages) > 0:
                last_msg = messages[-1]
                # check if in top 10% preferred items
                if self.preference.is_item_among_top_10_percent(
                    last_msg.get_content(), self.model.items
                ):
                    self.accept(last_msg)
                else:
                    self.ask_why(last_msg)

    def step_q6(self):
        """Step 6."""
        # Commit if received a commit message
        commit_messages = self.get_messages_from_performative(
            MessagePerformative.COMMIT
        )
        accept_messages = self.get_messages_from_performative(
            MessagePerformative.ACCEPT
        )
        proposition_messages = self.get_messages_from_performative(
            MessagePerformative.PROPOSE
        )
        # if len(commit_messages) > 0:
        #     last_msg = commit_messages[-1]
        #     self.commit(last_msg)
        #     self.remove_item_from_list(last_msg)
        # TODO: stop to commit

        if self.name == "Agent1":
            # if receives a COMMIT message
            if len(commit_messages) > 0:
                pass
            # if receives an ACCEPT message
            if len(accept_messages) > 0:
                # send a commit message
                # TODO : verif that still in items list
                self.commit(accept_messages[-1])
            # otherwise : send a propose message
            else:
                chosen_item = choice(self.model.items)
                all_agents = self.get_all_agents_except_me()
                for agent in all_agents:
                    self.propose(chosen_item, agent)

        # if agent 1 and not commited yet (?)
        # propose item
        # if accepted :
        #
        if self.name == "Agent2":
            last_msg = proposition_messages[-1]

        # if agent 2 and has item and has proposition:
        # accept
        # if commited :
        # commit

    def get_preference(self):
        return self.preference

    def generate_preferences(self):
        for item in self.model.items:
            for criterion_name in CriterionName:
                # generate random value
                self.preference.add_criterion_value(
                    CriterionValue(item, criterion_name, choice(list(Value)))
                )


class ArgumentModel(Model):
    """ArgumentModel."""

    def __init__(self) -> None:
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)

        # Define Items
        self.items = [Item("E", "Elec"), Item("D", "Diesel"), *[]]

        a1 = ArgumentAgent(0, self, "Agent1", items=self.items)
        a1.generate_preferences()
        self.schedule.add(a1)

        a2 = ArgumentAgent(1, self, "Agent2", items=self.items)
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
