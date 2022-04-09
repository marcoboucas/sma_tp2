"""Runserver."""
import logging

import matplotlib
import matplotlib.pyplot as plt
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import (BarChartModule, ChartModule,
                                        PieChartModule)
from mesa.visualization.UserParam import UserSettableParameter

from argument_model import ArgumentModel

CMAP = "gist_ncar"

logging.basicConfig(level=logging.ERROR)

model_params = {
    "nb_items": 10,
    "nb_agents": UserSettableParameter("slider", "Number of agents", 3, 0, 40, 1),
}
palette = plt.cm.get_cmap(CMAP, 10)
activities_types_repartition = BarChartModule(
    [
        {"Label": f"item_{i}", "Color": matplotlib.colors.to_hex(palette(i))}
        for i in range(model_params["nb_items"])
    ]
)
activities_types_repartition_pie = PieChartModule(
    [
        {"Label": f"item_{i}", "Color": matplotlib.colors.to_hex(palette(i))}
        for i in range(model_params["nb_items"])
    ]
)

count_lines = ChartModule(
    [
        {"Label": f"item_{i}", "Color": matplotlib.colors.to_hex(palette(i))}
        for i in range(model_params["nb_items"])
    ],
    data_collector_name="datacollector",
)

server = ModularServer(
    ArgumentModel,
    [activities_types_repartition, activities_types_repartition_pie, count_lines],
    "Discussion",
    model_params,
)
server.port = 8522  # The default
server.launch()
