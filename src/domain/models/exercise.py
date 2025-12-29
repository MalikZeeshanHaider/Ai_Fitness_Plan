"""
Exercise Model Module
=====================

Defines the Exercise class representing a gym exercise with all its attributes.

This is a domain entity that represents exercise data loaded from the dataset.
It serves as a data transfer object between the infrastructure and domain layers.

Author: AI Engineer
Date: December 17, 2025
"""

from dataclasses import dataclass, field
from typing import List, Set, Optional
from enum import Enum


class ExerciseCategory(Enum):
    """Exercise category enumeration."""
    CARDIO = "cardio"
    STRENGTH = "strength"
    FLEXIBILITY = "flexibility"
    BALANCE = "balance"
    ENDURANCE = "endurance"
    WARMUP = "warmup"
    COOLDOWN = "cooldown"
    STRETCHING = "stretching"
    CORE = "core"
    # Additional types for compatibility
    HIIT = "hiit"
    RESISTANCE = "resistance"
    COMPOUND = "compound"
    BODYWEIGHT = "bodyweight"
    HIGH_IMPACT = "high_impact"
    PLYOMETRICS = "plyometrics"
    FUNCTIONAL = "functional"


# Alias for backward compatibility
ExerciseType = ExerciseCategory


class IntensityLevel(Enum):
    """Exercise intensity level."""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


# Alias for backward compatibility
DifficultyLevel = IntensityLevel


