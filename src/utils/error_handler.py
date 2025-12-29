"""
Error Handling and Validation Module.

Provides comprehensive error handling, validation, and graceful degradation
for the AI Gym Workout Recommendation System.
"""

from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import logging
from functools import wraps


# Setup logger
logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """Error severity levels."""
    LOW = "low"  # Warning, system can continue
    MEDIUM = "medium"  # Error, but fallback available
    HIGH = "high"  # Critical error, operation fails
    CRITICAL = "critical"  # System-level error


class ErrorCode(Enum):
    """Standardized error codes."""
    # Data errors
    DATA_NOT_FOUND = "DATA_001"
    DATA_INVALID_FORMAT = "DATA_002"
    DATA_VALIDATION_FAILED = "DATA_003"
    DATA_LOAD_FAILED = "DATA_004"
    
    # Input validation errors
    INVALID_STATE = "INPUT_001"
    INVALID_EQUIPMENT = "INPUT_002"
    INVALID_TIME = "INPUT_003"
    INVALID_PREFERENCES = "INPUT_004"
    
    # Search algorithm errors
    SEARCH_NO_SOLUTION = "SEARCH_001"
    SEARCH_TIMEOUT = "SEARCH_002"
    SEARCH_INVALID_PROBLEM = "SEARCH_003"
    
    # Agent errors
    AGENT_INITIALIZATION_FAILED = "AGENT_001"
    AGENT_EXECUTION_FAILED = "AGENT_002"
    
    # Generation errors
    GENERATION_FAILED = "GEN_001"
    NO_EXERCISES_AVAILABLE = "GEN_002"
    INSUFFICIENT_TIME = "GEN_003"
    
    # System errors
    SYSTEM_ERROR = "SYS_001"
    CONFIGURATION_ERROR = "SYS_002"
    DEPENDENCY_ERROR = "SYS_003"


@dataclass
class SystemError:
    """Structured error information."""
    code: ErrorCode
    message: str
    severity: ErrorSeverity
    context: Dict[str, Any]
    original_exception: Optional[Exception] = None
    
    def __str__(self) -> str:
        """String representation."""
        return f"[{self.code.value}] {self.severity.value.upper()}: {self.message}"


class ErrorHandler:
    """
    Centralized error handling system.
    
    Provides:
    - Error logging and tracking
    - Graceful degradation
    - User-friendly error messages
    - Error recovery strategies
    """
    
    def __init__(self):
        """Initialize error handler."""
        self.errors: List[SystemError] = []
        self.error_count: Dict[ErrorCode, int] = {}
    
    def handle_error(
        self,
        code: ErrorCode,
        message: str,
        severity: ErrorSeverity,
        context: Optional[Dict[str, Any]] = None,
        exception: Optional[Exception] = None
    ) -> SystemError:
        """
        Handle an error with proper logging and tracking.
        
        Args:
            code: Error code
            message: Error message
            severity: Error severity
            context: Additional context
            exception: Original exception if any
        
        Returns:
            SystemError object
        """
        error = SystemError(
            code=code,
            message=message,
            severity=severity,
            context=context or {},
            original_exception=exception
        )
        
        # Track error
        self.errors.append(error)
        self.error_count[code] = self.error_count.get(code, 0) + 1
        
        # Log based on severity
        if severity == ErrorSeverity.CRITICAL:
            logger.critical(str(error), exc_info=exception)
        elif severity == ErrorSeverity.HIGH:
            logger.error(str(error), exc_info=exception)
        elif severity == ErrorSeverity.MEDIUM:
            logger.warning(str(error))
        else:
            logger.info(str(error))
        
        return error
    
    def get_user_friendly_message(self, error: SystemError) -> str:
        """
        Convert technical error to user-friendly message.
        
        Args:
            error: System error
        
        Returns:
            User-friendly error message
        """
        messages = {
            ErrorCode.DATA_NOT_FOUND: "Exercise database not found. Please ensure GymDataset.csv is in the data folder.",
            ErrorCode.DATA_INVALID_FORMAT: "Exercise data format is invalid. Please check the data file.",
            ErrorCode.DATA_VALIDATION_FAILED: "Some exercises failed validation and were excluded.",
            ErrorCode.INVALID_STATE: "Invalid user profile. Please check your age, weight, height, and fitness level.",
            ErrorCode.INVALID_EQUIPMENT: "Invalid equipment selection. Please choose from available options.",
            ErrorCode.INVALID_TIME: "Invalid workout duration. Please enter a time between 10 and 180 minutes.",
            ErrorCode.SEARCH_NO_SOLUTION: "Could not find a workout matching your requirements. Try adjusting constraints.",
            ErrorCode.SEARCH_TIMEOUT: "Workout generation took too long. Using simplified search.",
            ErrorCode.NO_EXERCISES_AVAILABLE: "No exercises match your requirements. Try different equipment or constraints.",
            ErrorCode.INSUFFICIENT_TIME: "Not enough time for any exercises. Please increase available time.",
            ErrorCode.GENERATION_FAILED: "Workout generation failed. Please try again or adjust parameters.",
            ErrorCode.SYSTEM_ERROR: "An unexpected error occurred. Please try again.",
        }
        
        return messages.get(error.code, error.message)
    
    def get_recovery_suggestion(self, error: SystemError) -> Optional[str]:
        """
        Get suggested recovery action for error.
        
        Args:
            error: System error
        
        Returns:
            Recovery suggestion or None
        """
        suggestions = {
            ErrorCode.DATA_NOT_FOUND: "Run: python src/infrastructure/data/data_loader.py to generate sample data.",
            ErrorCode.INVALID_TIME: "Set available_time between 10 and 180 minutes.",
            ErrorCode.NO_EXERCISES_AVAILABLE: "Try: 1) Select 'None' equipment for bodyweight exercises, 2) Increase available time, 3) Change fitness level.",
            ErrorCode.SEARCH_NO_SOLUTION: "Reduce max_exercises, increase available_time, or change search strategy.",
            ErrorCode.GENERATION_FAILED: "Try a different generation algorithm (GREEDY, BALANCED, or TIME_OPTIMIZED).",
        }
        
        return suggestions.get(error.code)
    
    def clear_errors(self):
        """Clear error history."""
        self.errors.clear()
        self.error_count.clear()
    
    def get_error_summary(self) -> Dict[str, Any]:
        """
        Get summary of all errors.
        
        Returns:
            Error summary statistics
        """
        return {
            "total_errors": len(self.errors),
            "by_severity": {
                severity.value: sum(1 for e in self.errors if e.severity == severity)
                for severity in ErrorSeverity
            },
            "by_code": {
                code.value: count
                for code, count in self.error_count.items()
            },
            "recent_errors": [str(e) for e in self.errors[-5:]]
        }


