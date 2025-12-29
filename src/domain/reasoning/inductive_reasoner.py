"""
Inductive Reasoning Engine Implementation.

Inductive reasoning learns general patterns from specific examples.
It moves from observations to generalizations:
Observations → Pattern Discovery → Generalization

This implementation uses:
1. Pattern Mining: Discover frequent patterns in examples
2. Generalization: Create rules from patterns
3. Confidence Scoring: Measure pattern reliability
4. Pattern Application: Use learned patterns for prediction

Common Inductive Learning Algorithms:
- Frequent Pattern Mining (Apriori-like)
- Decision Tree Learning (ID3/C4.5)
- Association Rule Learning
- Clustering for pattern discovery

Time Complexity: O(n * m) where n=examples, m=attributes
Space Complexity: O(p) where p=patterns stored
"""

from typing import List, Dict, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, Counter
from datetime import datetime
from enum import Enum

from ..models.state import State, ExperienceLevel, FitnessGoal
from ..models.action import Action, Difficulty, ExerciseType


class PatternType(Enum):
    """Types of patterns that can be learned."""
    FREQUENT_ITEMSET = "frequent_itemset"  # Co-occurring attributes
    ASSOCIATION_RULE = "association_rule"  # A → B relationships
    SEQUENTIAL = "sequential"  # Temporal patterns
    CLASSIFICATION = "classification"  # Predictive patterns


@dataclass
class Example:
    """
    A training example for inductive learning.
    
    Examples contain:
    - Attributes: Features describing the situation
    - Outcome: Result or class label
    - Context: Additional contextual information
    
    Attributes:
        example_id: Unique identifier
        attributes: Feature dictionary
        outcome: Result/label for this example
        weight: Example weight/importance
        timestamp: When example occurred
    """
    example_id: str
    attributes: Dict[str, Any]
    outcome: Any
    weight: float = 1.0
    timestamp: datetime = field(default_factory=datetime.now)
    
    def matches_pattern(self, pattern_attributes: Dict[str, Any]) -> bool:
        """
        Check if this example matches a pattern.
        
        Args:
            pattern_attributes: Pattern to match
            
        Returns:
            True if matches, False otherwise
            
        Time Complexity: O(k) where k is pattern attributes
        Space Complexity: O(1)
        """
        for key, value in pattern_attributes.items():
            if key not in self.attributes or self.attributes[key] != value:
                return False
        return True
    
    def __hash__(self) -> int:
        """Hash for set operations."""
        return hash(self.example_id)
    
    def __eq__(self, other) -> bool:
        """Equality comparison."""
        if not isinstance(other, Example):
            return False
        return self.example_id == other.example_id


