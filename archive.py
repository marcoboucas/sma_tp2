class OldAgent:
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

        if self.name == "Agent1":
            # if receives a COMMIT message
            if len(commit_messages) > 0:
                return
            # if receives an ACCEPT message
            if len(accept_messages) > 0:
                # send a commit message
                # TODO : verif that still in items list
                self.commit(accept_messages.pop())
            # otherwise : send a propose message
            else:
                chosen_item = choice(self.model.items)
                all_agents = self.get_all_agents_except_me()
                for agent in all_agents:
                    self.propose(chosen_item, agent)

        if self.name == "Agent2":
            # if receives proposition
            if len(commit_messages) > 0:
                self.commit(commit_messages.pop())
            if len(proposition_messages) > 0:
                self.accept(proposition_messages.pop())
            # if receives an COMMIT message

    def step_q8(self):
        """Q8. Selecting arguments."""

        proposition_messages = self.get_messages_from_performative(
            MessagePerformative.PROPOSE
        )

        if self.name == "Agent1":
            # if  the agent's mailbox contains an ASK_WHY message
            if self.has_unread_message_with_performative(MessagePerformative.ASK_WHY):
                ask_why_message = self.get_last_unread_message_with_performative(
                    MessagePerformative.ASK_WHY
                )
                argument = self.select_argument_from_item(ask_why_message.get_content())
                # answer an argument
                self.argue(ask_why_message, argument)
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

    def step_q9(self):
        """Q8. Selecting arguments."""

        if self.has_unread_message_with_performative(MessagePerformative.ARGUE):
            argue_message = self.get_last_unread_message_with_performative(
                MessagePerformative.ARGUE
            )
            if self.can_attack_this_argument(argue_message.get_content()):
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
