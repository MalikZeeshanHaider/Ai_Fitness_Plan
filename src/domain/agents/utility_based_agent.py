"""
Utility-Based Agent Implementation.

A utility-based agent selects exercises that maximize expected utility, making
rational decisions by considering multiple objectives and preferences.

Function: exercise_score = utility(exercise, state, goal)
         best_exercises = argmax(utility_score)

Properties:
- Utility function represents preferences and objectives
- Handles conflicting goals gracefully (safety vs effectiveness)
- Rational decision making with trade-offs
- Can balance multiple factors simultaneously
- More sophisticated than goal-based agents alone

Use Case: Exercise optimization balancing multiple objectives.

Purpose in Workflow:
- Step 3: Scores exercises using a utility function after safety filtering and goal definition
- Utility function considers:
  * Effectiveness: How well exercise achieves the fitness goal
  * Safety: Injury risk and difficulty appropriateness
  * Time Efficiency: Calorie burn or muscle gain per minute
  * User Preference: User's exercise preferences
- Formula: U(exercise) = w1*Effectiveness + w2*Safety + w3*TimeEfficiency + w4*Preference
- Higher utility score = better exercise selection

Time Complexity: O(n) where n is number of exercises to score
Space Complexity: O(n) for storing utility scores
"""

from typing import List, Dict, Any, Optional, Callable, Tuple
from dataclasses import dataclass
from datetime import datetime
import math

from .agent import Agent, AgentType, Percept, AgentAction
from ..models.state import State, FitnessGoal, ExperienceLevel
from ..models.action import Action, ActionType, Difficulty


@dataclass
class UtilityFunction:
    """
    Utility function for evaluating action outcomes.
    
    A utility function maps states (or state-action pairs) to real numbers
    representing the desirability of that state/outcome.
    
    Attributes:
        name: Function name
        weight: Weight/importance of this utility component
        evaluator: Function that calculates utility
        description: Human-readable description
    """
    name: str
    weight: float
    evaluator: Callable[[State, Action], float]
    description: str = ""
    
    def evaluate(self, state: State, action: Action) -> float:
        """
        Calculate utility for state-action pair.
        
        Args:
            state: Current state
            action: Action being evaluated
            
        Returns:
            Weighted utility value
            
        Time Complexity: O(1) to O(k) depending on evaluator
        Space Complexity: O(1)
        """
        raw_utility = self.evaluator(state, action)
        return self.weight * raw_utility