@dataclass
class Pattern:
    """
    A learned pattern from examples.
    
    Patterns represent generalizations discovered in data:
    - Frequent itemsets: {experience=beginner, goal=weight_loss} appears often
    - Association rules: {experience=beginner} → {difficulty=beginner}
    - Classification rules: IF attributes THEN outcome
    
    Attributes:
        pattern_id: Unique identifier
        antecedent: Input attributes (condition)
        consequent: Output prediction (conclusion)
        pattern_type: Type of pattern
        support: Frequency in examples (support count)
        confidence: Prediction reliability (0.0-1.0)
        examples_seen: Number of examples this pattern covers
        description: Human-readable description
    """
    pattern_id: str
    antecedent: Dict[str, Any]
    consequent: Optional[Dict[str, Any]]
    pattern_type: PatternType
    support: int = 0  # Number of examples supporting this pattern
    confidence: float = 0.0  # Confidence in pattern
    examples_seen: int = 0
    description: str = ""
    
    def applies_to(self, attributes: Dict[str, Any]) -> bool:
        """
        Check if pattern applies to given attributes.
        
        Args:
            attributes: Attributes to check
            
        Returns:
            True if pattern matches, False otherwise
            
        Time Complexity: O(k) where k is antecedent size
        Space Complexity: O(1)
        """
        for key, value in self.antecedent.items():
            if key not in attributes or attributes[key] != value:
                return False
        return True
    
    def predict(self) -> Optional[Dict[str, Any]]:
        """
        Get prediction from this pattern.
        
        Returns:
            Consequent if confidence is high enough, None otherwise
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if self.confidence >= 0.5:  # Minimum confidence threshold
            return self.consequent
        return None
    
    def __str__(self) -> str:
        """String representation."""
        antecedent_str = ", ".join(f"{k}={v}" for k, v in self.antecedent.items())
        consequent_str = ", ".join(f"{k}={v}" for k, v in (self.consequent or {}).items())
        return f"{{{antecedent_str}}} → {{{consequent_str}}} (conf={self.confidence:.2f})"


class InductiveReasoner:
    """
    Inductive Reasoning Engine for pattern learning.
    
    This reasoner learns from examples:
    1. Collects training examples
    2. Mines frequent patterns using Apriori-like algorithm
    3. Generates association rules
    4. Uses patterns for prediction
    
    Apriori Algorithm (simplified):
    1. Find frequent 1-itemsets (individual attributes)
    2. Generate candidate 2-itemsets
    3. Prune infrequent candidates
    4. Repeat until no frequent itemsets
    5. Generate rules from frequent itemsets
    
    Association Rule Learning:
    - Support(A → B) = frequency of A and B together
    - Confidence(A → B) = Support(A ∪ B) / Support(A)
    - Lift(A → B) = Confidence(A → B) / Support(B)
    
    Properties:
    - Probabilistic: Patterns have confidence scores
    - Data-driven: Learns from observed examples
    - Generalizable: Creates rules from specific cases
    - Explainable: Patterns show what was learned
    
    Use Cases in Workout System:
    - Learn exercise preferences from history
    - Discover effective workout combinations
    - Predict outcomes based on user attributes
    - Identify successful progression patterns
    - Recommend based on similar users
    
    Time Complexity: O(n * m * p) where n=examples, m=attributes, p=patterns
    Space Complexity: O(p + n)
    """
    
    def __init__(
        self,
        name: str = "Inductive Reasoner",
        min_support: int = 2,
        min_confidence: float = 0.6
    ):
        """
        Initialize inductive reasoner.
        
        Args:
            name: Reasoner name
            min_support: Minimum support count for patterns
            min_confidence: Minimum confidence for rules
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._name = name
        self._examples: List[Example] = []
        self._patterns: List[Pattern] = []
        self._min_support = min_support
        self._min_confidence = min_confidence
        self._learning_log: List[str] = []
    
    @property
    def examples(self) -> List[Example]:
        """Get training examples."""
        return self._examples.copy()
    
    @property
    def patterns(self) -> List[Pattern]:
        """Get learned patterns."""
        return self._patterns.copy()
    
    @property
    def learning_log(self) -> List[str]:
        """Get learning log (explanation)."""
        return self._learning_log.copy()
    
    def add_example(self, example: Example) -> None:
        """
        Add a training example.
        
        Args:
            example: Example to add
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._examples.append(example)
        self._learning_log.append(f"Added example: {example.example_id}")
    
    def add_examples(self, examples: List[Example]) -> None:
        """
        Add multiple training examples.
        
        Args:
            examples: Examples to add
            
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        self._examples.extend(examples)
        self._learning_log.append(f"Added {len(examples)} examples")
    
    def learn_patterns(self) -> List[Pattern]:
        """
        Learn patterns from examples using association rule mining.
        
        Algorithm:
        1. Find frequent 1-itemsets (single attributes)
        2. Generate frequent 2-itemsets
        3. Create association rules with confidence
        4. Learn classification patterns (attributes → outcome)
        
        Returns:
            List of learned patterns
            
        Time Complexity: O(n * m^2) where n=examples, m=attributes
        Space Complexity: O(p) where p=patterns
        """
        if not self._examples:
            self._learning_log.append("No examples to learn from")
            return []
        
        self._learning_log.append(f"Learning patterns from {len(self._examples)} examples")
        self._patterns.clear()
        
        # Step 1: Find frequent 1-itemsets
        attribute_counts = self._count_attribute_frequencies()
        frequent_1_itemsets = self._filter_frequent_itemsets(attribute_counts)
        
        self._learning_log.append(
            f"Found {len(frequent_1_itemsets)} frequent 1-itemsets"
        )
        
        # Step 2: Find frequent 2-itemsets (pairs)
        pair_counts = self._count_pair_frequencies()
        frequent_2_itemsets = self._filter_frequent_itemsets(pair_counts)
        
        self._learning_log.append(
            f"Found {len(frequent_2_itemsets)} frequent 2-itemsets"
        )
        
        # Step 3: Generate association rules from frequent itemsets
        self._generate_association_rules(frequent_2_itemsets, pair_counts)
        
        # Step 4: Learn classification patterns (attributes → outcome)
        self._learn_classification_patterns(frequent_1_itemsets)
        
        self._learning_log.append(f"Learned {len(self._patterns)} total patterns")
        
        return self._patterns.copy()
    
    def _count_attribute_frequencies(self) -> Dict[Tuple[str, Any], int]:
        """
        Count frequency of each attribute value.
        
        Returns:
            Dictionary of (attribute, value) → count
            
        Time Complexity: O(n * m)
        Space Complexity: O(m * v) where v is unique values
        """
        counts: Dict[Tuple[str, Any], int] = Counter()
        
        for example in self._examples:
            for attr, value in example.attributes.items():
                counts[(attr, value)] += 1
        
        return counts
    
    def _count_pair_frequencies(self) -> Dict[Tuple[Tuple[str, Any], Tuple[str, Any]], int]:
        """
        Count frequency of attribute pairs.
        
        Returns:
            Dictionary of pairs → count
            
        Time Complexity: O(n * m^2)
        Space Complexity: O(m^2 * v^2)
        """
        counts: Dict[Tuple[Tuple[str, Any], Tuple[str, Any]], int] = Counter()
        
        for example in self._examples:
            items = [(attr, value) for attr, value in example.attributes.items()]
            
            # Count all pairs
            for i in range(len(items)):
                for j in range(i + 1, len(items)):
                    pair = tuple(sorted([items[i], items[j]]))
                    counts[pair] += 1
        
        return counts
    
    def _filter_frequent_itemsets(
        self,
        counts: Dict[Any, int]
    ) -> Dict[Any, int]:
        """
        Filter itemsets by minimum support.
        
        Args:
            counts: Itemset counts
            
        Returns:
            Frequent itemsets
            
        Time Complexity: O(k) where k is itemsets
        Space Complexity: O(f) where f is frequent itemsets
        """
        return {
            itemset: count
            for itemset, count in counts.items()
            if count >= self._min_support
        }
    
    def _generate_association_rules(
        self,
        frequent_itemsets: Dict[Tuple[Tuple[str, Any], Tuple[str, Any]], int],
        pair_counts: Dict[Tuple[Tuple[str, Any], Tuple[str, Any]], int]
    ) -> None:
        """
        Generate association rules from frequent 2-itemsets.
        
        For each frequent pair (A, B):
        - Create rule A → B
        - Calculate confidence = P(B|A) = count(A,B) / count(A)
        
        Args:
            frequent_itemsets: Frequent pairs
            pair_counts: Pair counts
            
        Time Complexity: O(p) where p is frequent pairs
        Space Complexity: O(r) where r is rules generated
        """
        single_counts = self._count_attribute_frequencies()
        
        for pair, support in frequent_itemsets.items():
            item1, item2 = pair
            
            # Create rule: item1 → item2
            antecedent_count = single_counts.get(item1, 0)
            if antecedent_count > 0:
                confidence = support / antecedent_count
                
                if confidence >= self._min_confidence:
                    pattern = Pattern(
                        pattern_id=f"ASSOC_{len(self._patterns)}",
                        antecedent={item1[0]: item1[1]},
                        consequent={item2[0]: item2[1]},
                        pattern_type=PatternType.ASSOCIATION_RULE,
                        support=support,
                        confidence=confidence,
                        examples_seen=antecedent_count,
                        description=f"If {item1[0]}={item1[1]} then likely {item2[0]}={item2[1]}"
                    )
                    self._patterns.append(pattern)
            
            # Create reverse rule: item2 → item1
            antecedent_count = single_counts.get(item2, 0)
            if antecedent_count > 0:
                confidence = support / antecedent_count
                
                if confidence >= self._min_confidence:
                    pattern = Pattern(
                        pattern_id=f"ASSOC_{len(self._patterns)}",
                        antecedent={item2[0]: item2[1]},
                        consequent={item1[0]: item1[1]},
                        pattern_type=PatternType.ASSOCIATION_RULE,
                        support=support,
                        confidence=confidence,
                        examples_seen=antecedent_count,
                        description=f"If {item2[0]}={item2[1]} then likely {item1[0]}={item1[1]}"
                    )
                    self._patterns.append(pattern)
    
    def _learn_classification_patterns(
        self,
        frequent_itemsets: Dict[Tuple[str, Any], int]
    ) -> None:
        """
        Learn patterns that predict outcomes.
        
        For each frequent attribute:
        - Find most common outcome when attribute present
        - Create classification rule: attribute → outcome
        
        Args:
            frequent_itemsets: Frequent single attributes
            
        Time Complexity: O(f * n) where f is frequent, n is examples
        Space Complexity: O(p) where p is patterns
        """
        for (attr, value), support in frequent_itemsets.items():
            # Find outcomes when this attribute present
            outcomes = []
            for example in self._examples:
                if example.attributes.get(attr) == value:
                    outcomes.append(example.outcome)
            
            if not outcomes:
                continue
            
            # Find most common outcome
            outcome_counts = Counter(outcomes)
            most_common_outcome, outcome_count = outcome_counts.most_common(1)[0]
            
            confidence = outcome_count / len(outcomes)
            
            if confidence >= self._min_confidence:
                pattern = Pattern(
                    pattern_id=f"CLASS_{len(self._patterns)}",
                    antecedent={attr: value},
                    consequent={"outcome": most_common_outcome},
                    pattern_type=PatternType.CLASSIFICATION,
                    support=outcome_count,
                    confidence=confidence,
                    examples_seen=len(outcomes),
                    description=f"If {attr}={value} then outcome likely {most_common_outcome}"
                )
                self._patterns.append(pattern)
    
    def predict(self, attributes: Dict[str, Any]) -> List[Tuple[Pattern, Dict[str, Any]]]:
        """
        Predict outcomes using learned patterns.
        
        Args:
            attributes: Input attributes
            
        Returns:
            List of (pattern, prediction) tuples sorted by confidence
            
        Time Complexity: O(p) where p is patterns
        Space Complexity: O(m) where m is matching patterns
        """
        predictions = []
        
        for pattern in self._patterns:
            if pattern.applies_to(attributes):
                prediction = pattern.predict()
                if prediction:
                    predictions.append((pattern, prediction))
        
        # Sort by confidence (highest first)
        predictions.sort(key=lambda x: x[0].confidence, reverse=True)
        
        return predictions
    
    def get_best_prediction(self, attributes: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get single best prediction.
        
        Args:
            attributes: Input attributes
            
        Returns:
            Best prediction or None if no patterns match
            
        Time Complexity: O(p)
        Space Complexity: O(1)
        """
        predictions = self.predict(attributes)
        
        if predictions:
            return predictions[0][1]  # Return prediction from highest confidence pattern
        
        return None
    
    def get_patterns_for_attribute(self, attribute: str, value: Any) -> List[Pattern]:
        """
        Get all patterns involving a specific attribute.
        
        Args:
            attribute: Attribute name
            value: Attribute value
            
        Returns:
            List of matching patterns
            
        Time Complexity: O(p)
        Space Complexity: O(m) where m is matching patterns
        """
        return [
            pattern for pattern in self._patterns
            if attribute in pattern.antecedent and pattern.antecedent[attribute] == value
        ]
    
    def explain_prediction(
        self,
        attributes: Dict[str, Any],
        prediction: Dict[str, Any]
    ) -> List[str]:
        """
        Explain how a prediction was made.
        
        Args:
            attributes: Input attributes
            prediction: Prediction to explain
            
        Returns:
            List of explanation strings
            
        Time Complexity: O(p)
        Space Complexity: O(e) where e is explanations
        """
        explanations = []
        
        for pattern in self._patterns:
            if pattern.applies_to(attributes) and pattern.consequent == prediction:
                explanations.append(
                    f"Pattern {pattern.pattern_id}: {pattern.description} "
                    f"(confidence={pattern.confidence:.2f}, support={pattern.support})"
                )
        
        if not explanations:
            explanations.append("No learned patterns explain this prediction")
        
        return explanations
    
    def reset(self) -> None:
        """
        Reset learner (clear examples and patterns).
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._examples.clear()
        self._patterns.clear()
        self._learning_log.clear()
    
    @staticmethod
    def create_workout_learner() -> 'InductiveReasoner':
        """
        Create an inductive reasoner with sample workout examples.
        
        Returns:
            Configured InductiveReasoner
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        reasoner = InductiveReasoner(
            name="Workout Pattern Learner",
            min_support=2,
            min_confidence=0.7
        )
        
        # Add training examples
        examples = [
            Example(
                example_id="E1",
                attributes={"experience": "beginner", "goal": "weight_loss", "time": 30},
                outcome="cardio_focus"
            ),
            Example(
                example_id="E2",
                attributes={"experience": "beginner", "goal": "weight_loss", "time": 45},
                outcome="cardio_focus"
            ),
            Example(
                example_id="E3",
                attributes={"experience": "intermediate", "goal": "muscle_gain", "time": 60},
                outcome="strength_focus"
            ),
            Example(
                example_id="E4",
                attributes={"experience": "intermediate", "goal": "muscle_gain", "time": 45},
                outcome="strength_focus"
            ),
            Example(
                example_id="E5",
                attributes={"experience": "advanced", "goal": "endurance", "time": 60},
                outcome="mixed_training"
            ),
            Example(
                example_id="E6",
                attributes={"experience": "beginner", "goal": "general_fitness", "time": 30},
                outcome="mixed_training"
            ),
        ]
        
        reasoner.add_examples(examples)
        
        return reasoner
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get learning statistics.
        
        Returns:
            Dictionary with statistics
            
        Time Complexity: O(p)
        Space Complexity: O(1)
        """
        pattern_type_counts = Counter(p.pattern_type for p in self._patterns)
        
        return {
            "name": self._name,
            "total_examples": len(self._examples),
            "total_patterns": len(self._patterns),
            "pattern_types": {pt.value: pattern_type_counts[pt] for pt in PatternType},
            "min_support": self._min_support,
            "min_confidence": self._min_confidence,
            "average_pattern_confidence": (
                sum(p.confidence for p in self._patterns) / len(self._patterns)
                if self._patterns else 0.0
            ),
            "learning_steps": len(self._learning_log)
        }
    
    def __str__(self) -> str:
        """String representation."""
        return (
            f"InductiveReasoner(name={self._name}, "
            f"examples={len(self._examples)}, patterns={len(self._patterns)})"
        )


# Example usage and testing
if __name__ == "__main__":
    print("Inductive Reasoning Engine")
    print("==========================")
    print()
    
    # Create learner with examples
    learner = InductiveReasoner.create_workout_learner()
    
    print(f"Training examples: {len(learner.examples)}")
    
    # Learn patterns
    patterns = learner.learn_patterns()
    
    print(f"Learned patterns: {len(patterns)}")
    print("\nPatterns:")
    for pattern in patterns:
        print(f"  {pattern}")
    
    # Test prediction
    test_attrs = {"experience": "beginner", "goal": "weight_loss"}
    predictions = learner.predict(test_attrs)
    
    print(f"\nPredictions for {test_attrs}:")
    for pattern, prediction in predictions:
        print(f"  {prediction} (confidence={pattern.confidence:.2f})")
