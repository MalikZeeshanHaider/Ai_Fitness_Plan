"""
Intelligent Agents package for gym workout recommendation system.

This package implements three types of intelligent agents following
AI course concepts (simplified for academic clarity):

1. Simple Reflex Agent: 
   - Rule-based safety filtering (if-then rules)
   - Filters unsafe exercises based on injuries and constraints
   
2. Goal-Based Agent:
   - Fitness goal definition and planning
   - Defines target state and workout direction
   
3. Utility-Based Agent:
   - Exercise optimization using utility function
   - Scores exercises based on multiple objectives

These three agents work in sequence with A* Search to generate optimal workout plans.
"""

from .agent import Agent, Percept, AgentAction
from .simple_reflex_agent import SimpleReflexAgent
from .goal_based_agent import GoalBasedAgent
from .utility_based_agent import UtilityBasedAgent

__all__ = [
    'Agent',
    'Percept',
    'AgentAction',
    'SimpleReflexAgent',
    'GoalBasedAgent',
    'UtilityBasedAgent',
]
