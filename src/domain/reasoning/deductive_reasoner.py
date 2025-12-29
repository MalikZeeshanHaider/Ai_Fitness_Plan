"""
Deductive Reasoning Engine Implementation.

Deductive reasoning applies general rules to specific situations to derive
logical conclusions. It follows the form: IF conditions THEN conclusion.

This is a forward-chaining inference engine that:
1. Starts with known facts
2. Applies rules to derive new facts
3. Continues until goal is reached or no new facts can be derived

Time Complexity: O(r * f) where r=rules, f=facts
Space Complexity: O(f) for fact storage
"""

from typing import List, Dict, Any, Optional, Callable, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from ..models.state import State, ExperienceLevel, FitnessGoal
from ..models.action import Action, Difficulty


class FactType(Enum):
    """Types of facts in the knowledge base."""
    USER_ATTRIBUTE = "user_attribute"
    CONSTRAINT = "constraint"
    RECOMMENDATION = "recommendation"
    SAFETY = "safety"
    DERIVED = "derived"


@dataclass
class Fact:
    """
    A fact represents a piece of knowledge about the world.
    
    Facts can be:
    - User attributes: age=30, experience=beginner
    - Constraints: has_injury=True, time_available=30
    - Safety rules: avoid_high_impact=True
    - Derived facts: suitable_difficulty=beginner
    
    Attributes:
        predicate: The fact predicate (e.g., "has_injury")
        arguments: Arguments to the predicate
        fact_type: Type of fact
        confidence: Confidence in this fact (0.0-1.0)
        timestamp: When fact was asserted
        source: Source of this fact (rule, user, sensor)
    """
    predicate: str
    arguments: Dict[str, Any] = field(default_factory=dict)
    fact_type: FactType = FactType.USER_ATTRIBUTE
    confidence: float = 1.0
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = "user"
    
    def matches(self, pattern: Dict[str, Any]) -> bool:
        """
        Check if this fact matches a pattern.
        
        Args:
            pattern: Pattern to match against
            
        Returns:
            True if matches, False otherwise
            
        Time Complexity: O(k) where k is number of arguments
        Space Complexity: O(1)
        """
        if "predicate" in pattern and pattern["predicate"] != self.predicate:
            return False
        
        for key, value in pattern.get("arguments", {}).items():
            if key not in self.arguments or self.arguments[key] != value:
                return False
        
        return True
    
    def __str__(self) -> str:
        """String representation."""
        args_str = ", ".join(f"{k}={v}" for k, v in self.arguments.items())
        return f"{self.predicate}({args_str})"
    
    def __hash__(self) -> int:
        """Hash for set operations."""
        return hash((self.predicate, tuple(sorted(self.arguments.items()))))
    
    def __eq__(self, other) -> bool:
        """Equality comparison."""
        if not isinstance(other, Fact):
            return False
        return self.predicate == other.predicate and self.arguments == other.arguments


@dataclass
class Rule:
    """
    A rule represents an IF-THEN logical implication.
    
    Rules have the form:
    IF condition1 AND condition2 AND ... THEN conclusion
    
    Attributes:
        rule_id: Unique identifier
        conditions: List of conditions (predicates to match)
        conclusion: Fact to derive if conditions met
        priority: Rule priority (higher = applied first)
        description: Human-readable description
        confidence: Confidence in this rule (0.0-1.0)
    """
    rule_id: str
    conditions: List[Dict[str, Any]]
    conclusion: Fact
    priority: int = 1
    description: str = ""
    confidence: float = 1.0
    
    def evaluate(self, facts: Set[Fact]) -> bool:
        """
        Check if all conditions are satisfied by facts.
        
        Args:
            facts: Current fact base
            
        Returns:
            True if all conditions met, False otherwise
            
        Time Complexity: O(c * f) where c=conditions, f=facts
        Space Complexity: O(1)
        """
        for condition in self.conditions:
            if not any(fact.matches(condition) for fact in facts):
                return False
        return True
    
    def __str__(self) -> str:
        """String representation."""
        conds = " AND ".join(str(c) for c in self.conditions)
        return f"IF {conds} THEN {self.conclusion}"


