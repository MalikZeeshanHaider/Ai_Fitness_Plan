"""
Action Module
=============

Defines the Action class representing workout actions that can be
taken to transition between states in the state-space search.

In AI problem solving:
- ACTIONS: Available operations that can be applied to a state
- ACTION COST: Cost associated with performing an action
- PRECONDITIONS: Conditions that must be satisfied to execute action
- EFFECTS: How the action modifies the state

Author: AI Engineer
Date: December 17, 2025
"""

from dataclasses import dataclass, field
from typing import Set, FrozenSet, Optional
from enum import Enum


class ActionType(Enum):
    """
    Type of workout action.
    
    Used for categorizing and filtering actions.
    """
    ADD_EXERCISE = "add_exercise"
    SKIP_EXERCISE = "skip_exercise"
    MODIFY_INTENSITY = "modify_intensity"
    ADD_REST = "add_rest"


class Difficulty(Enum):
    """Exercise difficulty levels."""
    BEGINNER = "beginner"
    EASY = "easy"
    INTERMEDIATE = "intermediate"
    MODERATE = "moderate"
    ADVANCED = "advanced"
    HARD = "hard"
    EXPERT = "expert"


class ExerciseType(Enum):
    """Exercise type/category for actions."""
    CARDIO = "cardio"
    STRENGTH = "strength"
    FLEXIBILITY = "flexibility"
    BALANCE = "balance"
    ENDURANCE = "endurance"
    HIIT = "hiit"
    RESISTANCE = "resistance"
    COMPOUND = "compound"
    BODYWEIGHT = "bodyweight"
    HIGH_IMPACT = "high_impact"
    STRETCHING = "stretching"
    WARMUP = "warmup"
    COOLDOWN = "cooldown"


