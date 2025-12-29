"""
Abstract base class for intelligent agents.

This module defines the Agent interface and supporting classes for the
agent-based architecture in the workout recommendation system.

An agent is anything that can perceive its environment through sensors
and act upon that environment through actuators (Russell & Norvig).

Time Complexity: Depends on concrete implementation
Space Complexity: Depends on concrete implementation
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum

from ..models.state import State
from ..models.action import Action


class AgentType(Enum):
    """Types of intelligent agents."""
    SIMPLE_REFLEX = "Simple Reflex Agent"
    MODEL_BASED = "Model-Based Reflex Agent"
    GOAL_BASED = "Goal-Based Agent"
    UTILITY_BASED = "Utility-Based Agent"
    LEARNING = "Learning Agent"


@dataclass
class Percept:
    """
    A percept is the agent's perceptual input at any given instant.
    
    In our workout system, percepts include:
    - Current user state (fitness level, goals, constraints)
    - Environmental factors (equipment availability, time)
    - Feedback from previous actions
    
    Attributes:
        state: Current user fitness state
        timestamp: When the percept was created
        available_equipment: List of available equipment
        time_available_minutes: Available workout time
        energy_level: User's current energy (0.0-1.0)
        previous_action_feedback: Feedback from last action
        environmental_data: Additional environmental information
    """
    state: State
    timestamp: datetime = field(default_factory=datetime.now)
    available_equipment: List[str] = field(default_factory=list)
    time_available_minutes: int = 60
    energy_level: float = 1.0
    previous_action_feedback: Optional[Dict[str, Any]] = None
    environmental_data: Dict[str, Any] = field(default_factory=dict)
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return (
            f"Percept(state={self.state.experience_level.value}, "
            f"time={self.time_available_minutes}min, "
            f"energy={self.energy_level:.2f})"
        )


@dataclass
class AgentAction:
    """
    An action is what the agent does in response to percepts.
    
    Attributes:
        action: The recommended action (exercise/workout)
        confidence: Confidence in this action (0.0-1.0)
        reasoning: Explanation for why this action was chosen
        metadata: Additional action information
        timestamp: When the action was decided
    """
    action: Action
    confidence: float = 1.0
    reasoning: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return (
            f"AgentAction(action={self.action.name}, "
            f"confidence={self.confidence:.2f})"
        )


class Agent(ABC):
    """
    Abstract base class for all intelligent agents.
    
    An agent perceives its environment through sensors (percepts) and
    acts upon the environment through actuators (actions). The agent
    function maps percept sequences to actions.
    
    Agent = Architecture + Program
    - Architecture: Physical structure (sensors, actuators, computing)
    - Program: Agent function implementation
    
    Key Properties:
    - Autonomy: Operates without human intervention
    - Reactivity: Responds to changes in environment
    - Pro-activeness: Takes initiative to achieve goals
    - Social ability: Interacts with other agents/users
    
    Time Complexity: Depends on concrete implementation
    Space Complexity: Depends on concrete implementation
    """
    
    def __init__(self, agent_type: AgentType, name: str = ""):
        """
        Initialize the agent.
        
        Args:
            agent_type: Type of agent (reflex, model-based, etc.)
            name: Optional name for the agent
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._agent_type = agent_type
        self._name = name or agent_type.value
        self._percept_history: List[Percept] = []
        self._action_history: List[AgentAction] = []
        self._created_at = datetime.now()
        self._performance_score = 0.0
    
    @property
    def agent_type(self) -> AgentType:
        """Get the agent type."""
        return self._agent_type
    
    @property
    def name(self) -> str:
        """Get the agent name."""
        return self._name
    
    @property
    def percept_history(self) -> List[Percept]:
        """Get the history of percepts received."""
        return self._percept_history
    
    @property
    def action_history(self) -> List[AgentAction]:
        """Get the history of actions taken."""
        return self._action_history
    
    @property
    def performance_score(self) -> float:
        """Get the current performance score."""
        return self._performance_score
    
    @abstractmethod
    def perceive(self, percept: Percept) -> None:
        """
        Process a percept from the environment.
        
        This method updates the agent's internal state based on
        the received percept. Different agent types process percepts
        differently:
        - Simple reflex: Ignores history
        - Model-based: Updates internal model
        - Goal-based: Evaluates progress toward goals
        - Utility-based: Updates utility estimates
        - Learning: Stores for learning
        
        Args:
            percept: The current percept from environment
            
        Time Complexity: Depends on implementation
        Space Complexity: Depends on implementation
        """
        pass
    
    @abstractmethod
    def decide_action(self, percept: Percept) -> AgentAction:
        """
        Decide what action to take based on the current percept.
        
        This is the core agent function that maps percepts to actions.
        Different agent architectures make decisions differently:
        - Simple reflex: Rule-based reaction
        - Model-based: Uses internal state model
        - Goal-based: Plans to achieve goals
        - Utility-based: Maximizes expected utility
        - Learning: Uses learned knowledge
        
        Args:
            percept: The current percept
            
        Returns:
            The action to take
            
        Time Complexity: Depends on implementation
        Space Complexity: Depends on implementation
        """
        pass
    
    def act(self, percept: Percept) -> AgentAction:
        """
        Complete agent cycle: perceive → decide → act.
        
        This is the main agent loop that:
        1. Processes the percept
        2. Decides what action to take
        3. Records the action
        4. Returns the action
        
        Args:
            percept: The current percept from environment
            
        Returns:
            The action decided by the agent
            
        Time Complexity: O(perceive) + O(decide_action)
        Space Complexity: O(1) plus history storage
        """
        # Store percept in history
        self._percept_history.append(percept)
        
        # Process percept (updates internal state)
        self.perceive(percept)
        
        # Decide action based on percept
        action = self.decide_action(percept)
        
        # Store action in history
        self._action_history.append(action)
        
        return action
    
    def update_performance(self, score_delta: float) -> None:
        """
        Update the agent's performance score.
        
        Performance measures how well the agent is doing at achieving
        its objectives. This can be based on:
        - User satisfaction
        - Goal achievement
        - Efficiency metrics
        - Safety compliance
        
        Args:
            score_delta: Change in performance score (can be negative)
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._performance_score += score_delta
    
    def reset(self) -> None:
        """
        Reset the agent to initial state.
        
        Clears history and resets internal state. Useful for
        starting a new interaction or testing.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._percept_history.clear()
        self._action_history.clear()
        self._performance_score = 0.0
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get agent statistics and metrics.
        
        Returns:
            Dictionary of statistics
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return {
            "agent_type": self._agent_type.value,
            "name": self._name,
            "percepts_received": len(self._percept_history),
            "actions_taken": len(self._action_history),
            "performance_score": self._performance_score,
            "uptime_seconds": (datetime.now() - self._created_at).total_seconds(),
            "avg_confidence": (
                sum(a.confidence for a in self._action_history) / len(self._action_history)
                if self._action_history else 0.0
            )
        }
    
    def __str__(self) -> str:
        """String representation of the agent."""
        return f"{self._name} (percepts={len(self._percept_history)}, actions={len(self._action_history)})"
    
    def __repr__(self) -> str:
        """Detailed representation."""
        return (
            f"Agent(type={self._agent_type.value}, "
            f"performance={self._performance_score:.2f})"
        )


# Agent performance measurement

def measure_agent_performance(
    agent: Agent,
    environment_sequences: List[List[Percept]],
    performance_metric: callable
) -> float:
    """
    Measure agent performance across multiple environment sequences.
    
    Args:
        agent: The agent to evaluate
        environment_sequences: List of percept sequences (episodes)
        performance_metric: Function that calculates performance score
        
    Returns:
        Average performance score across all sequences
        
    Time Complexity: O(n * m) where n=sequences, m=percepts per sequence
    Space Complexity: O(n * m) for storing actions
    """
    total_score = 0.0
    
    for sequence in environment_sequences:
        agent.reset()
        actions = []
        
        for percept in sequence:
            action = agent.act(percept)
            actions.append(action)
        
        # Calculate performance for this sequence
        score = performance_metric(sequence, actions)
        total_score += score
    
    return total_score / len(environment_sequences) if environment_sequences else 0.0


# Example usage and testing
if __name__ == "__main__":
    print("Agent Base Class")
    print("================")
    print()
    print("Agent Types:")
    for agent_type in AgentType:
        print(f"  - {agent_type.value}")
    print()
    print("Agent Architecture: Percept → Agent Function → Action")