class DeductiveReasoner:
    """
    Deductive Reasoning Engine using forward chaining.
    
    This reasoner:
    1. Maintains a knowledge base of facts
    2. Applies rules to derive new facts
    3. Explains reasoning chains
    4. Handles rule priorities and conflicts
    
    Forward Chaining Algorithm:
    1. Start with initial facts
    2. Find all rules whose conditions are satisfied
    3. Apply highest priority rule to derive new fact
    4. Add new fact to knowledge base
    5. Repeat until goal reached or no new facts
    
    Properties:
    - Sound: Derived conclusions are logically valid
    - Complete: Will find all derivable facts
    - Monotonic: Facts never retracted (only added)
    - Explainable: Can trace reasoning chains
    
    Use Cases in Workout System:
    - Safety rule enforcement
    - Difficulty level determination
    - Exercise contraindication checking
    - Equipment requirement validation
    - Progressive overload logic
    
    Time Complexity: O(r * f * i) where r=rules, f=facts, i=iterations
    Space Complexity: O(f) for fact storage
    """
    
    def __init__(self, name: str = "Deductive Reasoner"):
        """
        Initialize deductive reasoner.
        
        Args:
            name: Reasoner name
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._name = name
        self._facts: Set[Fact] = set()
        self._rules: List[Rule] = []
        self._reasoning_chain: List[str] = []
        self._iterations = 0
        self._max_iterations = 100  # Prevent infinite loops
    
    @property
    def facts(self) -> Set[Fact]:
        """Get current facts."""
        return self._facts.copy()
    
    @property
    def rules(self) -> List[Rule]:
        """Get current rules."""
        return self._rules.copy()
    
    @property
    def reasoning_chain(self) -> List[str]:
        """Get reasoning chain (explanation)."""
        return self._reasoning_chain.copy()
    
    def add_fact(self, fact: Fact) -> None:
        """
        Add a fact to the knowledge base.
        
        Args:
            fact: Fact to add
            
        Time Complexity: O(1) average case
        Space Complexity: O(1)
        """
        self._facts.add(fact)
        self._reasoning_chain.append(f"Asserted: {fact}")
    
    def add_rule(self, rule: Rule) -> None:
        """
        Add a rule to the rule base.
        
        Args:
            rule: Rule to add
            
        Time Complexity: O(r log r) for sorting
        Space Complexity: O(1)
        """
        self._rules.append(rule)
        # Sort rules by priority (highest first)
        self._rules.sort(key=lambda r: r.priority, reverse=True)
    
    def infer(self, max_iterations: Optional[int] = None) -> Set[Fact]:
        """
        Run forward chaining inference to derive new facts.
        
        Algorithm:
        1. While changes occur and iteration limit not reached:
           a. For each rule in priority order:
              - Check if conditions are satisfied
              - If yes and conclusion not already known, add it
              - Record reasoning step
           b. If no new facts derived, stop
        
        Args:
            max_iterations: Maximum inference iterations
            
        Returns:
            Set of all facts (initial + derived)
            
        Time Complexity: O(r * f * i)
        Space Complexity: O(f)
        """
        max_iter = max_iterations or self._max_iterations
        self._iterations = 0
        self._reasoning_chain.append(f"Starting inference with {len(self._facts)} facts")
        
        while self._iterations < max_iter:
            self._iterations += 1
            new_facts_added = False
            
            # Try each rule in priority order
            for rule in self._rules:
                # Check if rule conditions are satisfied
                if rule.evaluate(self._facts):
                    # Check if conclusion is new
                    if rule.conclusion not in self._facts:
                        # Add derived fact
                        self._facts.add(rule.conclusion)
                        new_facts_added = True
                        
                        # Record reasoning step
                        self._reasoning_chain.append(
                            f"Applied rule '{rule.rule_id}': {rule.description} → {rule.conclusion}"
                        )
            
            # Stop if no new facts were derived
            if not new_facts_added:
                self._reasoning_chain.append(
                    f"Inference complete after {self._iterations} iterations. No new facts derived."
                )
                break
        
        if self._iterations >= max_iter:
            self._reasoning_chain.append(
                f"Inference stopped: reached maximum iterations ({max_iter})"
            )
        
        return self._facts.copy()
    
    def query(self, pattern: Dict[str, Any]) -> List[Fact]:
        """
        Query the knowledge base for facts matching a pattern.
        
        Args:
            pattern: Pattern to match (predicate and/or arguments)
            
        Returns:
            List of matching facts
            
        Time Complexity: O(f) where f is number of facts
        Space Complexity: O(k) where k is matching facts
        """
        return [fact for fact in self._facts if fact.matches(pattern)]
    
    def has_fact(self, predicate: str, arguments: Optional[Dict[str, Any]] = None) -> bool:
        """
        Check if a specific fact exists.
        
        Args:
            predicate: Fact predicate
            arguments: Optional arguments to match
            
        Returns:
            True if fact exists, False otherwise
            
        Time Complexity: O(f)
        Space Complexity: O(1)
        """
        pattern = {"predicate": predicate}
        if arguments:
            pattern["arguments"] = arguments
        
        return len(self.query(pattern)) > 0
    
    def explain(self, fact: Fact) -> List[str]:
        """
        Generate explanation for how a fact was derived.
        
        Args:
            fact: Fact to explain
            
        Returns:
            List of reasoning steps
            
        Time Complexity: O(c) where c is chain length
        Space Complexity: O(c)
        """
        explanation = []
        fact_str = str(fact)
        
        for step in self._reasoning_chain:
            if fact_str in step:
                explanation.append(step)
        
        if not explanation:
            explanation.append(f"Fact '{fact}' was not derived (may be initial fact)")
        
        return explanation
    
    def reset(self) -> None:
        """
        Reset the reasoner (clear facts and reasoning chain).
        
        Rules are preserved.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._facts.clear()
        self._reasoning_chain.clear()
        self._iterations = 0
    
    @staticmethod
    def create_workout_reasoner() -> 'DeductiveReasoner':
        """
        Create a deductive reasoner with workout safety rules.
        
        Returns:
            Configured DeductiveReasoner
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        reasoner = DeductiveReasoner("Workout Safety Reasoner")
        
        # Rule 1: Beginner level → Beginner difficulty
        reasoner.add_rule(Rule(
            rule_id="R1_beginner_difficulty",
            conditions=[
                {"predicate": "experience_level", "arguments": {"level": "beginner"}}
            ],
            conclusion=Fact(
                predicate="recommended_difficulty",
                arguments={"difficulty": "beginner"},
                fact_type=FactType.RECOMMENDATION,
                source="rule_R1"
            ),
            priority=10,
            description="Beginners should do beginner exercises",
            confidence=1.0
        ))
        
        # Rule 2: Has injury → Avoid high impact
        reasoner.add_rule(Rule(
            rule_id="R2_injury_safety",
            conditions=[
                {"predicate": "has_injury", "arguments": {"value": True}}
            ],
            conclusion=Fact(
                predicate="avoid_exercise_type",
                arguments={"type": "high_impact"},
                fact_type=FactType.SAFETY,
                source="rule_R2"
            ),
            priority=100,  # High priority - safety critical
            description="Injuries require avoiding high impact exercises",
            confidence=1.0
        ))
        
        # Rule 3: Low energy → Light workout
        reasoner.add_rule(Rule(
            rule_id="R3_energy_adjustment",
            conditions=[
                {"predicate": "energy_level", "arguments": {"status": "low"}}
            ],
            conclusion=Fact(
                predicate="workout_intensity",
                arguments={"level": "light"},
                fact_type=FactType.RECOMMENDATION,
                source="rule_R3"
            ),
            priority=50,
            description="Low energy requires light intensity",
            confidence=0.9
        ))
        
        # Rule 4: Advanced level + No injury → Can do advanced
        reasoner.add_rule(Rule(
            rule_id="R4_advanced_clearance",
            conditions=[
                {"predicate": "experience_level", "arguments": {"level": "advanced"}},
                {"predicate": "has_injury", "arguments": {"value": False}}
            ],
            conclusion=Fact(
                predicate="recommended_difficulty",
                arguments={"difficulty": "advanced"},
                fact_type=FactType.RECOMMENDATION,
                source="rule_R4"
            ),
            priority=20,
            description="Advanced users without injuries can do advanced exercises",
            confidence=1.0
        ))
        
        # Rule 5: Weight loss goal → Cardio focus
        reasoner.add_rule(Rule(
            rule_id="R5_weight_loss_cardio",
            conditions=[
                {"predicate": "fitness_goal", "arguments": {"goal": "weight_loss"}}
            ],
            conclusion=Fact(
                predicate="exercise_type_priority",
                arguments={"type": "cardio", "priority": "high"},
                fact_type=FactType.RECOMMENDATION,
                source="rule_R5"
            ),
            priority=30,
            description="Weight loss goals benefit from cardio exercises",
            confidence=0.95
        ))
        
        # Rule 6: Muscle gain goal → Strength focus
        reasoner.add_rule(Rule(
            rule_id="R6_muscle_gain_strength",
            conditions=[
                {"predicate": "fitness_goal", "arguments": {"goal": "muscle_gain"}}
            ],
            conclusion=Fact(
                predicate="exercise_type_priority",
                arguments={"type": "strength", "priority": "high"},
                fact_type=FactType.RECOMMENDATION,
                source="rule_R6"
            ),
            priority=30,
            description="Muscle gain goals benefit from strength training",
            confidence=0.95
        ))
        
        # Rule 7: Limited time → Short workout
        reasoner.add_rule(Rule(
            rule_id="R7_time_constraint",
            conditions=[
                {"predicate": "time_available", "arguments": {"duration": "limited"}}
            ],
            conclusion=Fact(
                predicate="workout_duration",
                arguments={"length": "short", "max_minutes": 20},
                fact_type=FactType.CONSTRAINT,
                source="rule_R7"
            ),
            priority=60,
            description="Limited time requires short workouts",
            confidence=1.0
        ))
        
        return reasoner
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get reasoning statistics.
        
        Returns:
            Dictionary with statistics
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return {
            "name": self._name,
            "total_facts": len(self._facts),
            "total_rules": len(self._rules),
            "inference_iterations": self._iterations,
            "reasoning_chain_length": len(self._reasoning_chain),
            "fact_types": {
                fact_type.value: sum(1 for f in self._facts if f.fact_type == fact_type)
                for fact_type in FactType
            }
        }
    
    def __str__(self) -> str:
        """String representation."""
        return (
            f"DeductiveReasoner(name={self._name}, "
            f"facts={len(self._facts)}, rules={len(self._rules)})"
        )


# Example usage and testing
if __name__ == "__main__":
    print("Deductive Reasoning Engine")
    print("==========================")
    print()
    
    # Create reasoner
    reasoner = DeductiveReasoner.create_workout_reasoner()
    
    # Add initial facts
    reasoner.add_fact(Fact(
        predicate="experience_level",
        arguments={"level": "beginner"},
        fact_type=FactType.USER_ATTRIBUTE
    ))
    reasoner.add_fact(Fact(
        predicate="has_injury",
        arguments={"value": True},
        fact_type=FactType.USER_ATTRIBUTE
    ))
    
    print("Initial facts:", len(reasoner.facts))
    
    # Run inference
    final_facts = reasoner.infer()
    
    print(f"After inference: {len(final_facts)} facts")
    print("\nReasoning chain:")
    for step in reasoner.reasoning_chain:
        print(f"  {step}")
