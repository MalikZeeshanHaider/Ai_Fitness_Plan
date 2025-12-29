"""
Search algorithms package for gym workout recommendation system.

This package provides the A* Search algorithm for finding optimal workout plans.

A* (A-Star) Search:
- Informed search algorithm using evaluation function f(n) = g(n) + h(n)
- g(n) = path cost from start to node n
- h(n) = heuristic estimate from node n to goal
- Complete and optimal with admissible heuristic
- Used to generate optimal workout sequences

This is the ONLY search algorithm used in the simplified system.
"""

from .search_problem import SearchProblem, SearchSolution
from .astar import AStarSearch
from .search_strategy import SearchStrategy, TreeSearchStrategy, GraphSearchStrategy

__all__ = [
    'SearchProblem',
    'SearchSolution',
    'AStarSearch',
    'SearchStrategy',
    'TreeSearchStrategy',
    'GraphSearchStrategy',
]
