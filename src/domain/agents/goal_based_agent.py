"""
Goal-Based Agent Implementation.

A goal-based agent makes decisions by considering the desirability of goal
states. It defines explicit goals and plans actions to achieve them.

Function: action_sequence = GOAL-BASED(current_state, goal_state)

Properties:
- Explicit goal representation
- Defines target fitness state
- Plans workout direction toward goal
- More flexible than reflex agents
- Reasons about future goal achievement

Use Case: Long-term workout planning and fitness goal definition.

Purpose in Workflow:
- Step 2: Defines the fitness goal and target state after safety filtering
- Goal types:
  * Weight Loss → target weight, cardio focus
  * Muscle Gain → target muscle mass, strength focus
  * Endurance → target stamina, cardio/endurance focus
  * General Fitness → balanced target across all areas
- Sets the direction for workout plan optimization

Time Complexity: O(1) for goal definition
Space Complexity: O(1) for goal storage
"""

from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime

from .agent import Agent, AgentType, Percept, AgentAction
from ..models.state import State, FitnessGoal, ExperienceLevel
from ..models.action import Action, ActionType
from ..search.search_problem import SearchProblem, SearchSolution
from ..search.astar import AStarSearch


@dataclass
class Goal:
    """
    Representation of an agent goal.
    
    Attributes:
        goal_id: Unique identifier
        description: Human-readable description
        target_state: Desired state to achieve
        priority: Goal priority (higher = more important)
        deadline: Optional deadline for goal
        is_achieved: Whether goal has been achieved
        progress: Progress toward goal (0.0-1.0)
        metadata: Additional goal information
    """
    goal_id: str
    description: str
    target_state: State
    priority: int = 1
    deadline: Optional[datetime] = None
    is_achieved: bool = False
    progress: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def evaluate_progress(self, current_state: State) -> float:
        """
        Evaluate progress toward this goal.
        
        Args:
            current_state: Current state
            
        Returns:
            Progress score (0.0-1.0)
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        # Calculate progress based on exercises completed and duration
        target_exercises = self.metadata.get('target_exercises', 6)
        target_duration = self.metadata.get('target_duration', 45)
        
        # Progress is average of exercise completion and duration progress
        exercise_progress = min(1.0, current_state.exercises_completed / max(1, target_exercises))
        duration_progress = min(1.0, current_state.total_workout_duration / max(1, target_duration))
        
        self.progress = (exercise_progress + duration_progress) / 2.0
        return self.progress
    
    def is_satisfied(self, current_state: State) -> bool:
        """
        Check if goal is satisfied by current state.
        
        Args:
            current_state: Current state
            
        Returns:
            True if goal achieved, False otherwise
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        # Check if target state conditions are met using actual method signature
        target_exercises = self.metadata.get('target_exercises', 6)
        target_duration = self.metadata.get('target_duration', 45)
        self.is_achieved = current_state.is_goal_state(target_exercises, target_duration)
        return self.is_achieved


