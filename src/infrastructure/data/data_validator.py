"""
Data Validator Module
=====================

Provides comprehensive data validation for gym exercise data.

This module ensures data quality and integrity through:
- Schema validation
- Value range validation
- Referential integrity checks
- Business rule validation
- Data consistency checks

Follows the Validator pattern for separation of concerns.

Author: AI Engineer
Date: December 17, 2025
"""

from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass, field
import logging
from src.domain.models.exercise import Exercise, ExerciseCategory, IntensityLevel


logger = logging.getLogger(__name__)


@dataclass
class ValidationIssue:
    """
    Represents a validation issue.
    
    Attributes:
        severity: Severity level (error, warning, info)
        field: Field name with issue
        message: Description of the issue
        exercise_id: ID of exercise with issue (optional)
        value: Actual value that caused issue (optional)
    """
    severity: str  # "error", "warning", "info"
    field: str
    message: str
    exercise_id: Optional[str] = None
    value: Optional[any] = None
    
    def __str__(self) -> str:
        """String representation."""
        prefix = f"[{self.severity.upper()}]"
        ex_id = f" ({self.exercise_id})" if self.exercise_id else ""
        return f"{prefix}{ex_id} {self.field}: {self.message}"


@dataclass
class ValidationReport:
    """
    Comprehensive validation report.
    
    Attributes:
        is_valid: Whether data passed validation
        error_count: Number of errors
        warning_count: Number of warnings
        info_count: Number of info messages
        issues: List of all validation issues
        exercises_validated: Number of exercises validated
    """
    is_valid: bool = True
    error_count: int = 0
    warning_count: int = 0
    info_count: int = 0
    issues: List[ValidationIssue] = field(default_factory=list)
    exercises_validated: int = 0
    
    def add_issue(self, issue: ValidationIssue) -> None:
        """Add validation issue to report."""
        self.issues.append(issue)
        
        if issue.severity == "error":
            self.error_count += 1
            self.is_valid = False
        elif issue.severity == "warning":
            self.warning_count += 1
        elif issue.severity == "info":
            self.info_count += 1
    
    def get_errors(self) -> List[ValidationIssue]:
        """Get all error-level issues."""
        return [i for i in self.issues if i.severity == "error"]
    
    def get_warnings(self) -> List[ValidationIssue]:
        """Get all warning-level issues."""
        return [i for i in self.issues if i.severity == "warning"]
    
    def get_summary(self) -> str:
        """Get text summary of validation report."""
        lines = [
            "=== Validation Report ===",
            f"Valid: {self.is_valid}",
            f"Exercises Validated: {self.exercises_validated}",
            f"Errors: {self.error_count}",
            f"Warnings: {self.warning_count}",
            f"Info: {self.info_count}",
            ""
        ]
        
        if self.error_count > 0:
            lines.append("Errors:")
            for error in self.get_errors():
                lines.append(f"  - {error}")
            lines.append("")
        
        if self.warning_count > 0:
            lines.append("Warnings:")
            for warning in self.get_warnings()[:10]:  # Limit to 10
                lines.append(f"  - {warning}")
            if self.warning_count > 10:
                lines.append(f"  ... and {self.warning_count - 10} more")
        
        return "\n".join(lines)


