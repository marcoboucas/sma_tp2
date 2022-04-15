"""Run a batch."""


import os

from tqdm import tqdm

from argument_model import ArgumentModel


def run_and_save(nbr_steps: int = 100, results_folder: str = "./results"):
    """Run and save one epoch."""

    # Generate the model
    model = ArgumentModel(nb_agents=10, nb_items=10)

    # Run the simulation
    for _ in tqdm(range(nbr_steps)):
        model.step()

    # Save the results
    os.makedirs(results_folder, exist_ok=True)
    agent_vars = model.datacollector.get_agent_vars_dataframe()
    agent_vars.to_csv(os.path.join(results_folder, "agents.csv"))
    model_vars = model.datacollector.get_model_vars_dataframe()
    # model_vars.to_csv(os.path.join(results_folder, "model.csv"))


if __name__ == "__main__":

    run_and_save()