@dataclass(frozen=True)
class Action:
    """
    Immutable representation of a workout action.
    
    An action represents adding an exercise to the workout plan.
    Each action has:
    - Preconditions: What must be true to execute this action
    - Effects: How the state changes after execution
    - Cost: Path cost for search algorithms
    
    This is a key component of PROBLEM SOLVING in AI, where actions
    define the state space and enable search algorithms to find
    optimal workout plans.
    
    Attributes:
        action_id: Unique identifier for this action
        action_type: Type of action (add exercise, skip, etc.)
        exercise_name: Name of the exercise
        exercise_category: Category (cardio, strength, flexibility)
        muscle_groups: Primary muscle groups targeted (immutable set)
        secondary_muscles: Secondary muscle groups (immutable set)
        difficulty: Exercise difficulty level
        equipment_required: Equipment needed (immutable set)
        estimated_calories: Estimated calories burned
        estimated_duration: Estimated duration in minutes
        intensity_factor: Intensity multiplier (0.5 to 2.0)
        requires_warmup: Whether warmup is required
        requires_cooldown: Whether cooldown is required
        contraindications: Medical conditions that prevent this action
        
    Example:
        >>> action = Action(
        ...     action_id="ex_001",
        ...     action_type=ActionType.ADD_EXERCISE,
        ...     exercise_name="Barbell Bench Press",
        ...     exercise_category="strength",
        ...     muscle_groups=frozenset({"chest", "triceps", "shoulders"}),
        ...     difficulty=Difficulty.INTERMEDIATE,
        ...     equipment_required=frozenset({"barbell", "bench"})
        ... )
    """
    
    # Action Identity
    action_id: str
    action_type: ActionType
    exercise_name: str
    exercise_category: str
    
    # Muscle Groups (immutable)
    muscle_groups: FrozenSet[str] = field(default_factory=frozenset)
    secondary_muscles: FrozenSet[str] = field(default_factory=frozenset)
    
    # Exercise Characteristics
    difficulty: Difficulty = Difficulty.INTERMEDIATE
    equipment_required: FrozenSet[str] = field(default_factory=frozenset)
    
    # Metrics
    estimated_calories: float = 50.0
    estimated_duration: int = 10  # minutes
    intensity_factor: float = 1.0
    
    # Requirements
    requires_warmup: bool = False
    requires_cooldown: bool = False
    contraindications: FrozenSet[str] = field(default_factory=frozenset)
    
    # Additional metadata
    description: str = ""
    instructions: str = ""
    
    def __post_init__(self) -> None:
        """
        Validate action parameters.
        
        Raises:
            ValueError: If action parameters are invalid
        """
        if not self.action_id:
            raise ValueError("Action ID cannot be empty")
        
        if not self.exercise_name:
            raise ValueError("Exercise name cannot be empty")
        
        if self.estimated_calories < 0:
            raise ValueError(f"Calories cannot be negative: {self.estimated_calories}")
        
        if self.estimated_duration <= 0:
            raise ValueError(f"Duration must be positive: {self.estimated_duration}")
        
        if not 0.1 <= self.intensity_factor <= 3.0:
            raise ValueError(f"Intensity factor must be between 0.1 and 3.0: {self.intensity_factor}")
    
    def is_applicable(
        self,
        available_equipment: Set[str],
        experience_level: str,
        medical_conditions: Set[str],
        worked_muscles: Set[str],
        fatigue_level: float
    ) -> bool:
        """
        Check if action can be applied given current state (PRECONDITIONS).
        
        This implements ACTION PRECONDITION checking in AI problem solving.
        An action can only be applied if all preconditions are satisfied.
        
        Args:
            available_equipment: Equipment available to user
            experience_level: User's experience level
            medical_conditions: User's medical conditions
            worked_muscles: Muscle groups already worked
            fatigue_level: Current fatigue level (0.0 to 1.0)
            
        Returns:
            bool: True if action can be applied
            
        Example:
            >>> if action.is_applicable(
            ...     available_equipment={"barbell", "bench"},
            ...     experience_level="intermediate",
            ...     medical_conditions=set(),
            ...     worked_muscles={"legs"},
            ...     fatigue_level=0.5
            ... ):
            ...     print("Action can be applied!")
        """
        # Check equipment availability
        if not self._check_equipment(available_equipment):
            return False
        
        # Check experience level compatibility
        if not self._check_experience_level(experience_level):
            return False
        
        # Check medical contraindications
        if not self._check_contraindications(medical_conditions):
            return False
        
        # Check if muscle groups need rest (already heavily worked)
        if self._muscle_groups_overworked(worked_muscles):
            return False
        
        # Check fatigue level
        if fatigue_level > 0.85:  # Too fatigued for more exercises
            return False
        
        return True
    
    def _check_equipment(self, available_equipment: Set[str]) -> bool:
        """
        Check if required equipment is available.
        
        Args:
            available_equipment: Set of available equipment
            
        Returns:
            bool: True if all required equipment is available
        """
        if not self.equipment_required:
            return True  # No equipment required
        
        # Convert to lowercase for case-insensitive comparison
        available_lower = {e.lower() for e in available_equipment}
        required_lower = {e.lower() for e in self.equipment_required}
        
        return required_lower.issubset(available_lower)
    
    def _check_experience_level(self, experience_level: str) -> bool:
        """
        Check if user's experience level is sufficient.
        
        Args:
            experience_level: User's experience level
            
        Returns:
            bool: True if user can perform this exercise
        """
        # Experience level hierarchy
        level_hierarchy = {
            "beginner": 1,
            "intermediate": 2,
            "advanced": 3,
            "expert": 4
        }
        
        user_level = level_hierarchy.get(experience_level.lower(), 1)
        required_level = level_hierarchy.get(self.difficulty.value, 2)
        
        # Allow exercises at user's level or below
        # Also allow intermediate users to try advanced with caution
        return user_level >= required_level - 1
    
    def _check_contraindications(self, medical_conditions: Set[str]) -> bool:
        """
        Check for medical contraindications.
        
        Args:
            medical_conditions: User's medical conditions
            
        Returns:
            bool: True if exercise is safe for user
        """
        if not self.contraindications:
            return True
        
        # Convert to lowercase for comparison
        conditions_lower = {c.lower() for c in medical_conditions}
        contraindications_lower = {c.lower() for c in self.contraindications}
        
        # Return False if any contraindication matches
        return not bool(contraindications_lower.intersection(conditions_lower))
    
    def _muscle_groups_overworked(self, worked_muscles: Set[str]) -> bool:
        """
        Check if target muscle groups have been overworked.
        
        Args:
            worked_muscles: Set of already worked muscle groups
            
        Returns:
            bool: True if muscle groups need rest
        """
        if not worked_muscles:
            return False
        
        # Convert to lowercase
        worked_lower = {m.lower() for m in worked_muscles}
        target_lower = {m.lower() for m in self.muscle_groups}
        
        # Check if all target muscles have been worked
        # (indicates they may need rest)
        overlap = target_lower.intersection(worked_lower)
        
        # If more than 80% of target muscles already worked, consider overworked
        if target_lower:
            overlap_ratio = len(overlap) / len(target_lower)
            return overlap_ratio > 0.8
        
        return False
    
    def calculate_cost(self, fatigue_level: float = 0.0) -> float:
        """
        Calculate action cost (PATH COST in search algorithms).
        
        Lower cost = more desirable action
        Cost factors:
        - Duration (time is a resource)
        - Difficulty (harder = higher cost)
        - Current fatigue (more fatigue = higher cost)
        
        Args:
            fatigue_level: Current fatigue level (0.0 to 1.0)
            
        Returns:
            float: Action cost
            
        Note:
            Used by Uniform Cost Search and A* algorithms
            to find optimal paths through the state space.
        """
        # Base cost is duration
        base_cost = float(self.estimated_duration)
        
        # Difficulty multiplier
        difficulty_multiplier = {
            Difficulty.BEGINNER: 1.0,
            Difficulty.INTERMEDIATE: 1.2,
            Difficulty.ADVANCED: 1.5,
            Difficulty.EXPERT: 2.0
        }.get(self.difficulty, 1.0)
        
        # Fatigue penalty (increases cost as fatigue increases)
        fatigue_penalty = 1.0 + (fatigue_level * 2.0)
        
        # Calculate total cost
        total_cost = base_cost * difficulty_multiplier * fatigue_penalty
        
        return total_cost
    
    def calculate_benefit(self, fitness_goal: str) -> float:
        """
        Calculate action benefit for utility-based agent.
        
        Higher benefit = more aligned with user's goal
        
        Args:
            fitness_goal: User's fitness goal
            
        Returns:
            float: Benefit score (0.0 to 1.0)
            
        Note:
            Used by utility-based agent to select actions
            that maximize expected utility.
        """
        benefit = 0.5  # Base benefit
        
        # Adjust based on fitness goal
        if fitness_goal == "weight_loss":
            # Prioritize calorie burn
            benefit += (self.estimated_calories / 200.0) * 0.3
            if self.exercise_category.lower() == "cardio":
                benefit += 0.2
        
        elif fitness_goal == "muscle_gain":
            # Prioritize strength exercises
            if self.exercise_category.lower() == "strength":
                benefit += 0.3
            # More muscle groups = better
            benefit += len(self.muscle_groups) * 0.05
        
        elif fitness_goal == "flexibility":
            if self.exercise_category.lower() in ["flexibility", "stretching"]:
                benefit += 0.4
        
        elif fitness_goal == "endurance":
            if self.exercise_category.lower() in ["cardio", "endurance"]:
                benefit += 0.3
            # Longer duration = better for endurance
            benefit += (self.estimated_duration / 30.0) * 0.1
        
        # Cap benefit at 1.0
        return min(1.0, benefit)
    
    def get_all_muscle_groups(self) -> Set[str]:
        """
        Get all muscle groups (primary + secondary).
        
        Returns:
            Set[str]: Combined set of all muscle groups
        """
        return set(self.muscle_groups) | set(self.secondary_muscles)
    
    def __str__(self) -> str:
        """String representation of action."""
        return (
            f"Action({self.exercise_name}, category={self.exercise_category}, "
            f"muscles={list(self.muscle_groups)[:2]}, difficulty={self.difficulty.value})"
        )
    
    def to_dict(self) -> dict:
        """
        Convert action to dictionary for serialization.
        
        Returns:
            dict: Dictionary representation
        """
        return {
            'action_id': self.action_id,
            'action_type': self.action_type.value,
            'exercise_name': self.exercise_name,
            'exercise_category': self.exercise_category,
            'muscle_groups': list(self.muscle_groups),
            'secondary_muscles': list(self.secondary_muscles),
            'difficulty': self.difficulty.value,
            'equipment_required': list(self.equipment_required),
            'estimated_calories': self.estimated_calories,
            'estimated_duration': self.estimated_duration,
            'description': self.description
        }
