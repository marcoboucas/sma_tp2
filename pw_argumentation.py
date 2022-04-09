"""Main file."""


from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector


from communication.message.MessageService import MessageService
from communication.preferences.Item import Item
from argument_agent import ArgumentAgent

def count_item_deals(item_id: str):
    """Count the number of students in one activity."""

    def count(model):
        """Count function."""
        return model.done_deals[item_id]

    return count

class ArgumentModel(Model):
    """ArgumentModel."""

    def __init__(self, nb_items:int=5, nb_agents:int=2) -> None:
        self.schedule = RandomActivation(self)
        MessageService.__instance = None
        self.__messages_service = MessageService(self.schedule)
        

        # Define Items
        self.items = [Item("E", "Elec"), Item("D", "Diesel"), *[Item( str(i), "Car " +str(i)) for i in range(1, nb_items - 2 + 1)]]
        self.done_deals = {x.get_name(): 0 for x in self.items}

        # Define agents
        for agent_id in range(nb_agents):
            agent = ArgumentAgent(agent_id, self, f"Agent{agent_id+1}")
            agent.generate_preferences()
            self.schedule.add(agent)

        self.running = True

        self.datacollector = DataCollector(
            model_reporters={
                **{
                    f"item_{i}": count_item_deals(x.get_name())
                    for i, x in enumerate(self.items)
                },
            },
            agent_reporters={"nbr_won": "nbr_won", "nbr_sent_messages": "nbr_sent_messages"},
        )

    def step(self):
        self.datacollector.collect(self)
        self.__messages_service.dispatch_messages()
        self.schedule.step()


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.WARNING)
    argument_model = ArgumentModel()
    for _ in range(50):
        print('\n')
        argument_model.step()