class DataValidator:
    """
    Validates gym exercise data for correctness and consistency.
    
    This class implements comprehensive validation rules to ensure
    data quality before it's used by the AI system.
    
    Validation Categories:
    1. Schema Validation - Required fields, data types
    2. Range Validation - Value boundaries
    3. Referential Integrity - Valid references
    4. Business Rules - Domain-specific constraints
    5. Consistency - Logical consistency between fields
    
    Example:
        >>> validator = DataValidator()
        >>> report = validator.validate_exercises(exercises)
        >>> if not report.is_valid:
        ...     print(report.get_summary())
    """
    
    # Valid values for validation
    VALID_CATEGORIES = {cat.value for cat in ExerciseCategory}
    VALID_INTENSITIES = {intensity.value for intensity in IntensityLevel}
    VALID_DIFFICULTIES = {"beginner", "intermediate", "advanced", "expert"}
    
    # Reasonable ranges
    MIN_CALORIES_PER_MINUTE = 0.5
    MAX_CALORIES_PER_MINUTE = 20.0
    MIN_DURATION = 1
    MAX_DURATION = 120
    
    def __init__(self, strict_mode: bool = False):
        """
        Initialize validator.
        
        Args:
            strict_mode: If True, warnings become errors
        """
        self.strict_mode = strict_mode
        logger.info(f"DataValidator initialized (strict_mode={strict_mode})")
    
    def validate_exercises(self, exercises: List[Exercise]) -> ValidationReport:
        """
        Validate a list of exercises.
        
        Args:
            exercises: List of exercises to validate
            
        Returns:
            ValidationReport: Comprehensive validation report
        """
        report = ValidationReport()
        report.exercises_validated = len(exercises)
        
        logger.info(f"Validating {len(exercises)} exercises")
        
        # Track for cross-validation
        exercise_ids = set()
        exercise_names = set()
        
        for exercise in exercises:
            # Validate individual exercise
            self._validate_exercise(exercise, report)
            
            # Check for duplicate IDs
            if exercise.exercise_id in exercise_ids:
                report.add_issue(ValidationIssue(
                    severity="error",
                    field="exercise_id",
                    message=f"Duplicate exercise ID: {exercise.exercise_id}",
                    exercise_id=exercise.exercise_id
                ))
            exercise_ids.add(exercise.exercise_id)
            
            # Check for duplicate names
            if exercise.name.lower() in exercise_names:
                report.add_issue(ValidationIssue(
                    severity="warning",
                    field="name",
                    message=f"Duplicate exercise name: {exercise.name}",
                    exercise_id=exercise.exercise_id
                ))
            exercise_names.add(exercise.name.lower())
        
        # Cross-validation
        self._validate_dataset_completeness(exercises, report)
        
        logger.info(
            f"Validation complete: {report.exercises_validated} exercises, "
            f"{report.error_count} errors, {report.warning_count} warnings"
        )
        
        return report
    
    def _validate_exercise(self, exercise: Exercise, report: ValidationReport) -> None:
        """
        Validate a single exercise.
        
        Args:
            exercise: Exercise to validate
            report: Report to add issues to
        """
        ex_id = exercise.exercise_id
        
        # Required field validation
        self._validate_required_fields(exercise, report)
        
        # Value range validation
        self._validate_ranges(exercise, report)
        
        # Category and difficulty validation
        self._validate_enums(exercise, report)
        
        # Muscle group validation
        self._validate_muscle_groups(exercise, report)
        
        # Equipment validation
        self._validate_equipment(exercise, report)
        
        # Business rule validation
        self._validate_business_rules(exercise, report)
        
        # Consistency validation
        self._validate_consistency(exercise, report)
    
    def _validate_required_fields(self, exercise: Exercise, report: ValidationReport) -> None:
        """Validate required fields are present and non-empty."""
        ex_id = exercise.exercise_id
        
        if not exercise.exercise_id or exercise.exercise_id.strip() == "":
            report.add_issue(ValidationIssue(
                severity="error",
                field="exercise_id",
                message="Exercise ID is required",
                exercise_id=ex_id
            ))
        
        if not exercise.name or exercise.name.strip() == "":
            report.add_issue(ValidationIssue(
                severity="error",
                field="name",
                message="Exercise name is required",
                exercise_id=ex_id
            ))
        
        if not exercise.primary_muscles or len(exercise.primary_muscles) == 0:
            severity = "error" if self.strict_mode else "warning"
            report.add_issue(ValidationIssue(
                severity=severity,
                field="primary_muscles",
                message="No primary muscles specified",
                exercise_id=ex_id
            ))
    
    def _validate_ranges(self, exercise: Exercise, report: ValidationReport) -> None:
        """Validate numeric values are within reasonable ranges."""
        ex_id = exercise.exercise_id
        
        # Calories per minute
        if exercise.calories_per_minute < self.MIN_CALORIES_PER_MINUTE:
            report.add_issue(ValidationIssue(
                severity="warning",
                field="calories_per_minute",
                message=f"Calories per minute ({exercise.calories_per_minute}) is very low",
                exercise_id=ex_id,
                value=exercise.calories_per_minute
            ))
        
        if exercise.calories_per_minute > self.MAX_CALORIES_PER_MINUTE:
            report.add_issue(ValidationIssue(
                severity="warning",
                field="calories_per_minute",
                message=f"Calories per minute ({exercise.calories_per_minute}) is very high",
                exercise_id=ex_id,
                value=exercise.calories_per_minute
            ))
        
        # Duration
        if exercise.typical_duration_minutes < self.MIN_DURATION:
            report.add_issue(ValidationIssue(
                severity="error",
                field="typical_duration_minutes",
                message=f"Duration ({exercise.typical_duration_minutes}) is too short",
                exercise_id=ex_id,
                value=exercise.typical_duration_minutes
            ))
        
        if exercise.typical_duration_minutes > self.MAX_DURATION:
            report.add_issue(ValidationIssue(
                severity="warning",
                field="typical_duration_minutes",
                message=f"Duration ({exercise.typical_duration_minutes}) is very long",
                exercise_id=ex_id,
                value=exercise.typical_duration_minutes
            ))
    
    def _validate_enums(self, exercise: Exercise, report: ValidationReport) -> None:
        """Validate enum values are valid."""
        ex_id = exercise.exercise_id
        
        # Category is already validated by ExerciseCategory enum in Exercise class
        
        # Difficulty
        if exercise.difficulty.lower() not in self.VALID_DIFFICULTIES:
            report.add_issue(ValidationIssue(
                severity="error",
                field="difficulty",
                message=f"Invalid difficulty: {exercise.difficulty}",
                exercise_id=ex_id,
                value=exercise.difficulty
            ))
        
        # Intensity is already validated by IntensityLevel enum
    
    def _validate_muscle_groups(self, exercise: Exercise, report: ValidationReport) -> None:
        """Validate muscle group specifications."""
        ex_id = exercise.exercise_id
        
        # Check for overlap between primary and secondary
        primary_set = {m.lower() for m in exercise.primary_muscles}
        secondary_set = {m.lower() for m in exercise.secondary_muscles}
        
        overlap = primary_set.intersection(secondary_set)
        if overlap:
            report.add_issue(ValidationIssue(
                severity="warning",
                field="muscle_groups",
                message=f"Muscle groups in both primary and secondary: {overlap}",
                exercise_id=ex_id
            ))
        
        # Compound exercises should target multiple muscle groups
        if exercise.is_compound and len(exercise.primary_muscles) < 2:
            report.add_issue(ValidationIssue(
                severity="info",
                field="is_compound",
                message="Compound exercise should target multiple muscle groups",
                exercise_id=ex_id
            ))
    
    def _validate_equipment(self, exercise: Exercise, report: ValidationReport) -> None:
        """Validate equipment specifications."""
        ex_id = exercise.exercise_id
        
        # Bodyweight exercises should have no equipment or "none"
        if exercise.is_bodyweight:
            if exercise.equipment and len(exercise.equipment) > 0:
                equipment_list = [e.lower() for e in exercise.equipment]
                if equipment_list != ["none"]:
                    report.add_issue(ValidationIssue(
                        severity="warning",
                        field="is_bodyweight",
                        message="Bodyweight exercise has equipment listed",
                        exercise_id=ex_id
                    ))
        
        # Exercises with equipment should not be marked bodyweight
        if not exercise.is_bodyweight:
            if not exercise.equipment or exercise.equipment == ["none"]:
                report.add_issue(ValidationIssue(
                    severity="info",
                    field="is_bodyweight",
                    message="Exercise with no equipment should be marked bodyweight",
                    exercise_id=ex_id
                ))
    
    def _validate_business_rules(self, exercise: Exercise, report: ValidationReport) -> None:
        """Validate domain-specific business rules."""
        ex_id = exercise.exercise_id
        
        # Warmup/cooldown should have lower intensity
        if exercise.category in [ExerciseCategory.WARMUP, ExerciseCategory.COOLDOWN]:
            if exercise.intensity not in [IntensityLevel.LOW, IntensityLevel.MODERATE]:
                report.add_issue(ValidationIssue(
                    severity="warning",
                    field="intensity",
                    message=f"Warmup/cooldown should be low or moderate intensity",
                    exercise_id=ex_id
                ))
        
        # Cardio should have reasonable calorie burn
        if exercise.category == ExerciseCategory.CARDIO:
            if exercise.calories_per_minute < 5.0:
                report.add_issue(ValidationIssue(
                    severity="info",
                    field="calories_per_minute",
                    message="Cardio exercise has low calorie burn",
                    exercise_id=ex_id
                ))
        
        # Flexibility should have lower calories
        if exercise.category == ExerciseCategory.FLEXIBILITY:
            if exercise.calories_per_minute > 6.0:
                report.add_issue(ValidationIssue(
                    severity="info",
                    field="calories_per_minute",
                    message="Flexibility exercise has high calorie burn",
                    exercise_id=ex_id
                ))
        
        # Expert level should be challenging
        if exercise.difficulty == "expert":
            if exercise.intensity == IntensityLevel.LOW:
                report.add_issue(ValidationIssue(
                    severity="warning",
                    field="intensity",
                    message="Expert exercise should not be low intensity",
                    exercise_id=ex_id
                ))
    
    def _validate_consistency(self, exercise: Exercise, report: ValidationReport) -> None:
        """Validate logical consistency between fields."""
        ex_id = exercise.exercise_id
        
        # High intensity should correlate with higher calories
        if exercise.intensity == IntensityLevel.VERY_HIGH:
            if exercise.calories_per_minute < 7.0:
                report.add_issue(ValidationIssue(
                    severity="info",
                    field="calories_per_minute",
                    message="Very high intensity exercise has low calorie burn",
                    exercise_id=ex_id
                ))
        
        # Beginner exercises should not be very high intensity
        if exercise.difficulty == "beginner":
            if exercise.intensity == IntensityLevel.VERY_HIGH:
                report.add_issue(ValidationIssue(
                    severity="warning",
                    field="consistency",
                    message="Beginner exercise should not be very high intensity",
                    exercise_id=ex_id
                ))
    
    def _validate_dataset_completeness(
        self,
        exercises: List[Exercise],
        report: ValidationReport
    ) -> None:
        """Validate overall dataset completeness."""
        
        # Check category coverage
        categories_present = {ex.category for ex in exercises}
        essential_categories = {
            ExerciseCategory.STRENGTH,
            ExerciseCategory.CARDIO,
            ExerciseCategory.FLEXIBILITY
        }
        
        missing_categories = essential_categories - categories_present
        if missing_categories:
            report.add_issue(ValidationIssue(
                severity="warning",
                field="dataset",
                message=f"Missing essential categories: {[c.value for c in missing_categories]}"
            ))
        
        # Check difficulty level coverage
        difficulties_present = {ex.difficulty for ex in exercises}
        if len(difficulties_present) < 3:
            report.add_issue(ValidationIssue(
                severity="info",
                field="dataset",
                message="Limited difficulty level variety in dataset"
            ))
        
        # Check for bodyweight exercises
        bodyweight_count = len([ex for ex in exercises if ex.is_bodyweight])
        if bodyweight_count < 10:
            report.add_issue(ValidationIssue(
                severity="info",
                field="dataset",
                message=f"Limited bodyweight exercises ({bodyweight_count})"
            ))
    
    def validate_single_exercise(self, exercise: Exercise) -> ValidationReport:
        """
        Validate a single exercise.
        
        Args:
            exercise: Exercise to validate
            
        Returns:
            ValidationReport: Validation report
        """
        report = ValidationReport()
        report.exercises_validated = 1
        self._validate_exercise(exercise, report)
        return report
