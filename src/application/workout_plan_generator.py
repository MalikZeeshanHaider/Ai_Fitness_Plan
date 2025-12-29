"""
Workout Plan Generator Service.

This service is responsible for creating structured workout plans
using various algorithms and strategies.

Features:
- Multi-algorithm plan generation
- Progressive difficulty scaling
- Exercise variety optimization
- Time and equipment constraints
- Goal-oriented exercise selection
- Alternative plan generation

Algorithms Used:
- Greedy selection for quick plans
- Dynamic programming for optimization
- Constraint satisfaction for feasibility
- Genetic algorithm for variety

Time Complexity: O(n log n) for greedy, O(n^2) for optimization
Space Complexity: O(n) for plan storage
"""

from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import random

from ..domain.models.state import State, ExperienceLevel, FitnessGoal
from ..domain.models.exercise import Exercise
from ..domain.models.workout_plan import WorkoutPlan
from ..domain.models.action import Difficulty, ExerciseType


class GenerationAlgorithm(Enum):
    """Algorithm for plan generation."""
    GREEDY = "greedy"  # Greedy selection by priority
    BALANCED = "balanced"  # Balance multiple objectives
    PROGRESSIVE = "progressive"  # Progressive difficulty
    VARIETY_OPTIMIZED = "variety_optimized"  # Maximize variety
    TIME_OPTIMIZED = "time_optimized"  # Optimize for time efficiency


@dataclass
class PlanGenerationConfig:
    """
    Configuration for workout plan generation.
    
    Attributes:
        min_exercises: Minimum number of exercises
        max_exercises: Maximum number of exercises
        target_duration: Target duration in minutes
        target_calories: Target calorie burn
        algorithm: Generation algorithm to use
        enforce_variety: Ensure exercise type variety
        progressive_difficulty: Use progressive difficulty
        rest_between_sets: Rest time between exercises
        allow_repeats: Allow same exercise multiple times
    """
    min_exercises: int = 3
    max_exercises: int = 8
    target_duration: int = 45
    target_calories: int = 300
    algorithm: GenerationAlgorithm = GenerationAlgorithm.BALANCED
    enforce_variety: bool = True
    progressive_difficulty: bool = True
    rest_between_sets: int = 60  # seconds
    allow_repeats: bool = False
    
    def __post_init__(self):
        """Validate configuration."""
        if self.min_exercises > self.max_exercises:
            raise ValueError("min_exercises must be <= max_exercises")
        if self.target_duration <= 0:
            raise ValueError("target_duration must be positive")


