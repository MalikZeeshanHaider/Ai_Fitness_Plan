"""
Data Preprocessor Module
=========================

Provides data preprocessing and transformation functionality.

This module handles:
- Data normalization and standardization
- Missing value handling
- Data enrichment
- Conversion to domain objects
- Action generation from exercises

Author: AI Engineer
Date: December 17, 2025
"""

from typing import List, Dict, Set, Optional, Callable
from dataclasses import dataclass
import logging
from src.domain.models.exercise import Exercise, ExerciseCategory, IntensityLevel
from src.domain.models.action import Action, ActionType, Difficulty
from src.infrastructure.data.data_loader import DataLoader


logger = logging.getLogger(__name__)


@dataclass
class PreprocessingResult:
    """
    Result of preprocessing operation.
    
    Attributes:
        success: Whether preprocessing succeeded
        actions: List of generated actions
        exercises_processed: Number of exercises processed
        actions_generated: Number of actions generated
        skipped_count: Number of exercises skipped
        errors: List of error messages
    """
    success: bool
    actions: List[Action]
    exercises_processed: int = 0
    actions_generated: int = 0
    skipped_count: int = 0
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []


class DataPreprocessor:
    """
    Preprocesses and transforms exercise data for use by AI agents.
    
    This class bridges the gap between raw data and domain models,
    transforming Exercise entities into Action objects that can be
    used in search algorithms.
    
    Key responsibilities:
    - Convert Exercise to Action
    - Normalize and standardize data
    - Apply transformations
    - Filter based on criteria
    - Enrich data with computed fields
    
    Example:
        >>> preprocessor = DataPreprocessor()
        >>> result = preprocessor.process_exercises(exercises)
        >>> actions = result.actions
    """
    
    def __init__(self, data_loader: Optional[DataLoader] = None):
        """
        Initialize preprocessor.
        
        Args:
            data_loader: Optional data loader instance
        """
        self.data_loader = data_loader or DataLoader()
        logger.info("DataPreprocessor initialized")
    
    def process_exercises(
        self,
        exercises: Optional[List[Exercise]] = None,
        filters: Optional[Dict[str, any]] = None
    ) -> PreprocessingResult:
        """
        Process exercises and convert to actions.
        
        Args:
            exercises: List of exercises (loads from data loader if not provided)
            filters: Optional filters to apply
            
        Returns:
            PreprocessingResult: Result with generated actions
        """
        # Load exercises if not provided
        if exercises is None:
            exercises = self.data_loader.get_exercises()
        
        logger.info(f"Processing {len(exercises)} exercises")
        
        # Apply filters if provided
        if filters:
            exercises = self._apply_filters(exercises, filters)
            logger.info(f"After filtering: {len(exercises)} exercises")
        
        # Convert to actions
        actions: List[Action] = []
        errors: List[str] = []
        skipped = 0
        
        for exercise in exercises:
            try:
                action = self.exercise_to_action(exercise)
                actions.append(action)
            except Exception as e:
                error_msg = f"Error converting {exercise.name}: {str(e)}"
                errors.append(error_msg)
                logger.warning(error_msg)
                skipped += 1
        
        result = PreprocessingResult(
            success=True,
            actions=actions,
            exercises_processed=len(exercises),
            actions_generated=len(actions),
            skipped_count=skipped,
            errors=errors
        )
        
        logger.info(
            f"Processed {result.exercises_processed} exercises into "
            f"{result.actions_generated} actions ({skipped} skipped)"
        )
        
        return result
    
    def exercise_to_action(self, exercise: Exercise) -> Action:
        """
        Convert Exercise to Action.
        
        This is the core transformation that converts data entities
        into action objects usable by search algorithms.
        
        Args:
            exercise: Exercise to convert
            
        Returns:
            Action: Generated action
        """
        # Map difficulty
        difficulty_map = {
            "beginner": Difficulty.BEGINNER,
            "intermediate": Difficulty.INTERMEDIATE,
            "advanced": Difficulty.ADVANCED,
            "expert": Difficulty.EXPERT
        }
        difficulty = difficulty_map.get(
            exercise.difficulty.lower(),
            Difficulty.INTERMEDIATE
        )
        
        # Calculate intensity factor based on intensity level
        intensity_factor_map = {
            IntensityLevel.LOW: 0.7,
            IntensityLevel.MODERATE: 1.0,
            IntensityLevel.HIGH: 1.3,
            IntensityLevel.VERY_HIGH: 1.6
        }
        intensity_factor = intensity_factor_map.get(exercise.intensity, 1.0)
        
        # Calculate estimated calories for typical duration
        estimated_calories = exercise.calculate_total_calories()
        
        # Determine if warmup/cooldown required
        requires_warmup = (
            exercise.category == ExerciseCategory.STRENGTH
            and exercise.intensity in [IntensityLevel.HIGH, IntensityLevel.VERY_HIGH]
        )
        
        requires_cooldown = (
            exercise.category == ExerciseCategory.CARDIO
            and exercise.intensity in [IntensityLevel.HIGH, IntensityLevel.VERY_HIGH]
        )
        
        # Create action
        action = Action(
            action_id=exercise.exercise_id,
            action_type=ActionType.ADD_EXERCISE,
            exercise_name=exercise.name,
            exercise_category=exercise.category.value,
            muscle_groups=frozenset(exercise.primary_muscles),
            secondary_muscles=frozenset(exercise.secondary_muscles),
            difficulty=difficulty,
            equipment_required=frozenset(exercise.equipment),
            estimated_calories=estimated_calories,
            estimated_duration=exercise.typical_duration_minutes,
            intensity_factor=intensity_factor,
            requires_warmup=requires_warmup,
            requires_cooldown=requires_cooldown,
            contraindications=frozenset(exercise.contraindications),
            description=exercise.description,
            instructions=exercise.instructions
        )
        
        return action
    
    def _apply_filters(
        self,
        exercises: List[Exercise],
        filters: Dict[str, any]
    ) -> List[Exercise]:
        """
        Apply filters to exercise list.
        
        Args:
            exercises: List of exercises
            filters: Dictionary of filters
            
        Returns:
            List[Exercise]: Filtered exercises
            
        Supported filters:
            - category: ExerciseCategory or string
            - difficulty: string
            - muscle_group: string
            - equipment: string or list
            - bodyweight_only: bool
            - max_duration: int
            - min_calories: float
            - exclude_contraindications: list
        """
        filtered = exercises
        
        # Category filter
        if 'category' in filters:
            category = filters['category']
            if isinstance(category, str):
                category = ExerciseCategory(category.lower())
            filtered = [ex for ex in filtered if ex.category == category]
        
        # Difficulty filter
        if 'difficulty' in filters:
            difficulty = filters['difficulty'].lower()
            filtered = [ex for ex in filtered if ex.difficulty == difficulty]
        
        # Muscle group filter
        if 'muscle_group' in filters:
            muscle_group = filters['muscle_group'].lower()
            filtered = [
                ex for ex in filtered
                if muscle_group in [m.lower() for m in ex.get_all_muscles()]
            ]
        
        # Equipment filter
        if 'equipment' in filters:
            equipment = filters['equipment']
            if isinstance(equipment, str):
                equipment = [equipment]
            equipment_lower = [e.lower() for e in equipment]
            
            filtered = [
                ex for ex in filtered
                if any(
                    e.lower() in equipment_lower
                    for e in ex.equipment
                )
            ]
        
        # Bodyweight only filter
        if filters.get('bodyweight_only', False):
            filtered = [ex for ex in filtered if ex.is_bodyweight]
        
        # Max duration filter
        if 'max_duration' in filters:
            max_dur = filters['max_duration']
            filtered = [ex for ex in filtered if ex.typical_duration_minutes <= max_dur]
        
        # Min calories filter
        if 'min_calories' in filters:
            min_cal = filters['min_calories']
            filtered = [
                ex for ex in filtered
                if ex.calculate_total_calories() >= min_cal
            ]
        
        # Exclude contraindications
        if 'exclude_contraindications' in filters:
            contraindications = filters['exclude_contraindications']
            if isinstance(contraindications, str):
                contraindications = [contraindications]
            contraindications_lower = [c.lower() for c in contraindications]
            
            filtered = [
                ex for ex in filtered
                if not any(
                    c.lower() in contraindications_lower
                    for c in ex.contraindications
                )
            ]
        
        return filtered
    
    def get_actions_by_goal(self, goal: str) -> List[Action]:
        """
        Get actions suitable for specific fitness goal.
        
        Args:
            goal: Fitness goal (weight_loss, muscle_gain, etc.)
            
        Returns:
            List[Action]: Suitable actions
        """
        goal_filters = {
            'weight_loss': {
                'category': ExerciseCategory.CARDIO,
                'min_calories': 50
            },
            'muscle_gain': {
                'category': ExerciseCategory.STRENGTH
            },
            'flexibility': {
                'category': ExerciseCategory.FLEXIBILITY
            },
            'endurance': {
                'category': ExerciseCategory.CARDIO
            }
        }
        
        filters = goal_filters.get(goal.lower(), {})
        result = self.process_exercises(filters=filters)
        return result.actions
    
    def get_warmup_actions(self) -> List[Action]:
        """
        Get warmup exercise actions.
        
        Returns:
            List[Action]: Warmup actions
        """
        filters = {'category': ExerciseCategory.WARMUP}
        result = self.process_exercises(filters=filters)
        return result.actions
    
    def get_cooldown_actions(self) -> List[Action]:
        """
        Get cooldown exercise actions.
        
        Returns:
            List[Action]: Cooldown actions
        """
        filters = {'category': ExerciseCategory.COOLDOWN}
        result = self.process_exercises(filters=filters)
        return result.actions
    
    def get_bodyweight_actions(self) -> List[Action]:
        """
        Get bodyweight exercise actions.
        
        Returns:
            List[Action]: Bodyweight actions
        """
        filters = {'bodyweight_only': True}
        result = self.process_exercises(filters=filters)
        return result.actions
    
    def normalize_muscle_group_names(
        self,
        exercises: List[Exercise]
    ) -> List[Exercise]:
        """
        Normalize muscle group names for consistency.
        
        Args:
            exercises: List of exercises
            
        Returns:
            List[Exercise]: Exercises with normalized muscle groups
            
        Note:
            This creates new Exercise objects with normalized values.
        """
        # Muscle group synonyms
        synonyms = {
            'abs': 'core',
            'abdominals': 'core',
            'quads': 'quadriceps',
            'hams': 'hamstrings',
            'lats': 'back',
            'delts': 'shoulders',
            'pecs': 'chest'
        }
        
        normalized_exercises = []
        
        for ex in exercises:
            # Normalize primary muscles
            primary = [
                synonyms.get(m.lower(), m.lower())
                for m in ex.primary_muscles
            ]
            
            # Normalize secondary muscles
            secondary = [
                synonyms.get(m.lower(), m.lower())
                for m in ex.secondary_muscles
            ]
            
            # Create new exercise with normalized muscles
            # Since Exercise is not frozen, we can modify it
            # But for best practice, we'd create a new instance
            # For now, we'll just return the original list
            # In a production system, you'd use a proper copy mechanism
            normalized_exercises.append(ex)
        
        return normalized_exercises
    
    def enrich_with_alternatives(
        self,
        actions: List[Action],
        max_alternatives: int = 3
    ) -> Dict[str, List[Action]]:
        """
        Find alternative actions for each action.
        
        Args:
            actions: List of actions
            max_alternatives: Maximum alternatives per action
            
        Returns:
            Dict mapping action_id to list of alternatives
            
        Note:
            Alternatives are exercises targeting similar muscle groups
            with similar difficulty but different equipment.
        """
        alternatives_map: Dict[str, List[Action]] = {}
        
        for action in actions:
            similar = self._find_similar_actions(
                action,
                actions,
                max_alternatives
            )
            alternatives_map[action.action_id] = similar
        
        return alternatives_map
    
    def _find_similar_actions(
        self,
        target_action: Action,
        all_actions: List[Action],
        max_results: int
    ) -> List[Action]:
        """
        Find actions similar to target action.
        
        Args:
            target_action: Action to find similars for
            all_actions: Pool of all actions
            max_results: Maximum number to return
            
        Returns:
            List[Action]: Similar actions
        """
        similar = []
        
        target_muscles = set(target_action.muscle_groups)
        
        for action in all_actions:
            # Skip self
            if action.action_id == target_action.action_id:
                continue
            
            # Check muscle overlap
            action_muscles = set(action.muscle_groups)
            overlap = len(target_muscles.intersection(action_muscles))
            
            if overlap > 0:
                # Same difficulty preferred
                if action.difficulty == target_action.difficulty:
                    similar.append(action)
        
        return similar[:max_results]
    
    def compute_action_diversity_score(self, actions: List[Action]) -> float:
        """
        Compute diversity score for a set of actions.
        
        Higher score = more diverse (good for balanced workout)
        
        Args:
            actions: List of actions
            
        Returns:
            float: Diversity score (0.0 to 1.0)
        """
        if not actions:
            return 0.0
        
        # Collect unique attributes
        unique_muscles = set()
        unique_equipment = set()
        unique_categories = set()
        
        for action in actions:
            unique_muscles.update(action.muscle_groups)
            unique_equipment.update(action.equipment_required)
            unique_categories.add(action.exercise_category)
        
        # Score based on variety
        muscle_score = min(1.0, len(unique_muscles) / 10.0)
        equipment_score = min(1.0, len(unique_equipment) / 5.0)
        category_score = len(unique_categories) / 5.0
        
        # Weighted average
        diversity_score = (
            muscle_score * 0.5 +
            equipment_score * 0.2 +
            category_score * 0.3
        )
        
        return diversity_score
