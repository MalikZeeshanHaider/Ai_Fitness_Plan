"""
Streamlined Workout Recommendation Use Case.

This simplified use case implements the mandatory AI workflow:
1. Simple Reflex Agent → Safety filtering
2. Goal-Based Agent → Fitness goal definition
3. Utility-Based Agent → Exercise scoring
4. A* Search Algorithm → Optimal workout plan generation

This architecture is designed for clear explanation in academic viva presentations.

Architecture Flow:
User Input → Simple Reflex Agent → Goal-Based Agent → Utility-Based Agent → A* Search → Workout Plan

Time Complexity: O(n) + O(1) + O(n) + O(b^d) = O(b^d) dominated by A* search
Space Complexity: O(b^d) for search tree
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

from ..domain.models.state import State, ExperienceLevel, FitnessGoal
from ..domain.models.action import Action, Difficulty, ActionType
from ..domain.models.exercise import Exercise, ExerciseCategory, IntensityLevel
from ..domain.models.workout_plan import WorkoutPlan, ExerciseInPlan
from ..domain.search.search_problem import SearchProblem
from ..domain.search.astar import AStarSearch
from ..domain.agents.simple_reflex_agent import SimpleReflexAgent
from ..domain.agents.goal_based_agent import GoalBasedAgent
from ..domain.agents.utility_based_agent import UtilityBasedAgent
from ..domain.reasoning.heuristic_function import WorkoutHeuristic
from ..infrastructure.data.data_loader import DataLoader


@dataclass
class StreamlinedRequest:
    """
    Simplified request for workout recommendation.
    
    Attributes:
        current_state: User's current fitness state
        available_time: Available time in minutes
        available_equipment: List of available equipment
        user_preferences: User preferences for exercises
    """
    current_state: State
    available_time: int  # minutes
    available_equipment: List[str] = field(default_factory=list)
    user_preferences: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate request."""
        if self.available_time <= 0:
            raise ValueError("Available time must be positive")


@dataclass
class StreamlinedResponse:
    """
    Response containing workout recommendation and AI explanations.
    
    Attributes:
        workout_plan: Generated workout plan
        exercises: List of recommended exercises
        ai_workflow_explanation: Step-by-step explanation of AI decisions
        safety_filters_applied: Safety rules applied by reflex agent
        goal_definition: Goal defined by goal-based agent
        utility_scores: Utility scores from utility-based agent
        search_statistics: A* search statistics
        execution_time_ms: Total execution time
    """
    workout_plan: WorkoutPlan
    exercises: List[Exercise]
    ai_workflow_explanation: str
    safety_filters_applied: List[str]
    goal_definition: Dict[str, Any]
    utility_scores: Dict[str, float]
    search_statistics: Dict[str, Any]
    execution_time_ms: float


