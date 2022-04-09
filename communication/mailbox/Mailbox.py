#!/usr/bin/env python3

from typing import List, Optional

import mesa

from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative


class Mailbox:
    """Mailbox class.
    Class implementing the mailbox object which manages messages in communicating agents.

    attr:
        unread_messages: The list of unread messages
        read_messages: The list of read messages
    """

    def __init__(self):
        """Create a new Mailbox."""
        self.__unread_messages = []
        self.__read_messages = []

    def receive_messages(self, message):
        """Receive a message and add it in the unread messages list."""
        self.__unread_messages.append(message)

    def get_new_messages(self):
        """Return all the messages from unread messages list."""
        unread_messages = self.__unread_messages.copy()
        if len(unread_messages) > 0:
            for messages in unread_messages:
                self.__read_messages.append(messages)

        self.__unread_messages.clear()
        return unread_messages

    def get_messages(self):
        """Return all the messages from both unread and read messages list."""
        if len(self.__unread_messages) > 0:
            self.get_new_messages()
        return self.__read_messages

    def get_messages_from_performative(self, performative: MessagePerformative):
        """Return a list of messages which have the same performative."""
        messages_from_performative = []
        for message in self.__unread_messages + self.__read_messages:
            if message.get_performative() == performative:
                messages_from_performative.append(message)
        return messages_from_performative

    def get_messages_from_exp(self, exp):
        """Return a list of messages which have the same sender."""
        messages_from_exp = []
        for message in self.__unread_messages + self.__read_messages:
            if message.get_exp() == exp:
                messages_from_exp.append(message)
        return messages_from_exp

    def __get_unread_messages_with_performative(
        self, performative: MessagePerformative, agent_id: str = None
    ) -> List[Message]:
        """Get the unread messages with performative."""
        messages_from_performative = []
        for message in self.__unread_messages:
            if message.get_performative() == performative:
                if agent_id is None or message.get_exp() == agent_id:
                    messages_from_performative.append(message)
        return messages_from_performative

    def has_unread_message_with_performative(
        self, performative: MessagePerformative, agent_id: str = None
    ) -> bool:
        """Check if unread messages with this performative."""
        return (
            len(self.__get_unread_messages_with_performative(performative, agent_id))
            > 0
        )

    def get_last_unread_message_with_performative(
        self, performative: MessagePerformative, agent_id: str = None
    ) -> Optional[Message]:
        """Get the last unread message with this performative."""
        for message_idx, message in enumerate(self.__unread_messages):
            if message.get_performative() == performative:
                if agent_id is None or agent_id == message.get_exp():
                    self.__read_messages.append(message)
                    return self.__unread_messages.pop(message_idx)
        return None
