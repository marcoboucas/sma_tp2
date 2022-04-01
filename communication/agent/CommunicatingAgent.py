#!/usr/bin/env python3

from mesa import Agent
from communication.arguments.Argument import Argument

from communication.mailbox.Mailbox import Mailbox
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative
from communication.message.MessageService import MessageService
from communication.preferences.Item import Item


class CommunicatingAgent(Agent):
    """CommunicatingAgent class.
    Class implementing communicating agent in a generalized manner.

    Not intended to be used on its own, but to inherit its methods to multiple
    other agents.

    attr:
        name: The name of the agent (str)
        mailbox: The mailbox of the agent (Mailbox)
        message_service: The message service used to send and receive message (MessageService)
    """

    def __init__(self, unique_id, model, name):
        """Create a new communicating agent."""
        super().__init__(unique_id, model)
        self.__name = name
        self.__mailbox = Mailbox()
        self.__messages_service = MessageService.get_instance()

    def step(self):
        """The step methods of the agent called by the scheduler at each time tick."""
        super().step()

    @property
    def name(self):
        """Return the name of the communicating agent."""
        return self.__name

    def receive_message(self, message):
        """Receive a message (called by the MessageService object) and store it in the mailbox."""
        self.__mailbox.receive_messages(message)

    def send_message(self, message: Message) -> None:
        """Send message through the MessageService object."""
        self.__messages_service.send_message(message)

    def get_new_messages(self):
        """Return all the unread messages."""
        return self.__mailbox.get_new_messages()

    def get_messages(self):
        """Return all the received messages."""
        return self.__mailbox.get_messages()

    def get_messages_from_performative(self, performative: MessagePerformative):
        """Return a list of messages which have the same performative."""
        return self.__mailbox.get_messages_from_performative(performative)

    def get_messages_from_exp(self, exp):
        """Return a list of messages which have the same sender."""
        return self.__mailbox.get_messages_from_exp(exp)

    def has_unread_message_with_performative(self, performative: MessagePerformative, agent_id: str = None):
        return self.__mailbox.has_unread_message_with_performative(performative, agent_id)

    def get_last_unread_message_with_performative(
        self, performative: MessagePerformative, agent_id: str = None
    ):
        return self.__mailbox.get_last_unread_message_with_performative(performative, agent_id)

    def propose(self, item: Item, receiver) -> None:
        """Propose item."""
        self.send_message(
            Message(
                from_agent=self.unique_id,
                to_agent=receiver.unique_id,
                message_performative=MessagePerformative.PROPOSE,
                content=item,
            )
        )

    def accept(self, proposer_agent_id: str, item: Item):
        """Accept an agent proposition"""
        self.send_message(
            Message(
                from_agent=self.unique_id,
                to_agent=proposer_agent_id,
                message_performative=MessagePerformative.ACCEPT,
                content=item,
            )
        )

    def ask_why(self, to_agent: str, item: Item):
        """Init."""
        self.send_message(
            Message(
                from_agent=self.unique_id,
                to_agent=to_agent,
                message_performative=MessagePerformative.ASK_WHY,
                content=item,
            )
        )

    def commit(self, to_agent: str, item: Item, reply_to_commit: bool = False):
        """Init."""
        self.send_message(
            Message(
                from_agent=self.unique_id,
                to_agent=to_agent,
                message_performative=MessagePerformative.COMMIT,
                content=(item, reply_to_commit),
            )
        )

    def argue(self, to_agent: str, argument: Argument):
        """Argue."""
        self.send_message(
            Message(
                from_agent=self.unique_id,
                to_agent=to_agent,
                message_performative=MessagePerformative.ARGUE,
                content=argument,
            )
        )