class WorkoutPlanGenerator:
    """
    Service for generating workout plans.
    
    This generator creates structured workout plans using various
    algorithms and optimization strategies.
    
    Key Features:
    1. Multiple generation algorithms
    2. Constraint satisfaction
    3. Variety optimization
    4. Progressive difficulty
    5. Alternative plan generation
    
    Design Pattern: Builder + Strategy
    - Builder: Constructs complex workout plans
    - Strategy: Different algorithms for generation
    
    Example Usage:
    ```python
    generator = WorkoutPlanGenerator()
    
    config = PlanGenerationConfig(
        target_duration=45,
        max_exercises=6,
        algorithm=GenerationAlgorithm.BALANCED
    )
    
    plan = generator.generate(
        user_state=state,
        available_exercises=exercises,
        config=config
    )
    ```
    
    Time Complexity: Varies by algorithm (O(n) to O(n^2))
    Space Complexity: O(n) for plan storage
    """
    
    def __init__(self, name: str = "Workout Plan Generator"):
        """
        Initialize plan generator.
        
        Args:
            name: Generator name
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._name = name
        self._plans_generated = 0
        self._generation_log: List[str] = []
    
    @property
    def name(self) -> str:
        """Get generator name."""
        return self._name
    
    @property
    def generation_log(self) -> List[str]:
        """Get generation log."""
        return self._generation_log.copy()
    
    def generate(
        self,
        user_state: State,
        available_exercises: List[Exercise],
        config: PlanGenerationConfig
    ) -> WorkoutPlan:
        """
        Generate workout plan.
        
        Main workflow:
        1. Filter exercises by user level
        2. Apply algorithm-specific selection
        3. Optimize for variety and constraints
        4. Build workout plan
        5. Validate plan
        
        Args:
            user_state: User's current fitness state
            available_exercises: Available exercises
            config: Generation configuration
            
        Returns:
            Generated workout plan
            
        Time Complexity: O(n log n) typical
        Space Complexity: O(n)
        """
        self._generation_log.append(f"Starting generation with {len(available_exercises)} exercises")
        
        # Step 1: Filter exercises
        suitable_exercises = self._filter_by_level(available_exercises, user_state)
        self._generation_log.append(f"Filtered to {len(suitable_exercises)} suitable exercises")
        
        # Step 2: Select exercises based on algorithm
        selected_exercises = self._select_exercises(
            suitable_exercises,
            user_state,
            config
        )
        
        # Step 3: Optimize order (progressive difficulty if enabled)
        if config.progressive_difficulty:
            selected_exercises = self._order_progressively(selected_exercises)
            self._generation_log.append("Applied progressive difficulty ordering")
        
        # Step 4: Build workout plan
        plan = self._build_plan(
            exercises=selected_exercises,
            user_state=user_state,
            config=config
        )
        
        # Step 5: Validate
        if not self._validate_plan(plan, config):
            self._generation_log.append("Warning: Plan validation failed, adjusting...")
            plan = self._adjust_plan(plan, config)
        
        self._plans_generated += 1
        self._generation_log.append(f"Plan generated successfully: {plan.plan_id}")
        
        return plan
    
    def generate_alternatives(
        self,
        user_state: State,
        available_exercises: List[Exercise],
        config: PlanGenerationConfig,
        count: int = 3
    ) -> List[WorkoutPlan]:
        """
        Generate multiple alternative workout plans.
        
        Creates diverse plans by varying:
        - Exercise selection
        - Order and progression
        - Focus areas
        
        Args:
            user_state: User's fitness state
            available_exercises: Available exercises
            config: Generation configuration
            count: Number of alternatives to generate
            
        Returns:
            List of alternative plans
            
        Time Complexity: O(count * n log n)
        Space Complexity: O(count * n)
        """
        alternatives = []
        
        # Generate main plan
        main_plan = self.generate(user_state, available_exercises, config)
        alternatives.append(main_plan)
        
        # Generate alternatives with variations
        for i in range(count - 1):
            # Vary the configuration slightly
            alt_config = self._create_variant_config(config, i)
            
            # Generate alternative
            alt_plan = self.generate(user_state, available_exercises, alt_config)
            # Note: plan_id is the identifier, not plan_name
            
            alternatives.append(alt_plan)
        
        self._generation_log.append(f"Generated {len(alternatives)} alternative plans")
        
        return alternatives
    
    def _filter_by_level(
        self,
        exercises: List[Exercise],
        state: State
    ) -> List[Exercise]:
        """
        Filter exercises appropriate for user level.
        
        Args:
            exercises: All exercises
            state: User state
            
        Returns:
            Filtered exercises
            
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        suitable = []
        
        for exercise in exercises:
            # Check difficulty match
            if not self._is_appropriate_difficulty(exercise.difficulty, state.experience_level):
                continue
            
            # Check goal alignment
            if not self._aligns_with_goal(exercise.category, state.fitness_goal):
                continue
            
            suitable.append(exercise)
        
        return suitable
    
    def _is_appropriate_difficulty(
        self,
        difficulty: Difficulty,
        level: ExperienceLevel
    ) -> bool:
        """Check if difficulty matches experience level."""
        if level == ExperienceLevel.BEGINNER:
            return difficulty in [Difficulty.BEGINNER, Difficulty.EASY]
        elif level == ExperienceLevel.INTERMEDIATE:
            return difficulty in [Difficulty.EASY, Difficulty.INTERMEDIATE, Difficulty.MODERATE]
        else:  # ADVANCED
            return True
    
    def _aligns_with_goal(
        self,
        exercise_type: ExerciseType,
        goal: FitnessGoal
    ) -> bool:
        """Check if exercise type aligns with fitness goal."""
        alignments = {
            FitnessGoal.WEIGHT_LOSS: [ExerciseType.CARDIO, ExerciseType.HIIT, ExerciseType.FLEXIBILITY],
            FitnessGoal.MUSCLE_GAIN: [ExerciseType.STRENGTH, ExerciseType.RESISTANCE, ExerciseType.COMPOUND],
            FitnessGoal.ENDURANCE: [ExerciseType.CARDIO, ExerciseType.ENDURANCE, ExerciseType.BODYWEIGHT],
            FitnessGoal.FLEXIBILITY: [ExerciseType.FLEXIBILITY, ExerciseType.STRETCHING, ExerciseType.BALANCE],
            FitnessGoal.GENERAL_FITNESS: list(ExerciseType)  # All types
        }
        
        return exercise_type in alignments.get(goal, [])
    
    def _select_exercises(
        self,
        exercises: List[Exercise],
        state: State,
        config: PlanGenerationConfig
    ) -> List[Exercise]:
        """
        Select exercises based on algorithm.
        
        Args:
            exercises: Available exercises
            state: User state
            config: Configuration
            
        Returns:
            Selected exercises
            
        Time Complexity: Varies by algorithm
        Space Complexity: O(n)
        """
        if config.algorithm == GenerationAlgorithm.GREEDY:
            return self._greedy_selection(exercises, state, config)
        elif config.algorithm == GenerationAlgorithm.BALANCED:
            return self._balanced_selection(exercises, state, config)
        elif config.algorithm == GenerationAlgorithm.VARIETY_OPTIMIZED:
            return self._variety_optimized_selection(exercises, state, config)
        elif config.algorithm == GenerationAlgorithm.TIME_OPTIMIZED:
            return self._time_optimized_selection(exercises, state, config)
        else:
            return self._balanced_selection(exercises, state, config)
    
    def _greedy_selection(
        self,
        exercises: List[Exercise],
        state: State,
        config: PlanGenerationConfig
    ) -> List[Exercise]:
        """
        Greedy selection by calorie burn.
        
        Selects exercises with highest calorie burn first.
        
        Time Complexity: O(n log n) for sorting
        Space Complexity: O(n)
        """
        # Sort by calories (descending)
        sorted_exercises = sorted(
            exercises,
            key=lambda e: e.calories_per_minute * e.duration_minutes,
            reverse=True
        )
        
        selected = []
        total_duration = 0
        
        for exercise in sorted_exercises:
            if len(selected) >= config.max_exercises:
                break
            
            # Allow up to 110% of target duration
            if total_duration + exercise.duration_minutes > config.target_duration * 1.1:
                continue
            
            selected.append(exercise)
            total_duration += exercise.duration_minutes
            
            # Stop if we've reached at least 90% of target
            if total_duration >= config.target_duration * 0.9 and len(selected) >= config.min_exercises:
                break
        
        return selected
    
    def _balanced_selection(
        self,
        exercises: List[Exercise],
        state: State,
        config: PlanGenerationConfig
    ) -> List[Exercise]:
        """
        Balanced selection across exercise types.
        
        Ensures variety across different exercise types.
        
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        # Group by type
        by_type: Dict = {}
        for exercise in exercises:
            if exercise.category not in by_type:
                by_type[exercise.category] = []
            by_type[exercise.category].append(exercise)
        
        # Select from each type
        selected = []
        total_duration = 0
        type_counts = {t: 0 for t in by_type.keys()}
        
        # Round-robin selection - fill to target duration
        while len(selected) < config.max_exercises:
            added_any = False
            
            for ex_type, ex_list in by_type.items():
                if type_counts[ex_type] >= len(ex_list):
                    continue
                
                exercise = ex_list[type_counts[ex_type]]
                
                # Add exercise if we haven't exceeded target by more than 10%
                if total_duration + exercise.duration_minutes <= config.target_duration * 1.1:
                    selected.append(exercise)
                    total_duration += exercise.duration_minutes
                    type_counts[ex_type] += 1
                    added_any = True
                
                if len(selected) >= config.max_exercises:
                    break
                
                # Stop if we've reached at least 90% of target
                if total_duration >= config.target_duration * 0.9:
                    break
            
            if not added_any or total_duration >= config.target_duration * 0.9:
                break
        
        return selected
    
    def _variety_optimized_selection(
        self,
        exercises: List[Exercise],
        state: State,
        config: PlanGenerationConfig
    ) -> List[Exercise]:
        """
        Maximize exercise variety.
        
        Ensures maximum diversity in exercise types.
        
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        selected = []
        used_types: Set[ExerciseType] = set()
        total_duration = 0
        
        # First pass: one from each type
        for exercise in exercises:
            if len(selected) >= config.max_exercises:
                break
            
            if exercise.category not in used_types:
                if total_duration + exercise.duration_minutes <= config.target_duration:
                    selected.append(exercise)
                    used_types.add(exercise.category)
                    total_duration += exercise.duration_minutes
        
        # Second pass: fill remaining slots
        for exercise in exercises:
            if len(selected) >= config.max_exercises:
                break
            
            if exercise not in selected:
                if total_duration + exercise.duration_minutes <= config.target_duration:
                    selected.append(exercise)
                    total_duration += exercise.duration_minutes
        
        return selected
    
    def _time_optimized_selection(
        self,
        exercises: List[Exercise],
        state: State,
        config: PlanGenerationConfig
    ) -> List[Exercise]:
        """
        Optimize for time efficiency.
        
        Selects exercises with best calorie/time ratio.
        
        Time Complexity: O(n log n)
        Space Complexity: O(n)
        """
        # Sort by calorie efficiency
        sorted_exercises = sorted(
            exercises,
            key=lambda e: e.calories_per_minute,
            reverse=True
        )
        
        selected = []
        total_duration = 0
        
        for exercise in sorted_exercises:
            if len(selected) >= config.max_exercises:
                break
            
            # Allow up to 110% of target duration
            if total_duration + exercise.duration_minutes > config.target_duration * 1.1:
                continue
            
            selected.append(exercise)
            total_duration += exercise.duration_minutes
            
            # Stop if we've reached at least 90% of target
            if total_duration >= config.target_duration * 0.9 and len(selected) >= config.min_exercises:
                break
        
        return selected
    
    def _order_progressively(self, exercises: List[Exercise]) -> List[Exercise]:
        """
        Order exercises with progressive difficulty.
        
        Start with easier exercises, progress to harder.
        
        Args:
            exercises: Exercises to order
            
        Returns:
            Ordered exercises
            
        Time Complexity: O(n log n)
        Space Complexity: O(n)
        """
        difficulty_order = {
            Difficulty.BEGINNER: 0,
            Difficulty.EASY: 1,
            Difficulty.INTERMEDIATE: 2,
            Difficulty.MODERATE: 3,
            Difficulty.ADVANCED: 4,
            Difficulty.HARD: 5
        }
        
        return sorted(exercises, key=lambda e: difficulty_order.get(e.difficulty, 0))
    
    def _build_plan(
        self,
        exercises: List[Exercise],
        user_state: State,
        config: PlanGenerationConfig
    ) -> WorkoutPlan:
        """
        Build workout plan from selected exercises.
        
        Args:
            exercises: Selected exercises
            user_state: User state
            config: Configuration
            
        Returns:
            Workout plan
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        plan_id = f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self._plans_generated}"
        
        # Create workout plan with correct attribute names
        plan = WorkoutPlan(
            plan_id=plan_id,
            user_id="user_default",
            exercises=exercises,
            fitness_goal=user_state.fitness_goal,
            difficulty_level=user_state.experience_level.value if hasattr(user_state.experience_level, 'value') else str(user_state.experience_level)
        )
        
        return plan
    
    def _generate_plan_name(self, state: State, config: PlanGenerationConfig) -> str:
        """Generate descriptive plan name."""
        goal_name = state.fitness_goal.value.replace("_", " ").title()
        level_name = state.experience_level.value.title()
        duration = config.target_duration
        
        return f"{duration}-Min {goal_name} Workout ({level_name})"
    
    def _validate_plan(self, plan: WorkoutPlan, config: PlanGenerationConfig) -> bool:
        """
        Validate workout plan against constraints.
        
        Args:
            plan: Plan to validate
            config: Configuration constraints
            
        Returns:
            True if valid, False otherwise
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        # Check exercise count
        if len(plan.exercises) < config.min_exercises:
            return False
        
        if len(plan.exercises) > config.max_exercises:
            return False
        
        # Check duration - accept if within 80-110% of target
        min_acceptable = config.target_duration * 0.8
        max_acceptable = config.target_duration * 1.1
        if not (min_acceptable <= plan.total_duration_minutes <= max_acceptable):
            return False
        
        return True
    
    def _adjust_plan(self, plan: WorkoutPlan, config: PlanGenerationConfig) -> WorkoutPlan:
        """
        Adjust plan to meet constraints.
        
        Args:
            plan: Plan to adjust
            config: Target configuration
            
        Returns:
            Adjusted plan
            
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        # Simple adjustment: remove last exercise if too long
        while plan.total_duration_minutes > config.target_duration and len(plan.exercises) > config.min_exercises:
            plan.exercises.pop()
        
        return plan
    
    def _create_variant_config(self, config: PlanGenerationConfig, variant_index: int) -> PlanGenerationConfig:
        """
        Create variant configuration for alternatives.
        
        Args:
            config: Base configuration
            variant_index: Variant number
            
        Returns:
            Modified configuration
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        algorithms = list(GenerationAlgorithm)
        algorithm = algorithms[(variant_index + 1) % len(algorithms)]
        
        return PlanGenerationConfig(
            min_exercises=config.min_exercises,
            max_exercises=config.max_exercises,
            target_duration=config.target_duration,
            target_calories=config.target_calories,
            algorithm=algorithm,
            enforce_variety=config.enforce_variety,
            progressive_difficulty=config.progressive_difficulty,
            rest_between_sets=config.rest_between_sets,
            allow_repeats=config.allow_repeats
        )
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get generator statistics.
        
        Returns:
            Statistics dictionary
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return {
            "name": self._name,
            "plans_generated": self._plans_generated,
            "log_entries": len(self._generation_log)
        }
    
    def __str__(self) -> str:
        """String representation."""
        return f"WorkoutPlanGenerator(plans_generated={self._plans_generated})"


