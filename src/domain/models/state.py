"""
State Module
============

Defines the immutable State class representing a user's fitness state
in the workout recommendation system.

This module implements STATE-SPACE SEARCH concepts where each state
represents a snapshot of the user's current fitness condition and
workout progress.

Key Concepts:
- State: Complete description of user fitness condition
- Immutability: States cannot be modified (functional programming)
- State Space: All possible fitness states the system can represent
- State Transitions: Moving from one state to another via actions

Author: AI Engineer
Date: December 17, 2025
"""

from dataclasses import dataclass, field
from typing import List, Set, FrozenSet, Optional
from enum import Enum
import hashlib


class FitnessGoal(Enum):
    """
    Enumeration of fitness goals.
    
    Used for goal-based agent decision making.
    """
    WEIGHT_LOSS = "weight_loss"
    MUSCLE_GAIN = "muscle_gain"
    FLEXIBILITY = "flexibility"
    ENDURANCE = "endurance"
    GENERAL_FITNESS = "general_fitness"


class ExperienceLevel(Enum):
    """
    User experience level for workout difficulty matching.
    """
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass(frozen=True)
class State:
    """
    Immutable representation of a user's fitness state.
    
    This class represents a STATE in the state-space search problem.
    Each state captures:
    - User characteristics (age, weight, fitness level)
    - Current fitness goals
    - Muscle groups that have been worked
    - Equipment availability
    - Accumulated workout metrics
    
    The frozen=True parameter ensures immutability, making states
    hashable and suitable for graph search algorithms (explored set).
    
    Attributes:
        user_id: Unique identifier for the user
        age: User's age in years
        weight_kg: User's weight in kilograms
        height_cm: User's height in centimeters
        fitness_goal: Primary fitness goal
        experience_level: Fitness experience level
        worked_muscle_groups: Muscle groups already worked (immutable set)
        available_equipment: Equipment available to user (immutable set)
        total_calories_burned: Accumulated calories burned
        total_workout_duration: Accumulated workout time in minutes
        exercises_completed: Number of exercises completed
        current_fatigue_level: Fatigue level (0.0 to 1.0)
        days_per_week: Target workout days per week
        session_duration_minutes: Target session duration
        medical_conditions: Any medical conditions to consider
    
    Example:
        >>> initial_state = State(
        ...     user_id="user_001",
        ...     age=25,
        ...     weight_kg=70,
        ...     height_cm=175,
        ...     fitness_goal=FitnessGoal.MUSCLE_GAIN,
        ...     experience_level=ExperienceLevel.INTERMEDIATE
        ... )
    """
    
    # User Demographics
    user_id: str
    age: int
    weight_kg: float
    height_cm: float
    
    # Fitness Characteristics
    fitness_goal: FitnessGoal
    experience_level: ExperienceLevel
    
    # Workout State (immutable collections)
    worked_muscle_groups: FrozenSet[str] = field(default_factory=frozenset)
    available_equipment: FrozenSet[str] = field(default_factory=frozenset)
    
    # Progress Metrics
    total_calories_burned: float = 0.0
    total_workout_duration: int = 0  # minutes
    exercises_completed: int = 0
    current_fatigue_level: float = 0.0  # 0.0 (fresh) to 1.0 (exhausted)
    
    # Preferences
    days_per_week: int = 3
    session_duration_minutes: int = 45
    medical_conditions: FrozenSet[str] = field(default_factory=frozenset)
    
    def __post_init__(self) -> None:
        """
        Validate state after initialization.
        
        Raises:
            ValueError: If state parameters are invalid
        """
        # Validate age
        if not 10 <= self.age <= 100:
            raise ValueError(f"Age must be between 10 and 100, got {self.age}")
        
        # Validate weight
        if not 30 <= self.weight_kg <= 300:
            raise ValueError(f"Weight must be between 30 and 300 kg, got {self.weight_kg}")
        
        # Validate height
        if not 100 <= self.height_cm <= 250:
            raise ValueError(f"Height must be between 100 and 250 cm, got {self.height_cm}")
        
        # Validate fatigue level
        if not 0.0 <= self.current_fatigue_level <= 1.0:
            raise ValueError(f"Fatigue level must be between 0.0 and 1.0, got {self.current_fatigue_level}")
        
        # Validate days per week
        if not 1 <= self.days_per_week <= 7:
            raise ValueError(f"Days per week must be between 1 and 7, got {self.days_per_week}")
    
    def is_goal_state(self, target_exercises: int, target_duration: int) -> bool:
        """
        Check if this state represents a goal state.
        
        A goal state is reached when:
        - Target number of exercises completed
        - Target duration achieved
        - Fatigue level is acceptable
        
        Args:
            target_exercises: Target number of exercises
            target_duration: Target duration in minutes
            
        Returns:
            bool: True if this is a goal state
            
        Example:
            >>> state.is_goal_state(target_exercises=6, target_duration=45)
            True
        """
        return (
            self.exercises_completed >= target_exercises
            and self.total_workout_duration >= target_duration
            and self.current_fatigue_level < 0.9  # Not too fatigued
        )
    
    def calculate_bmi(self) -> float:
        """
        Calculate Body Mass Index.
        
        BMI = weight(kg) / (height(m))^2
        
        Returns:
            float: BMI value
            
        Example:
            >>> state = State(..., weight_kg=70, height_cm=175)
            >>> bmi = state.calculate_bmi()
            >>> print(f"{bmi:.2f}")
            22.86
        """
        height_m = self.height_cm / 100.0
        return self.weight_kg / (height_m ** 2)
    
    def get_intensity_factor(self) -> float:
        """
        Calculate recommended intensity factor based on experience level.
        
        Returns:
            float: Intensity multiplier (0.5 to 1.5)
            
        Note:
            Used by agents to adjust workout difficulty
        """
        intensity_map = {
            ExperienceLevel.BEGINNER: 0.5,
            ExperienceLevel.INTERMEDIATE: 0.8,
            ExperienceLevel.ADVANCED: 1.1,
            ExperienceLevel.EXPERT: 1.4,
        }
        return intensity_map.get(self.experience_level, 1.0)
    
    @property
    def has_injury(self) -> bool:
        """
        Check if user has any medical conditions/injuries.
        
        Returns:
            bool: True if user has medical conditions
        """
        return len(self.medical_conditions) > 0
    
    @property
    def energy_level(self) -> float:
        """
        Calculate energy level based on fatigue.
        
        Energy is the inverse of fatigue, scaled 0-100.
        
        Returns:
            float: Energy level (0-100)
        """
        return (1.0 - self.current_fatigue_level) * 100.0
    
    def has_equipment(self, equipment: str) -> bool:
        """
        Check if specific equipment is available.
        
        Args:
            equipment: Equipment name to check
            
        Returns:
            bool: True if equipment is available
        """
        return equipment.lower() in (e.lower() for e in self.available_equipment)
    
    def has_worked_muscle_group(self, muscle_group: str) -> bool:
        """
        Check if a muscle group has already been worked.
        
        Args:
            muscle_group: Muscle group name to check
            
        Returns:
            bool: True if muscle group has been worked
        """
        return muscle_group.lower() in (m.lower() for m in self.worked_muscle_groups)
    
    def transition(
        self,
        exercise_name: str,
        muscle_groups: Set[str],
        calories: float,
        duration: int,
        fatigue_increase: float = 0.1
    ) -> 'State':
        """
        Create a new state by transitioning from current state.
        
        This implements STATE TRANSITION in state-space search.
        States are immutable, so we create a new state with updated values.
        
        Args:
            exercise_name: Name of exercise performed
            muscle_groups: Set of muscle groups worked
            calories: Calories burned
            duration: Exercise duration in minutes
            fatigue_increase: Fatigue increase (0.0 to 1.0)
            
        Returns:
            State: New state after transition
            
        Example:
            >>> new_state = current_state.transition(
            ...     exercise_name="Push-ups",
            ...     muscle_groups={"chest", "triceps"},
            ...     calories=50,
            ...     duration=5
            ... )
        """
        # Combine existing and new muscle groups
        new_muscle_groups = frozenset(self.worked_muscle_groups | muscle_groups)
        
        # Calculate new fatigue level (capped at 1.0)
        new_fatigue = min(1.0, self.current_fatigue_level + fatigue_increase)
        
        # Create new state with updated values
        return State(
            user_id=self.user_id,
            age=self.age,
            weight_kg=self.weight_kg,
            height_cm=self.height_cm,
            fitness_goal=self.fitness_goal,
            experience_level=self.experience_level,
            worked_muscle_groups=new_muscle_groups,
            available_equipment=self.available_equipment,
            total_calories_burned=self.total_calories_burned + calories,
            total_workout_duration=self.total_workout_duration + duration,
            exercises_completed=self.exercises_completed + 1,
            current_fatigue_level=new_fatigue,
            days_per_week=self.days_per_week,
            session_duration_minutes=self.session_duration_minutes,
            medical_conditions=self.medical_conditions
        )
    
    def __hash__(self) -> int:
        """
        Generate hash for state (required for graph search explored set).
        
        Returns:
            int: Hash value for this state
            
        Note:
            Used to efficiently check if a state has been explored
            in graph search algorithms.
        """
        # Create a unique string representation
        state_repr = (
            f"{self.user_id}|{self.exercises_completed}|"
            f"{self.total_workout_duration}|{self.current_fatigue_level:.2f}|"
            f"{'|'.join(sorted(self.worked_muscle_groups))}"
        )
        return hash(state_repr)
    
    def __eq__(self, other: object) -> bool:
        """
        Check equality between states.
        
        Args:
            other: Another state to compare
            
        Returns:
            bool: True if states are equal
        """
        if not isinstance(other, State):
            return False
        
        return (
            self.user_id == other.user_id
            and self.exercises_completed == other.exercises_completed
            and self.total_workout_duration == other.total_workout_duration
            and abs(self.current_fatigue_level - other.current_fatigue_level) < 0.01
            and self.worked_muscle_groups == other.worked_muscle_groups
        )
    
    def __str__(self) -> str:
        """
        String representation of state.
        
        Returns:
            str: Human-readable state description
        """
        return (
            f"State(user={self.user_id}, goal={self.fitness_goal.value}, "
            f"exercises={self.exercises_completed}, duration={self.total_workout_duration}min, "
            f"calories={self.total_calories_burned:.0f}, fatigue={self.current_fatigue_level:.2f})"
        )
    
    def to_dict(self) -> dict:
        """
        Convert state to dictionary for serialization.
        
        Returns:
            dict: Dictionary representation of state
        """
        return {
            'user_id': self.user_id,
            'age': self.age,
            'weight_kg': self.weight_kg,
            'height_cm': self.height_cm,
            'fitness_goal': self.fitness_goal.value,
            'experience_level': self.experience_level.value,
            'worked_muscle_groups': list(self.worked_muscle_groups),
            'available_equipment': list(self.available_equipment),
            'total_calories_burned': self.total_calories_burned,
            'total_workout_duration': self.total_workout_duration,
            'exercises_completed': self.exercises_completed,
            'current_fatigue_level': self.current_fatigue_level,
            'bmi': self.calculate_bmi()
        }