# Global error handler instance
error_handler = ErrorHandler()


def handle_errors(
    default_return: Any = None,
    error_code: ErrorCode = ErrorCode.SYSTEM_ERROR,
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
):
    """
    Decorator for automatic error handling.
    
    Args:
        default_return: Value to return on error
        error_code: Error code to use
        severity: Error severity
    
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error = error_handler.handle_error(
                    code=error_code,
                    message=f"Error in {func.__name__}: {str(e)}",
                    severity=severity,
                    context={"function": func.__name__, "args": str(args)[:100]},
                    exception=e
                )
                
                logger.error(f"Function {func.__name__} failed: {error}")
                return default_return
        
        return wrapper
    return decorator


class InputValidator:
    """
    Validates user inputs with comprehensive checks.
    """
    
    @staticmethod
    def validate_age(age: int) -> tuple[bool, Optional[str]]:
        """Validate age input."""
        if not isinstance(age, int):
            return False, "Age must be an integer"
        if age < 10 or age > 100:
            return False, "Age must be between 10 and 100"
        return True, None
    
    @staticmethod
    def validate_weight(weight: float) -> tuple[bool, Optional[str]]:
        """Validate weight input."""
        if not isinstance(weight, (int, float)):
            return False, "Weight must be a number"
        if weight < 30 or weight > 300:
            return False, "Weight must be between 30 and 300 kg"
        return True, None
    
    @staticmethod
    def validate_height(height: float) -> tuple[bool, Optional[str]]:
        """Validate height input."""
        if not isinstance(height, (int, float)):
            return False, "Height must be a number"
        if height < 100 or height > 250:
            return False, "Height must be between 100 and 250 cm"
        return True, None
    
    @staticmethod
    def validate_energy(energy: int) -> tuple[bool, Optional[str]]:
        """Validate energy level."""
        if not isinstance(energy, int):
            return False, "Energy must be an integer"
        if energy < 1 or energy > 10:
            return False, "Energy must be between 1 and 10"
        return True, None
    
    @staticmethod
    def validate_time(time_minutes: int) -> tuple[bool, Optional[str]]:
        """Validate workout duration."""
        if not isinstance(time_minutes, int):
            return False, "Time must be an integer"
        if time_minutes < 10:
            return False, "Workout time must be at least 10 minutes"
        if time_minutes > 180:
            return False, "Workout time cannot exceed 180 minutes (3 hours)"
        return True, None
    
    @staticmethod
    def validate_equipment(equipment: List[str]) -> tuple[bool, Optional[str]]:
        """Validate equipment list."""
        if not isinstance(equipment, list):
            return False, "Equipment must be a list"
        if len(equipment) == 0:
            return False, "At least one equipment option must be selected"
        
        valid_equipment = {
            "None", "Dumbbells", "Barbell", "Resistance Bands",
            "Pull-up Bar", "Bench", "Kettlebell", "Medicine Ball",
            "Jump Rope", "Squat Rack", "Cable Machine"
        }
        
        for item in equipment:
            if item not in valid_equipment:
                return False, f"Invalid equipment: {item}"
        
        return True, None
    
    @staticmethod
    def validate_fitness_level(level: str) -> tuple[bool, Optional[str]]:
        """Validate fitness level."""
        valid_levels = {"beginner", "intermediate", "advanced"}
        if level.lower() not in valid_levels:
            return False, f"Fitness level must be one of: {', '.join(valid_levels)}"
        return True, None
    
    @staticmethod
    def validate_goal(goal: str) -> tuple[bool, Optional[str]]:
        """Validate fitness goal."""
        valid_goals = {
            "weight_loss", "muscle_gain", "endurance",
            "strength", "flexibility", "general_fitness"
        }
        if goal.lower() not in valid_goals:
            return False, f"Goal must be one of: {', '.join(valid_goals)}"
        return True, None
    
    @staticmethod
    def validate_state(state) -> List[str]:
        """
        Validate complete state object.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        valid, msg = InputValidator.validate_age(state.age)
        if not valid:
            errors.append(msg)
        
        valid, msg = InputValidator.validate_weight(state.weight)
        if not valid:
            errors.append(msg)
        
        valid, msg = InputValidator.validate_height(state.height)
        if not valid:
            errors.append(msg)
        
        valid, msg = InputValidator.validate_energy(state.current_energy)
        if not valid:
            errors.append(msg)
        
        valid, msg = InputValidator.validate_fitness_level(state.fitness_level)
        if not valid:
            errors.append(msg)
        
        valid, msg = InputValidator.validate_goal(state.goal)
        if not valid:
            errors.append(msg)
        
        return errors


