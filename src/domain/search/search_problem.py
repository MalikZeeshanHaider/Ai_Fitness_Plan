"""
Abstract base class for search problems in the workout recommendation system.

This module defines the SearchProblem interface that all search algorithms
will use, along with the SearchSolution data class for returning results.

Time Complexity: Varies by implementation
Space Complexity: Varies by implementation
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Set, Callable
from datetime import datetime

from ..models.state import State
from ..models.action import Action
from ..models.search_node import SearchNode


@dataclass
class SearchSolution:
    """
    Represents a solution found by a search algorithm.
    
    Attributes:
        success: Whether a solution was found
        goal_node: The goal node if found
        path: Sequence of actions from initial to goal state
        path_cost: Total cost of the solution path
        nodes_explored: Number of nodes explored during search
        max_frontier_size: Maximum size of the frontier during search
        execution_time_ms: Time taken to find solution in milliseconds
        algorithm_name: Name of the algorithm used
        search_strategy: Tree or Graph search strategy used
        memory_usage_bytes: Approximate memory used during search
    """
    success: bool
    goal_node: Optional[SearchNode] = None
    path: List[Action] = field(default_factory=list)
    path_cost: float = float('inf')
    nodes_explored: int = 0
    max_frontier_size: int = 0
    execution_time_ms: float = 0.0
    algorithm_name: str = ""
    search_strategy: str = ""
    memory_usage_bytes: int = 0
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        if self.success:
            return (
                f"Solution found by {self.algorithm_name} ({self.search_strategy})\n"
                f"Path length: {len(self.path)} actions\n"
                f"Path cost: {self.path_cost:.2f}\n"
                f"Nodes explored: {self.nodes_explored}\n"
                f"Max frontier size: {self.max_frontier_size}\n"
                f"Execution time: {self.execution_time_ms:.2f}ms\n"
                f"Memory usage: {self.memory_usage_bytes / 1024:.2f}KB"
            )
        else:
            return (
                f"No solution found by {self.algorithm_name}\n"
                f"Nodes explored: {self.nodes_explored}\n"
                f"Execution time: {self.execution_time_ms:.2f}ms"
            )


class SearchProblem(ABC):
    """
    Abstract base class for search problems.
    
    This class defines the interface that all search problems must implement.
    It follows the state-space search paradigm:
    - States: Configurations of the world
    - Actions: Transitions between states
    - Goal Test: Check if a state satisfies the goal
    - Path Cost: Cost of a sequence of actions
    
    Time Complexity: Depends on implementation
    Space Complexity: Depends on implementation
    """
    
    def __init__(self, initial_state: State, goal_state: State):
        """
        Initialize the search problem.
        
        Args:
            initial_state: The starting state
            goal_state: The target state (used for goal testing)
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._initial_state = initial_state
        self._goal_state = goal_state
        self._created_at = datetime.now()
    
    @property
    def initial_state(self) -> State:
        """Get the initial state."""
        return self._initial_state
    
    @property
    def goal_state(self) -> State:
        """Get the goal state."""
        return self._goal_state
    
    @abstractmethod
    def get_available_actions(self, state: State) -> List[Action]:
        """
        Return all actions that can be executed in the given state.
        
        This method should filter actions based on:
        - Preconditions (is_applicable)
        - Current state constraints
        - Domain-specific rules
        
        Args:
            state: The current state
            
        Returns:
            List of applicable actions
            
        Time Complexity: O(A) where A is total number of actions
        Space Complexity: O(A) for storing applicable actions
        """
        pass
    
    @abstractmethod
    def get_successor(self, state: State, action: Action) -> State:
        """
        Return the state that results from executing action in state.
        
        This method applies the action's effects to produce a new state.
        The original state should remain unchanged (immutability).
        
        Args:
            state: The current state
            action: The action to execute
            
        Returns:
            The resulting state after applying the action
            
        Time Complexity: O(1) - state transition
        Space Complexity: O(1) - new state object
        """
        pass
    
    @abstractmethod
    def is_goal(self, state: State) -> bool:
        """
        Test if the given state satisfies the goal.
        
        This method checks if the state meets all goal criteria.
        For workout planning, this might check:
        - Fitness goal alignment
        - Minimum workout duration
        - Required muscle group coverage
        - Exercise variety
        
        Args:
            state: The state to test
            
        Returns:
            True if state is a goal state, False otherwise
            
        Time Complexity: O(1) - simple comparison
        Space Complexity: O(1)
        """
        pass
    
    @abstractmethod
    def get_action_cost(self, state: State, action: Action, next_state: State) -> float:
        """
        Return the cost of applying action in state to reach next_state.
        
        The cost function can consider:
        - Action difficulty
        - Time required
        - Energy expenditure
        - Equipment availability
        - User preferences
        
        Args:
            state: The current state
            action: The action being applied
            next_state: The resulting state
            
        Returns:
            The cost (non-negative float)
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        pass
    
    @abstractmethod
    def get_heuristic(self, state: State) -> float:
        """
        Estimate the cost from state to the nearest goal state.
        
        This heuristic function guides informed search algorithms.
        It must be admissible (never overestimate) for A* optimality.
        
        For workout planning, heuristics can consider:
        - Remaining goals to achieve
        - Gap between current and target fitness level
        - Estimated actions needed
        
        Args:
            state: The state to evaluate
            
        Returns:
            Estimated cost to goal (non-negative float)
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        pass
    
    def create_initial_node(self) -> SearchNode:
        """
        Create the initial search node.
        
        Returns:
            SearchNode representing the initial state
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return SearchNode(
            state=self._initial_state,
            parent=None,
            action=None,
            path_cost=0.0,
            depth=0,
            heuristic=self.get_heuristic(self._initial_state)
        )
    
    def expand(self, node: SearchNode) -> List[SearchNode]:
        """
        Expand a node by generating its successors.
        
        This method:
        1. Gets all applicable actions from the node's state
        2. For each action, generates the successor state
        3. Calculates the path cost to the successor
        4. Creates a new SearchNode for each successor
        
        Args:
            node: The node to expand
            
        Returns:
            List of successor nodes
            
        Time Complexity: O(A) where A is number of applicable actions
        Space Complexity: O(A) for storing successor nodes
        """
        successors = []
        actions = self.get_available_actions(node.state)
        
        for action in actions:
            # Generate successor state
            next_state = self.get_successor(node.state, action)
            
            # Calculate path cost
            action_cost = self.get_action_cost(node.state, action, next_state)
            path_cost = node.path_cost + action_cost
            
            # Calculate heuristic for informed search
            heuristic_value = self.get_heuristic(next_state)
            
            # Create successor node
            successor = SearchNode(
                state=next_state,
                parent=node,
                action=action,
                path_cost=path_cost,
                depth=node.depth + 1,
                heuristic=heuristic_value
            )
            
            successors.append(successor)
        
        return successors
    
    def get_solution(self, goal_node: Optional[SearchNode]) -> List[Action]:
        """
        Extract the solution path from a goal node.
        
        Args:
            goal_node: The goal node (or None if no solution)
            
        Returns:
            List of actions from initial state to goal state
            
        Time Complexity: O(d) where d is depth of goal node
        Space Complexity: O(d) for storing action path
        """
        if goal_node is None:
            return []
        
        return goal_node.get_actions_path()
    
    def __str__(self) -> str:
        """String representation of the search problem."""
        return (
            f"SearchProblem(\n"
            f"  Initial State: {self._initial_state}\n"
            f"  Goal State: {self._goal_state}\n"
            f"  Created: {self._created_at}\n"
            f")"
        )
