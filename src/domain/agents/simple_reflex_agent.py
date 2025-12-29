"""
Simple Reflex Agent Implementation.

A simple reflex agent is the most basic type of agent that selects actions
based only on the current percept, ignoring the rest of the percept history.

Function: action = REFLEX(percept)

Properties:
- No internal state or memory
- Rule-based condition-action pairs (if-then rules)
- Fast and simple
- Works well in fully observable environments
- Limited to reactive behavior

Use Case: Safety and injury-prevention filtering for workouts.

Purpose in Workflow:
- Step 1: Filters unsafe exercises based on user injuries and constraints
- Applies if-then safety rules:
  * If user has knee injury → remove knee-intensive exercises
  * If user is beginner → remove advanced exercises
  * If energy level is low → recommend lighter exercises
  * If limited equipment → filter equipment-dependent exercises

Time Complexity: O(n) where n is number of exercises to filter
Space Complexity: O(1) for storing rules
"""

from typing import List, Callable, Dict, Any, Optional
from dataclasses import dataclass

from .agent import Agent, AgentType, Percept, AgentAction
from ..models.state import State, ExperienceLevel, FitnessGoal
from ..models.action import Action, Difficulty


@dataclass
class ReflexRule:
    """
    A condition-action rule for reflex agents.
    
    Attributes:
        condition: Function that checks if rule applies
        action_generator: Function that generates action if condition met
        priority: Rule priority (higher = checked first)
        description: Human-readable rule description
    """
    condition: Callable[[Percept], bool]
    action_generator: Callable[[Percept], Optional[Action]]
    priority: int = 0
    description: str = ""
    
    def matches(self, percept: Percept) -> bool:
        """
        Check if this rule's condition is satisfied.
        
        Args:
            percept: Current percept
            
        Returns:
            True if condition met, False otherwise
            
        Time Complexity: O(1) to O(k) depending on condition
        Space Complexity: O(1)
        """
        return self.condition(percept)
    
    def generate_action(self, percept: Percept) -> Optional[Action]:
        """
        Generate action for this rule.
        
        Args:
            percept: Current percept
            
        Returns:
            Action if generated, None otherwise
            
        Time Complexity: O(1) to O(k) depending on generator
        Space Complexity: O(1)
        """
        return self.action_generator(percept)


