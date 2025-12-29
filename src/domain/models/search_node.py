"""
Search Node Module
==================

Defines the SearchNode class for representing nodes in search trees.

In AI search algorithms:
- SEARCH TREE: Tree structure of all possible paths from initial state
- NODE: Represents a state in the search tree with metadata
- PATH: Sequence of nodes from root to current node
- FRONTIER: Set of nodes waiting to be explored

Key Components:
- Node stores: state, parent, action, path cost, depth
- Enables path reconstruction after goal is found
- Essential for all search algorithms (BFS, DFS, UCS, A*, etc.)

Author: AI Engineer
Date: December 17, 2025
"""

from dataclasses import dataclass, field
from typing import Optional, List, Any
from src.domain.models.state import State
from src.domain.models.action import Action


@dataclass
class SearchNode:
    """
    Node in a search tree representing a state and path to reach it.
    
    A search node contains:
    - STATE: The state at this node
    - PARENT: The node that generated this node
    - ACTION: The action that was applied to parent to generate this node
    - PATH_COST: Total cost from initial state to this node (g(n))
    - DEPTH: Number of steps from initial state
    - HEURISTIC: Estimated cost to goal (h(n)) - used in informed search
    
    This class is fundamental to implementing SEARCH ALGORITHMS.
    
    The search tree is formed by:
    1. Starting with initial state in root node
    2. Expanding nodes by applying actions
    3. Creating child nodes for each successor state
    4. Tracking parent pointers for path reconstruction
    
    Attributes:
        state: The state represented by this node
        parent: Parent node (None for root)
        action: Action that led to this node (None for root)
        path_cost: Total path cost from root (g(n))
        depth: Depth in search tree (0 for root)
        heuristic: Heuristic estimate to goal (h(n))
        
    Time Complexity:
        - Node creation: O(1)
        - Path extraction: O(d) where d is depth
        
    Space Complexity:
        - Per node: O(1) plus state size
        - Complete tree: O(b^d) where b is branching factor
        
    Example:
        >>> initial_state = State(...)
        >>> root_node = SearchNode(state=initial_state)
        >>> 
        >>> # Create child node by applying action
        >>> new_state = initial_state.transition(...)
        >>> child_node = SearchNode(
        ...     state=new_state,
        ...     parent=root_node,
        ...     action=some_action,
        ...     path_cost=root_node.path_cost + action.calculate_cost(),
        ...     depth=root_node.depth + 1
        ... )
    """
    
    # Core node attributes
    state: State
    parent: Optional['SearchNode'] = None
    action: Optional[Action] = None
    
    # Cost metrics
    path_cost: float = 0.0  # g(n) - cost from initial state
    depth: int = 0  # Number of actions from initial state
    heuristic: float = 0.0  # h(n) - estimated cost to goal
    
    # Metadata
    node_id: str = field(default_factory=lambda: "")
    
    def __post_init__(self) -> None:
        """Initialize computed fields."""
        if not self.node_id:
            # Generate unique node ID based on state hash and depth
            object.__setattr__(
                self, 
                'node_id', 
                f"node_{hash(self.state)}_{self.depth}"
            )
    
    def get_f_score(self) -> float:
        """
        Calculate f(n) = g(n) + h(n) for A* algorithm.
        
        In A* search:
        - g(n): Actual cost from start to node (path_cost)
        - h(n): Heuristic estimated cost from node to goal (heuristic)
        - f(n): Estimated total cost of cheapest solution through node
        
        Returns:
            float: Total estimated cost f(n)
            
        Note:
            If h(n) is admissible (never overestimates),
            A* is guaranteed to find optimal solution.
            
        Example:
            >>> node.path_cost = 10  # g(n)
            >>> node.heuristic = 5   # h(n)
            >>> f_score = node.get_f_score()  # Returns 15
        """
        return self.path_cost + self.heuristic
    
    def get_path(self) -> List['SearchNode']:
        """
        Extract path from initial state to this node.
        
        Follows parent pointers back to root and reverses the sequence.
        This is how we reconstruct the SOLUTION PATH after finding goal.
        
        Returns:
            List[SearchNode]: Path from root to this node
            
        Time Complexity: O(d) where d is depth
        
        Example:
            >>> goal_node = search_algorithm.find_goal()
            >>> path = goal_node.get_path()
            >>> for node in path:
            ...     print(node.action.exercise_name if node.action else "Start")
        """
        path: List[SearchNode] = []
        current: Optional[SearchNode] = self
        
        # Follow parent pointers to root
        while current is not None:
            path.append(current)
            current = current.parent
        
        # Reverse to get path from root to current
        path.reverse()
        return path
    
    def get_actions_path(self) -> List[Action]:
        """
        Extract sequence of actions from root to this node.
        
        Returns:
            List[Action]: List of actions in order
            
        Example:
            >>> actions = goal_node.get_actions_path()
            >>> for action in actions:
            ...     print(f"Exercise: {action.exercise_name}")
        """
        path = self.get_path()
        # Skip first node (root has no action)
        return [node.action for node in path[1:] if node.action is not None]
    
    def get_states_path(self) -> List[State]:
        """
        Extract sequence of states from root to this node.
        
        Returns:
            List[State]: List of states in order
        """
        path = self.get_path()
        return [node.state for node in path]
    
    def expand(
        self,
        actions: List[Action],
        calculate_heuristic=None
    ) -> List['SearchNode']:
        """
        Generate child nodes by applying applicable actions.
        
        This is the core EXPANSION operation in search algorithms:
        1. For each action, check if applicable to current state
        2. Apply action to get successor state
        3. Create child node with new state
        4. Calculate costs (path cost and heuristic)
        
        Args:
            actions: List of possible actions to try
            calculate_heuristic: Optional function to calculate h(n)
            
        Returns:
            List[SearchNode]: List of child nodes
            
        Time Complexity: O(|actions|) for applicability checks
        
        Example:
            >>> children = current_node.expand(
            ...     actions=all_available_actions,
            ...     calculate_heuristic=lambda state: estimate_cost(state)
            ... )
            >>> for child in children:
            ...     frontier.add(child)
        """
        children: List[SearchNode] = []
        
        for action in actions:
            # Check if action is applicable (PRECONDITION checking)
            if action.is_applicable(
                available_equipment=set(self.state.available_equipment),
                experience_level=self.state.experience_level.value,
                medical_conditions=set(self.state.medical_conditions),
                worked_muscles=set(self.state.worked_muscle_groups),
                fatigue_level=self.state.current_fatigue_level
            ):
                # Apply action to get successor state (STATE TRANSITION)
                successor_state = self.state.transition(
                    exercise_name=action.exercise_name,
                    muscle_groups=set(action.muscle_groups),
                    calories=action.estimated_calories,
                    duration=action.estimated_duration,
                    fatigue_increase=0.1
                )
                
                # Calculate path cost: g(child) = g(parent) + cost(action)
                action_cost = action.calculate_cost(self.state.current_fatigue_level)
                child_path_cost = self.path_cost + action_cost
                
                # Calculate heuristic if provided
                child_heuristic = 0.0
                if calculate_heuristic is not None:
                    child_heuristic = calculate_heuristic(successor_state)
                
                # Create child node
                child = SearchNode(
                    state=successor_state,
                    parent=self,
                    action=action,
                    path_cost=child_path_cost,
                    depth=self.depth + 1,
                    heuristic=child_heuristic
                )
                
                children.append(child)
        
        return children
    
    def is_goal(self, target_exercises: int, target_duration: int) -> bool:
        """
        Check if this node represents a goal state.
        
        Args:
            target_exercises: Target number of exercises
            target_duration: Target duration in minutes
            
        Returns:
            bool: True if this is a goal node
            
        Example:
            >>> if node.is_goal(target_exercises=6, target_duration=45):
            ...     print("Goal reached!")
            ...     solution = node.get_actions_path()
        """
        return self.state.is_goal_state(target_exercises, target_duration)
    
    def __lt__(self, other: 'SearchNode') -> bool:
        """
        Compare nodes for priority queue ordering.
        
        Used by heapq in priority queue implementations for:
        - Uniform Cost Search (compare by path_cost)
        - Greedy Best-First (compare by heuristic)
        - A* (compare by f_score)
        
        Args:
            other: Another search node
            
        Returns:
            bool: True if this node has lower f-score
            
        Note:
            This enables: `heapq.heappush(frontier, node)`
        """
        return self.get_f_score() < other.get_f_score()
    
    def __eq__(self, other: object) -> bool:
        """
        Check equality based on state.
        
        Two nodes are equal if they represent the same state.
        Used for duplicate detection in graph search.
        
        Args:
            other: Another node
            
        Returns:
            bool: True if states are equal
        """
        if not isinstance(other, SearchNode):
            return False
        return self.state == other.state
    
    def __hash__(self) -> int:
        """
        Hash based on state for explored set in graph search.
        
        Returns:
            int: Hash value
            
        Note:
            Enables: `explored.add(node)` and `if node in explored`
        """
        return hash(self.state)
    
    def __str__(self) -> str:
        """
        String representation of node.
        
        Returns:
            str: Human-readable node description
        """
        action_name = self.action.exercise_name if self.action else "START"
        return (
            f"Node(depth={self.depth}, cost={self.path_cost:.2f}, "
            f"h={self.heuristic:.2f}, f={self.get_f_score():.2f}, "
            f"action={action_name})"
        )
    
    def to_dict(self) -> dict:
        """
        Convert node to dictionary for serialization.
        
        Returns:
            dict: Dictionary representation
        """
        return {
            'node_id': self.node_id,
            'depth': self.depth,
            'path_cost': self.path_cost,
            'heuristic': self.heuristic,
            'f_score': self.get_f_score(),
            'action': self.action.to_dict() if self.action else None,
            'state': self.state.to_dict()
        }
    
    def get_summary(self) -> str:
        """
        Get a summary of the workout plan represented by this node.
        
        Returns:
            str: Summary string
        """
        actions = self.get_actions_path()
        return (
            f"Workout Plan:\n"
            f"  Exercises: {len(actions)}\n"
            f"  Duration: {self.state.total_workout_duration} minutes\n"
            f"  Calories: {self.state.total_calories_burned:.0f}\n"
            f"  Muscle Groups: {', '.join(sorted(self.state.worked_muscle_groups))}\n"
            f"  Fatigue Level: {self.state.current_fatigue_level:.2f}"
        )
