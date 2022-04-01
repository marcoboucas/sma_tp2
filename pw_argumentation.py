"""Main file."""


from mesa import Model
from mesa.time import RandomActivation


from communication.message.MessageService import MessageService
from communication.preferences.Item import Item
from argument_agent import ArgumentAgent


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
    import logging
    logging.basicConfig(level=logging.INFO)
    argument_model = ArgumentModel()
    for _ in range(10):
        print('\n')
        argument_model.step()