class UtilityBasedAgent(Agent):
    """
    Utility-Based Agent implementation for Exercise Optimization.
    
    This agent makes decisions by maximizing utility. It scores each exercise
    based on multiple factors (objectives) and selects those with highest scores.
    This allows balancing trade-offs between competing objectives.
    
    Architecture:
    Exercises → Utility Evaluation → Exercise Scores → Best Exercises
                      ↓
              (effectiveness, safety, time efficiency, preference)
    
    Algorithm:
    1. Receive list of safe exercises (from Simple Reflex Agent)
    2. Receive goal direction (from Goal-Based Agent)
    3. For each exercise:
       a. Calculate effectiveness score (how well it achieves goal)
       b. Calculate safety score (injury risk, difficulty match)
       c. Calculate time efficiency score (results per minute)
       d. Calculate preference score (user likes/dislikes)
       e. Combine: U = w1*eff + w2*safety + w3*time_eff + w4*pref
    4. Sort exercises by utility score
    5. Return top exercises for workout plan
    
    Utility Function:
    U(exercise) = w1 * Effectiveness(exercise, goal)
                + w2 * Safety(exercise, user_state)
                + w3 * TimeEfficiency(exercise)
                + w4 * UserPreference(exercise, preferences)
    
    Where weights (w1, w2, w3, w4) sum to 1.0 and represent importance.
    
    Advantages:
    - Handles trade-offs naturally (e.g., safety vs effectiveness)
    - Rational and explainable decisions
    - Can balance multiple objectives simultaneously
    - Flexible through weight adjustment
    - Works well with different user priorities
    
    Limitations:
    - Requires careful utility function design
    - Weight selection can be subjective
    - Assumes utilities are comparable
    
    Use Cases in Workout System:
    - STEP 3 in workflow: Score exercises after safety filtering and goal definition
    - Trade-off: high-effectiveness but risky vs safe but less effective
    - Trade-off: time-intensive with great results vs quick with moderate results
    
    Time Complexity: O(n) per scoring where n is number of exercises
    Space Complexity: O(n) for utility scores
    """
    
    def __init__(
        self,
        name: str = "Utility-Based Agent (Exercise Optimizer)",
        weights: Dict[str, float] = None
    ):
        """
        Initialize utility-based agent for exercise optimization.
        
        Args:
            name: Agent name
            weights: Custom weights for utility function components
                    Default: {"effectiveness": 0.4, "safety": 0.3, 
                             "time_efficiency": 0.2, "preference": 0.1}
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        super().__init__(AgentType.UTILITY_BASED, name)
        
        # Default utility function weights (must sum to 1.0)
        self._weights = weights or {
            "effectiveness": 0.4,    # How well exercise achieves goal
            "safety": 0.3,           # Injury risk and difficulty match
            "time_efficiency": 0.2,  # Results per minute
            "preference": 0.1        # User preferences
        }
        
        # Normalize weights to sum to 1.0
        total = sum(self._weights.values())
        self._weights = {k: v/total for k, v in self._weights.items()}
        
        self._utility_scores: Dict[str, float] = {}
    
    def score_exercises(
        self,
        exercises: List[Any],
        user_state: State,
        goal_direction: Dict[str, Any],
        user_preferences: Dict[str, Any] = None
    ) -> List[Tuple[Any, float]]:
        """
        Score exercises using utility function (main function for this agent).
        
        This calculates the utility score for each exercise, balancing
        multiple objectives through weighted combination.
        
        Args:
            exercises: List of Exercise objects to score
            user_state: Current user state
            goal_direction: Direction from Goal-Based Agent
            user_preferences: User preferences (liked/disliked exercises, etc.)
            
        Returns:
            List of (exercise, utility_score) tuples sorted by score (highest first)
            
        Algorithm:
        For each exercise:
            effectiveness_score = calculate_effectiveness(exercise, goal_direction)
            safety_score = calculate_safety(exercise, user_state)
            time_efficiency_score = calculate_time_efficiency(exercise)
            preference_score = calculate_preference(exercise, user_preferences)
            
            utility = w1*effectiveness + w2*safety + w3*time_eff + w4*preference
            
        Sort by utility (descending)
        Return scored exercises
        
        Time Complexity: O(n log n) where n is number of exercises (for sorting)
        Space Complexity: O(n) for scores
        """
        user_preferences = user_preferences or {}
        scored_exercises = []
        
        for exercise in exercises:
            # Calculate each utility component
            eff_score = self._calculate_effectiveness(exercise, goal_direction)
            safety_score = self._calculate_safety(exercise, user_state)
            time_eff_score = self._calculate_time_efficiency(exercise)
            pref_score = self._calculate_preference(exercise, user_preferences)
            
            # Calculate total utility (weighted sum)
            utility = (
                self._weights["effectiveness"] * eff_score +
                self._weights["safety"] * safety_score +
                self._weights["time_efficiency"] * time_eff_score +
                self._weights["preference"] * pref_score
            )
            
            # Store utility score
            exercise_id = getattr(exercise, 'exercise_id', getattr(exercise, 'name', str(id(exercise))))
            self._utility_scores[exercise_id] = utility
            
            scored_exercises.append((exercise, utility))
        
        # Sort by utility score (highest first)
        scored_exercises.sort(key=lambda x: x[1], reverse=True)
        
        return scored_exercises
    
    def _calculate_effectiveness(self, exercise: Any, goal_direction: Dict[str, Any]) -> float:
        """
        Calculate effectiveness score: how well exercise achieves the fitness goal.
        
        Args:
            exercise: Exercise object
            goal_direction: Goal direction parameters
            
        Returns:
            Effectiveness score (0.0 to 1.0)
            
        Higher score means exercise better aligns with fitness goal.
        """
        score = 0.5  # Base score
        
        # Get exercise category
        ex_category = getattr(exercise, 'category', None)
        if ex_category:
            category_str = getattr(ex_category, 'value', str(ex_category)).upper()
            
            # Check if exercise category matches goal focus
            preferred_categories = goal_direction.get("exercise_categories", [])
            if category_str in preferred_categories:
                score += 0.3  # Good match with goal
        
        # Check intensity alignment
        ex_intensity = getattr(exercise, 'intensity', None)
        if ex_intensity:
            intensity_value = getattr(ex_intensity, 'value', str(ex_intensity)).lower()
            preferred_intensity = goal_direction.get("intensity_preference", "moderate").lower()
            
            if preferred_intensity == "high" and intensity_value in ["high", "very_high"]:
                score += 0.2
            elif preferred_intensity == "moderate" and intensity_value in ["moderate", "medium"]:
                score += 0.2
            elif preferred_intensity == "moderate_to_high" and intensity_value in ["moderate", "medium", "high"]:
                score += 0.2
        
        # Calorie burn priority (for weight loss)
        if goal_direction.get("calorie_burn_priority") == "high":
            calories = getattr(exercise, 'calories_per_minute', 0) * getattr(exercise, 'duration_minutes', 1)
            if calories > 100:  # High calorie burn
                score += 0.2
        
        return min(1.0, score)  # Cap at 1.0
    
    def _calculate_safety(self, exercise: Any, user_state: State) -> float:
        """
        Calculate safety score: lower injury risk and appropriate difficulty.
        
        Args:
            exercise: Exercise object
            user_state: User state
            
        Returns:
            Safety score (0.0 to 1.0)
            
        Higher score means exercise is safer for the user.
        """
        score = 1.0  # Start with maximum safety
        
        # Penalize if difficulty doesn't match experience
        ex_difficulty = getattr(exercise, 'difficulty', '').lower()
        
        if user_state.experience_level == ExperienceLevel.BEGINNER:
            if ex_difficulty in ['advanced', 'expert', 'hard']:
                score -= 0.4  # Risky for beginner
            elif ex_difficulty in ['beginner', 'easy', 'low']:
                score += 0.0  # Perfect match (already at 1.0)
        elif user_state.experience_level == ExperienceLevel.INTERMEDIATE:
            if ex_difficulty in ['expert', 'very_hard']:
                score -= 0.2  # Slightly risky
            elif ex_difficulty in ['intermediate', 'moderate']:
                score += 0.0  # Good match
        
        # Penalize high intensity if user has injuries (though should be filtered already)
        if user_state.has_injury:
            ex_intensity = getattr(exercise, 'intensity', None)
            if ex_intensity:
                intensity_value = getattr(ex_intensity, 'value', '').lower()
                if intensity_value in ['high', 'very_high']:
                    score -= 0.3  # Extra caution with injuries
        
        return max(0.0, score)  # Floor at 0.0
    
    def _calculate_time_efficiency(self, exercise: Any) -> float:
        """
        Calculate time efficiency score: results per minute of exercise.
        
        Args:
            exercise: Exercise object
            
        Returns:
            Time efficiency score (0.0 to 1.0)
            
        Higher score means better results for time invested.
        """
        duration = getattr(exercise, 'duration_minutes', 30)
        calories_per_min = getattr(exercise, 'calories_per_minute', 5)
        
        # Time efficiency: higher calorie burn per minute is more efficient
        # Normalize to 0-1 scale (assume 15 cal/min is very high)
        efficiency = min(1.0, calories_per_min / 15.0)
        
        # Penalize very long exercises (opportunity cost)
        if duration > 45:
            efficiency *= 0.8
        elif duration > 30:
            efficiency *= 0.9
        
        return efficiency
    
    def _calculate_preference(self, exercise: Any, user_preferences: Dict[str, Any]) -> float:
        """
        Calculate preference score: how much user likes this type of exercise.
        
        Args:
            exercise: Exercise object
            user_preferences: User preferences dictionary
            
        Returns:
            Preference score (0.0 to 1.0)
            
        Higher score means user prefers this exercise.
        """
        score = 0.5  # Neutral by default
        
        # Check liked exercises
        liked_exercises = user_preferences.get("liked_exercises", [])
        disliked_exercises = user_preferences.get("disliked_exercises", [])
        
        exercise_name = getattr(exercise, 'name', '').lower()
        
        if any(liked.lower() in exercise_name for liked in liked_exercises):
            score = 1.0  # User likes this exercise
        elif any(disliked.lower() in exercise_name for disliked in disliked_exercises):
            score = 0.0  # User dislikes this exercise
        
        # Check category preferences
        liked_categories = user_preferences.get("liked_categories", [])
        ex_category = getattr(exercise, 'category', None)
        if ex_category:
            category_str = getattr(ex_category, 'value', str(ex_category)).upper()
            if category_str in [cat.upper() for cat in liked_categories]:
                score = max(score, 0.8)  # User likes this category
        
        return score
    
    def get_utility_scores(self) -> Dict[str, float]:
        """
        Get all calculated utility scores.
        
        Returns:
            Dictionary mapping exercise ID to utility score
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return self._utility_scores.copy()
    
    def set_weights(self, weights: Dict[str, float]) -> None:
        """
        Update utility function weights.
        
        Args:
            weights: New weights dictionary
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        total = sum(weights.values())
        self._weights = {k: v/total for k, v in weights.items()}
    
    def add_utility_function(self, utility_func: UtilityFunction) -> None:
        """
        Add a utility function component.
        
        Args:
            utility_func: Utility function to add
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._utility_functions.append(utility_func)
    
    def perceive(self, percept: Percept) -> None:
        """
        Update state from percept.
        
        Args:
            percept: Current percept
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._current_state = percept.state
    
    def decide_action(self, percept: Percept) -> AgentAction:
        """
        Select action that maximizes expected utility.
        
        Process:
        1. Filter applicable actions
        2. Calculate utility for each action
        3. Select action with maximum utility
        4. Apply exploration (occasionally try suboptimal)
        
        Args:
            percept: Current percept
            
        Returns:
            Action with maximum expected utility
            
        Time Complexity: O(A * U) where A=actions, U=utility functions
        Space Complexity: O(A)
        """
        # Get applicable actions
        applicable_actions = [
            action for action in self._available_actions
            if action.is_applicable(self._current_state)
        ]
        
        if not applicable_actions:
            return self._generate_default_action("No applicable actions")
        
        # Calculate utility for each action
        action_utilities: List[Tuple[Action, float, Dict[str, float]]] = []
        
        for action in applicable_actions:
            total_utility, component_utilities = self._calculate_expected_utility(
                self._current_state,
                action,
                percept
            )
            action_utilities.append((action, total_utility, component_utilities))
            self._action_utilities[action.action_id] = total_utility
        
        # Sort by utility (highest first)
        action_utilities.sort(key=lambda x: x[1], reverse=True)
        
        # Exploration vs exploitation
        import random
        if random.random() < self._exploration_rate and len(action_utilities) > 1:
            # Explore: select random action from top 3
            selected_idx = random.randint(0, min(2, len(action_utilities) - 1))
            selected_action, utility, components = action_utilities[selected_idx]
            reasoning = f"Exploration: selected action with utility {utility:.3f}"
        else:
            # Exploit: select best action
            selected_action, utility, components = action_utilities[0]
            reasoning = f"Maximizing utility: {utility:.3f}"
        
        # Build detailed reasoning
        component_details = ", ".join(
            f"{name}: {value:.2f}" for name, value in components.items()
        )
        full_reasoning = f"{reasoning}. Components: {component_details}"
        
        return AgentAction(
            action=selected_action,
            confidence=self._calculate_confidence(utility, action_utilities),
            reasoning=full_reasoning,
            metadata={
                "agent_type": "utility_based",
                "total_utility": utility,
                "utility_components": components,
                "alternatives_evaluated": len(action_utilities),
                "exploration": random.random() < self._exploration_rate
            }
        )
    
    def _calculate_expected_utility(
        self,
        state: State,
        action: Action,
        percept: Percept
    ) -> Tuple[float, Dict[str, float]]:
        """
        Calculate expected utility of an action.
        
        EU(a) = Σ weight_i * utility_i(s, a)
        
        Args:
            state: Current state
            action: Action to evaluate
            percept: Current percept (for context)
            
        Returns:
            Tuple of (total utility, component utilities dict)
            
        Time Complexity: O(U) where U is number of utility functions
        Space Complexity: O(U)
        """
        total_utility = 0.0
        component_utilities = {}
        
        for utility_func in self._utility_functions:
            component_utility = utility_func.evaluate(state, action)
            total_utility += component_utility
            component_utilities[utility_func.name] = component_utility
        
        # Apply context-specific adjustments
        total_utility *= self._get_context_multiplier(percept, action)
        
        return total_utility, component_utilities
    
    def _get_context_multiplier(self, percept: Percept, action: Action) -> float:
        """
        Get context-based utility multiplier.
        
        Adjusts utility based on:
        - Energy level
        - Time availability
        - Equipment availability
        
        Args:
            percept: Current percept
            action: Action being evaluated
            
        Returns:
            Multiplier (0.0-1.5)
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        multiplier = 1.0
        
        # Energy level adjustment
        if action.difficulty == Difficulty.ADVANCED and percept.energy_level < 0.5:
            multiplier *= 0.7  # Penalize hard exercises when tired
        elif action.difficulty == Difficulty.BEGINNER and percept.energy_level > 0.8:
            multiplier *= 0.9  # Slightly penalize easy exercises when energetic
        
        # Time availability adjustment
        if action.duration_minutes > percept.time_available_minutes:
            multiplier *= 0.3  # Heavy penalty if not enough time
        
        # Equipment availability (if action requires equipment)
        # For now, assume all equipment available
        
        return multiplier
    
    def _calculate_confidence(
        self,
        selected_utility: float,
        all_utilities: List[Tuple[Action, float, Dict[str, float]]]
    ) -> float:
        """
        Calculate confidence in selected action.
        
        Higher confidence when:
        - Selected utility is much higher than alternatives
        - Utility functions agree (low variance)
        
        Args:
            selected_utility: Utility of selected action
            all_utilities: All action utilities
            
        Returns:
            Confidence score (0.0-1.0)
            
        Time Complexity: O(A)
        Space Complexity: O(1)
        """
        if len(all_utilities) <= 1:
            return 1.0
        
        # Calculate gap between best and second-best
        utilities = [u for _, u, _ in all_utilities]
        best = utilities[0]
        second_best = utilities[1] if len(utilities) > 1 else 0.0
        
        gap = best - second_best
        normalized_gap = min(1.0, gap / max(abs(best), 1.0))
        
        # Base confidence on gap
        confidence = 0.5 + 0.5 * normalized_gap
        
        return min(1.0, max(0.0, confidence))
    
    def _generate_default_action(self, reason: str) -> AgentAction:
        """Generate default action when no actions available."""
        from ..models.action import ActionType
        default_action = Action(
            action_id="rest_default",
            name="Rest",
            action_type=ActionType.REST,
            difficulty=Difficulty.BEGINNER,
            duration_minutes=10,
            description="Default rest action"
        )
        
        return AgentAction(
            action=default_action,
            confidence=0.3,
            reasoning=reason,
            metadata={"agent_type": "utility_based", "default": True}
        )
    
    @staticmethod
    def create_balanced_agent(
        initial_state: State,
        available_actions: List[Action]
    ) -> 'UtilityBasedAgent':
        """
        Create utility agent with balanced objective functions.
        
        Balances:
        - Effectiveness (progress toward goals)
        - Safety (injury risk, difficulty match)
        - Efficiency (time usage, energy expenditure)
        - Enjoyment (variety, preferences)
        
        Args:
            initial_state: Initial state
            available_actions: Available actions
            
        Returns:
            Configured UtilityBasedAgent
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        agent = UtilityBasedAgent(initial_state, available_actions, "Balanced Utility Agent")
        
        # Utility 1: Effectiveness (how well action achieves goal)
        def effectiveness_utility(state: State, action: Action) -> float:
            fitness_goal = state.fitness_goal.value if hasattr(state.fitness_goal, 'value') else str(state.fitness_goal)
            benefit = action.calculate_benefit(fitness_goal)
            return benefit / 100.0  # Normalize to 0-1 range
        
        agent.add_utility_function(UtilityFunction(
            name="effectiveness",
            weight=3.0,  # High weight - most important
            evaluator=effectiveness_utility,
            description="How effective the action is for achieving goals"
        ))
        
        # Utility 2: Safety (match difficulty to level, avoid injury)
        def safety_utility(state: State, action: Action) -> float:
            # Perfect match: 1.0, mismatches: lower
            level_match = {
                ExperienceLevel.BEGINNER: {Difficulty.BEGINNER: 1.0, Difficulty.INTERMEDIATE: 0.5, Difficulty.ADVANCED: 0.2},
                ExperienceLevel.INTERMEDIATE: {Difficulty.BEGINNER: 0.7, Difficulty.INTERMEDIATE: 1.0, Difficulty.ADVANCED: 0.6},
                ExperienceLevel.ADVANCED: {Difficulty.BEGINNER: 0.5, Difficulty.INTERMEDIATE: 0.8, Difficulty.ADVANCED: 1.0},
                ExperienceLevel.EXPERT: {Difficulty.BEGINNER: 0.4, Difficulty.INTERMEDIATE: 0.7, Difficulty.ADVANCED: 1.0}
            }
            
            match_score = level_match.get(state.experience_level, {}).get(action.difficulty, 0.5)
            
            # Penalty for injuries
            injury_penalty = 0.3 if state.has_injury else 0.0
            
            return max(0.0, match_score - injury_penalty)
        
        agent.add_utility_function(UtilityFunction(
            name="safety",
            weight=2.5,  # Very important
            evaluator=safety_utility,
            description="Safety and appropriate difficulty"
        ))
        
        # Utility 3: Efficiency (time and energy optimization)
        def efficiency_utility(state: State, action: Action) -> float:
            # Prefer shorter, higher-intensity actions
            time_score = max(0.0, 1.0 - (action.duration_minutes / 60.0))
            benefit_per_minute = action.calculate_benefit(state) / max(action.estimated_duration, 1)
            return (time_score + min(benefit_per_minute / 10.0, 1.0)) / 2.0
        
        agent.add_utility_function(UtilityFunction(
            name="efficiency",
            weight=1.5,
            evaluator=efficiency_utility,
            description="Time and energy efficiency"
        ))
        
        # Utility 4: Variety (avoid repetition, promote balance)
        def variety_utility(state: State, action: Action) -> float:
            # Simple variety: prefer actions not recently used
            # (In full implementation, would track action history)
            return 0.7  # Baseline variety score
        
        agent.add_utility_function(UtilityFunction(
            name="variety",
            weight=1.0,
            evaluator=variety_utility,
            description="Exercise variety and balance"
        ))
        
        return agent
    
    def get_utility_summary(self) -> Dict[str, Any]:
        """
        Get summary of utility functions and recent utilities.
        
        Returns:
            Dictionary with utility information
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return {
            "utility_functions": len(self._utility_functions),
            "function_details": [
                {
                    "name": uf.name,
                    "weight": uf.weight,
                    "description": uf.description
                }
                for uf in self._utility_functions
            ],
            "recent_action_utilities": dict(list(self._action_utilities.items())[-10:]),
            "exploration_rate": self._exploration_rate
        }
    
    def __str__(self) -> str:
        """String representation."""
        return (
            f"UtilityBasedAgent(utilities={len(self._utility_functions)}, "
            f"actions_evaluated={len(self._action_utilities)})"
        )


# Example usage and testing
if __name__ == "__main__":
    print("Utility-Based Agent")
    print("===================")
    print()
    print("Properties:")
    print("- Maximizes expected utility")
    print("- Balances multiple objectives")
    print("- Rational decision making")
    print("- Handles trade-offs gracefully")
