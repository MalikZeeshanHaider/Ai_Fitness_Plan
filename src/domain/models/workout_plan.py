"""
Workout Plan Model Module
==========================

Defines the WorkoutPlan class representing a complete workout plan
with exercises, reasoning, and metadata.

This is the final output of the intelligent agent system - a personalized
workout plan with full justification and alternatives.

Author: AI Engineer
Date: December 17, 2025
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from datetime import datetime
from enum import Enum
from src.domain.models.exercise import Exercise
from src.domain.models.state import State, FitnessGoal


class PlanStatus(Enum):
    """Status of workout plan."""
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


@dataclass
class ExerciseInPlan:
    """
    Represents an exercise within a workout plan with specific parameters.
    
    Attributes:
        exercise: The exercise object
        sets: Number of sets
        reps: Repetitions per set (or duration for cardio)
        rest_seconds: Rest time between sets
        notes: Special instructions or notes
        order: Position in workout sequence
    """
    exercise: Exercise
    sets: int = 3
    reps: str = "10-12"  # Can be "10-12" or "30 seconds", etc.
    rest_seconds: int = 30
    notes: str = ""
    order: int = 0
    
    def get_total_duration_minutes(self) -> int:
        """
        Calculate total duration for this exercise including rest.
        
        Returns:
            int: Total duration in minutes
        """
        # Use typical duration as the base (this represents a complete exercise session)
        # For workout planning, we use this as-is without multiplying by sets
        return self.exercise.typical_duration_minutes
    
    def get_total_calories(self) -> float:
        """
        Calculate total calories for this exercise.
        
        Returns:
            float: Total calories burned
        """
        duration = self.get_total_duration_minutes()
        return self.exercise.calculate_total_calories(duration)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'exercise': self.exercise.to_dict(),
            'sets': self.sets,
            'reps': self.reps,
            'rest_seconds': self.rest_seconds,
            'notes': self.notes,
            'order': self.order,
            'duration_minutes': self.get_total_duration_minutes(),
            'calories': self.get_total_calories()
        }


@dataclass
class ReasoningExplanation:
    """
    Explanation of why specific exercises were chosen.
    
    This provides transparency in the AI's decision-making process,
    showing which reasoning methods were used and why.
    
    Attributes:
        exercise_name: Name of the exercise
        reasons: List of reasons for selection
        agent_type: Which agent made the selection
        confidence_score: Confidence in this choice (0.0 to 1.0)
        alternatives: Alternative exercises considered
        decision_factors: Factors that influenced decision
    """
    exercise_name: str
    reasons: List[str] = field(default_factory=list)
    agent_type: str = ""
    confidence_score: float = 0.0
    alternatives: List[str] = field(default_factory=list)
    decision_factors: Dict[str, float] = field(default_factory=dict)
    
    def add_reason(self, reason: str) -> None:
        """Add a reason to the explanation."""
        self.reasons.append(reason)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'exercise_name': self.exercise_name,
            'reasons': self.reasons,
            'agent_type': self.agent_type,
            'confidence_score': self.confidence_score,
            'alternatives': self.alternatives,
            'decision_factors': self.decision_factors
        }


@dataclass
class WorkoutPlan:
    """
    Complete workout plan with exercises and reasoning.
    
    This is the primary output of the AI system, containing:
    - Personalized exercise selection
    - Detailed reasoning for each choice
    - Alternative exercises
    - Plan metadata and statistics
    
    The plan represents the SOLUTION found by search algorithms
    and validated/enhanced by intelligent agents and reasoning systems.
    
    Attributes:
        plan_id: Unique identifier
        user_id: User identifier
        created_at: Creation timestamp
        fitness_goal: User's fitness goal
        exercises: List of exercises in the plan
        reasoning: Reasoning explanations for each exercise
        status: Current status of the plan
        search_algorithm_used: Algorithm that generated initial plan
        search_statistics: Statistics from search process
        total_duration_minutes: Total plan duration
        total_calories: Total estimated calories
        difficulty_level: Overall difficulty
        muscle_groups_covered: All muscle groups in plan
        equipment_used: Equipment required for plan
        tags: Tags for categorization
        notes: Additional notes or instructions
        
    Example:
        >>> plan = WorkoutPlan(
        ...     plan_id="plan_001",
        ...     user_id="user_001",
        ...     fitness_goal=FitnessGoal.MUSCLE_GAIN,
        ...     exercises=[ex1, ex2, ex3]
        ... )
    """
    
    # Identity
    plan_id: str
    user_id: str
    created_at: datetime = field(default_factory=datetime.now)
    
    # User Context
    fitness_goal: FitnessGoal = FitnessGoal.GENERAL_FITNESS
    experience_level: str = "intermediate"
    initial_state: Optional[State] = None
    
    # Plan Content
    exercises: List[ExerciseInPlan] = field(default_factory=list)
    reasoning: List[ReasoningExplanation] = field(default_factory=list)
    
    # Metadata
    status: PlanStatus = PlanStatus.DRAFT
    search_algorithm_used: str = ""
    search_statistics: Dict[str, any] = field(default_factory=dict)
    
    # Computed Metrics
    total_duration_minutes: int = 0
    total_calories: float = 0.0
    difficulty_level: str = "intermediate"
    muscle_groups_covered: Set[str] = field(default_factory=set)
    equipment_used: Set[str] = field(default_factory=set)
    
    # Additional Information
    tags: List[str] = field(default_factory=list)
    notes: str = ""
    warmup_included: bool = False
    cooldown_included: bool = False
    
    def __post_init__(self) -> None:
        """Calculate metrics after initialization."""
        self._calculate_metrics()
    
    def add_exercise(
        self,
        exercise: Exercise,
        sets: int = 3,
        reps: str = "10-12",
        rest_seconds: int = 30,
        notes: str = ""
    ) -> None:
        """
        Add an exercise to the workout plan.
        
        Args:
            exercise: Exercise to add
            sets: Number of sets
            reps: Reps per set
            rest_seconds: Rest between sets
            notes: Additional notes
        """
        exercise_in_plan = ExerciseInPlan(
            exercise=exercise,
            sets=sets,
            reps=reps,
            rest_seconds=rest_seconds,
            notes=notes,
            order=len(self.exercises)
        )
        self.exercises.append(exercise_in_plan)
        self._calculate_metrics()
    
    def add_reasoning(
        self,
        exercise_name: str,
        reasons: List[str],
        agent_type: str = "",
        confidence: float = 0.0,
        alternatives: Optional[List[str]] = None
    ) -> None:
        """
        Add reasoning explanation for an exercise.
        
        Args:
            exercise_name: Name of exercise
            reasons: List of reasons
            agent_type: Agent that made decision
            confidence: Confidence score
            alternatives: Alternative exercises
        """
        explanation = ReasoningExplanation(
            exercise_name=exercise_name,
            reasons=reasons,
            agent_type=agent_type,
            confidence_score=confidence,
            alternatives=alternatives or []
        )
        self.reasoning.append(explanation)
    
    def _calculate_metrics(self) -> None:
        """Recalculate all metrics based on current exercises."""
        if not self.exercises:
            return
        
        # Calculate totals
        self.total_duration_minutes = sum(
            ex.get_total_duration_minutes() for ex in self.exercises
        )
        self.total_calories = sum(
            ex.get_total_calories() for ex in self.exercises
        )
        
        # Collect muscle groups
        muscle_groups = set()
        for ex_in_plan in self.exercises:
            muscle_groups.update(ex_in_plan.exercise.get_all_muscles())
        self.muscle_groups_covered = muscle_groups
        
        # Collect equipment
        equipment = set()
        for ex_in_plan in self.exercises:
            equipment.update(ex_in_plan.exercise.equipment)
        self.equipment_used = equipment
        
        # Determine overall difficulty
        difficulties = [ex.exercise.difficulty for ex in self.exercises]
        if all(d == "beginner" for d in difficulties):
            self.difficulty_level = "beginner"
        elif any(d in ["advanced", "expert"] for d in difficulties):
            self.difficulty_level = "advanced"
        else:
            self.difficulty_level = "intermediate"
    
    def get_exercise_by_name(self, name: str) -> Optional[ExerciseInPlan]:
        """
        Find exercise in plan by name.
        
        Args:
            name: Exercise name
            
        Returns:
            ExerciseInPlan or None if not found
        """
        for ex in self.exercises:
            if ex.exercise.name.lower() == name.lower():
                return ex
        return None
    
    def get_reasoning_for_exercise(self, name: str) -> Optional[ReasoningExplanation]:
        """
        Get reasoning explanation for specific exercise.
        
        Args:
            name: Exercise name
            
        Returns:
            ReasoningExplanation or None if not found
        """
        for reasoning in self.reasoning:
            if reasoning.exercise_name.lower() == name.lower():
                return reasoning
        return None
    
    def get_exercises_by_muscle_group(self, muscle_group: str) -> List[ExerciseInPlan]:
        """
        Get all exercises targeting specific muscle group.
        
        Args:
            muscle_group: Muscle group name
            
        Returns:
            List of exercises
        """
        result = []
        for ex in self.exercises:
            if muscle_group.lower() in (m.lower() for m in ex.exercise.get_all_muscles()):
                result.append(ex)
        return result
    
    def validate(self) -> List[str]:
        """
        Validate the workout plan for completeness and safety.
        
        Returns:
            List[str]: List of validation warnings/errors
        """
        warnings = []
        
        # Check minimum exercises
        if len(self.exercises) < 3:
            warnings.append("Plan has fewer than 3 exercises")
        
        # Check duration
        if self.total_duration_minutes < 20:
            warnings.append("Plan duration is less than 20 minutes")
        elif self.total_duration_minutes > 120:
            warnings.append("Plan duration exceeds 2 hours (may be too long)")
        
        # Check muscle group diversity
        if len(self.muscle_groups_covered) < 2:
            warnings.append("Plan targets only one muscle group")
        
        # Check for warmup/cooldown
        if not self.warmup_included:
            warnings.append("Plan does not include warmup")
        if not self.cooldown_included:
            warnings.append("Plan does not include cooldown")
        
        return warnings
    
    def get_summary(self) -> str:
        """
        Get a text summary of the workout plan.
        
        Returns:
            str: Formatted summary
        """
        summary_lines = [
            f"=== Workout Plan: {self.plan_id} ===",
            f"Goal: {self.fitness_goal.value}",
            f"Level: {self.experience_level}",
            f"Duration: {self.total_duration_minutes} minutes",
            f"Calories: {self.total_calories:.0f}",
            f"Exercises: {len(self.exercises)}",
            f"Muscle Groups: {', '.join(sorted(self.muscle_groups_covered))}",
            f"",
            "Exercises:"
        ]
        
        for i, ex in enumerate(self.exercises, 1):
            summary_lines.append(
                f"  {i}. {ex.exercise.name} - {ex.sets} sets x {ex.reps}"
            )
        
        return "\n".join(summary_lines)
    
    def to_dict(self) -> dict:
        """
        Convert workout plan to dictionary for serialization.
        
        Returns:
            dict: Dictionary representation
        """
        return {
            'plan_id': self.plan_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'fitness_goal': self.fitness_goal.value,
            'experience_level': self.experience_level,
            'status': self.status.value,
            'exercises': [ex.to_dict() for ex in self.exercises],
            'reasoning': [r.to_dict() for r in self.reasoning],
            'total_duration_minutes': self.total_duration_minutes,
            'total_calories': self.total_calories,
            'difficulty_level': self.difficulty_level,
            'muscle_groups_covered': list(self.muscle_groups_covered),
            'equipment_used': list(self.equipment_used),
            'search_algorithm_used': self.search_algorithm_used,
            'search_statistics': self.search_statistics,
            'notes': self.notes,
            'warmup_included': self.warmup_included,
            'cooldown_included': self.cooldown_included
        }
    
    def __str__(self) -> str:
        """String representation."""
        return (
            f"WorkoutPlan(id={self.plan_id}, exercises={len(self.exercises)}, "
            f"duration={self.total_duration_minutes}min, goal={self.fitness_goal.value})"
        )
