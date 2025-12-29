"""
Reasoning Explainer Service.

This service generates human-readable explanations of AI reasoning
processes and decisions.

Explanation Types:
- Deductive reasoning chains
- Inductive pattern discoveries
- Probabilistic calculations
- Search algorithm paths
- Agent decision logic
- Heuristic evaluations

Features:
- Natural language generation
- Step-by-step reasoning traces
- Visual explanation support
- Multi-level detail (summary, detailed, technical)
- Context-aware explanations

Time Complexity: O(n) for explanation generation
Space Complexity: O(n) for storing explanation text
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from ..domain.reasoning.deductive_reasoner import DeductiveReasoner, Fact, Rule
from ..domain.reasoning.inductive_reasoner import InductiveReasoner, Pattern
from ..domain.reasoning.probability_calculator import ProbabilityCalculator, ConditionalProbability
from ..domain.reasoning.heuristic_function import HeuristicFunction, HeuristicResult
from ..domain.agents.agent import Agent, AgentAction
from ..domain.search.search_problem import SearchSolution
from ..domain.models.workout_plan import WorkoutPlan


class ExplanationType(Enum):
    """Type of explanation."""
    DEDUCTIVE = "deductive"  # Rule-based reasoning
    INDUCTIVE = "inductive"  # Pattern learning
    PROBABILISTIC = "probabilistic"  # Probability calculations
    SEARCH = "search"  # Search algorithm
    AGENT = "agent"  # Agent decision
    HEURISTIC = "heuristic"  # Heuristic evaluation
    PLAN = "plan"  # Workout plan
    SUMMARY = "summary"  # Overall summary


class DetailLevel(Enum):
    """Level of explanation detail."""
    BRIEF = "brief"  # One-sentence summary
    SUMMARY = "summary"  # Key points only
    DETAILED = "detailed"  # Full explanation
    TECHNICAL = "technical"  # Technical details


@dataclass
class Explanation:
    """
    An explanation of reasoning or decision.
    
    Attributes:
        explanation_type: Type of explanation
        title: Explanation title
        content: Main explanation text
        details: Additional details
        reasoning_steps: Step-by-step reasoning
        confidence: Confidence in explanation (0.0-1.0)
        detail_level: Level of detail
        metadata: Additional metadata
        timestamp: When explanation was generated
    """
    explanation_type: ExplanationType
    title: str
    content: str
    details: List[str] = field(default_factory=list)
    reasoning_steps: List[str] = field(default_factory=list)
    confidence: float = 1.0
    detail_level: DetailLevel = DetailLevel.SUMMARY
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "type": self.explanation_type.value,
            "title": self.title,
            "content": self.content,
            "details": self.details,
            "reasoning_steps": self.reasoning_steps,
            "confidence": self.confidence,
            "detail_level": self.detail_level.value,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat()
        }
    
    def to_markdown(self) -> str:
        """Convert to Markdown format."""
        lines = [
            f"## {self.title}",
            "",
            self.content,
            ""
        ]
        
        if self.reasoning_steps:
            lines.append("### Reasoning Steps:")
            for i, step in enumerate(self.reasoning_steps, 1):
                lines.append(f"{i}. {step}")
            lines.append("")
        
        if self.details:
            lines.append("### Details:")
            for detail in self.details:
                lines.append(f"- {detail}")
            lines.append("")
        
        if self.confidence < 1.0:
            lines.append(f"*Confidence: {self.confidence:.1%}*")
        
        return "\n".join(lines)


class ReasoningExplainer:
    """
    Service for generating explanations of AI reasoning.
    
    This explainer creates human-readable explanations of:
    1. How decisions were made
    2. Why certain options were chosen
    3. What reasoning was applied
    4. How algorithms worked
    5. What factors were considered
    
    Explanation Generation Process:
    1. Analyze reasoning artifacts (rules, patterns, probabilities)
    2. Extract key decision points
    3. Generate natural language descriptions
    4. Organize into logical flow
    5. Add context and examples
    6. Format for presentation
    
    Design Principles:
    - Transparency: Show how AI works
    - Clarity: Use plain language
    - Completeness: Cover all important factors
    - Relevance: Focus on user needs
    - Honesty: Acknowledge limitations
    
    Example Usage:
    ```python
    explainer = ReasoningExplainer()
    
    # Explain deductive reasoning
    explanation = explainer.explain_deductive_reasoning(
        reasoner=deductive_reasoner,
        detail_level=DetailLevel.DETAILED
    )
    
    print(explanation.to_markdown())
    ```
    
    Time Complexity: O(n) where n is complexity of reasoning
    Space Complexity: O(n) for explanation storage
    """
    
    def __init__(self, name: str = "Reasoning Explainer"):
        """
        Initialize explainer.
        
        Args:
            name: Explainer name
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._name = name
        self._explanations_generated = 0
    
    @property
    def name(self) -> str:
        """Get explainer name."""
        return self._name
    
    def explain_deductive_reasoning(
        self,
        reasoner: DeductiveReasoner,
        detail_level: DetailLevel = DetailLevel.SUMMARY
    ) -> Explanation:
        """
        Explain deductive reasoning process.
        
        Args:
            reasoner: Deductive reasoner to explain
            detail_level: Level of detail
            
        Returns:
            Explanation of deductive reasoning
            
        Time Complexity: O(f + r) where f=facts, r=rules
        Space Complexity: O(f + r)
        """
        # Get reasoning chain
        chain = reasoner.reasoning_chain
        facts = reasoner.facts
        rules = reasoner.rules
        
        # Build content
        if detail_level == DetailLevel.BRIEF:
            content = f"Applied {len(rules)} safety rules and derived {len(facts)} facts through logical inference."
        else:
            content = (
                f"The system applied deductive reasoning using {len(rules)} rules "
                f"to analyze your fitness profile. Starting with {sum(1 for f in facts if f.source == 'user')} "
                f"initial facts about your experience, goals, and constraints, "
                f"it derived {len(facts) - sum(1 for f in facts if f.source == 'user')} "
                f"additional insights through logical inference."
            )
        
        # Extract reasoning steps
        steps = []
        if detail_level in [DetailLevel.DETAILED, DetailLevel.TECHNICAL]:
            for entry in chain[:10]:  # Limit to 10 steps
                if "Applied rule" in entry:
                    steps.append(entry)
        
        # Extract details
        details = []
        if detail_level == DetailLevel.TECHNICAL:
            for rule in rules[:5]:
                details.append(f"Rule {rule.rule_id}: {rule.description}")
        
        explanation = Explanation(
            explanation_type=ExplanationType.DEDUCTIVE,
            title="Safety & Feasibility Analysis",
            content=content,
            details=details,
            reasoning_steps=steps,
            detail_level=detail_level,
            metadata={
                "total_facts": len(facts),
                "total_rules": len(rules),
                "inference_iterations": len([e for e in chain if "iteration" in e.lower()])
            }
        )
        
        self._explanations_generated += 1
        return explanation
    
    def explain_inductive_reasoning(
        self,
        reasoner: InductiveReasoner,
        detail_level: DetailLevel = DetailLevel.SUMMARY
    ) -> Explanation:
        """
        Explain inductive reasoning (pattern learning).
        
        Args:
            reasoner: Inductive reasoner to explain
            detail_level: Level of detail
            
        Returns:
            Explanation of inductive reasoning
            
        Time Complexity: O(p) where p=patterns
        Space Complexity: O(p)
        """
        patterns = reasoner.patterns
        examples = reasoner.examples
        
        # Build content
        if detail_level == DetailLevel.BRIEF:
            content = f"Learned {len(patterns)} workout patterns from {len(examples)} past examples."
        else:
            content = (
                f"The system learned from {len(examples)} historical workout examples "
                f"to discover {len(patterns)} patterns about what works best. "
                f"These patterns help predict which exercises are most effective "
                f"for users with similar profiles and goals."
            )
        
        # Extract top patterns
        steps = []
        if detail_level in [DetailLevel.DETAILED, DetailLevel.TECHNICAL]:
            sorted_patterns = sorted(patterns, key=lambda p: p.confidence, reverse=True)
            for pattern in sorted_patterns[:5]:
                steps.append(
                    f"Pattern: {pattern.description} (confidence: {pattern.confidence:.1%})"
                )
        
        explanation = Explanation(
            explanation_type=ExplanationType.INDUCTIVE,
            title="Pattern Learning from Experience",
            content=content,
            reasoning_steps=steps,
            detail_level=detail_level,
            metadata={
                "total_patterns": len(patterns),
                "total_examples": len(examples),
                "average_confidence": sum(p.confidence for p in patterns) / len(patterns) if patterns else 0
            }
        )
        
        self._explanations_generated += 1
        return explanation
    
    def explain_probabilistic_reasoning(
        self,
        calculator: ProbabilityCalculator,
        success_probability: float,
        detail_level: DetailLevel = DetailLevel.SUMMARY
    ) -> Explanation:
        """
        Explain probabilistic reasoning.
        
        Args:
            calculator: Probability calculator to explain
            success_probability: Predicted success probability
            detail_level: Level of detail
            
        Returns:
            Explanation of probabilistic reasoning
            
        Time Complexity: O(c) where c=calculations
        Space Complexity: O(c)
        """
        calc_log = calculator.calculation_log
        
        # Build content
        if detail_level == DetailLevel.BRIEF:
            content = f"Success probability: {success_probability:.1%}"
        else:
            content = (
                f"Based on probabilistic analysis, there is a {success_probability:.1%} "
                f"chance of successfully completing this workout. This prediction considers "
                f"your energy level, experience match with exercise difficulty, "
                f"and injury status using conditional probability calculations."
            )
        
        # Extract calculation steps
        steps = []
        if detail_level in [DetailLevel.DETAILED, DetailLevel.TECHNICAL]:
            for entry in calc_log[-5:]:  # Last 5 calculations
                steps.append(entry)
        
        explanation = Explanation(
            explanation_type=ExplanationType.PROBABILISTIC,
            title="Success Probability Prediction",
            content=content,
            reasoning_steps=steps,
            confidence=success_probability,
            detail_level=detail_level,
            metadata={
                "success_probability": success_probability,
                "calculations_performed": len(calc_log)
            }
        )
        
        self._explanations_generated += 1
        return explanation
    
    def explain_search_algorithm(
        self,
        search_result: SearchSolution,
        detail_level: DetailLevel = DetailLevel.SUMMARY
    ) -> Explanation:
        """
        Explain search algorithm process.
        
        Args:
            search_result: Search result to explain
            detail_level: Level of detail
            
        Returns:
            Explanation of search process
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        # Build content
        if detail_level == DetailLevel.BRIEF:
            content = f"Explored {search_result.nodes_expanded} workout combinations using A* search."
        else:
            content = (
                f"The system used A* search algorithm to find the optimal workout plan. "
                f"It explored {search_result.nodes_expanded} possible combinations, "
                f"searching to a maximum depth of {search_result.max_depth} exercises. "
                f"The algorithm used a heuristic function to guide the search toward "
                f"exercises that best match your goals, resulting in a plan with "
                f"total cost of {search_result.path_cost:.1f}."
            )
        
        # Extract steps
        steps = []
        if detail_level in [DetailLevel.DETAILED, DetailLevel.TECHNICAL]:
            steps.append(f"Algorithm: A* Search (informed search)")
            steps.append(f"Nodes expanded: {search_result.nodes_expanded}")
            steps.append(f"Maximum depth: {search_result.max_depth}")
            steps.append(f"Path cost: {search_result.path_cost:.2f}")
            steps.append(f"Search time: {search_result.search_time:.3f}s")
        
        explanation = Explanation(
            explanation_type=ExplanationType.SEARCH,
            title="Workout Plan Search Process",
            content=content,
            reasoning_steps=steps,
            detail_level=detail_level,
            metadata={
                "nodes_expanded": search_result.nodes_expanded,
                "max_depth": search_result.max_depth,
                "path_cost": search_result.path_cost,
                "search_time": search_result.search_time
            }
        )
        
        self._explanations_generated += 1
        return explanation
    
    def explain_agent_decision(
        self,
        agent: Agent,
        action: Optional[AgentAction] = None,
        detail_level: DetailLevel = DetailLevel.SUMMARY
    ) -> Explanation:
        """
        Explain agent decision-making.
        
        Args:
            agent: Agent to explain
            action: Specific action to explain
            detail_level: Level of detail
            
        Returns:
            Explanation of agent decision
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        agent_stats = agent.get_statistics()
        
        # Build content
        if detail_level == DetailLevel.BRIEF:
            content = f"{agent.name} made recommendations based on {agent_stats['decisions_made']} decisions."
        else:
            content = (
                f"The {agent.name} analyzed your profile and made personalized recommendations. "
                f"This agent type uses {self._describe_agent_type(agent)} to select exercises. "
                f"It has made {agent_stats['decisions_made']} decisions with an average "
                f"confidence of {agent_stats['average_confidence']:.1%}."
            )
        
        # Add action-specific reasoning
        steps = []
        if action and detail_level in [DetailLevel.DETAILED, DetailLevel.TECHNICAL]:
            steps.append(f"Decision: {action.action_type}")
            steps.append(f"Confidence: {action.confidence:.1%}")
            if action.reasoning:
                steps.append(f"Reasoning: {action.reasoning}")
        
        explanation = Explanation(
            explanation_type=ExplanationType.AGENT,
            title="AI Agent Decision Making",
            content=content,
            reasoning_steps=steps,
            confidence=action.confidence if action else 1.0,
            detail_level=detail_level,
            metadata=agent_stats
        )
        
        self._explanations_generated += 1
        return explanation
    
    def explain_workout_plan(
        self,
        workout_plan: WorkoutPlan,
        detail_level: DetailLevel = DetailLevel.SUMMARY
    ) -> Explanation:
        """
        Explain workout plan composition.
        
        Args:
            workout_plan: Workout plan to explain
            detail_level: Level of detail
            
        Returns:
            Explanation of workout plan
            
        Time Complexity: O(e) where e=exercises
        Space Complexity: O(e)
        """
        exercises = workout_plan.exercises
        
        # Build content
        if detail_level == DetailLevel.BRIEF:
            content = f"{len(exercises)} exercises, {workout_plan.total_duration_minutes} minutes, {workout_plan.total_calories:.0f} calories"
        else:
            goal_value = workout_plan.fitness_goal.value if hasattr(workout_plan.fitness_goal, 'value') else str(workout_plan.fitness_goal)
            content = (
                f"This {workout_plan.total_duration_minutes}-minute workout includes "
                f"{len(exercises)} carefully selected exercises targeting your "
                f"{goal_value} goal. The plan is designed for "
                f"{workout_plan.difficulty_level} level and will burn approximately "
                f"{workout_plan.total_calories:.0f} calories."
            )
        
        # Exercise breakdown
        details = []
        if detail_level in [DetailLevel.DETAILED, DetailLevel.TECHNICAL]:
            for ex_in_plan in exercises:
                exercise = ex_in_plan.exercise
                details.append(
                    f"{exercise.name}: {exercise.duration_minutes}min, "
                    f"{exercise.category.value}, {exercise.difficulty}"
                )
        
        goal_value = workout_plan.fitness_goal.value if hasattr(workout_plan.fitness_goal, 'value') else str(workout_plan.fitness_goal)
        explanation = Explanation(
            explanation_type=ExplanationType.PLAN,
            title=f"Workout Plan {workout_plan.plan_id}",
            content=content,
            details=details,
            detail_level=detail_level,
            metadata={
                "total_exercises": len(exercises),
                "total_duration": workout_plan.total_duration_minutes,
                "total_calories": workout_plan.total_calories,
                "difficulty": workout_plan.difficulty_level,
                "goal": goal_value
            }
        )
        
        self._explanations_generated += 1
        return explanation
    
    def create_comprehensive_explanation(
        self,
        deductive_reasoner: Optional[DeductiveReasoner] = None,
        inductive_reasoner: Optional[InductiveReasoner] = None,
        probability_calculator: Optional[ProbabilityCalculator] = None,
        search_result: Optional[SearchSolution] = None,
        agent: Optional[Agent] = None,
        workout_plan: Optional[WorkoutPlan] = None,
        success_probability: float = 0.0,
        detail_level: DetailLevel = DetailLevel.SUMMARY
    ) -> List[Explanation]:
        """
        Create comprehensive explanation covering all reasoning.
        
        Args:
            deductive_reasoner: Deductive reasoner (optional)
            inductive_reasoner: Inductive reasoner (optional)
            probability_calculator: Probability calculator (optional)
            search_result: Search result (optional)
            agent: Agent (optional)
            workout_plan: Workout plan (optional)
            success_probability: Success probability
            detail_level: Level of detail
            
        Returns:
            List of explanations
            
        Time Complexity: O(n) where n is components
        Space Complexity: O(n)
        """
        explanations = []
        
        # Summary explanation
        if detail_level != DetailLevel.BRIEF:
            summary = self._create_summary_explanation(
                has_deductive=deductive_reasoner is not None,
                has_inductive=inductive_reasoner is not None,
                has_probabilistic=probability_calculator is not None,
                has_search=search_result is not None,
                has_agent=agent is not None,
                detail_level=detail_level
            )
            explanations.append(summary)
        
        # Component explanations
        if deductive_reasoner:
            explanations.append(self.explain_deductive_reasoning(deductive_reasoner, detail_level))
        
        if inductive_reasoner:
            explanations.append(self.explain_inductive_reasoning(inductive_reasoner, detail_level))
        
        if probability_calculator:
            explanations.append(self.explain_probabilistic_reasoning(
                probability_calculator, success_probability, detail_level
            ))
        
        if search_result:
            explanations.append(self.explain_search_algorithm(search_result, detail_level))
        
        if agent:
            explanations.append(self.explain_agent_decision(agent, None, detail_level))
        
        if workout_plan:
            explanations.append(self.explain_workout_plan(workout_plan, detail_level))
        
        return explanations
    
    def _create_summary_explanation(
        self,
        has_deductive: bool,
        has_inductive: bool,
        has_probabilistic: bool,
        has_search: bool,
        has_agent: bool,
        detail_level: DetailLevel
    ) -> Explanation:
        """Create overall summary explanation."""
        components_used = []
        if has_deductive:
            components_used.append("deductive reasoning (rule-based safety)")
        if has_inductive:
            components_used.append("inductive learning (pattern discovery)")
        if has_probabilistic:
            components_used.append("probabilistic analysis (success prediction)")
        if has_search:
            components_used.append("A* search (plan optimization)")
        if has_agent:
            components_used.append("intelligent agent (decision making)")
        
        content = (
            f"This workout recommendation was generated using {len(components_used)} "
            f"AI techniques: {', '.join(components_used)}. Each component analyzed "
            f"different aspects of your fitness profile to create a personalized, "
            f"safe, and effective workout plan."
        )
        
        return Explanation(
            explanation_type=ExplanationType.SUMMARY,
            title="How Your Workout Was Generated",
            content=content,
            detail_level=detail_level,
            metadata={"components_count": len(components_used)}
        )
    
    def _describe_agent_type(self, agent: Agent) -> str:
        """Get description of agent type."""
        agent_name = agent.name.lower()
        
        if "utility" in agent_name:
            return "multi-objective optimization to balance safety, effectiveness, and variety"
        elif "learning" in agent_name:
            return "reinforcement learning to improve recommendations over time"
        elif "goal" in agent_name:
            return "goal-based planning with A* search"
        elif "model" in agent_name:
            return "internal world model tracking your progress"
        elif "reflex" in agent_name:
            return "safety rules to ensure appropriate exercises"
        else:
            return "advanced decision-making algorithms"
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get explainer statistics.
        
        Returns:
            Statistics dictionary
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return {
            "name": self._name,
            "explanations_generated": self._explanations_generated
        }
    
    def __str__(self) -> str:
        """String representation."""
        return f"ReasoningExplainer(explanations_generated={self._explanations_generated})"


# Example usage
if __name__ == "__main__":
    print("Reasoning Explainer Service")
    print("===========================")
    print()
    
    explainer = ReasoningExplainer()
    
    # Create sample deductive reasoner
    reasoner = DeductiveReasoner.create_workout_reasoner()
    from ..domain.reasoning.deductive_reasoner import Fact, FactType
    
    reasoner.add_fact(Fact(
        predicate="experience_level",
        arguments={"level": "beginner"},
        fact_type=FactType.USER_ATTRIBUTE
    ))
    reasoner.infer()
    
    # Generate explanation
    explanation = explainer.explain_deductive_reasoning(
        reasoner,
        detail_level=DetailLevel.DETAILED
    )
    
    print(explanation.to_markdown())
