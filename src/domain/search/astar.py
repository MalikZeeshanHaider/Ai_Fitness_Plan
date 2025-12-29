"""
A* Search Algorithm Implementation.

A* is an informed search algorithm that combines UCS and Greedy search.
It uses f(n) = g(n) + h(n) where g(n) is path cost and h(n) is heuristic.

Properties:
- Complete: Yes (with admissible heuristic)
- Optimal: Yes (with admissible heuristic)
- Time Complexity: O(b^d) exponential, but often much better
- Space Complexity: O(b^d) - stores all generated nodes

Use Case: Finding optimal solution efficiently with good heuristic.
"""

import sys
import heapq
from typing import Optional, Set, List, Tuple, Dict
from datetime import datetime

from .search_problem import SearchProblem, SearchSolution
from ..models.search_node import SearchNode
from ..models.state import State


class AStarSearch:
    """
    A* Search algorithm implementation.
    
    A* is the most widely used informed search algorithm. It combines
    the cost-so-far g(n) from UCS with the heuristic estimate h(n) from
    Greedy search to create the evaluation function f(n) = g(n) + h(n).
    
    Algorithm:
    1. Initialize priority queue with initial node (ordered by f(n))
    2. While queue is not empty:
       a. Pop node with lowest f(n) value
       b. If node is goal, return solution
       c. If not explored or found better path, expand node
       d. Add successors to queue with updated f values
    3. If queue becomes empty, return failure
    
    Time Complexity: O(b^d)
    - b = branching factor
    - d = depth of solution
    - With good heuristic, explores far fewer nodes than uninformed search
    
    Space Complexity: O(b^d)
    - Stores all generated nodes
    - Can be memory-intensive for large search spaces
    """
    
    def __init__(self, use_graph_search: bool = True, weight: float = 1.0):
        """
        Initialize A* Search algorithm.
        
        Args:
            use_graph_search: If True, use graph search (avoid revisiting states)
                            If False, use tree search (may revisit states)
            weight: Weight for heuristic (1.0 = standard A*, >1.0 = weighted A*)
                   Higher weight makes search greedier (faster but less optimal)
                   
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._use_graph_search = use_graph_search
        self._weight = weight
        self._algorithm_name = f"A* Search (w={weight})" if weight != 1.0 else "A* Search"
        self._search_strategy = "Graph Search" if use_graph_search else "Tree Search"
    
    def search(
        self, 
        problem: SearchProblem,
        max_iterations: Optional[int] = None,
        max_cost: Optional[float] = None
    ) -> SearchSolution:
        """
        Execute A* Search to find a solution to the search problem.
        
        Args:
            problem: The search problem to solve
            max_iterations: Maximum number of nodes to explore (None = unlimited)
            max_cost: Maximum f-cost to explore (None = unlimited)
            
        Returns:
            SearchSolution containing the result
            
        Time Complexity: O(b^d)
        - Best case: O(b) if heuristic leads directly to optimal solution
        - Worst case: O(b^d) if heuristic is uninformative
        - Typically much better than uninformed search
        
        Space Complexity: O(b^d)
        - Priority queue can contain many nodes
        - Explored set tracks visited states
        """
        start_time = datetime.now()
        
        # Initialize metrics
        nodes_explored = 0
        max_frontier_size = 0
        
        # Create initial node
        initial_node = problem.create_initial_node()
        
        # Calculate initial f-cost with weighted heuristic
        initial_f = initial_node.path_cost + self._weight * initial_node.heuristic
        
        # Initialize priority queue (min-heap ordered by f-cost)
        # Format: (f_cost, counter, node)
        # Counter ensures FIFO ordering for equal f-costs
        counter = 0
        frontier: List[Tuple[float, int, SearchNode]] = []
        heapq.heappush(frontier, (initial_f, counter, initial_node))
        counter += 1
        
        # Initialize explored set for graph search
        # Store state -> best_g_cost mapping to handle revisits with better costs
        explored: Dict[State, float] = {} if self._use_graph_search else None
        
        # Track memory usage (approximate)
        memory_usage = sys.getsizeof(frontier)
        if explored is not None:
            memory_usage += sys.getsizeof(explored)
        
        # Main search loop
        while frontier:
            # Update metrics
            max_frontier_size = max(max_frontier_size, len(frontier))
            
            # Check iteration limit
            if max_iterations is not None and nodes_explored >= max_iterations:
                break
            
            # Pop node with lowest f-cost
            f_cost, _, node = heapq.heappop(frontier)
            nodes_explored += 1
            
            # Check cost limit
            if max_cost is not None and f_cost > max_cost:
                continue
            
            # Goal test (test when popping, not when generating)
            if problem.is_goal(node.state):
                # Solution found!
                execution_time = (datetime.now() - start_time).total_seconds() * 1000
                return SearchSolution(
                    success=True,
                    goal_node=node,
                    path=problem.get_solution(node),
                    path_cost=node.path_cost,
                    nodes_explored=nodes_explored,
                    max_frontier_size=max_frontier_size,
                    execution_time_ms=execution_time,
                    algorithm_name=self._algorithm_name,
                    search_strategy=self._search_strategy,
                    memory_usage_bytes=memory_usage
                )
            
            # Graph search: skip if already explored with equal or better g-cost
            if self._use_graph_search:
                if node.state in explored and explored[node.state] <= node.path_cost:
                    continue
                explored[node.state] = node.path_cost
                memory_usage += sys.getsizeof(node.state)
            
            # Expand node
            successors = problem.expand(node)
            
            # Add successors to priority queue
            for successor in successors:
                # Graph search: only add if not explored or found better path
                if self._use_graph_search:
                    if successor.state in explored and explored[successor.state] <= successor.path_cost:
                        continue
                
                # Calculate f-cost with weighted heuristic
                successor_f = successor.path_cost + self._weight * successor.heuristic
                
                heapq.heappush(frontier, (successor_f, counter, successor))
                counter += 1
                memory_usage += sys.getsizeof(successor)
        
        # No solution found
        execution_time = (datetime.now() - start_time).total_seconds() * 1000
        return SearchSolution(
            success=False,
            goal_node=None,
            path=[],
            path_cost=float('inf'),
            nodes_explored=nodes_explored,
            max_frontier_size=max_frontier_size,
            execution_time_ms=execution_time,
            algorithm_name=self._algorithm_name,
            search_strategy=self._search_strategy,
            memory_usage_bytes=memory_usage
        )
    
    def __str__(self) -> str:
        """String representation of the algorithm."""
        return f"{self._algorithm_name} ({self._search_strategy})"
    
    @staticmethod
    def get_algorithm_info() -> str:
        """
        Get detailed information about the A* Search algorithm.
        
        Returns:
            Formatted string with algorithm properties and characteristics
        """
        return """
        A* Search Algorithm
        ===================
        
        Type: Informed Search Algorithm (Best-First Search)
        
        Properties:
        -----------
        - Complete: YES (with admissible heuristic)
        - Optimal: YES (with admissible + consistent heuristic)
        - Time Complexity: O(b^d) exponential
        - Space Complexity: O(b^d) exponential
        
        Where:
        - b = branching factor
        - d = depth of optimal solution
        - Performance heavily depends on heuristic quality
        
        Characteristics:
        ---------------
        - Evaluation function: f(n) = g(n) + h(n)
        - g(n) = path cost from start to node n
        - h(n) = estimated cost from node n to goal
        - Combines benefits of UCS (optimality) and Greedy (efficiency)
        - Uses priority queue ordered by f(n)
        
        Best Use Cases:
        --------------
        - Need optimal solution
        - Good admissible heuristic available
        - Search space not too large
        - Balance between speed and optimality required
        
        Limitations:
        -----------
        - Exponential space complexity (stores all generated nodes)
        - Can be slow if heuristic is weak
        - Requires domain-specific heuristic
        - Memory intensive for large search spaces
        
        Heuristic Properties:
        --------------------
        
        Admissible Heuristic:
        - Never overestimates cost to goal: h(n) ≤ h*(n)
        - h*(n) is true cost to nearest goal
        - Guarantees optimality of A*
        - Examples: straight-line distance, pattern databases
        
        Consistent (Monotonic) Heuristic:
        - h(n) ≤ c(n,a,n') + h(n') for every action a
        - Stronger than admissibility
        - Guarantees optimal path to every expanded node
        - Allows goal test when generating (not just expanding)
        
        Dominant Heuristic:
        - h2 dominates h1 if h2(n) ≥ h1(n) for all n
        - Higher heuristic values → fewer nodes expanded
        - Must still be admissible
        - Better heuristic = better performance
        
        Algorithm Variants:
        ------------------
        
        Weighted A* (WA*):
        - f(n) = g(n) + w·h(n) where w > 1
        - Trades optimality for speed
        - Solution cost ≤ w × optimal cost
        - Useful when approximate solutions acceptable
        
        Iterative Deepening A* (IDA*):
        - Space-efficient variant using depth-first search
        - Uses f-cost limit instead of depth limit
        - Space: O(d) instead of O(b^d)
        - Time: slightly worse due to regeneration
        
        Memory-Bounded A*:
        - SMA* (Simplified Memory-bounded A*)
        - Drops worst nodes when memory full
        - More complex but space-efficient
        
        Comparison with Other Algorithms:
        --------------------------------
        
        vs UCS (Uniform Cost Search):
        - UCS: f(n) = g(n) only
        - A*: f(n) = g(n) + h(n)
        - A* more efficient with good heuristic
        - Both optimal with admissible h
        
        vs Greedy Best-First:
        - Greedy: f(n) = h(n) only
        - A*: f(n) = g(n) + h(n)
        - Greedy faster but not optimal
        - A* balances both factors
        
        vs Dijkstra's Algorithm:
        - Dijkstra is special case of A* with h(n) = 0
        - A* more efficient with good heuristic
        - Both find optimal paths
        
        Optimality Proof:
        ----------------
        
        Theorem: A* with admissible heuristic is optimal.
        
        Proof Sketch:
        1. Suppose A* returns suboptimal goal G2 with cost f2
        2. Let G1 be optimal goal with cost f1 < f2
        3. Let n be unexpanded node on path to G1
        4. f(n) = g(n) + h(n) ≤ g(n) + h*(n) = f1 (admissibility)
        5. Therefore f(n) < f2, so n expanded before G2
        6. Contradiction! A* cannot return G2 before G1
        
        Heuristic Design Guidelines:
        ---------------------------
        
        For Workout Planning:
        1. Gap-based: difference between current and target state
        2. Count-based: remaining exercises needed
        3. Time-based: estimated time to complete workout
        4. Fitness-based: fitness level progression needed
        
        Requirements:
        - Must never overestimate (admissible)
        - Should be easy to compute (efficient)
        - Should be informative (close to h*)
        - Domain-specific knowledge helps
        
        Performance Considerations:
        --------------------------
        - Better heuristic → fewer nodes expanded
        - Branching factor has exponential impact
        - Goal depth significantly affects runtime
        - Memory can be bottleneck for large spaces
        - Graph search essential for optimality
        
        Implementation Notes:
        --------------------
        - Priority queue: min-heap for O(log n) operations
        - Goal test: when expanding node (ensures optimality)
        - Tie-breaking: use counter for FIFO among equal f-costs
        - State tracking: map state to best g-cost (graph search)
        - Reopening: allow revisiting with better g-cost
        """


# Example usage and testing
if __name__ == "__main__":
    print(AStarSearch.get_algorithm_info())