class SimpleReflexAgent(Agent):
    """
    Simple Reflex Agent implementation for Safety and Injury Prevention.
    
    This agent uses condition-action rules (if-then rules) to filter exercises
    based on safety constraints. It has no memory of past percepts and makes 
    decisions based solely on the current situation.
    
    Architecture:
    Percept → If-Then Safety Rules → Safe Exercise List
    
    Algorithm:
    1. Receive list of exercises and user constraints (percept)
    2. For each exercise:
       - Apply safety rules (if injury → filter)
       - Apply experience level rules (if beginner → filter advanced)
       - Apply equipment rules (if no equipment → filter)
    3. Return filtered safe exercises
    
    Safety Rules Applied:
    - Injury-based filtering: Remove exercises that stress injured areas
    - Experience-based filtering: Remove exercises too advanced for user
    - Equipment-based filtering: Remove exercises requiring unavailable equipment
    - Energy-based filtering: Recommend lighter exercises if low energy
    
    Advantages:
    - Simple and efficient
    - Fast decision making
    - Easy to understand and explain (good for viva)
    - No memory requirements
    
    Use Case in Workout System:
    - STEP 1 in workflow: Safety filtering before planning
    
    Time Complexity: O(n) where n is number of exercises
    Space Complexity: O(1) for rule storage
    """
    
    def __init__(self, name: str = "Simple Reflex Agent (Safety Filter)"):
        """
        Initialize simple reflex agent for safety filtering.
        
        Args:
            name: Agent name
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        super().__init__(AgentType.SIMPLE_REFLEX, name)
        self._rules: List[ReflexRule] = []
        self._default_action: Optional[Callable[[Percept], Action]] = None
        self._rules_fired_count: Dict[str, int] = {}
    
    def filter_exercises_by_safety(
        self, 
        exercises: List[Any],
        user_state: State,
        available_equipment: List[str] = None,
        energy_level: float = 1.0
    ) -> List[Any]:
        """
        Filter exercises based on safety rules (main function for this agent).
        
        This is the core safety filtering function that applies if-then rules.
        
        Args:
            exercises: List of Exercise objects to filter
            user_state: Current user state (injuries, experience, etc.)
            available_equipment: List of available equipment
            energy_level: User's current energy level (0.0-1.0)
            
        Returns:
            Filtered list of safe exercises
            
        Algorithm:
        For each exercise:
            If user has injury AND exercise affects injured area:
                Remove exercise
            Else If user is beginner AND exercise is advanced:
                Remove exercise
            Else If exercise needs equipment AND equipment not available:
                Remove exercise
            Else If energy is low AND exercise is high intensity:
                Remove exercise
            Else:
                Keep exercise (it's safe)
        
        Time Complexity: O(n) where n is number of exercises
        Space Complexity: O(k) where k is safe exercises
        """
        safe_exercises = []
        available_equipment = available_equipment or []
        
        for exercise in exercises:
            # Rule 1: Check injury contraindications
            if self._check_injury_rule(exercise, user_state):
                continue  # Skip unsafe exercise
            
            # Rule 2: Check experience level appropriateness
            if self._check_experience_rule(exercise, user_state):
                continue  # Skip too advanced exercise
            
            # Rule 3: Check equipment availability
            if self._check_equipment_rule(exercise, available_equipment):
                continue  # Skip exercise with unavailable equipment
            
            # Rule 4: Check energy level vs intensity
            if self._check_energy_rule(exercise, energy_level):
                continue  # Skip too intense exercise for low energy
            
            # Exercise passed all safety checks
            safe_exercises.append(exercise)
        
        return safe_exercises
    
    def _check_injury_rule(self, exercise: Any, user_state: State) -> bool:
        """
        If-Then Rule: If user has injury affecting muscle group, remove exercise.
        
        ENHANCED ACCURACY with multi-layer checking:
        1. Check contraindications field in exercise data
        2. Check primary and secondary muscles
        3. Check exercise name for movement patterns
        4. Check exercise description for keywords
        5. Check exercise category
        
        Returns: True if exercise should be filtered (unsafe), False if safe
        """
        if not user_state.has_injury or not user_state.medical_conditions:
            return False  # No injuries, exercise is safe
        
        # Get exercise attributes (with safe type conversion)
        exercise_name = str(getattr(exercise, 'name', '')).lower()
        exercise_desc = str(getattr(exercise, 'description', '')).lower()
        contraindications_raw = getattr(exercise, 'contraindications', '')
        exercise_contraindications = str(contraindications_raw).lower() if contraindications_raw else ''
        exercise_category = getattr(exercise, 'category', None)
        category_name = str(getattr(exercise_category, 'value', '')).lower() if exercise_category else ''
        
        # Get all muscle groups involved
        exercise_muscles = set()
        if hasattr(exercise, 'primary_muscles') and exercise.primary_muscles:
            exercise_muscles.update([m.lower().strip() for m in exercise.primary_muscles])
        if hasattr(exercise, 'secondary_muscles') and exercise.secondary_muscles:
            exercise_muscles.update([m.lower().strip() for m in exercise.secondary_muscles])
        
        # Combine all text for comprehensive keyword search
        exercise_text = f"{exercise_name} {exercise_desc} {' '.join(exercise_muscles)}"
        
        # Check each injury against exercise
        for injury in user_state.medical_conditions:
            injury_lower = injury.lower().strip()
            
            # LAYER 1: Check contraindications field (most reliable)
            if exercise_contraindications and 'none' not in exercise_contraindications:
                if any(keyword in exercise_contraindications for keyword in [
                    'knee', 'shoulder', 'back', 'wrist', 'elbow', 'ankle', 'hip', 'neck'
                ]):
                    if any(kw in injury_lower for kw in ['knee', 'shoulder', 'back', 'wrist', 'elbow', 'ankle', 'hip', 'neck']):
                        return True  # Contraindication matches injury
            
            # ============ KNEE INJURIES ============
            if any(keyword in injury_lower for keyword in ['knee', 'patella', 'meniscus', 'acl', 'mcl']):
                # Check muscles
                if any(muscle in exercise_muscles for muscle in [
                    'quadriceps', 'quads', 'quad', 'hamstrings', 'hamstring', 'calves', 'calf',
                    'glutes', 'glute', 'legs', 'leg', 'hip flexors', 'hip flexor',
                    'adductors', 'adductor', 'abductors', 'abductor', 'vastus', 'rectus femoris'
                ]):
                    return True
                # Check exercise name and description for knee movements
                if any(keyword in exercise_text for keyword in [
                    'squat', 'squatting', 'lunge', 'lunging', 'leg press', 'leg curl', 'leg extension',
                    'jump', 'jumping', 'hop', 'hopping', 'run', 'running', 'jog', 'jogging',
                    'step', 'stepping', 'climb', 'climbing', 'stair', 'bicycle', 'bike', 'cycling',
                    'kick', 'kicking', 'knee', 'knees', 'leg raise', 'calf raise', 'wall sit',
                    'box jump', 'burpee', 'mountain climber', 'pistol', 'goblet squat'
                ]):
                    return True
                # Check category
                if category_name in ['legs', 'lower_body', 'leg', 'cardio', 'plyometric']:
                    return True
            
            # ============ SHOULDER INJURIES ============  
            if any(keyword in injury_lower for keyword in ['shoulder', 'rotator', 'cuff', 'deltoid']):
                # Check muscles (comprehensive shoulder complex)
                if any(muscle in exercise_muscles for muscle in [
                    'shoulder', 'shoulders', 'deltoid', 'deltoids', 'delts', 'delt',
                    'traps', 'trap', 'trapezius', 'upper traps', 'middle traps',
                    'biceps', 'bicep', 'triceps', 'tricep', 'chest', 'pectorals', 'pecs', 'pec',
                    'back', 'lats', 'lat', 'latissimus', 'rhomboids', 'rhomboid',
                    'upper back', 'rotator cuff', 'forearms', 'forearm', 'serratus',
                    'teres', 'infraspinatus', 'supraspinatus', 'subscapularis'
                ]):
                    return True
                # Check exercise name and description for shoulder movements
                if any(keyword in exercise_text for keyword in [
                    'press', 'pressing', 'push', 'pushing', 'pull', 'pulling', 'row', 'rowing',
                    'raise', 'raising', 'lateral', 'front', 'rear', 'fly', 'flye', 'flies',
                    'shrug', 'shrugging', 'curl', 'curling', 'extension', 'extending',
                    'bench', 'overhead', 'military', 'arnold', 'dip', 'dipping',
                    'pullup', 'pull-up', 'pulldown', 'pushup', 'push-up', 'plank',
                    'upright', 'shoulder', 'arm', 'cable', 'rotation', 'rotate'
                ]):
                    return True
                # Check category
                if category_name in ['upper_body', 'strength', 'arms', 'arm', 'chest', 'back', 'shoulders']:
                    return True
            
            # ============ ARM/WRIST/ELBOW INJURIES ============
            if any(keyword in injury_lower for keyword in ['wrist', 'elbow', 'forearm', 'arm']):
                # Check muscles
                if any(muscle in exercise_muscles for muscle in [
                    'biceps', 'triceps', 'forearms', 'forearm', 'wrist', 'grip',
                    'brachialis', 'brachioradialis'
                ]):
                    return True
                # Check movements requiring wrist/elbow stability
                if any(keyword in exercise_text for keyword in [
                    'curl', 'press', 'push', 'pull', 'row', 'plank', 'hold',
                    'grip', 'wrist', 'forearm', 'elbow', 'arm'
                ]):
                    return True
            
            # ============ BACK INJURIES ============
            if any(keyword in injury_lower for keyword in ['back', 'spine', 'spinal', 'disc', 'lumbar']):
                # Check muscles
                if any(muscle in exercise_muscles for muscle in [
                    'lower back', 'back', 'spinal erectors', 'erector spinae', 'erectors',
                    'lats', 'latissimus', 'rhomboids', 'multifidus', 'quadratus lumborum'
                ]):
                    return True
                # Check movements that stress the back
                if any(keyword in exercise_text for keyword in [
                    'deadlift', 'row', 'rowing', 'pull', 'pulling', 'back',
                    'crunch', 'crunching', 'sit-up', 'sit up', 'situp',
                    'twist', 'twisting', 'rotation', 'rotate', 'bend', 'bending',
                    'good morning', 'hyperextension', 'extension', 'spine'
                ]):
                    return True
            
            # ============ HIP INJURIES ============
            if any(keyword in injury_lower for keyword in ['hip', 'groin', 'pelvis']):
                if any(muscle in exercise_muscles for muscle in [
                    'hip flexors', 'hip', 'glutes', 'adductors', 'abductors', 'psoas'
                ]):
                    return True
                if any(keyword in exercise_text for keyword in [
                    'squat', 'lunge', 'hip', 'circle', 'bridge', 'thrust'
                ]):
                    return True
            
            # ============ ANKLE INJURIES ============
            if any(keyword in injury_lower for keyword in ['ankle', 'foot']):
                if any(muscle in exercise_muscles for muscle in [
                    'calves', 'calf', 'ankle', 'tibialis', 'achilles'
                ]):
                    return True
                if any(keyword in exercise_text for keyword in [
                    'calf raise', 'jump', 'hop', 'run', 'ankle', 'foot'
                ]):
                    return True
            
            # ============ NECK INJURIES ============
            if any(keyword in injury_lower for keyword in ['neck', 'cervical']):
                if any(muscle in exercise_muscles for muscle in [
                    'neck', 'traps', 'trapezius', 'sternocleidomastoid'
                ]):
                    return True
                if any(keyword in exercise_text for keyword in [
                    'shrug', 'neck', 'head', 'overhead', 'crunch'
                ]):
                    return True
        
        return False  # Exercise is safe
    
    def _check_experience_rule(self, exercise: Any, user_state: State) -> bool:
        """
        If-Then Rule: If user is beginner and exercise is advanced, remove it.
        
        Returns: True if exercise should be filtered, False if appropriate
        """
        if user_state.experience_level != ExperienceLevel.BEGINNER:
            return False  # Not beginner, can handle any difficulty
        
        # Get exercise difficulty
        ex_difficulty = getattr(exercise, 'difficulty', '').lower()
        ex_intensity = getattr(exercise, 'intensity', None)
        
        # Beginners should avoid advanced/expert exercises
        if ex_difficulty in ['advanced', 'expert', 'hard', 'difficult']:
            return True  # Filter out
        
        # Check intensity level
        if ex_intensity:
            intensity_value = getattr(ex_intensity, 'value', '').lower() if hasattr(ex_intensity, 'value') else str(ex_intensity).lower()
            if intensity_value in ['high', 'very_high', 'extreme']:
                return True  # Filter out high intensity for beginners
        
        return False  # Appropriate for beginner
    
    def _check_equipment_rule(self, exercise: Any, available_equipment: List[str]) -> bool:
        """
        If-Then Rule: If exercise needs equipment and it's not available, remove it.
        
        Returns: True if exercise should be filtered, False if equipment available
        """
        if not available_equipment:
            # If no equipment list provided, assume all equipment available
            return False
        
        # Get required equipment
        required_equipment = getattr(exercise, 'equipment', []) or []
        if not required_equipment:
            return False  # No equipment needed, exercise is fine
        
        # Normalize equipment names for comparison
        available_lower = [eq.lower().strip() for eq in available_equipment]
        
        # Check if all required equipment is available
        for req_equip in required_equipment:
            req_lower = req_equip.lower().strip()
            # Special cases for common equipment names
            if req_lower == 'none' or req_lower == 'bodyweight':
                continue
            if req_lower not in available_lower:
                return True  # Required equipment not available, filter out
        
        return False  # All equipment available
    
    def _check_energy_rule(self, exercise: Any, energy_level: float) -> bool:
        """
        If-Then Rule: If energy is low and exercise is high intensity, remove it.
        
        Returns: True if exercise should be filtered, False if appropriate
        """
        if energy_level >= 0.7:
            return False  # Good energy, can handle any intensity
        
        # Get exercise intensity
        ex_intensity = getattr(exercise, 'intensity', None)
        if not ex_intensity:
            return False  # Unknown intensity, assume moderate
        
        intensity_value = getattr(ex_intensity, 'value', '').lower() if hasattr(ex_intensity, 'value') else str(ex_intensity).lower()
        
        # Low energy (< 0.7) should avoid high intensity
        if energy_level < 0.3 and intensity_value in ['moderate', 'medium', 'high', 'very_high']:
            return True  # Filter out for very low energy
        elif energy_level < 0.5 and intensity_value in ['high', 'very_high', 'extreme']:
            return True  # Filter out high intensity for low energy
        
        return False  # Intensity appropriate for energy level
    
    def add_rule(self, rule: ReflexRule) -> None:
        """
        Add a condition-action rule to the agent.
        
        Args:
            rule: The reflex rule to add
            
        Time Complexity: O(r log r) for sorting by priority
        Space Complexity: O(1)
        """
        self._rules.append(rule)
        # Sort by priority (higher first)
        self._rules.sort(key=lambda r: r.priority, reverse=True)
    
    def set_default_action(self, action_generator: Callable[[Percept], Action]) -> None:
        """
        Set default action when no rules match.
        
        Args:
            action_generator: Function to generate default action
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._default_action = action_generator
    
    def perceive(self, percept: Percept) -> None:
        """
        Process percept (simple reflex agents don't store state).
        
        Simple reflex agents ignore percept history and don't maintain
        internal state. This method is essentially a no-op.
        
        Args:
            percept: Current percept
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        # Simple reflex agents don't maintain state
        pass
    
    def decide_action(self, percept: Percept) -> AgentAction:
        """
        Decide action using condition-action rules.
        
        Iterates through rules in priority order and returns the first
        matching action. If no rules match, uses default action.
        
        Args:
            percept: Current percept
            
        Returns:
            AgentAction based on matching rule
            
        Time Complexity: O(r) where r is number of rules
        Space Complexity: O(1)
        """
        # Try each rule in priority order
        for rule in self._rules:
            if rule.matches(percept):
                action = rule.generate_action(percept)
                if action is not None:
                    # Track rule usage
                    rule_key = rule.description or str(id(rule))
                    self._rules_fired_count[rule_key] = self._rules_fired_count.get(rule_key, 0) + 1
                    
                    return AgentAction(
                        action=action,
                        confidence=1.0,
                        reasoning=f"Reflex rule: {rule.description}",
                        metadata={
                            "rule_description": rule.description,
                            "rule_priority": rule.priority,
                            "agent_type": "simple_reflex"
                        }
                    )
        
        # No rule matched - use default action if available
        if self._default_action is not None:
            action = self._default_action(percept)
            return AgentAction(
                action=action,
                confidence=0.5,
                reasoning="No specific rule matched, using default action",
                metadata={"agent_type": "simple_reflex", "default": True}
            )
        
        # No action available - return a null action (rest/skip)
        from ..models.action import ActionType
        null_action = Action(
            action_id="rest",
            name="Rest",
            action_type=ActionType.REST,
            difficulty=Difficulty.BEGINNER,
            duration_minutes=5,
            description="No suitable action found, rest recommended"
        )
        
        return AgentAction(
            action=null_action,
            confidence=0.0,
            reasoning="No matching rules and no default action",
            metadata={"agent_type": "simple_reflex", "fallback": True}
        )
    
    def get_rule_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about rule usage.
        
        Returns:
            Dictionary of rule firing counts and statistics
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return {
            "total_rules": len(self._rules),
            "rules_fired": self._rules_fired_count.copy(),
            "most_fired_rule": max(self._rules_fired_count.items(), key=lambda x: x[1])[0]
            if self._rules_fired_count else None,
            "rules_never_fired": len(self._rules) - len(self._rules_fired_count)
        }
    
    @staticmethod
    def create_safety_agent() -> 'SimpleReflexAgent':
        """
        Create a simple reflex agent focused on safety rules.
        
        This agent checks for:
        - Medical contraindications
        - Injury limitations
        - Experience level mismatches
        - Energy level too low
        - Equipment unavailability
        
        Returns:
            Configured SimpleReflexAgent for safety
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        agent = SimpleReflexAgent("Safety Reflex Agent")
        
        # Rule 1: Check for injuries (highest priority)
        def has_injury_condition(percept: Percept) -> bool:
            return len(percept.state.medical_conditions) > 0
        
        def generate_safe_action(percept: Percept) -> Optional[Action]:
            # Return rest or very light activity
            from ..models.action import ActionType
            return Action(
                action_id="rest_injury",
                name="Rest and Recovery",
                action_type=ActionType.REST,
                difficulty=Difficulty.BEGINNER,
                duration_minutes=10,
                description=f"Rest recommended due to injuries: {', '.join(percept.state.medical_conditions)}"
            )
        
        agent.add_rule(ReflexRule(
            condition=has_injury_condition,
            action_generator=generate_safe_action,
            priority=100,
            description="Injury detected - recommend rest"
        ))
        
        # Rule 2: Low energy level
        def low_energy_condition(percept: Percept) -> bool:
            return percept.energy_level < 0.3
        
        def generate_light_action(percept: Percept) -> Optional[Action]:
            from ..models.action import ActionType
            return Action(
                action_id="light_exercise",
                name="Light Activity",
                action_type=ActionType.CARDIO,
                difficulty=Difficulty.BEGINNER,
                duration_minutes=15,
                description="Light exercise due to low energy level"
            )
        
        agent.add_rule(ReflexRule(
            condition=low_energy_condition,
            action_generator=generate_light_action,
            priority=80,
            description="Low energy - recommend light activity"
        ))
        
        # Rule 3: Beginner level check
        def beginner_condition(percept: Percept) -> bool:
            return percept.state.experience_level == ExperienceLevel.BEGINNER
        
        def generate_beginner_action(percept: Percept) -> Optional[Action]:
            from ..models.action import ActionType
            return Action(
                action_id="beginner_safe",
                name="Beginner-Safe Exercise",
                action_type=ActionType.STRENGTH,
                difficulty=Difficulty.BEGINNER,
                duration_minutes=20,
                description="Safe beginner exercise with proper form focus"
            )
        
        agent.add_rule(ReflexRule(
            condition=beginner_condition,
            action_generator=generate_beginner_action,
            priority=60,
            description="Beginner level - recommend safe exercises"
        ))
        
        # Rule 4: Limited time
        def limited_time_condition(percept: Percept) -> bool:
            return percept.time_available_minutes < 20
        
        def generate_quick_action(percept: Percept) -> Optional[Action]:
            from ..models.action import ActionType
            return Action(
                action_id="quick_workout",
                name="Quick Workout",
                action_type=ActionType.CARDIO,
                difficulty=Difficulty.INTERMEDIATE,
                duration_minutes=15,
                description="High-intensity quick workout"
            )
        
        agent.add_rule(ReflexRule(
            condition=limited_time_condition,
            action_generator=generate_quick_action,
            priority=40,
            description="Limited time - recommend quick workout"
        ))
        
        # Default action
        def default_action_gen(percept: Percept) -> Action:
            from ..models.action import ActionType
            return Action(
                action_id="standard_workout",
                name="Standard Workout",
                action_type=ActionType.STRENGTH,
                difficulty=Difficulty.INTERMEDIATE,
                duration_minutes=30,
                description="Standard workout routine"
            )
        
        agent.set_default_action(default_action_gen)
        
        return agent
    
    def __str__(self) -> str:
        """String representation."""
        return f"SimpleReflexAgent(rules={len(self._rules)}, actions={len(self._action_history)})"


# Example usage and testing
if __name__ == "__main__":
    print("Simple Reflex Agent")
    print("===================")
    print()
    print("Properties:")
    print("- No memory or internal state")
    print("- Rule-based condition-action pairs")
    print("- Fast and reactive")
    print("- Suitable for safety checks")
    print()
    
    # Create safety agent
    safety_agent = SimpleReflexAgent.create_safety_agent()
    print(f"Created: {safety_agent}")
    print(f"Rules: {len(safety_agent._rules)}")