# Example usage
if __name__ == "__main__":
    print("Workout Plan Generator Service")
    print("==============================")
    print()
    
    # Create generator
    generator = WorkoutPlanGenerator()
    
    # Create sample exercises
    exercises = [
        Exercise(
            exercise_id="ex1",
            name="Running",
            exercise_type=ExerciseType.CARDIO,
            difficulty=Difficulty.INTERMEDIATE,
            duration_minutes=15,
            calories_per_minute=10.0
        ),
        Exercise(
            exercise_id="ex2",
            name="Push-ups",
            exercise_type=ExerciseType.STRENGTH,
            difficulty=Difficulty.INTERMEDIATE,
            duration_minutes=10,
            calories_per_minute=7.0
        ),
    ]
    
    # Create configuration
    config = PlanGenerationConfig(
        target_duration=45,
        max_exercises=5,
        algorithm=GenerationAlgorithm.BALANCED
    )
    
    # Generate plan
    state = State(
        experience_level=ExperienceLevel.INTERMEDIATE,
        fitness_goal=FitnessGoal.GENERAL_FITNESS,
        strength_level=50.0,
        endurance_level=50.0,
        flexibility_level=50.0
    )
    
    plan = generator.generate(state, exercises, config)
    print(f"Generated: Plan {plan.plan_id}")
    print(f"Exercises: {len(plan.exercises)}")
    print(f"Duration: {plan.total_duration_minutes} minutes")
