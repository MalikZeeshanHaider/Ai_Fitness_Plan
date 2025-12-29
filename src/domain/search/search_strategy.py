"""
Search Strategy Implementations: Tree Search vs Graph Search.

This module provides abstract and concrete implementations of search strategies
that can be applied to any search algorithm (BFS, DFS, UCS, Greedy, A*).

Tree Search: Simple strategy that may revisit states (risk of infinite loops)
Graph Search: Tracks explored states to avoid revisiting (complete & optimal)
"""

from abc import ABC, abstractmethod
from typing import Set, Optional, Callable
from dataclasses import dataclass

from ..models.state import State
from ..models.search_node import SearchNode


@dataclass
class SearchMetrics:
    """
    Metrics collected during search execution.
    
    Attributes:
        nodes_explored: Total number of nodes expanded
        nodes_generated: Total number of nodes generated
        max_frontier_size: Maximum size of frontier during search
        duplicate_states_avoided: Number of duplicate states avoided (graph search)
    """
    nodes_explored: int = 0
    nodes_generated: int = 0
    max_frontier_size: int = 0
    duplicate_states_avoided: int = 0
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return (
            f"SearchMetrics(\n"
            f"  Nodes Explored: {self.nodes_explored}\n"
            f"  Nodes Generated: {self.nodes_generated}\n"
            f"  Max Frontier Size: {self.max_frontier_size}\n"
            f"  Duplicates Avoided: {self.duplicate_states_avoided}\n"
            f")"
        )


class SearchStrategy(ABC):
    """
    Abstract base class for search strategies.
    
    A search strategy defines how to handle state exploration and
    duplicate detection during search execution.
    
    Time Complexity: Depends on concrete implementation
    Space Complexity: Depends on concrete implementation
    """
    
    def __init__(self):
        """
        Initialize the search strategy.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._metrics = SearchMetrics()
    
    @property
    def metrics(self) -> SearchMetrics:
        """Get the current search metrics."""
        return self._metrics
    
    @abstractmethod
    def should_explore(self, node: SearchNode) -> bool:
        """
        Determine if a node should be explored.
        
        Args:
            node: The node to check
            
        Returns:
            True if node should be explored, False otherwise
            
        Time Complexity: Depends on implementation
        Space Complexity: Depends on implementation
        """
        pass
    
    @abstractmethod
    def mark_explored(self, node: SearchNode) -> None:
        """
        Mark a node as explored.
        
        Args:
            node: The node to mark as explored
            
        Time Complexity: Depends on implementation
        Space Complexity: Depends on implementation
        """
        pass
    
    @abstractmethod
    def is_duplicate(self, node: SearchNode) -> bool:
        """
        Check if a node's state has already been encountered.
        
        Args:
            node: The node to check
            
        Returns:
            True if state is duplicate, False otherwise
            
        Time Complexity: Depends on implementation
        Space Complexity: Depends on implementation
        """
        pass
    
    @abstractmethod
    def reset(self) -> None:
        """
        Reset the strategy state for a new search.
        
        Time Complexity: Depends on implementation
        Space Complexity: Depends on implementation
        """
        pass
    
    @abstractmethod
    def get_memory_usage(self) -> int:
        """
        Get approximate memory usage in bytes.
        
        Returns:
            Estimated memory usage
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """
        Get the name of the strategy.
        
        Returns:
            Strategy name
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        pass


class TreeSearchStrategy(SearchStrategy):
    """
    Tree Search Strategy implementation.
    
    Tree search does NOT track explored states, treating the search space
    as a tree. This means states can be revisited, which may lead to:
    - Redundant exploration
    - Infinite loops (in graphs with cycles)
    - Non-optimal solutions
    
    Advantages:
    - Simple implementation
    - No memory overhead for tracking states
    - Fast state checking (no lookups)
    
    Disadvantages:
    - May revisit same state multiple times
    - Not complete for graphs with cycles
    - Can waste time on duplicate paths
    
    Time Complexity: O(1) per operation
    Space Complexity: O(1) - no state tracking
    """
    
    def __init__(self):
        """
        Initialize tree search strategy.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        super().__init__()
        self._name = "Tree Search"
    
    def should_explore(self, node: SearchNode) -> bool:
        """
        Tree search always explores nodes (no duplicate checking).
        
        Args:
            node: The node to check
            
        Returns:
            Always True
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return True
    
    def mark_explored(self, node: SearchNode) -> None:
        """
        Tree search doesn't track explored nodes.
        
        Args:
            node: The node to mark (ignored)
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._metrics.nodes_explored += 1
    
    def is_duplicate(self, node: SearchNode) -> bool:
        """
        Tree search doesn't check for duplicates.
        
        Args:
            node: The node to check
            
        Returns:
            Always False
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return False
    
    def reset(self) -> None:
        """
        Reset the strategy (nothing to reset for tree search).
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._metrics = SearchMetrics()
    
    def get_memory_usage(self) -> int:
        """
        Get memory usage (minimal for tree search).
        
        Returns:
            Memory usage in bytes
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        import sys
        return sys.getsizeof(self._metrics)
    
    def get_strategy_name(self) -> str:
        """
        Get strategy name.
        
        Returns:
            "Tree Search"
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return self._name
    
    def __str__(self) -> str:
        """String representation."""
        return f"TreeSearchStrategy(explored={self._metrics.nodes_explored})"


