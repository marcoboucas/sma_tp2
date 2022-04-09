# Multi-Agent Systems - TP2


![Visualisation of the winning items](./docs/bar_chart.gif)

# Introduction
In this practical work, we have implemented the code for argumentation agents that negotiate to select the best car type.
We first programmed each agent separately, and then aggregated them into a general agent, with some modifications to make it work with more than 2 agents. 

# How to run the code

1. Install the required packages `pip install -r requirements.txt`
1. Run the code `python pw_argumentation.py`
1. If you prefer the version with Mesa visualization, run `python run.py`


# Technical choices

- To make the algorithm able to handle more than 2 agents, we have decided to proceed using the following method: Each agent will check for each **unread** _Message Performative_. It will then do action corresponding to the message and go to the next one.
That way, the number of agents is not important anymore
- To avoid deadloops during a negociation, agents are not allowed to discuss againn about an already discussed item. For instance, if 2 agents are discussing about the Item 1 and then about the Item 2, they will not be able to go back to the Item 1. __(Those information are stored in each agent and reset at each end of deal)_
- A couple of agents will always have 2 discussions in parallel, because the outcome of the negotiation depends on which started it (They will start with their favorite item).
- For debugging purposes, we have displayed the preferences of each user at the start of the script. That way, it is much easier to understand the negociation process and the decisions made by each agent.




# Metrics used

- For each negotiation : the winning agent (redundant with #won)
- Number of messages sent (by promise type)
- Number of agreements
- Number of won (last message sent before agreement)
- Which items he defended & supportive arguments
- Most defended item
- Criterion most put forward

# Results

TODO





