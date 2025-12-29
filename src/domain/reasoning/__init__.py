"""
Reasoning Systems package for gym workout recommendation system.

This package implements various reasoning mechanisms following AI course concepts:
- Deductive Reasoning: Rule-based logical inference
- Inductive Reasoning: Pattern learning from examples
- Probabilistic Reasoning: Conditional probability calculations
- Heuristic Functions: Domain-specific estimation functions

These reasoning systems enable the agents to make informed decisions,
learn from data, and provide explanations for recommendations.
"""

from .deductive_reasoner import DeductiveReasoner, Rule, Fact, FactType
from .inductive_reasoner import InductiveReasoner, Pattern, Example, PatternType
from .probability_calculator import ProbabilityCalculator, ConditionalProbability, ProbabilityType
from .heuristic_function import (
    HeuristicFunction,
    WorkoutHeuristic,
    ManhattanHeuristic,
    EuclideanHeuristic,
    ZeroHeuristic,
    HeuristicResult,
    HeuristicType,
    create_default_heuristic,
    compare_heuristics
)

__all__ = [
    # Deductive Reasoning
    'DeductiveReasoner',
    'Rule',
    'Fact',
    'FactType',
    
    # Inductive Reasoning
    'InductiveReasoner',
    'Pattern',
    'Example',
    'PatternType',
    
    # Probabilistic Reasoning
    'ProbabilityCalculator',
    'ConditionalProbability',
    'ProbabilityType',
    
    # Heuristic Functions
    'HeuristicFunction',
    'WorkoutHeuristic',
    'ManhattanHeuristic',
    'EuclideanHeuristic',
    'ZeroHeuristic',
    'HeuristicResult',
    'HeuristicType',
    'create_default_heuristic',
    'compare_heuristics',
]
