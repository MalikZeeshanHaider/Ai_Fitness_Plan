"""
Data Loader Module
==================

Provides data loading functionality for the gym exercise dataset.

This module handles:
- CSV file loading and parsing
- Data type conversion
- Error handling for missing or corrupted data
- Caching for performance
- Integration with domain models

Follows Repository pattern for data access abstraction.

Author: AI Engineer
Date: December 17, 2025
"""

import pandas as pd
from pathlib import Path
from typing import List, Optional, Dict, Set
from dataclasses import dataclass
import logging
from src.domain.models.exercise import Exercise, ExerciseCategory, IntensityLevel
from src.infrastructure.config_loader import get_config_value


logger = logging.getLogger(__name__)


@dataclass
class DataLoadResult:
    """
    Result of data loading operation.
    
    Attributes:
        success: Whether loading succeeded
        exercises: List of loaded exercises
        error_count: Number of errors encountered
        errors: List of error messages
        total_rows: Total rows in dataset
        loaded_count: Number successfully loaded
    """
    success: bool
    exercises: List[Exercise]
    error_count: int = 0
    errors: List[str] = None
    total_rows: int = 0
    loaded_count: int = 0
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []


class DataLoader:
    """
    Loads gym exercise data from CSV files.
    
    This class implements the Repository pattern, providing
    a clean interface for data access while hiding the details
    of file I/O and data parsing.
    
    Features:
    - CSV parsing with pandas
    - Automatic type conversion
    - Error handling and logging
    - Optional caching
    - Data filtering and querying
    
    Example:
        >>> loader = DataLoader("data/GymDataset.csv")
        >>> result = loader.load()
        >>> if result.success:
        ...     exercises = result.exercises
        ...     print(f"Loaded {len(exercises)} exercises")
    """
    
    def __init__(self, dataset_path: Optional[str] = None, enable_cache: bool = True):
        """
        Initialize data loader.
        
        Args:
            dataset_path: Path to CSV file (uses config if not provided)
            enable_cache: Whether to cache loaded data
        """
        if dataset_path is None:
            dataset_path = get_config_value('data.dataset_path', 'data/GymDataset.csv')
        
        self.dataset_path = Path(dataset_path)
        self.enable_cache = enable_cache
        self._cache: Optional[List[Exercise]] = None
        self._raw_dataframe: Optional[pd.DataFrame] = None
        
        logger.info(f"DataLoader initialized with path: {self.dataset_path}")
    
    def load(self, force_reload: bool = False) -> DataLoadResult:
        """
        Load exercises from CSV file.
        
        Args:
            force_reload: Force reload even if cached
            
        Returns:
            DataLoadResult: Result containing exercises and status
            
        Raises:
            FileNotFoundError: If dataset file doesn't exist
        """
        # Return cached data if available and not forcing reload
        if not force_reload and self._cache is not None and self.enable_cache:
            logger.info("Returning cached exercise data")
            return DataLoadResult(
                success=True,
                exercises=self._cache,
                loaded_count=len(self._cache),
                total_rows=len(self._cache)
            )
        
        # Check if file exists
        if not self.dataset_path.exists():
            error_msg = f"Dataset file not found: {self.dataset_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        
        try:
            logger.info(f"Loading dataset from: {self.dataset_path}")
            
            # Load CSV with pandas
            df = pd.read_csv(self.dataset_path)
            self._raw_dataframe = df
            
            total_rows = len(df)
            logger.info(f"Loaded {total_rows} rows from CSV")
            
            # Parse exercises
            exercises: List[Exercise] = []
            errors: List[str] = []
            
            for idx, row in df.iterrows():
                try:
                    exercise = self._parse_exercise_row(row, idx)
                    exercises.append(exercise)
                except Exception as e:
                    error_msg = f"Error parsing row {idx}: {str(e)}"
                    errors.append(error_msg)
                    logger.warning(error_msg)
            
            # Cache if enabled
            if self.enable_cache:
                self._cache = exercises
            
            result = DataLoadResult(
                success=True,
                exercises=exercises,
                error_count=len(errors),
                errors=errors,
                total_rows=total_rows,
                loaded_count=len(exercises)
            )
            
            logger.info(
                f"Successfully loaded {len(exercises)}/{total_rows} exercises "
                f"({len(errors)} errors)"
            )
            
            return result
            
        except Exception as e:
            error_msg = f"Failed to load dataset: {str(e)}"
            logger.error(error_msg)
            return DataLoadResult(
                success=False,
                exercises=[],
                error_count=1,
                errors=[error_msg]
            )
    
    def _parse_exercise_row(self, row: pd.Series, row_index: int) -> Exercise:
        """
        Parse a single row into an Exercise object.
        
        Args:
            row: Pandas Series representing a row
            row_index: Row index for error reporting
            
        Returns:
            Exercise: Parsed exercise object
            
        Raises:
            ValueError: If required fields are missing or invalid
        """
        # Parse category (required)
        try:
            category = ExerciseCategory(row['category'].lower())
        except (ValueError, KeyError) as e:
            raise ValueError(f"Invalid or missing category: {e}")
        
        # Parse intensity (optional, defaults to moderate)
        try:
            intensity_str = str(row.get('intensity', 'moderate')).lower()
            intensity = IntensityLevel(intensity_str)
        except (ValueError, AttributeError):
            intensity = IntensityLevel.MODERATE
        
        # Parse muscle groups (comma-separated)
        primary_muscles = self._parse_list_field(row.get('primary_muscles', ''))
        secondary_muscles = self._parse_list_field(row.get('secondary_muscles', ''))
        
        # Parse equipment (comma-separated)
        equipment = self._parse_list_field(row.get('equipment', 'none'))
        
        # Parse contraindications (semicolon-separated)
        contraindications = []
        if pd.notna(row.get('contraindications')):
            contraindications = [
                c.strip() for c in str(row['contraindications']).split(';')
                if c.strip()
            ]
        
        # Parse boolean fields
        is_compound = self._parse_bool(row.get('is_compound', False))
        is_bodyweight = self._parse_bool(row.get('is_bodyweight', False))
        
        # Create Exercise object
        exercise = Exercise(
            exercise_id=str(row.get('exercise_id', f'ex_{row_index}')),
            name=str(row['name']),
            category=category,
            primary_muscles=primary_muscles,
            secondary_muscles=secondary_muscles,
            difficulty=str(row.get('difficulty', 'intermediate')).lower(),
            equipment=equipment,
            calories_per_minute=float(row.get('calories_per_minute', 5.0)),
            typical_duration_minutes=int(row.get('typical_duration_minutes', 10)),
            intensity=intensity,
            description=str(row.get('description', '')),
            instructions=str(row.get('instructions', '')),
            benefits=self._parse_list_field(row.get('benefits', ''), separator=';'),
            contraindications=contraindications,
            is_compound=is_compound,
            is_bodyweight=is_bodyweight
        )
        
        return exercise
    
    def _parse_list_field(self, field_value, separator: str = ',') -> List[str]:
        """
        Parse comma-separated or semicolon-separated field into list.
        
        Args:
            field_value: Field value to parse
            separator: Separator character
            
        Returns:
            List[str]: Parsed list of strings
        """
        if pd.isna(field_value) or field_value == '':
            return []
        
        items = str(field_value).split(separator)
        return [item.strip() for item in items if item.strip()]
    
    def _parse_bool(self, value) -> bool:
        """
        Parse boolean value from various formats.
        
        Args:
            value: Value to parse
            
        Returns:
            bool: Parsed boolean
        """
        if isinstance(value, bool):
            return value
        if pd.isna(value):
            return False
        
        str_value = str(value).lower()
        return str_value in ['true', '1', 'yes', 't', 'y']
    
    def get_exercises(self) -> List[Exercise]:
        """
        Get all loaded exercises.
        
        Returns:
            List[Exercise]: All exercises (loads if not cached)
        """
        if self._cache is None:
            result = self.load()
            if not result.success:
                logger.error("Failed to load exercises")
                return []
        return self._cache or []
    
    def get_exercise_by_id(self, exercise_id: str) -> Optional[Exercise]:
        """
        Get exercise by ID.
        
        Args:
            exercise_id: Exercise identifier
            
        Returns:
            Exercise or None if not found
        """
        exercises = self.get_exercises()
        for exercise in exercises:
            if exercise.exercise_id == exercise_id:
                return exercise
        return None
    
    def get_exercise_by_name(self, name: str) -> Optional[Exercise]:
        """
        Get exercise by name (case-insensitive).
        
        Args:
            name: Exercise name
            
        Returns:
            Exercise or None if not found
        """
        exercises = self.get_exercises()
        name_lower = name.lower()
        for exercise in exercises:
            if exercise.name.lower() == name_lower:
                return exercise
        return None
    
    def filter_by_category(self, category: ExerciseCategory) -> List[Exercise]:
        """
        Filter exercises by category.
        
        Args:
            category: Exercise category
            
        Returns:
            List[Exercise]: Filtered exercises
        """
        exercises = self.get_exercises()
        return [ex for ex in exercises if ex.category == category]
    
    def filter_by_difficulty(self, difficulty: str) -> List[Exercise]:
        """
        Filter exercises by difficulty level.
        
        Args:
            difficulty: Difficulty level
            
        Returns:
            List[Exercise]: Filtered exercises
        """
        exercises = self.get_exercises()
        difficulty_lower = difficulty.lower()
        return [ex for ex in exercises if ex.difficulty == difficulty_lower]
    
    def filter_by_muscle_group(self, muscle_group: str) -> List[Exercise]:
        """
        Filter exercises that target specific muscle group.
        
        Args:
            muscle_group: Muscle group name
            
        Returns:
            List[Exercise]: Filtered exercises
        """
        exercises = self.get_exercises()
        muscle_lower = muscle_group.lower()
        
        filtered = []
        for ex in exercises:
            all_muscles = [m.lower() for m in ex.get_all_muscles()]
            if muscle_lower in all_muscles:
                filtered.append(ex)
        
        return filtered
    
    def filter_by_equipment(self, equipment: str) -> List[Exercise]:
        """
        Filter exercises that require specific equipment.
        
        Args:
            equipment: Equipment name
            
        Returns:
            List[Exercise]: Filtered exercises
        """
        exercises = self.get_exercises()
        equipment_lower = equipment.lower()
        
        return [
            ex for ex in exercises
            if equipment_lower in [e.lower() for e in ex.equipment]
        ]
    
    def filter_bodyweight_only(self) -> List[Exercise]:
        """
        Filter exercises that require no equipment.
        
        Returns:
            List[Exercise]: Bodyweight exercises
        """
        exercises = self.get_exercises()
        return [ex for ex in exercises if ex.is_bodyweight]
    
    def get_all_muscle_groups(self) -> Set[str]:
        """
        Get set of all muscle groups in dataset.
        
        Returns:
            Set[str]: All unique muscle groups
        """
        exercises = self.get_exercises()
        muscle_groups = set()
        for ex in exercises:
            muscle_groups.update(ex.get_all_muscles())
        return muscle_groups
    
    def get_all_equipment(self) -> Set[str]:
        """
        Get set of all equipment in dataset.
        
        Returns:
            Set[str]: All unique equipment
        """
        exercises = self.get_exercises()
        equipment = set()
        for ex in exercises:
            equipment.update(ex.equipment)
        return equipment
    
    def get_statistics(self) -> Dict[str, any]:
        """
        Get dataset statistics.
        
        Returns:
            Dict: Statistics about the dataset
        """
        exercises = self.get_exercises()
        
        if not exercises:
            return {}
        
        # Category distribution
        category_counts = {}
        for ex in exercises:
            cat = ex.category.value
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        # Difficulty distribution
        difficulty_counts = {}
        for ex in exercises:
            diff = ex.difficulty
            difficulty_counts[diff] = difficulty_counts.get(diff, 0) + 1
        
        return {
            'total_exercises': len(exercises),
            'categories': category_counts,
            'difficulties': difficulty_counts,
            'total_muscle_groups': len(self.get_all_muscle_groups()),
            'total_equipment_types': len(self.get_all_equipment()),
            'bodyweight_exercises': len(self.filter_bodyweight_only()),
            'compound_exercises': len([ex for ex in exercises if ex.is_compound])
        }
    
    def clear_cache(self) -> None:
        """Clear cached data."""
        self._cache = None
        self._raw_dataframe = None
        logger.info("Cache cleared")
    
    def __len__(self) -> int:
        """Return number of loaded exercises."""
        return len(self.get_exercises())
    
    def __repr__(self) -> str:
        """String representation."""
        return f"DataLoader(path={self.dataset_path}, exercises={len(self)})"
