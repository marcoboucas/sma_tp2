"""Communicating agent."""

from ast import arg
import logging
from re import A
from typing import List, Set, Dict
from random import choice
from communication.message.MessagePerformative import MessagePerformative

from communication.preferences.Preferences import Preferences
from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.agent.preferences_agent import PreferencesAgent
from communication.arguments.Argument import Argument
from communication.preferences.Value import Value
from communication.preferences.Item import Item


class ArgumentAgent(CommunicatingAgent, PreferencesAgent):
    """ArgumentAgent."""

    def __init__(self, unique_id, model, name):
        CommunicatingAgent.__init__(self, unique_id, model, name)
        self.preference = Preferences()
        self.logger = logging.getLogger(self.name)
        self.current_discussions: Dict[str, List[Argument]] = {}
        self.previous_argument = []

    def step(self):
        """Init."""
        self.step_final()

    def step_final(self) -> None:
        """Step for the client agent."""
        # TODO: REMOVE LATER
        if self.name == "Agent1":
            item_to_send = self.preference.most_preferred(self.model.items)
            for agent in self.get_all_agents_except_me():
                if agent.unique_id not in self.current_discussions:
                    self.current_discussions[agent.unique_id] = []
                    self.propose(item_to_send, agent)
        
        # We argue while we still can
        while self.has_unread_message_with_performative(MessagePerformative.ARGUE):
            argue_message = self.get_last_unread_message_with_performative(MessagePerformative.ARGUE)
            argument: Argument = argue_message.get_content()
            self.current_discussions[argue_message.get_exp()].append(argument)
            
            new_argument = self.generate_argument(item=argument.item, argument=argument)
            if new_argument is None:
                self.accept(proposer_agent_id=argue_message.get_exp(), item=argument.item)
            else:
                self.argue(to_agent=argue_message.get_exp(), argument=new_argument)
                

        # If we receive a commit message, we check if we need to reply
        while self.has_unread_message_with_performative(MessagePerformative.COMMIT):
            commit_message = self.get_last_unread_message_with_performative(MessagePerformative.COMMIT)
            if commit_message.get_exp() in self.current_discussions:
                del self.current_discussions[commit_message.get_exp()]

            item, reply_to_commit = commit_message.get_content()
            if reply_to_commit:
                self.logger.warning("Deal done with item %s  (agent %s -> %s)", item, commit_message.get_exp(), self.unique_id)
            else:
                self.commit(to_agent=commit_message.get_exp(), item=item, reply_to_commit=True)
        

        # For each propose message
        while self.has_unread_message_with_performative(MessagePerformative.PROPOSE):
            propose_message = self.get_last_unread_message_with_performative(MessagePerformative.PROPOSE)
            self.current_discussions[propose_message.get_exp()] = []
            item = propose_message.get_content()
            
            # Check if it is the best item
            if self.preference.most_preferred(self.model.items) == item:
                self.accept(proposer_agent_id=propose_message.get_exp(), item=item)
            else:
                self.ask_why(to_agent=propose_message.get_exp(), item=item)
    
        # For each accept message
        while self.has_unread_message_with_performative(MessagePerformative.ACCEPT):
            accept_message = self.get_last_unread_message_with_performative(MessagePerformative.ACCEPT)
            self.commit(to_agent=accept_message.get_exp(), item=accept_message.get_content())

        
        # For each ask why message
        while self.has_unread_message_with_performative(MessagePerformative.ASK_WHY):
            ask_message = self.get_last_unread_message_with_performative(MessagePerformative.ASK_WHY)
            item = ask_message.get_content()
            argument = self.generate_argument(item)
            if argument is not None:
                self.argue(ask_message.get_exp(), argument)
            else:
                new_item = choice([x for x in self.model.items if x != item])
                self.propose(item=new_item, receiver=ask_message.get_exp())


    def generate_argument(self, item: Item, argument: Argument = None):
        """Check if we can attack argument."""
        # if no previous argument, then just create one (first time)
        if argument is None:
            print('No previous argument, we generate one')
            argument = Argument(True, item)
            premisses = argument.list_supporting_proposals(item=item, preferences=self.preference)
        
            if len(premisses) == 0:
                return None
            selected_premiss = premisses[0]
            argument.add_premiss_couple_values(
                criterion_name=selected_premiss.criterion_name, value=selected_premiss.value
            )
            return argument

        # If resaons are like (c_i = x)
        if ...:
            couple_value = argument.couple_values_list[0]
            # If Y has a better alternative O_j, j != i, on c_i
            if ...:
                argument = Argument(True, other_item)
                argument.add_premiss_couple_values(couple_value.criterion_name, other_value)
                # other_value better than couple_value.value
                return argument
            
            # If O_i has a bad evaluation on c_i
            if ...:
                argument = Argument(False, item)
                argument.add_premiss_couple_values(couple_value.criterion_name, other_value)
                return argument
            
            # If O_i has bad evaluation on c_j (j!=i) and c_j more important than c_i
            if ...:
                argument = Argument(False, item)
                argument.add_premiss_comparison(best_criterion_name=other_criterion, worst_criterion_name=couple_value.criterion_name)
                argument.add_premiss_couple_values(other_criterion, other_value)
                return argument
        
        # If reasons are like (c_i = x) and (c_i > c_j)
        if ...:
            # If Y has a better alternative O_j, j != i, on c_i
            if ...:
                argument = Argument(True, other_item)
                argument.add_premiss_couple_values(couple_value.criterion_name, other_value)
                return argument

            # If Y prefers c_j to c_i
            if ...:
                argument = Argument(False, item)
                argument.add_premiss_comparison(best_criterion_name=other_criterion, worst_criterion_name=couple_value.criterion_name)
                argument.add_premiss_couple_values(other_criterion, other_value)
                return argument

        
        return None


        return False
    def get_all_agents_except_me(self) -> List[CommunicatingAgent]:
        """Return all agents except me."""
        return [
            agent
            for agent in self.model.schedule.agents
            if agent.unique_id != self.unique_id
        ]