class SafetyValidator:
    """
    Validates safety constraints for workouts.
    """
    
    @staticmethod
    def check_injury_compatibility(exercise_name: str, injuries: List[str]) -> tuple[bool, List[str]]:
        """
        Check if exercise is safe with given injuries.
        
        Args:
            exercise_name: Exercise name
            injuries: List of injuries
        
        Returns:
            (is_safe, warnings)
        """
        if not injuries:
            return True, []
        
        warnings = []
        exercise_lower = exercise_name.lower()
        
        # Injury-exercise incompatibility rules
        rules = {
            "knee": ["squat", "lunge", "jump", "run", "leg press", "box jump"],
            "lower back": ["deadlift", "squat", "row", "sit-up", "leg raise"],
            "shoulder": ["overhead press", "pull-up", "shoulder press", "lateral raise", "bench press"],
            "ankle": ["run", "jump", "calf raise", "box jump", "burpee"],
            "wrist": ["push-up", "plank", "bench press", "overhead press", "barbell"],
            "elbow": ["push-up", "pull-up", "tricep", "bicep curl", "overhead press"],
            "hip": ["squat", "lunge", "leg press", "hip thrust", "leg raise"]
        }
        
        for injury in injuries:
            injury_lower = injury.lower()
            if injury_lower in rules:
                risky_exercises = rules[injury_lower]
                for risky in risky_exercises:
                    if risky in exercise_lower:
                        warnings.append(f"Exercise '{exercise_name}' may aggravate {injury} injury")
                        return False, warnings
        
        return True, warnings
    
    @staticmethod
    def check_intensity_safety(
        difficulty: str,
        fitness_level: str,
        energy: int
    ) -> tuple[bool, Optional[str]]:
        """
        Check if exercise intensity is safe for user.
        
        Args:
            difficulty: Exercise difficulty
            fitness_level: User fitness level
            energy: Current energy level
        
        Returns:
            (is_safe, warning)
        """
        # Map levels to scores
        difficulty_scores = {"easy": 1, "medium": 2, "hard": 3}
        fitness_scores = {"beginner": 1, "intermediate": 2, "advanced": 3}
        
        diff_score = difficulty_scores.get(difficulty.lower(), 2)
        fit_score = fitness_scores.get(fitness_level.lower(), 1)
        
        # Check if difficulty too high
        if diff_score > fit_score + 1:
            return False, f"Exercise difficulty ({difficulty}) may be too high for {fitness_level} level"
        
        # Check if energy too low
        if energy < 4 and diff_score >= 3:
            return False, f"Current energy ({energy}/10) may be too low for {difficulty} exercises"
        
        return True, None
    
    @staticmethod
    def check_duration_safety(
        total_duration: int,
        fitness_level: str,
        age: int
    ) -> tuple[bool, Optional[str]]:
        """
        Check if workout duration is safe.
        
        Args:
            total_duration: Total workout duration in minutes
            fitness_level: User fitness level
            age: User age
        
        Returns:
            (is_safe, warning)
        """
        # Maximum safe durations
        max_durations = {
            "beginner": 45,
            "intermediate": 75,
            "advanced": 120
        }
        
        max_duration = max_durations.get(fitness_level.lower(), 60)
        
        # Adjust for age
        if age > 60:
            max_duration = int(max_duration * 0.75)
        elif age > 50:
            max_duration = int(max_duration * 0.85)
        
        if total_duration > max_duration:
            return False, f"Workout duration ({total_duration} min) exceeds recommended maximum ({max_duration} min) for {fitness_level} level"
        
        return True, None