class GraphSearchStrategy(SearchStrategy):
    """
    Graph Search Strategy implementation.
    
    Graph search tracks explored states to avoid revisiting them. This
    ensures completeness and optimality for algorithms like A* and UCS.
    
    The strategy maintains a set of explored states and optionally tracks
    the best cost to reach each state (for optimal algorithms).
    
    Advantages:
    - Prevents infinite loops
    - Complete for finite search spaces
    - Ensures optimality (with proper cost tracking)
    - Avoids redundant exploration
    
    Disadvantages:
    - Memory overhead for storing explored states
    - Slower state checking (hash lookups)
    - Can use significant memory for large spaces
    
    Time Complexity: O(1) per operation (average case with hash table)
    Space Complexity: O(|S|) where |S| is number of unique states
    """
    
    def __init__(self, track_costs: bool = True):
        """
        Initialize graph search strategy.
        
        Args:
            track_costs: If True, track best cost to each state
                        If False, only track visited states
                        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        super().__init__()
        self._name = "Graph Search"
        self._track_costs = track_costs
        
        # Store explored states
        if track_costs:
            # Map state -> best cost found so far
            self._explored_costs: dict[State, float] = {}
        else:
            # Set of explored states
            self._explored_states: Set[State] = set()
    
    def should_explore(self, node: SearchNode) -> bool:
        """
        Check if node should be explored based on graph search rules.
        
        For cost-tracking:
        - Explore if state not seen before
        - Explore if found better path to state
        
        For simple tracking:
        - Explore only if state not seen before
        
        Args:
            node: The node to check
            
        Returns:
            True if should explore, False if duplicate
            
        Time Complexity: O(1) average case (hash lookup)
        Space Complexity: O(1)
        """
        if self._track_costs:
            # Check if we've found a better path
            if node.state in self._explored_costs:
                best_cost = self._explored_costs[node.state]
                if node.path_cost >= best_cost:
                    self._metrics.duplicate_states_avoided += 1
                    return False
            return True
        else:
            # Simple duplicate check
            if node.state in self._explored_states:
                self._metrics.duplicate_states_avoided += 1
                return False
            return True
    
    def mark_explored(self, node: SearchNode) -> None:
        """
        Mark node as explored and update cost tracking if enabled.
        
        Args:
            node: The node to mark as explored
            
        Time Complexity: O(1) average case (hash insert)
        Space Complexity: O(1) per state
        """
        self._metrics.nodes_explored += 1
        
        if self._track_costs:
            # Update best cost to this state
            self._explored_costs[node.state] = node.path_cost
        else:
            # Add state to explored set
            self._explored_states.add(node.state)
    
    def is_duplicate(self, node: SearchNode) -> bool:
        """
        Check if node's state has been explored.
        
        Args:
            node: The node to check
            
        Returns:
            True if duplicate, False otherwise
            
        Time Complexity: O(1) average case (hash lookup)
        Space Complexity: O(1)
        """
        if self._track_costs:
            return node.state in self._explored_costs
        else:
            return node.state in self._explored_states
    
    def get_best_cost(self, state: State) -> Optional[float]:
        """
        Get the best known cost to reach a state (if cost tracking enabled).
        
        Args:
            state: The state to query
            
        Returns:
            Best cost if state explored, None otherwise
            
        Time Complexity: O(1) average case
        Space Complexity: O(1)
        """
        if self._track_costs:
            return self._explored_costs.get(state)
        return None
    
    def reset(self) -> None:
        """
        Reset the strategy for a new search.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._metrics = SearchMetrics()
        if self._track_costs:
            self._explored_costs.clear()
        else:
            self._explored_states.clear()
    
    def get_memory_usage(self) -> int:
        """
        Get approximate memory usage in bytes.
        
        Returns:
            Estimated memory usage
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        import sys
        base_size = sys.getsizeof(self._metrics)
        
        if self._track_costs:
            return base_size + sys.getsizeof(self._explored_costs)
        else:
            return base_size + sys.getsizeof(self._explored_states)
    
    def get_strategy_name(self) -> str:
        """
        Get strategy name.
        
        Returns:
            "Graph Search" with cost tracking info
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        suffix = " (with cost tracking)" if self._track_costs else ""
        return self._name + suffix
    
    def __str__(self) -> str:
        """String representation."""
        explored_count = (
            len(self._explored_costs) if self._track_costs 
            else len(self._explored_states)
        )
        return (
            f"GraphSearchStrategy("
            f"explored={explored_count}, "
            f"duplicates_avoided={self._metrics.duplicate_states_avoided})"
        )


# Comparison utilities

def compare_strategies(tree_metrics: SearchMetrics, graph_metrics: SearchMetrics) -> str:
    """
    Compare tree search and graph search metrics.
    
    Args:
        tree_metrics: Metrics from tree search
        graph_metrics: Metrics from graph search
        
    Returns:
        Formatted comparison string
        
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    return f"""
    Search Strategy Comparison
    ==========================
    
    Tree Search:
    - Nodes Explored: {tree_metrics.nodes_explored}
    - Nodes Generated: {tree_metrics.nodes_generated}
    - Max Frontier: {tree_metrics.max_frontier_size}
    - Duplicates Avoided: {tree_metrics.duplicate_states_avoided}
    
    Graph Search:
    - Nodes Explored: {graph_metrics.nodes_explored}
    - Nodes Generated: {graph_metrics.nodes_generated}
    - Max Frontier: {graph_metrics.max_frontier_size}
    - Duplicates Avoided: {graph_metrics.duplicate_states_avoided}
    
    Efficiency Gain:
    - Nodes Saved: {tree_metrics.nodes_explored - graph_metrics.nodes_explored}
    - Reduction: {(1 - graph_metrics.nodes_explored / max(tree_metrics.nodes_explored, 1)) * 100:.1f}%
    """


# Example usage and testing
if __name__ == "__main__":
    print("Tree Search Strategy:")
    print("- Simple, no state tracking")
    print("- May revisit states")
    print("- Memory efficient")
    print()
    print("Graph Search Strategy:")
    print("- Tracks explored states")
    print("- Avoids revisiting states")
    print("- Complete and optimal")