class StreamlinedWorkoutUseCase:
    """
    Streamlined Workout Recommendation Use Case.
    
    Implements the mandatory 4-step AI workflow:
    
    STEP 1: Simple Reflex Agent (Safety Filter)
    - Input: All exercises + user constraints
    - Process: Apply if-then safety rules
    - Output: Safe exercises list
    
    STEP 2: Goal-Based Agent (Goal Definition)
    - Input: User fitness goal + current state
    - Process: Define target state and workout direction
    - Output: Goal parameters and direction
    
    STEP 3: Utility-Based Agent (Exercise Scoring)
    - Input: Safe exercises + goal direction
    - Process: Score each exercise using utility function
    - Output: Scored exercises (best to worst)
    
    STEP 4: A* Search Algorithm (Optimal Plan)
    - Input: Scored exercises + constraints
    - Process: Search for optimal exercise sequence
    - Output: Optimal workout plan
    
    This architecture is:
    - Simple to explain in viva
    - Clearly mapped to AI course concepts
    - Uses only specified agents and algorithms
    - Follows clean architecture principles
    
    Time Complexity: O(b^d) dominated by A* search
    Space Complexity: O(b^d) for search tree
    """
    
    def __init__(self, data_loader: DataLoader):
        """
        Initialize streamlined use case.
        
        Args:
            data_loader: Data loader for exercises dataset
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._data_loader = data_loader
        
        # Initialize the three required agents
        self._reflex_agent = SimpleReflexAgent("Safety Filter Agent")
        self._goal_agent = None  # Created per request (needs user state)
        self._utility_agent = UtilityBasedAgent("Exercise Optimizer Agent")
        
        # Statistics
        self._workflow_logs: List[str] = []
    
    def execute(self, request: StreamlinedRequest) -> StreamlinedResponse:
        """
        Execute the streamlined workout recommendation workflow.
        
        Mandatory Workflow:
        Step 1: Simple Reflex Agent filters unsafe exercises
        Step 2: Goal-Based Agent defines fitness goal
        Step 3: Utility-Based Agent scores exercises
        Step 4: A* Search generates optimal plan
        
        Args:
            request: Workout recommendation request
            
        Returns:
            Response with workout plan and AI explanations
            
        Time Complexity: O(n) + O(1) + O(n log n) + O(b^d) = O(b^d)
        Space Complexity: O(b^d)
        """
        start_time = datetime.now()
        self._workflow_logs = []
        
        # ===================================================================
        # STEP 1: SIMPLE REFLEX AGENT - Safety Filtering
        # ===================================================================
        self._workflow_logs.append("=" * 70)
        self._workflow_logs.append("STEP 1: SIMPLE REFLEX AGENT (Safety Filter)")
        self._workflow_logs.append("=" * 70)
        self._workflow_logs.append("Purpose: Apply if-then rules to filter unsafe exercises")
        self._workflow_logs.append("")
        
        # Load all exercises
        all_exercises = self._data_loader.get_exercises()
        self._workflow_logs.append(f"Input: {len(all_exercises)} total exercises from dataset")
        
        # Apply safety filtering using reflex rules
        safe_exercises = self._reflex_agent.filter_exercises_by_safety(
            exercises=all_exercises,
            user_state=request.current_state,
            available_equipment=request.available_equipment,
            energy_level=0.8  # Assume good energy
        )
        
        safety_filters = []
        if len(safe_exercises) < len(all_exercises):
            filtered_count = len(all_exercises) - len(safe_exercises)
            safety_filters.append(f"Filtered {filtered_count} unsafe exercises")
            
            if request.current_state.has_injury:
                safety_filters.append(f"IF injury detected THEN remove exercises affecting: {', '.join(request.current_state.medical_conditions)}")
            
            if request.current_state.experience_level == ExperienceLevel.BEGINNER:
                safety_filters.append("IF beginner THEN remove advanced exercises")
            
            if request.available_equipment:
                safety_filters.append(f"IF equipment limited THEN filter unavailable equipment exercises")
        
        self._workflow_logs.append(f"Rules Applied:")
        for filter_rule in safety_filters:
            self._workflow_logs.append(f"  - {filter_rule}")
        self._workflow_logs.append(f"Output: {len(safe_exercises)} safe exercises")
        self._workflow_logs.append("")
        
        # ===================================================================
        # STEP 2: GOAL-BASED AGENT - Fitness Goal Definition
        # ===================================================================
        self._workflow_logs.append("=" * 70)
        self._workflow_logs.append("STEP 2: GOAL-BASED AGENT (Goal Definition)")
        self._workflow_logs.append("=" * 70)
        self._workflow_logs.append("Purpose: Define target fitness state and workout direction")
        self._workflow_logs.append("")
        
        # Create goal-based agent for this user
        self._goal_agent = GoalBasedAgent(
            initial_state=request.current_state,
            name="Fitness Goal Planner"
        )
        
        # Define the fitness goal
        fitness_goal = request.current_state.fitness_goal
        goal = self._goal_agent.define_fitness_goal(fitness_goal)
        goal_direction = self._goal_agent.get_workout_direction()
        
        self._workflow_logs.append(f"Input: User fitness goal = {fitness_goal.value}")
        self._workflow_logs.append(f"Goal Definition: {goal.description}")
        self._workflow_logs.append(f"Target State:")
        self._workflow_logs.append(f"  - Target Weight: {goal.target_state.weight_kg:.1f} kg")
        self._workflow_logs.append(f"  - Target Duration: {goal.target_state.session_duration_minutes} min")
        self._workflow_logs.append(f"Workout Direction:")
        for key, value in goal_direction.items():
            self._workflow_logs.append(f"  - {key}: {value}")
        self._workflow_logs.append(f"Output: Goal parameters set for utility evaluation")
        self._workflow_logs.append("")
        
        goal_definition = {
            "goal_type": fitness_goal.value,
            "description": goal.description,
            "target_weight": goal.target_state.weight_kg,
            "target_duration": goal.target_state.session_duration_minutes,
            "direction": goal_direction
        }
        
        # ===================================================================
        # STEP 3: UTILITY-BASED AGENT - Exercise Scoring
        # ===================================================================
        self._workflow_logs.append("=" * 70)
        self._workflow_logs.append("STEP 3: UTILITY-BASED AGENT (Exercise Optimization)")
        self._workflow_logs.append("=" * 70)
        self._workflow_logs.append("Purpose: Score exercises using utility function")
        self._workflow_logs.append("")
        
        # Score exercises using utility function
        scored_exercises = self._utility_agent.score_exercises(
            exercises=safe_exercises,
            user_state=request.current_state,
            goal_direction=goal_direction,
            user_preferences=request.user_preferences
        )
        
        self._workflow_logs.append(f"Input: {len(safe_exercises)} safe exercises")
        self._workflow_logs.append(f"Utility Function:")
        self._workflow_logs.append(f"  U(exercise) = w1*Effectiveness + w2*Safety + w3*TimeEfficiency + w4*Preference")
        self._workflow_logs.append(f"  Weights: effectiveness=0.4, safety=0.3, time_eff=0.2, preference=0.1")
        self._workflow_logs.append(f"")
        self._workflow_logs.append(f"Top 5 Exercises by Utility Score:")
        for i, (exercise, score) in enumerate(scored_exercises[:5], 1):
            self._workflow_logs.append(f"  {i}. {exercise.name} → Utility = {score:.3f}")
        self._workflow_logs.append(f"Output: {len(scored_exercises)} scored exercises (sorted by utility)")
        self._workflow_logs.append("")
        
        utility_scores = self._utility_agent.get_utility_scores()
        
        # ===================================================================
        # STEP 4: A* SEARCH ALGORITHM - Optimal Workout Plan
        # ===================================================================
        self._workflow_logs.append("=" * 70)
        self._workflow_logs.append("STEP 4: A* SEARCH ALGORITHM (Optimal Plan Generation)")
        self._workflow_logs.append("=" * 70)
        self._workflow_logs.append("Purpose: Find optimal sequence of exercises")
        self._workflow_logs.append("")
        
        # Create search problem
        workout_plan, exercises, search_stats = self._generate_plan_with_astar(
            request=request,
            scored_exercises=scored_exercises,
            goal_state=goal.target_state
        )
        
        self._workflow_logs.append(f"Input: Scored exercises + time constraint ({request.available_time} min)")
        self._workflow_logs.append(f"Search Algorithm: A* (A-Star)")
        self._workflow_logs.append(f"  - Evaluation Function: f(n) = g(n) + h(n)")
        self._workflow_logs.append(f"  - g(n) = Path cost (time + fatigue)")
        self._workflow_logs.append(f"  - h(n) = Heuristic (distance to goal state)")
        self._workflow_logs.append(f"")
        self._workflow_logs.append(f"Search Statistics:")
        self._workflow_logs.append(f"  - Nodes Explored: {search_stats.get('nodes_explored', 0)}")
        self._workflow_logs.append(f"  - Execution Time: {search_stats.get('execution_time_ms', 0):.2f} ms")
        self._workflow_logs.append(f"  - Path Cost: {search_stats.get('path_cost', 0):.2f}")
        self._workflow_logs.append(f"")
        self._workflow_logs.append(f"Output: Optimal workout plan with {len(exercises)} exercises")
        for i, ex in enumerate(exercises, 1):
            self._workflow_logs.append(f"  {i}. {ex.name} ({ex.duration_minutes} min)")
        self._workflow_logs.append("")
        
        # ===================================================================
        # Generate Complete AI Workflow Explanation
        # ===================================================================
        ai_explanation = "\n".join(self._workflow_logs)
        
        # Calculate total execution time
        execution_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # Create response
        response = StreamlinedResponse(
            workout_plan=workout_plan,
            exercises=exercises,
            ai_workflow_explanation=ai_explanation,
            safety_filters_applied=safety_filters,
            goal_definition=goal_definition,
            utility_scores=utility_scores,
            search_statistics=search_stats,
            execution_time_ms=execution_time
        )
        
        return response
    
    def _generate_plan_with_astar(
        self,
        request: StreamlinedRequest,
        scored_exercises: List[Tuple[Exercise, float]],
        goal_state: State
    ) -> Tuple[WorkoutPlan, List[Exercise], Dict[str, Any]]:
        """
        Generate workout plan using A* search algorithm.
        
        Args:
            request: User request
            scored_exercises: Exercises scored by utility agent
            goal_state: Target state from goal agent
            
        Returns:
            Tuple of (workout_plan, exercises, search_statistics)
            
        Time Complexity: O(b^d) for A* search
        Space Complexity: O(b^d)
        """
        # Convert top scored exercises to actions
        top_exercises = [ex for ex, score in scored_exercises[:15]]  # Top 15 for search
        actions = self._exercises_to_actions(top_exercises)
        
        # Create search problem
        search_problem = WorkoutSearchProblem(
            initial_state=request.current_state,
            goal_state=goal_state,
            available_actions=actions,
            max_time=request.available_time,
            max_exercises=6
        )
        
        # Create A* search
        astar = AStarSearch(use_graph_search=True, weight=1.0)
        
        # Execute search
        solution = astar.search(
            problem=search_problem,
            max_iterations=1000,
            max_cost=request.available_time * 2
        )
        
        # Extract results
        if solution.success and solution.path:
            selected_actions = solution.path
            selected_exercises = self._actions_to_exercises(selected_actions, top_exercises)
        else:
            # Fallback: select top exercises by utility up to time limit
            selected_exercises = self._select_exercises_greedy(top_exercises, request.available_time)
        
        # Create workout plan
        workout_plan = self._create_workout_plan(
            exercises=selected_exercises,
            user_state=request.current_state
        )
        
        # Search statistics
        search_stats = {
            "nodes_explored": solution.nodes_explored,
            "execution_time_ms": solution.execution_time_ms,
            "path_cost": solution.path_cost,
            "success": solution.success,
            "algorithm": "A* Search"
        }
        
        return workout_plan, selected_exercises, search_stats
    
    def _exercises_to_actions(self, exercises: List[Exercise]) -> List[Action]:
        """Convert exercises to actions for search."""
        actions = []
        for exercise in exercises:
            # Map exercise to action
            diff_map = {
                IntensityLevel.LOW: Difficulty.BEGINNER,
                IntensityLevel.MODERATE: Difficulty.INTERMEDIATE,
                IntensityLevel.HIGH: Difficulty.ADVANCED,
                IntensityLevel.VERY_HIGH: Difficulty.EXPERT
            }
            action_difficulty = diff_map.get(exercise.intensity, Difficulty.INTERMEDIATE)
            
            action = Action(
                action_id=f"do_{exercise.exercise_id}",
                action_type=ActionType.ADD_EXERCISE,
                exercise_name=exercise.name,
                exercise_category=exercise.category.value if exercise.category else "general",
                muscle_groups=frozenset(exercise.primary_muscles) if exercise.primary_muscles else frozenset(),
                secondary_muscles=frozenset(exercise.secondary_muscles) if exercise.secondary_muscles else frozenset(),
                difficulty=action_difficulty,
                equipment_required=frozenset(exercise.equipment) if exercise.equipment else frozenset(),
                estimated_calories=exercise.calories_per_minute * exercise.duration_minutes,
                estimated_duration=exercise.duration_minutes
            )
            actions.append(action)
        
        return actions
    
    def _actions_to_exercises(self, actions: List[Action], exercises: List[Exercise]) -> List[Exercise]:
        """Convert actions back to exercises."""
        selected = []
        for action in actions:
            # Find matching exercise
            for ex in exercises:
                if ex.name == action.exercise_name:
                    selected.append(ex)
                    break
        return selected
    
    def _select_exercises_greedy(self, exercises: List[Exercise], max_time: int) -> List[Exercise]:
        """Greedy selection as fallback if search fails."""
        selected = []
        total_time = 0
        
        for exercise in exercises:
            if total_time + exercise.duration_minutes <= max_time:
                selected.append(exercise)
                total_time += exercise.duration_minutes
                
                if len(selected) >= 6:  # Max 6 exercises
                    break
        
        return selected
    
    def _create_workout_plan(self, exercises: List[Exercise], user_state: State) -> WorkoutPlan:
        """Create workout plan from selected exercises."""
        exercises_in_plan = []
        
        for i, exercise in enumerate(exercises, 1):
            # Determine sets and reps based on exercise category
            if exercise.category == ExerciseCategory.STRENGTH:
                sets = 3
                reps = "10-12"
                rest_seconds = 60
            else:
                sets = 1
                reps = f"{exercise.typical_duration_minutes} minutes"
                rest_seconds = 30
            
            ex_in_plan = ExerciseInPlan(
                exercise=exercise,
                order=i,
                sets=sets,
                reps=reps,
                rest_seconds=rest_seconds,
                notes=f"Focus on proper form. {exercise.instructions[:100] if exercise.instructions else ''}"
            )
            exercises_in_plan.append(ex_in_plan)
        
        # Calculate totals
        total_duration = sum(ex.duration_minutes for ex in exercises)
        total_calories = sum(ex.calories_per_minute * ex.duration_minutes for ex in exercises)
        
        workout_plan = WorkoutPlan(
            plan_id=f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            user_id=user_state.user_id,
            fitness_goal=user_state.fitness_goal,
            experience_level=user_state.experience_level.value,
            initial_state=user_state,
            exercises=exercises_in_plan,
            total_duration_minutes=total_duration,
            total_calories=total_calories,
            difficulty_level=user_state.experience_level.value,
            search_algorithm_used="A* Search",
            notes="Generated using AI: Simple Reflex Agent → Goal-Based Agent → Utility-Based Agent → A* Search"
        )
        
        return workout_plan


class WorkoutSearchProblem(SearchProblem):
    """
    Search problem for A* algorithm to find optimal workout sequence.
    
    State: User fitness state (current_fitness, fatigue, time_used, exercises_done)
    Actions: Available exercises to add
    Goal: Achieve target fitness state within time constraint
    Cost: Time + fatigue + muscle imbalance penalty
    Heuristic: Distance to goal fitness level
    """
    
    def __init__(
        self,
        initial_state: State,
        goal_state: State,
        available_actions: List[Action],
        max_time: int,
        max_exercises: int = 6
    ):
        """Initialize workout search problem for A* algorithm."""
        super().__init__(initial_state, goal_state)
        self._available_actions = available_actions
        self._max_time = max_time
        self._max_exercises = max_exercises
    
    def get_available_actions(self, state: State) -> List[Action]:
        """Get applicable actions (exercises not yet selected)."""
        # Track selected exercises to avoid duplicates
        selected = getattr(state, 'selected_exercises', set())
        
        # Filter out already selected exercises
        available = [
            action for action in self._available_actions
            if action.exercise_name not in selected
        ]
        
        # Check time constraint
        available = [
            action for action in available
            if state.total_workout_duration + action.estimated_duration <= self._max_time
        ]
        
        # Check exercise count limit
        if len(selected) >= self._max_exercises:
            return []
        
        return available
    
    def get_successor(self, state: State, action: Action) -> State:
        """Apply action to get successor state."""
        # Transition state
        new_state = state.transition(
            exercise_name=action.exercise_name,
            muscle_groups=set(action.muscle_groups),
            calories=action.estimated_calories,
            duration=action.estimated_duration,
            fatigue_increase=0.1
        )
        
        # Track selected exercises
        selected = set(getattr(state, 'selected_exercises', set()))
        selected.add(action.exercise_name)
        object.__setattr__(new_state, 'selected_exercises', selected)
        
        return new_state
    
    def is_goal(self, state: State) -> bool:
        """Check if goal reached (good workout or time limit reached)."""
        selected_count = len(getattr(state, 'selected_exercises', set()))
        
        # Goal if we have 3-6 exercises and reasonable time used
        if 3 <= selected_count <= self._max_exercises:
            if state.total_workout_duration >= self._max_time * 0.6:  # Used at least 60% of time
                return True
        
        # Also goal if we've used most of the time
        if state.total_workout_duration >= self._max_time * 0.9:
            return selected_count >= 3
        
        return False
    
    def get_action_cost(self, state: State, action: Action, next_state: State) -> float:
        """Calculate cost of action (prefer efficient exercises)."""
        # Cost = time + fatigue penalty
        time_cost = action.estimated_duration
        fatigue_cost = next_state.current_fatigue_level * 10  # Penalize high fatigue
        
        return time_cost + fatigue_cost
    
    def get_heuristic(self, state: State) -> float:
        """
        Heuristic function for A* search.
        
        h(n) = estimated cost to reach goal from current state
        
        Admissible: Never overestimates actual cost
        """
        selected_count = len(getattr(state, 'selected_exercises', set()))
        
        # Need at least 3 exercises
        if selected_count < 3:
            exercises_needed = 3 - selected_count
            # Estimate 15 minutes per exercise
            return exercises_needed * 15
        
        # If we have enough exercises, estimate remaining time to fill
        time_remaining = self._max_time - state.total_workout_duration
        if time_remaining > 0 and selected_count < self._max_exercises:
            # Could add more exercises
            return time_remaining * 0.1  # Small cost to encourage filling time
        
        return 0  # At or near goal