class GracefulDegradation:
    """
    Provides fallback strategies when operations fail.
    """
    
    @staticmethod
    def get_fallback_exercises(
        all_exercises: List,
        required_count: int = 3
    ) -> List:
        """
        Get safe fallback exercises when generation fails.
        
        Args:
            all_exercises: Complete exercise list
            required_count: Number of exercises needed
        
        Returns:
            List of safe fallback exercises
        """
        # Select simple, safe exercises
        safe_exercises = [
            ex for ex in all_exercises
            if ex.equipment == "None" and ex.difficulty.value == "easy"
        ]
        
        # If not enough safe exercises, include medium difficulty
        if len(safe_exercises) < required_count:
            safe_exercises.extend([
                ex for ex in all_exercises
                if ex.equipment == "None" and ex.difficulty.value == "medium"
            ])
        
        # Return requested count
        return safe_exercises[:required_count]
    
    @staticmethod
    def simplify_search_strategy(original_strategy: str) -> str:
        """
        Simplify search strategy if original fails.
        
        Args:
            original_strategy: Original strategy that failed
        
        Returns:
            Simpler fallback strategy
        """
        fallback_chain = {
            "UTILITY_BASED": "GOAL_BASED",
            "GOAL_BASED": "MODEL_BASED",
            "MODEL_BASED": "SIMPLE_REFLEX",
            "LEARNING": "SIMPLE_REFLEX",
        }
        
        return fallback_chain.get(original_strategy, "SIMPLE_REFLEX")
    
    @staticmethod
    def reduce_constraints(
        config: Dict[str, Any],
        step: int = 1
    ) -> Dict[str, Any]:
        """
        Progressively reduce constraints to find solution.
        
        Args:
            config: Original configuration
            step: Reduction step (1-3)
        
        Returns:
            Modified configuration with relaxed constraints
        """
        modified = config.copy()
        
        if step >= 1:
            # Increase time tolerance
            if "target_duration" in modified:
                modified["target_duration"] = int(modified["target_duration"] * 1.2)
        
        if step >= 2:
            # Reduce exercise count requirement
            if "min_exercises" in modified:
                modified["min_exercises"] = max(2, modified["min_exercises"] - 1)
        
        if step >= 3:
            # Remove equipment restrictions
            if "available_equipment" in modified:
                if "None" not in modified["available_equipment"]:
                    modified["available_equipment"].append("None")
        
        return modified


def validate_and_handle_errors(func: Callable) -> Callable:
    """
    Comprehensive decorator combining validation and error handling.
    
    Args:
        func: Function to wrap
    
    Returns:
        Wrapped function with validation and error handling
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Attempt execution
            result = func(*args, **kwargs)
            return result
            
        except ValueError as e:
            error_handler.handle_error(
                code=ErrorCode.INVALID_STATE,
                message=f"Validation error: {str(e)}",
                severity=ErrorSeverity.MEDIUM,
                context={"function": func.__name__},
                exception=e
            )
            raise
            
        except FileNotFoundError as e:
            error_handler.handle_error(
                code=ErrorCode.DATA_NOT_FOUND,
                message=f"Data file not found: {str(e)}",
                severity=ErrorSeverity.HIGH,
                context={"function": func.__name__},
                exception=e
            )
            raise
            
        except Exception as e:
            error_handler.handle_error(
                code=ErrorCode.SYSTEM_ERROR,
                message=f"Unexpected error: {str(e)}",
                severity=ErrorSeverity.HIGH,
                context={"function": func.__name__},
                exception=e
            )
            raise
    
    return wrapper
