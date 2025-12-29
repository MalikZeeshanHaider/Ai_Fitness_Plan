"""
Probabilistic Reasoning with Conditional Probability.

Probabilistic reasoning handles uncertainty using probability theory.
Key concepts:
- Conditional Probability: P(A|B) = P(A ∩ B) / P(B)
- Bayes' Theorem: P(A|B) = P(B|A) * P(A) / P(B)
- Independence: P(A ∩ B) = P(A) * P(B)
- Joint Probability: P(A, B, C) = P(A) * P(B|A) * P(C|A,B)

This implementation provides:
1. Conditional probability calculation
2. Bayes' Theorem application
3. Probability table management
4. Inference with uncertainty

Time Complexity: O(n) for probability lookups
Space Complexity: O(n) for probability storage
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict
from enum import Enum
import math

from ..models.state import State, ExperienceLevel, FitnessGoal
from ..models.action import Action, Difficulty


class ProbabilityType(Enum):
    """Types of probabilities."""
    MARGINAL = "marginal"  # P(A)
    CONDITIONAL = "conditional"  # P(A|B)
    JOINT = "joint"  # P(A, B)
    POSTERIOR = "posterior"  # P(A|B) via Bayes


@dataclass
class ConditionalProbability:
    """
    Represents a conditional probability P(event|evidence).
    
    Conditional probability is the likelihood of an event occurring
    given that another event has already occurred:
    P(A|B) = P(A ∩ B) / P(B)
    
    Attributes:
        event: The event we're computing probability for
        evidence: The condition/evidence given
        probability: The probability value (0.0-1.0)
        prob_type: Type of probability
        sample_count: Number of samples this is based on
        description: Human-readable description
    """
    event: Dict[str, Any]
    evidence: Optional[Dict[str, Any]] = None
    probability: float = 0.0
    prob_type: ProbabilityType = ProbabilityType.CONDITIONAL
    sample_count: int = 0
    description: str = ""
    
    def __str__(self) -> str:
        """String representation."""
        event_str = ", ".join(f"{k}={v}" for k, v in self.event.items())
        if self.evidence:
            evidence_str = ", ".join(f"{k}={v}" for k, v in self.evidence.items())
            return f"P({event_str} | {evidence_str}) = {self.probability:.4f}"
        else:
            return f"P({event_str}) = {self.probability:.4f}"


class ProbabilityCalculator:
    """
    Probabilistic Reasoning Engine.
    
    This calculator implements:
    1. Conditional Probability: P(A|B)
    2. Bayes' Theorem: P(A|B) = P(B|A) * P(A) / P(B)
    3. Joint Probability: P(A, B)
    4. Independence Testing
    5. Probability Tables
    
    Bayes' Theorem:
    --------------
    Used to update beliefs given new evidence:
    P(hypothesis|evidence) = P(evidence|hypothesis) * P(hypothesis) / P(evidence)
    
    Components:
    - Prior P(H): Initial belief before evidence
    - Likelihood P(E|H): Probability of evidence given hypothesis
    - Evidence P(E): Probability of observing the evidence
    - Posterior P(H|E): Updated belief after evidence
    
    Example in Workout Context:
    - H: User will succeed with difficult workout
    - E: User has high energy and no injuries
    - P(H|E): Updated probability of success given evidence
    
    Properties:
    - Handles uncertainty quantitatively
    - Updates beliefs with evidence
    - Provides probabilistic predictions
    - Explainable reasoning
    
    Use Cases in Workout System:
    - Predict workout success probability
    - Estimate injury risk
    - Calculate goal achievement likelihood
    - Update user skill estimates
    - Recommend exercises with confidence scores
    
    Time Complexity: O(n) for probability calculations
    Space Complexity: O(n) for probability storage
    """
    
    def __init__(self, name: str = "Probability Calculator"):
        """
        Initialize probability calculator.
        
        Args:
            name: Calculator name
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._name = name
        
        # Probability tables
        # Format: (event_key, evidence_key) → ConditionalProbability
        self._probabilities: Dict[Tuple[str, str], ConditionalProbability] = {}
        
        # Frequency counts for learning from data
        # Format: event_key → count
        self._event_counts: Dict[str, int] = defaultdict(int)
        self._total_observations = 0
        
        # Calculation log
        self._calculation_log: List[str] = []
    
    @property
    def probabilities(self) -> Dict[Tuple[str, str], ConditionalProbability]:
        """Get probability table."""
        return self._probabilities.copy()
    
    @property
    def calculation_log(self) -> List[str]:
        """Get calculation log."""
        return self._calculation_log.copy()
    
    def add_probability(self, prob: ConditionalProbability) -> None:
        """
        Add a conditional probability to the table.
        
        Args:
            prob: Conditional probability to add
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        event_key = self._dict_to_key(prob.event)
        evidence_key = self._dict_to_key(prob.evidence) if prob.evidence else ""
        
        self._probabilities[(event_key, evidence_key)] = prob
        self._calculation_log.append(f"Added: {prob}")
    
    def _dict_to_key(self, d: Optional[Dict[str, Any]]) -> str:
        """
        Convert dictionary to hashable key.
        
        Args:
            d: Dictionary to convert
            
        Returns:
            String key
            
        Time Complexity: O(k) where k is dict size
        Space Complexity: O(1)
        """
        if not d:
            return ""
        return "|".join(f"{k}:{v}" for k, v in sorted(d.items()))
    
    def observe_event(self, event: Dict[str, Any]) -> None:
        """
        Record observation of an event (for learning probabilities).
        
        Args:
            event: Event observed
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        event_key = self._dict_to_key(event)
        self._event_counts[event_key] += 1
        self._total_observations += 1
    
    def compute_marginal_probability(self, event: Dict[str, Any]) -> float:
        """
        Compute marginal probability P(event) from observations.
        
        P(A) = count(A) / total_observations
        
        Args:
            event: Event to compute probability for
            
        Returns:
            Marginal probability
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if self._total_observations == 0:
            return 0.0
        
        event_key = self._dict_to_key(event)
        count = self._event_counts.get(event_key, 0)
        probability = count / self._total_observations
        
        self._calculation_log.append(
            f"P({event}) = {count}/{self._total_observations} = {probability:.4f}"
        )
        
        return probability
    
    def get_conditional_probability(
        self,
        event: Dict[str, Any],
        evidence: Dict[str, Any]
    ) -> Optional[float]:
        """
        Get stored conditional probability P(event|evidence).
        
        Args:
            event: Event to query
            evidence: Given evidence
            
        Returns:
            Probability if stored, None otherwise
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        event_key = self._dict_to_key(event)
        evidence_key = self._dict_to_key(evidence)
        
        prob = self._probabilities.get((event_key, evidence_key))
        return prob.probability if prob else None
    
    def compute_conditional_probability(
        self,
        event: Dict[str, Any],
        evidence: Dict[str, Any],
        joint_count: int,
        evidence_count: int
    ) -> ConditionalProbability:
        """
        Compute conditional probability from counts.
        
        P(A|B) = count(A and B) / count(B)
        
        Args:
            event: Event to compute probability for
            evidence: Given evidence
            joint_count: Number of times event and evidence both occurred
            evidence_count: Number of times evidence occurred
            
        Returns:
            Conditional probability object
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if evidence_count == 0:
            probability = 0.0
        else:
            probability = joint_count / evidence_count
        
        cond_prob = ConditionalProbability(
            event=event,
            evidence=evidence,
            probability=probability,
            prob_type=ProbabilityType.CONDITIONAL,
            sample_count=evidence_count,
            description=f"Computed from {joint_count} joint occurrences out of {evidence_count}"
        )
        
        self.add_probability(cond_prob)
        
        return cond_prob
    
    def bayes_theorem(
        self,
        hypothesis: Dict[str, Any],
        evidence: Dict[str, Any],
        likelihood: Optional[float] = None,
        prior: Optional[float] = None,
        evidence_prob: Optional[float] = None
    ) -> ConditionalProbability:
        """
        Apply Bayes' Theorem to compute posterior probability.
        
        Bayes' Theorem:
        P(H|E) = P(E|H) * P(H) / P(E)
        
        Where:
        - H: Hypothesis
        - E: Evidence
        - P(H|E): Posterior (what we want)
        - P(E|H): Likelihood (probability of evidence given hypothesis)
        - P(H): Prior (initial belief in hypothesis)
        - P(E): Evidence probability (normalization constant)
        
        Args:
            hypothesis: Hypothesis to evaluate
            evidence: Observed evidence
            likelihood: P(evidence|hypothesis) - if None, will try to look up
            prior: P(hypothesis) - if None, will compute from observations
            evidence_prob: P(evidence) - if None, will compute from observations
            
        Returns:
            Posterior probability P(hypothesis|evidence)
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        # Get or compute likelihood P(E|H)
        if likelihood is None:
            likelihood = self.get_conditional_probability(evidence, hypothesis)
            if likelihood is None:
                raise ValueError(
                    f"Likelihood P({evidence}|{hypothesis}) not available. "
                    "Please provide it or add it to probability table."
                )
        
        # Get or compute prior P(H)
        if prior is None:
            prior = self.compute_marginal_probability(hypothesis)
            if prior == 0.0:
                self._calculation_log.append(
                    f"Warning: Prior P({hypothesis}) = 0, using small value 0.01"
                )
                prior = 0.01  # Smoothing
        
        # Get or compute evidence probability P(E)
        if evidence_prob is None:
            evidence_prob = self.compute_marginal_probability(evidence)
            if evidence_prob == 0.0:
                self._calculation_log.append(
                    f"Warning: Evidence P({evidence}) = 0, using small value 0.01"
                )
                evidence_prob = 0.01  # Smoothing
        
        # Apply Bayes' Theorem
        posterior = (likelihood * prior) / evidence_prob
        
        # Create posterior probability object
        posterior_prob = ConditionalProbability(
            event=hypothesis,
            evidence=evidence,
            probability=posterior,
            prob_type=ProbabilityType.POSTERIOR,
            description=(
                f"Bayes: P(E|H)={likelihood:.4f} * P(H)={prior:.4f} / P(E)={evidence_prob:.4f}"
            )
        )
        
        self._calculation_log.append(
            f"Bayes' Theorem: P({hypothesis}|{evidence}) = "
            f"{likelihood:.4f} * {prior:.4f} / {evidence_prob:.4f} = {posterior:.4f}"
        )
        
        self.add_probability(posterior_prob)
        
        return posterior_prob
    
    def compute_joint_probability(
        self,
        events: List[Dict[str, Any]]
    ) -> float:
        """
        Compute joint probability P(A, B, C, ...) assuming independence.
        
        If events are independent:
        P(A, B, C) = P(A) * P(B) * P(C)
        
        Args:
            events: List of events
            
        Returns:
            Joint probability
            
        Time Complexity: O(n) where n is number of events
        Space Complexity: O(1)
        """
        joint_prob = 1.0
        
        for event in events:
            marginal = self.compute_marginal_probability(event)
            joint_prob *= marginal
        
        self._calculation_log.append(
            f"Joint probability (assuming independence): {joint_prob:.4f}"
        )
        
        return joint_prob
    
    def are_independent(
        self,
        event_a: Dict[str, Any],
        event_b: Dict[str, Any],
        tolerance: float = 0.01
    ) -> bool:
        """
        Test if two events are independent.
        
        Events A and B are independent if:
        P(A, B) = P(A) * P(B)
        
        Equivalently:
        P(A|B) = P(A)
        
        Args:
            event_a: First event
            event_b: Second event
            tolerance: Tolerance for floating point comparison
            
        Returns:
            True if independent, False otherwise
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        # Method 1: Check if P(A|B) ≈ P(A)
        prob_a = self.compute_marginal_probability(event_a)
        prob_a_given_b = self.get_conditional_probability(event_a, event_b)
        
        if prob_a_given_b is not None:
            independent = abs(prob_a_given_b - prob_a) < tolerance
            
            self._calculation_log.append(
                f"Independence test: P(A)={prob_a:.4f}, P(A|B)={prob_a_given_b:.4f}, "
                f"Independent={independent}"
            )
            
            return independent
        
        self._calculation_log.append("Cannot test independence: P(A|B) not available")
        return False
    
    def normalize_probabilities(
        self,
        probabilities: List[ConditionalProbability]
    ) -> List[ConditionalProbability]:
        """
        Normalize a list of probabilities to sum to 1.0.
        
        Used when we have un-normalized posterior probabilities.
        
        Args:
            probabilities: List of probabilities to normalize
            
        Returns:
            Normalized probabilities
            
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        total = sum(p.probability for p in probabilities)
        
        if total == 0:
            return probabilities
        
        normalized = []
        for prob in probabilities:
            normalized_value = prob.probability / total
            normalized_prob = ConditionalProbability(
                event=prob.event,
                evidence=prob.evidence,
                probability=normalized_value,
                prob_type=prob.prob_type,
                sample_count=prob.sample_count,
                description=f"Normalized: {prob.description}"
            )
            normalized.append(normalized_prob)
        
        self._calculation_log.append(f"Normalized {len(probabilities)} probabilities")
        
        return normalized
    
    def entropy(self, probabilities: List[float]) -> float:
        """
        Compute entropy (measure of uncertainty).
        
        H(X) = -Σ P(x) * log₂(P(x))
        
        High entropy = high uncertainty
        Low entropy = low uncertainty
        
        Args:
            probabilities: List of probabilities
            
        Returns:
            Entropy value
            
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        entropy_value = 0.0
        
        for p in probabilities:
            if p > 0:  # log(0) is undefined
                entropy_value -= p * math.log2(p)
        
        self._calculation_log.append(f"Entropy: {entropy_value:.4f}")
        
        return entropy_value
    
    def reset(self) -> None:
        """
        Reset calculator (clear probabilities and observations).
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._probabilities.clear()
        self._event_counts.clear()
        self._total_observations = 0
        self._calculation_log.clear()
    
    @staticmethod
    def create_workout_calculator() -> 'ProbabilityCalculator':
        """
        Create a probability calculator with workout probabilities.
        
        Returns:
            Configured ProbabilityCalculator
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        calc = ProbabilityCalculator("Workout Probability Calculator")
        
        # Add some example probabilities
        
        # P(success | high_energy)
        calc.add_probability(ConditionalProbability(
            event={"outcome": "success"},
            evidence={"energy": "high"},
            probability=0.85,
            description="High energy leads to successful workout"
        ))
        
        # P(success | low_energy)
        calc.add_probability(ConditionalProbability(
            event={"outcome": "success"},
            evidence={"energy": "low"},
            probability=0.40,
            description="Low energy reduces workout success"
        ))
        
        # P(injury | difficulty=advanced, experience=beginner)
        calc.add_probability(ConditionalProbability(
            event={"injury": True},
            evidence={"difficulty": "advanced", "experience": "beginner"},
            probability=0.30,
            description="Beginners doing advanced exercises risk injury"
        ))
        
        # P(injury | difficulty=beginner, experience=beginner)
        calc.add_probability(ConditionalProbability(
            event={"injury": True},
            evidence={"difficulty": "beginner", "experience": "beginner"},
            probability=0.05,
            description="Appropriate difficulty minimizes injury risk"
        ))
        
        # P(goal_achieved | consistent_training)
        calc.add_probability(ConditionalProbability(
            event={"goal": "achieved"},
            evidence={"consistency": "high"},
            probability=0.75,
            description="Consistent training increases goal achievement"
        ))
        
        return calc
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get calculator statistics.
        
        Returns:
            Dictionary with statistics
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return {
            "name": self._name,
            "total_probabilities": len(self._probabilities),
            "total_observations": self._total_observations,
            "unique_events": len(self._event_counts),
            "calculation_steps": len(self._calculation_log)
        }
    
    def __str__(self) -> str:
        """String representation."""
        return (
            f"ProbabilityCalculator(name={self._name}, "
            f"probabilities={len(self._probabilities)})"
        )


# Example usage and testing
if __name__ == "__main__":
    print("Probabilistic Reasoning Engine")
    print("==============================")
    print()
    
    # Create calculator
    calc = ProbabilityCalculator.create_workout_calculator()
    
    print(f"Stored probabilities: {len(calc.probabilities)}")
    print("\nProbabilities:")
    for prob in calc.probabilities.values():
        print(f"  {prob}")
    
    # Test Bayes' Theorem
    print("\n--- Bayes' Theorem Example ---")
    hypothesis = {"skill_level": "advanced"}
    evidence = {"performance": "excellent"}
    
    # Add required probabilities
    calc.add_probability(ConditionalProbability(
        event=evidence,
        evidence=hypothesis,
        probability=0.80,  # P(excellent_performance | advanced_skill)
        description="Advanced users perform excellently"
    ))
    
    # Record some observations
    for _ in range(30):
        calc.observe_event(hypothesis)
    for _ in range(100):
        calc.observe_event({"skill_level": "beginner"})
    for _ in range(20):
        calc.observe_event(evidence)
    
    # Apply Bayes
    posterior = calc.bayes_theorem(hypothesis, evidence)
    print(f"\n{posterior}")
