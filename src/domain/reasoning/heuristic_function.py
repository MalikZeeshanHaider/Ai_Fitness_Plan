"""
Heuristic Functions for Informed Search Algorithms.

A heuristic function h(n) estimates the cost from node n to the goal.
It's used in informed search algorithms like Greedy Best-First and A*.

Properties of Good Heuristics:
1. Admissible: Never overestimates (h(n) ≤ true cost)
2. Consistent: h(n) ≤ cost(n, n') + h(n') (triangle inequality)
3. Informative: Provides good guidance toward goal
4. Efficient: Fast to compute

Common Heuristics:
- Euclidean distance: √((x₁-x₂)² + (y₁-y₂)²)
- Manhattan distance: |x₁-x₂| + |y₁-y₂|
- Hamming distance: number of differing attributes
- Domain-specific heuristics

Time Complexity: O(1) for heuristic computation
Space Complexity: O(1)
"""

from typing import Optional, Callable, Dict, Any, List
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import math

from ..models.state import State, ExperienceLevel, FitnessGoal
from ..models.action import Action, Difficulty, ExerciseType


class HeuristicType(Enum):
    """Types of heuristic functions."""
    EUCLIDEAN = "euclidean"  # Straight-line distance
    MANHATTAN = "manhattan"  # Sum of absolute differences
    HAMMING = "hamming"  # Number of differences
    CUSTOM = "custom"  # Domain-specific


@dataclass
class HeuristicResult:
    """
    Result of heuristic evaluation.
    
    Attributes:
        value: Estimated cost to goal
        heuristic_type: Type of heuristic used
        components: Breakdown of heuristic components
        is_admissible: Whether heuristic is admissible
        explanation: Human-readable explanation
    """
    value: float
    heuristic_type: HeuristicType
    components: Dict[str, float]
    is_admissible: bool = True
    explanation: str = ""
    
    def __str__(self) -> str:
        """String representation."""
        return f"h(n) = {self.value:.2f} ({self.heuristic_type.value})"


class HeuristicFunction(ABC):
    """
    Abstract base class for heuristic functions.
    
    A heuristic function estimates the cost from a state to the goal.
    It must be:
    - Fast to compute (called many times during search)
    - Admissible (never overestimate) for A* optimality
    - Consistent for A* efficiency
    
    The heuristic guides the search toward promising paths,
    reducing the number of nodes explored.
    
    Admissibility:
    - h(n) ≤ h*(n) where h*(n) is true cost to goal
    - Guarantees A* finds optimal solution
    - Never reject optimal path
    
    Consistency (Monotonicity):
    - h(n) ≤ cost(n, n') + h(n') for all successors n'
    - Triangle inequality property
    - Ensures we never re-explore nodes in A*
    
    Time Complexity: O(1) for most heuristics
    Space Complexity: O(1)
    """
    
    def __init__(self, name: str, heuristic_type: HeuristicType):
        """
        Initialize heuristic function.
        
        Args:
            name: Heuristic name
            heuristic_type: Type of heuristic
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._name = name
        self._heuristic_type = heuristic_type
        self._calls = 0
        self._total_value = 0.0
    
    @abstractmethod
    def evaluate(self, state: State, goal_state: State) -> HeuristicResult:
        """
        Evaluate heuristic for a state.
        
        Args:
            state: Current state
            goal_state: Goal state
            
        Returns:
            Heuristic result with estimated cost
            
        Time Complexity: O(1) typically
        Space Complexity: O(1)
        """
        pass
    
    def __call__(self, state: State, goal_state: State) -> float:
        """
        Callable interface for heuristic.
        
        Args:
            state: Current state
            goal_state: Goal state
            
        Returns:
            Heuristic value
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        result = self.evaluate(state, goal_state)
        self._calls += 1
        self._total_value += result.value
        return result.value
    
    @property
    def name(self) -> str:
        """Get heuristic name."""
        return self._name
    
    @property
    def heuristic_type(self) -> HeuristicType:
        """Get heuristic type."""
        return self._heuristic_type
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get heuristic statistics.
        
        Returns:
            Dictionary with statistics
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return {
            "name": self._name,
            "type": self._heuristic_type.value,
            "calls": self._calls,
            "average_value": self._total_value / self._calls if self._calls > 0 else 0.0
        }
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self._name} ({self._heuristic_type.value})"


