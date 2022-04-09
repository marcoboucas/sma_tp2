""" Create graphs to visualize the measuredd metrics """

import os

import matplotlib.pyplot as plt
import pandas as pd

df = pd.from_csv(os.path.join("results", "agent.csv"))
