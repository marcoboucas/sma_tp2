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

        self.nbr_won = 0
        self.nbr_agreements = 0

    def step(self):
        """Init."""
        self.step_final()

    def step_final(self) -> None:
        """Step for the client agent."""
        # TODO: REMOVE LATER
        if self.name == "Agent1" or True:
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
            
            new_argument = self.generate_argument(item=argument.item, argument=argument, past_arguments=self.current_discussions[argue_message.get_exp()])
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
                self.model.done_deals[item.get_name()] += 1
                self.nbr_won += 1
            else:
                self.nbr_agreements +=1
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
            self.nbr_agreements+=1

        
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


    def generate_argument(self, item: Item, argument: Argument = None, past_arguments: List[Argument] = None) -> Argument:
        """Check if we can attack argument."""
        if past_arguments is None:
            past_arguments = []
        already_talked_about = set([x.get_item() for x in past_arguments])
    
        # if no previous argument, then just create one (first time)
        if argument is None:
            self.logger.info('No previous argument, we generate one')
            argument = Argument(True, item)
            premisses = argument.list_supporting_proposals(item=item, preferences=self.preference)
        
            if len(premisses) == 0:
                return None
            selected_premiss = premisses[0]
            argument.add_premiss_couple_values(
                criterion_name=selected_premiss.criterion_name, value=selected_premiss.value
            )
            return argument

        # If reasons are like (c_i = x)
        if len(argument.couple_values_list) == 1 and len(argument.comparison_list) == 0:
            couple_value = argument.couple_values_list[0]
            
            # If Y has a better alternative O_j, j != i, on c_i
            other_items = [
                x for x in self.model.items
                if x != item and self.preference.get_value(x, couple_value.criterion_name) > couple_value.value
            ]
            other_items = list(filter(lambda x: x not in already_talked_about, other_items))
            if len(other_items) > 0:
                self.logger.info("We have a criterion value, If Y has a better alternative O_j, j != i, on c_i")
                other_items = list(sorted(other_items, key=lambda x: self.preference.get_value(item=x, criterion_name=couple_value.criterion_name), reverse=True))
                argument = Argument(True, other_items[0])
                argument.add_premiss_couple_values(couple_value.criterion_name, self.preference.get_value(other_items[0], couple_value.criterion_name))

                return argument
            
            # If O_i has a bad evaluation on c_i
            if self.preference.get_value(item, couple_value.criterion_name) <= couple_value.value and self.preference.get_value(item, couple_value.criterion_name) < Value.GOOD:
                self.logger.info("We have a criterion value, If O_i has a bad evaluation on c_i")
                argument = Argument(False, item)
                argument.add_premiss_couple_values(couple_value.criterion_name, self.preference.get_value(item, couple_value.criterion_name))
                return argument
            
            # If O_i has bad evaluation on c_j (j!=i) and c_j more important than c_i
            criteria = self.preference.get_criterion_name_list()
            criteria = criteria[:criteria.index(couple_value.criterion_name)]
            criteria = list(filter(lambda x: self.preference.get_value(item, x) < Value.GOOD, criteria))
            if len(criteria):
                self.logger.info("We have a criterion value, If O_i has bad evaluation on c_j (j!=i) and c_j more important than c_i")
                argument = Argument(False, item)
                argument.add_premiss_comparison(best_criterion_name=criteria[0], worst_criterion_name=couple_value.criterion_name)
                argument.add_premiss_couple_values(criteria[0], self.preference.get_value(item, criteria[0]))
                return argument
        
        # If reasons are like (c_i = x) and (c_i > c_j)
        if len(argument.couple_values_list) == 1 and len(argument.comparison_list) == 1:
            
            couple_value = argument.couple_values_list[0]
            comparison = argument.comparison_list[0]
            # If Y has a better alternative O_j, j != i, on c_i
            items = self.model.items[:]
            items = list(filter(lambda x: x != item, items))
            items = list(filter(lambda x: self.preference.get_value(x, couple_value.criterion_name) > couple_value.value, items))
            items = list(sorted(items, key=lambda x: x.get_score(self.preference), reverse=True))
            items = list(filter(lambda x: x not in already_talked_about, items))
            if len(items)>0:
                self.logger.info("We have a comparison, If Y has a better alternative O_j, j != i, on c_i")
                argument = Argument(True, items[0])
                argument.add_premiss_couple_values(couple_value.criterion_name, self.preference.get_value(items[0], couple_value.criterion_name))
                return argument

            # If Y prefers c_j to c_i
            order = self.preference.get_criterion_name_list()
            if order.index(comparison.best_criterion_name)>order.index(comparison.worst_criterion_name):
                self.logger.info("We have a comparison,  If Y prefers c_j to c_i")
                argument = Argument(False, item)
                argument.add_premiss_comparison(best_criterion_name=comparison.worst_criterion_name, worst_criterion_name=comparison.best_criterion_name)
                argument.add_premiss_couple_values(comparison.best_criterion_name, self.preference.get_value(item, comparison.best_criterion_name))
                return argument

        logging.info("No further argument your Honor... (nbr items seen: %i)", len(already_talked_about))
        return None


        return False
    def get_all_agents_except_me(self) -> List[CommunicatingAgent]:
        """Return all agents except me."""
        return [
            agent
            for agent in self.model.schedule.agents
            if agent.unique_id != self.unique_id
        ]