class WorkoutHeuristic(HeuristicFunction):
    """
    Domain-specific heuristic for workout recommendation.
    
    This heuristic estimates how far a current state is from goal state.
    It considers multiple fitness dimensions:
    
    1. Experience Level Gap:
       - Distance from current to target experience level
       - Measured in progression steps
    
    2. Fitness Goal Alignment:
       - Penalty if current path doesn't align with goal
       - Weight loss needs different approach than muscle gain
    
    3. Progress Toward Goals:
       - Weighted sum of attribute differences
       - Weight, strength, endurance, flexibility gaps
    
    4. Safety Considerations:
       - Injury status affects cost estimation
       - Energy level impacts feasibility
    
    The heuristic is admissible (never overestimates) because:
    - Each component represents minimum steps needed
    - We use optimistic estimates
    - No hidden costs are ignored
    
    Properties:
    - Admissible: Yes (optimistic estimates)
    - Consistent: Yes (obeys triangle inequality)
    - Informative: Guides search toward goal-aligned workouts
    - Fast: O(1) computation
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    
    def __init__(
        self,
        name: str = "Workout Distance Heuristic",
        weights: Optional[Dict[str, float]] = None
    ):
        """
        Initialize workout heuristic.
        
        Args:
            name: Heuristic name
            weights: Weights for different components
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        super().__init__(name, HeuristicType.CUSTOM)
        
        # Default weights for heuristic components
        self._weights = weights or {
            "experience": 10.0,      # Experience level gap
            "fitness_goal": 5.0,     # Goal alignment
            "weight": 1.0,           # Weight difference
            "strength": 0.5,         # Strength difference
            "endurance": 0.5,        # Endurance difference
            "flexibility": 0.3,      # Flexibility difference
            "injury_penalty": 20.0,  # Injury present
            "energy_factor": 0.5     # Energy impact
        }
    
    def evaluate(self, state: State, goal_state: State) -> HeuristicResult:
        """
        Evaluate workout heuristic.
        
        Computes estimated "distance" from current state to goal state
        by summing weighted differences across all fitness dimensions.
        
        Args:
            state: Current fitness state
            goal_state: Target fitness state
            
        Returns:
            Heuristic result with estimated cost
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        components = {}
        
        # 1. Experience level gap
        experience_gap = self._experience_distance(
            state.experience_level,
            goal_state.experience_level
        )
        components["experience"] = experience_gap * self._weights["experience"]
        
        # 2. Fitness goal alignment (binary: aligned or not)
        goal_aligned = (state.fitness_goal == goal_state.fitness_goal)
        components["goal_alignment"] = 0.0 if goal_aligned else self._weights["fitness_goal"]
        
        # 3. Weight difference (absolute)
        if state.weight is not None and goal_state.weight is not None:
            weight_diff = abs(state.weight - goal_state.weight)
            components["weight"] = weight_diff * self._weights["weight"]
        else:
            components["weight"] = 0.0
        
        # 4. Strength difference
        strength_diff = abs(state.strength_level - goal_state.strength_level)
        components["strength"] = strength_diff * self._weights["strength"]
        
        # 5. Endurance difference
        endurance_diff = abs(state.endurance_level - goal_state.endurance_level)
        components["endurance"] = endurance_diff * self._weights["endurance"]
        
        # 6. Flexibility difference
        flexibility_diff = abs(state.flexibility_level - goal_state.flexibility_level)
        components["flexibility"] = flexibility_diff * self._weights["flexibility"]
        
        # 7. Injury penalty (if currently injured, goal achievement harder)
        if state.has_injury:
            components["injury"] = self._weights["injury_penalty"]
        else:
            components["injury"] = 0.0
        
        # 8. Energy factor (low energy increases difficulty)
        energy_penalty = (100 - state.energy_level) / 100 * self._weights["energy_factor"]
        components["energy"] = energy_penalty
        
        # Sum all components
        total_heuristic = sum(components.values())
        
        # Build explanation
        explanation = self._build_explanation(components, state, goal_state)
        
        return HeuristicResult(
            value=total_heuristic,
            heuristic_type=self._heuristic_type,
            components=components,
            is_admissible=True,  # This heuristic is admissible (optimistic)
            explanation=explanation
        )
    
    def _experience_distance(
        self,
        current: ExperienceLevel,
        goal: ExperienceLevel
    ) -> float:
        """
        Compute distance between experience levels.
        
        Experience levels form a progression:
        beginner → intermediate → advanced
        
        Args:
            current: Current experience level
            goal: Goal experience level
            
        Returns:
            Number of progression steps
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        level_order = {
            ExperienceLevel.BEGINNER: 0,
            ExperienceLevel.INTERMEDIATE: 1,
            ExperienceLevel.ADVANCED: 2
        }
        
        current_order = level_order.get(current, 0)
        goal_order = level_order.get(goal, 0)
        
        # Distance is absolute difference
        # (can't skip levels)
        return abs(goal_order - current_order)
    
    def _build_explanation(
        self,
        components: Dict[str, float],
        state: State,
        goal_state: State
    ) -> str:
        """
        Build human-readable explanation of heuristic.
        
        Args:
            components: Heuristic components
            state: Current state
            goal_state: Goal state
            
        Returns:
            Explanation string
            
        Time Complexity: O(k) where k is components
        Space Complexity: O(k)
        """
        lines = ["Heuristic breakdown:"]
        
        # Sort components by value (highest first)
        sorted_components = sorted(
            components.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        for component, value in sorted_components:
            if value > 0:
                lines.append(f"  {component}: {value:.2f}")
        
        total = sum(components.values())
        lines.append(f"  TOTAL: {total:.2f}")
        
        return "\n".join(lines)
    
    def is_goal_reached(self, state: State, goal_state: State, tolerance: float = 1.0) -> bool:
        """
        Check if state is close enough to goal.
        
        Args:
            state: Current state
            goal_state: Goal state
            tolerance: Maximum acceptable heuristic value
            
        Returns:
            True if goal reached, False otherwise
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        result = self.evaluate(state, goal_state)
        return result.value <= tolerance


class ManhattanHeuristic(HeuristicFunction):
    """
    Manhattan distance heuristic.
    
    Manhattan distance is the sum of absolute differences:
    h(n) = |x₁ - x₂| + |y₁ - y₂| + ...
    
    It's admissible when we can only move along grid lines
    (no diagonal moves).
    
    For workout system, we compute Manhattan distance across
    all numeric fitness attributes.
    
    Properties:
    - Admissible: Yes (if no diagonal moves)
    - Consistent: Yes
    - Simpler than Euclidean
    - Works well for grid-like spaces
    
    Time Complexity: O(k) where k is attributes
    Space Complexity: O(1)
    """
    
    def __init__(self, name: str = "Manhattan Distance"):
        """Initialize Manhattan heuristic."""
        super().__init__(name, HeuristicType.MANHATTAN)
    
    def evaluate(self, state: State, goal_state: State) -> HeuristicResult:
        """
        Compute Manhattan distance.
        
        Args:
            state: Current state
            goal_state: Goal state
            
        Returns:
            Heuristic result
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        components = {}
        
        # Sum absolute differences
        components["strength"] = abs(state.strength_level - goal_state.strength_level)
        components["endurance"] = abs(state.endurance_level - goal_state.endurance_level)
        components["flexibility"] = abs(state.flexibility_level - goal_state.flexibility_level)
        
        if state.weight is not None and goal_state.weight is not None:
            components["weight"] = abs(state.weight - goal_state.weight)
        
        total = sum(components.values())
        
        return HeuristicResult(
            value=total,
            heuristic_type=self._heuristic_type,
            components=components,
            is_admissible=True,
            explanation=f"Manhattan distance: {total:.2f}"
        )


class EuclideanHeuristic(HeuristicFunction):
    """
    Euclidean distance heuristic.
    
    Euclidean distance is straight-line distance:
    h(n) = √((x₁-x₂)² + (y₁-y₂)² + ...)
    
    It's admissible when we can move in any direction
    (straight line is shortest path).
    
    Properties:
    - Admissible: Yes (straight line is shortest)
    - Consistent: Yes
    - More accurate than Manhattan
    - Slightly more expensive to compute (sqrt)
    
    Time Complexity: O(k) where k is attributes
    Space Complexity: O(1)
    """
    
    def __init__(self, name: str = "Euclidean Distance"):
        """Initialize Euclidean heuristic."""
        super().__init__(name, HeuristicType.EUCLIDEAN)
    
    def evaluate(self, state: State, goal_state: State) -> HeuristicResult:
        """
        Compute Euclidean distance.
        
        Args:
            state: Current state
            goal_state: Goal state
            
        Returns:
            Heuristic result
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        components = {}
        
        # Squared differences
        strength_diff = (state.strength_level - goal_state.strength_level) ** 2
        endurance_diff = (state.endurance_level - goal_state.endurance_level) ** 2
        flexibility_diff = (state.flexibility_level - goal_state.flexibility_level) ** 2
        
        components["strength"] = strength_diff
        components["endurance"] = endurance_diff
        components["flexibility"] = flexibility_diff
        
        if state.weight is not None and goal_state.weight is not None:
            weight_diff = (state.weight - goal_state.weight) ** 2
            components["weight"] = weight_diff
        
        # Euclidean distance
        sum_squared = sum(components.values())
        euclidean_distance = math.sqrt(sum_squared)
        
        return HeuristicResult(
            value=euclidean_distance,
            heuristic_type=self._heuristic_type,
            components=components,
            is_admissible=True,
            explanation=f"Euclidean distance: {euclidean_distance:.2f}"
        )


class ZeroHeuristic(HeuristicFunction):
    """
    Zero heuristic (always returns 0).
    
    This turns A* into Uniform Cost Search.
    Useful for:
    - Debugging
    - Guaranteeing completeness
    - When no good heuristic available
    
    Properties:
    - Admissible: Yes (trivially, 0 ≤ true cost)
    - Consistent: Yes
    - Uninformative: No guidance
    - A* becomes UCS
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    
    def __init__(self, name: str = "Zero Heuristic"):
        """Initialize zero heuristic."""
        super().__init__(name, HeuristicType.CUSTOM)
    
    def evaluate(self, state: State, goal_state: State) -> HeuristicResult:
        """
        Return zero heuristic.
        
        Args:
            state: Current state (ignored)
            goal_state: Goal state (ignored)
            
        Returns:
            Zero heuristic result
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return HeuristicResult(
            value=0.0,
            heuristic_type=self._heuristic_type,
            components={},
            is_admissible=True,
            explanation="Zero heuristic (A* becomes UCS)"
        )


def create_default_heuristic() -> HeuristicFunction:
    """
    Create default heuristic for workout system.
    
    Returns:
        WorkoutHeuristic with balanced weights
        
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    return WorkoutHeuristic()


def compare_heuristics(
    state: State,
    goal_state: State,
    heuristics: List[HeuristicFunction]
) -> Dict[str, HeuristicResult]:
    """
    Compare multiple heuristics on same state.
    
    Args:
        state: Current state
        goal_state: Goal state
        heuristics: List of heuristics to compare
        
    Returns:
        Dictionary of heuristic name → result
        
    Time Complexity: O(h) where h is number of heuristics
    Space Complexity: O(h)
    """
    results = {}
    
    for heuristic in heuristics:
        result = heuristic.evaluate(state, goal_state)
        results[heuristic.name] = result
    
    return results


# Example usage and testing
if __name__ == "__main__":
    print("Heuristic Functions for Search")
    print("==============================")
    print()
    
    # Create sample states
    current_state = State(
        experience_level=ExperienceLevel.BEGINNER,
        fitness_goal=FitnessGoal.WEIGHT_LOSS,
        strength_level=30.0,
        endurance_level=40.0,
        flexibility_level=35.0,
        weight=80.0,
        energy_level=70.0,
        has_injury=False
    )
    
    goal_state = State(
        experience_level=ExperienceLevel.INTERMEDIATE,
        fitness_goal=FitnessGoal.WEIGHT_LOSS,
        strength_level=50.0,
        endurance_level=60.0,
        flexibility_level=50.0,
        weight=70.0,
        energy_level=80.0,
        has_injury=False
    )
    
    # Test different heuristics
    heuristics = [
        WorkoutHeuristic(),
        ManhattanHeuristic(),
        EuclideanHeuristic(),
        ZeroHeuristic()
    ]
    
    print("Current State:")
    print(f"  Experience: {current_state.experience_level}")
    print(f"  Strength: {current_state.strength_level}")
    print(f"  Endurance: {current_state.endurance_level}")
    print()
    
    print("Goal State:")
    print(f"  Experience: {goal_state.experience_level}")
    print(f"  Strength: {goal_state.strength_level}")
    print(f"  Endurance: {goal_state.endurance_level}")
    print()
    
    print("Heuristic Comparison:")
    results = compare_heuristics(current_state, goal_state, heuristics)
    
    for name, result in results.items():
        print(f"\n{name}:")
        print(f"  Value: {result.value:.2f}")
        print(f"  Type: {result.heuristic_type.value}")
        print(f"  Admissible: {result.is_admissible}")