@dataclass
class Exercise:
    """
    Domain model representing a gym exercise.
    
    This class encapsulates all information about a specific exercise
    including its characteristics, requirements, and estimated benefits.
    
    Unlike Action (which represents adding exercise to plan), Exercise
    is a pure data model loaded from the dataset.
    
    Attributes:
        exercise_id: Unique identifier
        name: Exercise name
        category: Exercise category
        primary_muscles: Primary muscle groups targeted
        secondary_muscles: Secondary muscle groups
        difficulty: Difficulty level (beginner/intermediate/advanced/expert)
        equipment: Required equipment
        calories_per_minute: Estimated calories burned per minute
        typical_duration_minutes: Typical duration
        intensity: Exercise intensity level
        description: Detailed description
        instructions: Step-by-step instructions
        benefits: List of benefits
        contraindications: Medical conditions to avoid
        variations: Alternative variations
        is_compound: Whether it's a compound exercise
        is_bodyweight: Whether it's bodyweight only
        
    Example:
        >>> exercise = Exercise(
        ...     exercise_id="ex_bench_press",
        ...     name="Barbell Bench Press",
        ...     category=ExerciseCategory.STRENGTH,
        ...     primary_muscles=["chest", "triceps"],
        ...     difficulty="intermediate",
        ...     equipment=["barbell", "bench"]
        ... )
    """
    
    # Identity
    exercise_id: str
    name: str
    category: ExerciseCategory
    
    # Muscle Groups
    primary_muscles: List[str] = field(default_factory=list)
    secondary_muscles: List[str] = field(default_factory=list)
    
    # Characteristics
    difficulty: str = "intermediate"
    equipment: List[str] = field(default_factory=list)
    
    # Metrics
    calories_per_minute: float = 5.0
    typical_duration_minutes: int = 10
    intensity: IntensityLevel = IntensityLevel.MODERATE
    
    # Details
    description: str = ""
    instructions: str = ""
    benefits: List[str] = field(default_factory=list)
    contraindications: List[str] = field(default_factory=list)
    variations: List[str] = field(default_factory=list)
    
    # Flags
    is_compound: bool = False  # Works multiple joints
    is_bodyweight: bool = False  # No equipment needed
    requires_spotter: bool = False
    
    # Tags for search and filtering
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        """Validate exercise data after initialization."""
        if not self.exercise_id:
            raise ValueError("Exercise ID cannot be empty")
        
        if not self.name:
            raise ValueError("Exercise name cannot be empty")
        
        if self.calories_per_minute < 0:
            raise ValueError(f"Calories per minute cannot be negative: {self.calories_per_minute}")
        
        if self.typical_duration_minutes <= 0:
            raise ValueError(f"Duration must be positive: {self.typical_duration_minutes}")
        
        # Set is_bodyweight flag if no equipment required
        if not self.equipment or self.equipment == ["none"]:
            object.__setattr__(self, 'is_bodyweight', True)
    
    @property
    def duration_minutes(self) -> int:
        """Alias for typical_duration_minutes for backward compatibility."""
        return self.typical_duration_minutes
    
    def calculate_total_calories(self, duration_minutes: Optional[int] = None) -> float:
        """
        Calculate total calories burned for given duration.
        
        Args:
            duration_minutes: Duration in minutes (uses typical if not provided)
            
        Returns:
            float: Estimated calories burned
            
        Example:
            >>> exercise = Exercise(..., calories_per_minute=8.0)
            >>> calories = exercise.calculate_total_calories(duration_minutes=15)
            >>> print(f"{calories} calories")
            120.0 calories
        """
        duration = duration_minutes if duration_minutes else self.typical_duration_minutes
        return self.calories_per_minute * duration
    
    def get_all_muscles(self) -> Set[str]:
        """
        Get all muscle groups (primary + secondary).
        
        Returns:
            Set[str]: Combined set of all muscles
        """
        return set(self.primary_muscles) | set(self.secondary_muscles)
    
    def is_suitable_for_level(self, experience_level: str) -> bool:
        """
        Check if exercise is suitable for given experience level.
        
        Args:
            experience_level: User's experience level
            
        Returns:
            bool: True if suitable
        """
        level_hierarchy = {
            "beginner": 1,
            "intermediate": 2,
            "advanced": 3,
            "expert": 4
        }
        
        user_level = level_hierarchy.get(experience_level.lower(), 1)
        exercise_level = level_hierarchy.get(self.difficulty.lower(), 2)
        
        # Allow exercises at or below user level
        return user_level >= exercise_level
    
    def requires_equipment(self, equipment_name: str) -> bool:
        """
        Check if specific equipment is required.
        
        Args:
            equipment_name: Equipment to check
            
        Returns:
            bool: True if equipment is required
        """
        return equipment_name.lower() in (e.lower() for e in self.equipment)
    
    def matches_goal(self, fitness_goal: str) -> bool:
        """
        Check if exercise matches fitness goal.
        
        Args:
            fitness_goal: User's fitness goal
            
        Returns:
            bool: True if exercise aligns with goal
        """
        goal_mappings = {
            "weight_loss": [ExerciseCategory.CARDIO, ExerciseCategory.ENDURANCE],
            "muscle_gain": [ExerciseCategory.STRENGTH],
            "flexibility": [ExerciseCategory.FLEXIBILITY, ExerciseCategory.STRETCHING],
            "endurance": [ExerciseCategory.CARDIO, ExerciseCategory.ENDURANCE],
            "general_fitness": [ExerciseCategory.CARDIO, ExerciseCategory.STRENGTH]
        }
        
        target_categories = goal_mappings.get(fitness_goal.lower(), [])
        return self.category in target_categories
    
    def has_contraindication(self, medical_condition: str) -> bool:
        """
        Check if exercise has contraindication for medical condition.
        
        Args:
            medical_condition: Medical condition to check
            
        Returns:
            bool: True if contraindicated
        """
        return medical_condition.lower() in (c.lower() for c in self.contraindications)
    
    def get_intensity_score(self) -> float:
        """
        Get numerical intensity score.
        
        Returns:
            float: Intensity score (0.0 to 1.0)
        """
        intensity_scores = {
            IntensityLevel.LOW: 0.25,
            IntensityLevel.MODERATE: 0.5,
            IntensityLevel.HIGH: 0.75,
            IntensityLevel.VERY_HIGH: 1.0
        }
        return intensity_scores.get(self.intensity, 0.5)
    
    def __str__(self) -> str:
        """String representation."""
        return (
            f"Exercise({self.name}, category={self.category.value}, "
            f"difficulty={self.difficulty}, muscles={self.primary_muscles[:2]})"
        )
    
    def to_dict(self) -> dict:
        """
        Convert to dictionary for serialization.
        
        Returns:
            dict: Dictionary representation
        """
        return {
            'exercise_id': self.exercise_id,
            'name': self.name,
            'category': self.category.value,
            'primary_muscles': self.primary_muscles,
            'secondary_muscles': self.secondary_muscles,
            'difficulty': self.difficulty,
            'equipment': self.equipment,
            'calories_per_minute': self.calories_per_minute,
            'typical_duration_minutes': self.typical_duration_minutes,
            'intensity': self.intensity.value,
            'description': self.description,
            'benefits': self.benefits,
            'is_compound': self.is_compound,
            'is_bodyweight': self.is_bodyweight
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Exercise':
        """
        Create Exercise from dictionary.
        
        Args:
            data: Dictionary containing exercise data
            
        Returns:
            Exercise: New Exercise instance
        """
        # Convert category string to enum
        category = ExerciseCategory(data.get('category', 'strength'))
        
        # Convert intensity string to enum if present
        intensity_str = data.get('intensity', 'moderate')
        intensity = IntensityLevel(intensity_str) if intensity_str else IntensityLevel.MODERATE
        
        return cls(
            exercise_id=data.get('exercise_id', ''),
            name=data.get('name', ''),
            category=category,
            primary_muscles=data.get('primary_muscles', []),
            secondary_muscles=data.get('secondary_muscles', []),
            difficulty=data.get('difficulty', 'intermediate'),
            equipment=data.get('equipment', []),
            calories_per_minute=data.get('calories_per_minute', 5.0),
            typical_duration_minutes=data.get('typical_duration_minutes', 10),
            intensity=intensity,
            description=data.get('description', ''),
            instructions=data.get('instructions', ''),
            benefits=data.get('benefits', []),
            contraindications=data.get('contraindications', []),
            variations=data.get('variations', []),
            is_compound=data.get('is_compound', False),
            is_bodyweight=data.get('is_bodyweight', False),
            requires_spotter=data.get('requires_spotter', False),
            tags=data.get('tags', [])
        )