class WorkoutSearchProblem(SearchProblem):
    """
    Search problem for finding workout plans to achieve goals.
    
    This problem defines:
    - Initial state: Current user fitness state
    - Goal state: Desired fitness state
    - Actions: Workout exercises
    - Cost: Time, difficulty, energy expenditure
    """
    
    def __init__(
        self, 
        initial_state: State, 
        goal_state: State,
        available_actions: List[Action]
    ):
        """
        Initialize workout search problem.
        
        Args:
            initial_state: Starting state
            goal_state: Target state
            available_actions: List of possible actions
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        super().__init__(initial_state, goal_state)
        self._available_actions = available_actions
    
    def get_available_actions(self, state: State) -> List[Action]:
        """
        Get actions applicable in the given state.
        
        Args:
            state: Current state
            
        Returns:
            List of applicable actions
            
        Time Complexity: O(A) where A is total actions
        Space Complexity: O(k) where k is applicable actions
        """
        return [
            action for action in self._available_actions
            if action.is_applicable(state)
        ]
    
    def get_successor(self, state: State, action: Action) -> State:
        """
        Apply action to get successor state.
        
        Args:
            state: Current state
            action: Action to apply
            
        Returns:
            Resulting state
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return state.transition(action)
    
    def is_goal(self, state: State) -> bool:
        """
        Check if state satisfies goal.
        
        Args:
            state: State to test
            
        Returns:
            True if goal state, False otherwise
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        # Use target exercises and duration for goal state check
        target_exercises = 6  # Default target
        target_duration = self._goal_state.session_duration_minutes
        return state.is_goal_state(target_exercises, target_duration)
    
    def get_action_cost(self, state: State, action: Action, next_state: State) -> float:
        """
        Calculate cost of applying action.
        
        Args:
            state: Current state
            action: Action being applied
            next_state: Resulting state
            
        Returns:
            Action cost
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return action.calculate_cost()
    
    def get_heuristic(self, state: State) -> float:
        """
        Estimate cost from state to goal.
        
        Heuristic: exercises remaining + duration gap
        
        Args:
            state: State to evaluate
            
        Returns:
            Estimated cost to goal
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        # Calculate remaining exercises and duration gap
        target_exercises = 6
        target_duration = self._goal_state.session_duration_minutes
        
        exercises_remaining = max(0, target_exercises - state.exercises_completed)
        duration_remaining = max(0, target_duration - state.total_workout_duration)
        
        # Heuristic: exercises remaining * 10 + duration remaining
        return exercises_remaining * 10.0 + duration_remaining


class GoalBasedAgent(Agent):
    """
    Goal-Based Agent implementation for Fitness Goal Planning.
    
    This agent formulates explicit fitness goals and defines the target state
    that the workout plan should achieve. Unlike search-based planning, this
    simplified version focuses on goal definition and direction setting.
    
    Architecture:
    Current State → Goal Definition → Target State → Workout Direction
    
    Algorithm:
    1. Receive current user state (fitness level, weight, etc.)
    2. Based on user's desired fitness goal:
       - Define target fitness level
       - Define target weight (if applicable)
       - Define primary exercise focus area
    3. Set workout plan direction toward goal
    4. Provide goal criteria for utility evaluation
    
    Goal Types and Planning:
    - WEIGHT_LOSS:
        * Target: Reduce weight
        * Focus: Cardio and endurance exercises
        * Direction: High calorie burn exercises
    
    - MUSCLE_GAIN:
        * Target: Increase muscle mass
        * Focus: Strength training exercises
        * Direction: Progressive resistance training
    
    - ENDURANCE:
        * Target: Increase stamina
        * Focus: Cardiovascular and endurance exercises
        * Direction: Long-duration, moderate intensity
    
    - GENERAL_FITNESS:
        * Target: Balanced improvement
        * Focus: Mix of all exercise types
        * Direction: Well-rounded workout plan
    
    Advantages:
    - Clear goal definition
    - Easy to explain and justify
    - Provides direction for optimization
    - Simple to implement and understand
    
    Use Case in Workout System:
    - STEP 2 in workflow: Define fitness goal after safety filtering
    - Provides goal criteria for next steps (utility evaluation and A* search)
    
    Time Complexity: O(1) for goal definition
    Space Complexity: O(1) for goal storage
    """
    
    def __init__(
        self,
        initial_state: State,
        name: str = "Goal-Based Agent (Fitness Planner)"
    ):
        """
        Initialize goal-based agent for fitness planning.
        
        Args:
            initial_state: User's current fitness state
            name: Agent name
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        super().__init__(AgentType.GOAL_BASED, name)
        self._current_state = initial_state
        self._goal_state: Optional[State] = None
        self._goal: Optional[Goal] = None
        self._workout_direction: Dict[str, Any] = {}
    
    def define_fitness_goal(self, fitness_goal: FitnessGoal) -> Goal:
        """
        Define the fitness goal and create target state.
        
        This is the core function that sets the goal based on user's desired outcome.
        
        Args:
            fitness_goal: User's desired fitness goal (enum)
            
        Returns:
            Goal object with target state and description
            
        Algorithm:
        Based on fitness_goal type:
            If WEIGHT_LOSS:
                Set target weight = current weight - reasonable loss
                Set focus = cardio/endurance
            Else If MUSCLE_GAIN:
                Set target muscle_mass increase
                Set focus = strength training
            Else If ENDURANCE:
                Set target stamina increase
                Set focus = cardio/endurance
            Else If GENERAL_FITNESS:
                Set balanced targets
                Set focus = mixed exercises
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        current_state = self._current_state
        
        # Map experience level to a numeric fitness level for goal setting
        experience_to_level = {
            ExperienceLevel.BEGINNER: 2.0,
            ExperienceLevel.INTERMEDIATE: 5.0,
            ExperienceLevel.ADVANCED: 7.5,
            ExperienceLevel.EXPERT: 9.0
        }
        current_fitness_numeric = experience_to_level.get(current_state.experience_level, 5.0)
        
        # Define target state based on goal type
        if fitness_goal == FitnessGoal.WEIGHT_LOSS:
            # Goal: Lose weight (reasonable target: 5-10% of current weight)
            target_weight = max(
                current_state.weight_kg * 0.90,  # 10% loss
                current_state.weight_kg - 10  # or 10kg max
            )
            target_exercises = 8  # More exercises for calorie burn
            target_duration = current_state.session_duration_minutes + 15
            description = f"Lose weight from {current_state.weight_kg:.1f}kg to {target_weight:.1f}kg through cardio focus"
            
            self._workout_direction = {
                "primary_focus": ["cardio", "endurance"],
                "exercise_categories": ["CARDIO", "ENDURANCE"],
                "intensity_preference": "moderate_to_high",
                "calorie_burn_priority": "high",
                "target_exercises": target_exercises,
                "target_duration": target_duration
            }
            
        elif fitness_goal == FitnessGoal.MUSCLE_GAIN:
            # Goal: Gain muscle mass
            target_weight = current_state.weight_kg + 5  # Gain muscle mass
            target_exercises = 6  # Focused strength exercises
            target_duration = current_state.session_duration_minutes
            description = f"Build muscle mass through strength training"
            
            self._workout_direction = {
                "primary_focus": ["strength", "resistance"],
                "exercise_categories": ["STRENGTH"],
                "intensity_preference": "high",
                "progressive_overload": True,
                "target_exercises": target_exercises,
                "target_duration": target_duration
            }
            
        elif fitness_goal == FitnessGoal.ENDURANCE:
            # Goal: Increase endurance and stamina
            target_weight = current_state.weight_kg  # Maintain weight
            target_exercises = 5  # Fewer but longer exercises
            target_duration = current_state.session_duration_minutes + 20
            description = f"Increase endurance and stamina through sustained cardio training"
            
            self._workout_direction = {
                "primary_focus": ["cardio", "endurance"],
                "exercise_categories": ["CARDIO", "ENDURANCE"],
                "intensity_preference": "moderate",
                "duration_priority": "high",
                "target_exercises": target_exercises,
                "target_duration": target_duration
            }
            
        else:  # GENERAL_FITNESS or other
            # Goal: Overall fitness improvement
            target_weight = current_state.weight_kg  # Maintain healthy weight
            target_exercises = 6
            target_duration = current_state.session_duration_minutes
            description = f"Improve general fitness through balanced workout program"
            
            self._workout_direction = {
                "primary_focus": ["balanced", "all_around"],
                "exercise_categories": ["STRENGTH", "CARDIO", "FLEXIBILITY"],
                "intensity_preference": "moderate",
                "variety": "high",
                "target_exercises": target_exercises,
                "target_duration": target_duration
            }
        
        # Create target state using actual State class attributes
        self._goal_state = State(
            user_id=current_state.user_id,
            age=current_state.age,
            weight_kg=target_weight,
            height_cm=current_state.height_cm,
            fitness_goal=fitness_goal,
            experience_level=current_state.experience_level,
            worked_muscle_groups=frozenset(),  # Fresh start
            available_equipment=current_state.available_equipment,
            total_calories_burned=0.0,
            total_workout_duration=0,
            exercises_completed=0,
            current_fatigue_level=0.0,
            days_per_week=current_state.days_per_week,
            session_duration_minutes=target_duration,
            medical_conditions=current_state.medical_conditions
        )
        
        # Create goal object
        self._goal = Goal(
            goal_id=f"fitness_goal_{fitness_goal.value}",
            description=description,
            target_state=self._goal_state,
            priority=100
        )
        
        return self._goal
    
    def get_target_state(self) -> State:
        """
        Get the defined target state for the fitness goal.
        
        Returns:
            Target state that workout plan should aim for
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return self._goal_state
    
    def get_workout_direction(self) -> Dict[str, Any]:
        """
        Get the workout direction parameters for the goal.
        
        This tells other agents (utility-based, search) what to prioritize.
        
        Returns:
            Dictionary with workout direction parameters:
            - primary_focus: List of focus areas
            - exercise_categories: Preferred exercise categories
            - intensity_preference: Desired intensity level
            - Other goal-specific parameters
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return self._workout_direction
    
    def evaluate_progress(self, current_state: State) -> float:
        """
        Evaluate progress toward the defined goal.
        
        Args:
            current_state: Current user state
            
        Returns:
            Progress score (0.0 = no progress, 1.0 = goal achieved)
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if not self._goal:
            return 0.0
        
        return self._goal.evaluate_progress(current_state)
    
    def is_goal_achieved(self, current_state: State) -> bool:
        """
        Check if the fitness goal has been achieved.
        
        Args:
            current_state: Current user state
            
        Returns:
            True if goal achieved, False otherwise
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if not self._goal:
            return False
        
        return self._goal.is_satisfied(current_state)
    
    def perceive(self, percept: Percept) -> None:
        """
        Process percept and update internal state.
        
        Goal-based agents update their current state based on percepts
        and track progress toward goals.
        
        Args:
            percept: Current percept from environment
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        # Update current state based on percept
        self._current_state = percept.state
        
        # Store percept in history
        self._percept_history.append(percept)
        
        # Evaluate progress toward goal if goal exists
        if self._goal:
            self._goal.evaluate_progress(self._current_state)
    
    def decide_action(self, percept: Percept) -> AgentAction:
        """
        Simplified decide_action for compatibility (not used in streamlined workflow).
        
        The streamlined workflow uses define_fitness_goal() directly.
        """
        return AgentAction(
            action=None,
            confidence=1.0,
            reasoning="Goal-Based Agent defines goals, does not select actions directly",
            metadata={"agent_type": "goal_based"}
        )


# Example usage
if __name__ == "__main__":
    print("Goal-Based Agent - Fitness Goal Planner")
    print("=" * 50)
    print("Purpose: Define fitness goals and target states")
    print("Method: Goal formulation based on fitness objectives")
