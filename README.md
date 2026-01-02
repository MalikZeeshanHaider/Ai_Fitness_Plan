# 💪 AI Gym Workout Recommendation System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![AI](https://img.shields.io/badge/AI-Intelligent%20Agents-green.svg)](https://en.wikipedia.org/wiki/Intelligent_agent)
[![Search](https://img.shields.io/badge/Search-A*%20Algorithm-orange.svg)](https://en.wikipedia.org/wiki/A*_search_algorithm)

> **An intelligent AI-powered workout recommendation system demonstrating multiple AI concepts including Intelligent Agents, Search Algorithms, Reasoning Systems, and Optimization Techniques - Perfect for Academic Viva Presentations**

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [AI Concepts Implemented](#-ai-concepts-implemented)
- [System Architecture](#-system-architecture)
- [Installation & Setup](#-installation--setup)
- [How to Run](#️-how-to-run)
- [Code Structure](#-code-structure)
- [Algorithms Explained](#-algorithms-explained)
- [Libraries Used](#-libraries-used)
- [Complexity Analysis](#-complexity-analysis)
- [Viva Questions & Answers](#-viva-questions--answers)
- [Features](#-features)
- [Example Usage](#-example-usage)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Project Overview

The **AI Gym Workout Recommendation System** is an intelligent application that generates personalized workout plans using a **4-step AI workflow**:

```
Step 1: Simple Reflex Agent (Safety Filtering)
          ↓
Step 2: Goal-Based Agent (Goal Definition)
          ↓
Step 3: Utility-Based Agent (Exercise Scoring)
          ↓
Step 4: A* Search Algorithm (Optimal Plan Generation)
          ↓
Result: Personalized Workout Plan
```

### 🎓 Academic Value
This project is **specifically designed for academic presentations** and demonstrates:
- ✅ Multiple types of Intelligent Agents
- ✅ State-Space Search Problem formulation
- ✅ Informed Search Algorithms (A*)
- ✅ Heuristic Functions
- ✅ Reasoning Systems (Deductive, Inductive, Probabilistic)
- ✅ Utility Optimization
- ✅ Clean Architecture Principles

---

## 🤖 AI Concepts Implemented

### 1️⃣ **Intelligent Agents (4 Types)**

#### **A. Simple Reflex Agent**
```python
Type: Condition-Action Rule-Based Agent
Function: action = REFLEX(percept)
Purpose: Safety filtering and injury prevention
```

**Explanation:**
- Most basic type of agent that responds to current percept only
- Uses **IF-THEN rules** for decision making
- No memory or internal state
- Fast and efficient for well-defined rules

**Code Implementation:**
```python
class SimpleReflexAgent:
    def filter_unsafe_exercises(self, exercises, user_state):
        safe_exercises = []
        for exercise in exercises:
            if self.apply_safety_rules(exercise, user_state):
                safe_exercises.append(exercise)
        return safe_exercises
```

**Example Rules:**
- `IF knee_injury THEN remove_high_impact_exercises`
- `IF beginner THEN remove_advanced_exercises`
- `IF low_energy THEN recommend_light_exercises`

**Complexity:** O(n) where n = number of exercises

---

#### **B. Goal-Based Agent**
```python
Type: Goal-Oriented Agent
Function: plan = GOAL_BASED(current_state, goal_state)
Purpose: Fitness goal definition and planning
```

**Explanation:**
- Makes decisions by considering desirability of goal states
- Defines explicit target state
- Plans actions to achieve goals
- More flexible than reflex agents

**Code Implementation:**
```python
class GoalBasedAgent:
    def define_goal(self, user_goal, current_state):
        target_state = self.create_target_state(user_goal)
        return Goal(
            description=user_goal,
            target_state=target_state,
            priority=self.calculate_priority(user_goal)
        )
```

**Goal Types:**
- **Weight Loss** → Target: Reduce weight, Focus: Cardio
- **Muscle Gain** → Target: Increase muscle mass, Focus: Strength
- **Endurance** → Target: Increase stamina, Focus: Cardio/Endurance
- **General Fitness** → Target: Balanced improvement, Focus: Mixed

**Complexity:** O(1) for goal definition

---

#### **C. Utility-Based Agent**
```python
Type: Rational Decision-Making Agent
Function: best_action = argmax(utility(action, state))
Purpose: Exercise optimization with multiple objectives
```

**Explanation:**
- Selects actions that maximize utility function
- Handles multiple conflicting objectives
- Makes rational trade-off decisions
- Most sophisticated type of agent

**Utility Function:**
```
U(exercise) = w1·Effectiveness + w2·Safety + w3·TimeEfficiency + w4·Preference
            = 0.4·Eff + 0.3·Safety + 0.2·Time + 0.1·Pref
```

**Code Implementation:**
```python
class UtilityBasedAgent:
    def calculate_utility(self, exercise, state, goal):
        effectiveness = self.calculate_effectiveness(exercise, goal)
        safety = self.calculate_safety(exercise, state)
        time_efficiency = exercise.calories_per_minute
        preference = state.user_preferences.get(exercise.type, 0.5)
        
        utility = (0.4 * effectiveness + 
                   0.3 * safety + 
                   0.2 * time_efficiency + 
                   0.1 * preference)
        return utility
```

**Complexity:** O(n) for scoring n exercises

---

### 2️⃣ **Search Algorithms**

#### **A. A* Search Algorithm** ⭐ (Primary Algorithm)

**Explanation:**
A* is an **informed search algorithm** that finds the optimal path from initial state to goal state.

**Formula:**
```
f(n) = g(n) + h(n)

where:
- f(n) = Total estimated cost
- g(n) = Actual cost from start to node n
- h(n) = Heuristic (estimated cost from n to goal)
```

**Properties:**
- ✅ **Complete:** Always finds a solution if one exists
- ✅ **Optimal:** Finds the least-cost solution
- ✅ **Admissible Heuristic:** h(n) ≤ actual cost (never overestimates)
- ✅ **Consistent Heuristic:** h(n) ≤ cost(n,n') + h(n')

**Algorithm Steps:**
```
1. Initialize: Add initial node to priority queue (ordered by f(n))
2. While queue not empty:
   a. Pop node with lowest f(n)
   b. If node is goal → return solution
   c. Expand node → generate successors
   d. Calculate f(n) for each successor
   e. Add successors to queue
3. If queue empty → no solution
```

**Code Implementation:**
```python
class AStarSearch:
    def search(self, problem):
        frontier = PriorityQueue()  # Min-heap ordered by f(n)
        frontier.put((0, initial_node))
        explored = set()
        
        while not frontier.empty():
            _, node = frontier.get()
            
            if problem.is_goal(node.state):
                return self.extract_solution(node)
            
            explored.add(node.state)
            
            for action in problem.get_actions(node.state):
                child = node.expand(action)
                
                if child.state not in explored:
                    g_n = child.path_cost
                    h_n = problem.heuristic(child.state)
                    f_n = g_n + h_n
                    
                    frontier.put((f_n, child))
        
        return None  # No solution
```

**Time Complexity:** O(b^d) where b=branching factor, d=depth
- With good heuristic: Much better in practice
- Explores fewer nodes than uninformed search

**Space Complexity:** O(b^d) - stores all generated nodes

**Why A* over other algorithms?**
- BFS: Optimal but explores too many nodes (slow)
- DFS: Fast but not optimal
- UCS: Optimal but ignores goal direction
- Greedy: Fast but not optimal
- **A*: Optimal + Efficient (best of both worlds)**

---

#### **B. Heuristic Function**

**Explanation:**
Heuristic estimates remaining cost to goal. Good heuristics make A* efficient.

**Implementation in Project:**
```python
def workout_heuristic(state, goal_state):
    """
    Admissible heuristic for workout planning.
    Estimates minimum time needed to complete workout.
    """
    remaining_time = goal_state.target_duration - state.current_duration
    remaining_calories = goal_state.target_calories - state.calories_burned
    remaining_muscle_groups = len(goal_state.target_muscles - state.worked_muscles)
    
    # Estimate minimum time needed
    time_for_calories = remaining_calories / MAX_CALORIES_PER_MINUTE
    time_for_muscles = remaining_muscle_groups * MIN_EXERCISE_DURATION
    
    h_n = max(remaining_time, time_for_calories, time_for_muscles)
    
    return h_n  # Never overestimates (admissible)
```

**Properties:**
- **Admissible:** Never overestimates actual cost
- **Consistent:** Satisfies triangle inequality
- **Informative:** Provides good guidance

---

### 3️⃣ **Reasoning Systems**

#### **A. Deductive Reasoning**
```
General Rules → Specific Conclusions
```

**Explanation:**
- Applies general rules to specific situations
- Logical inference from known facts
- Forward-chaining inference engine

**Example:**
```
Rule: IF (beginner AND knee_injury) THEN avoid_high_impact
Fact: User is beginner
Fact: User has knee_injury
Conclusion: Avoid high-impact exercises
```

---

#### **B. Inductive Reasoning**
```
Specific Observations → General Patterns
```

**Explanation:**
- Learns patterns from examples
- Discovers associations and rules
- Bottom-up learning approach

**Example:**
```
Observation: 80% of beginners prefer cardio
Observation: 75% of beginners avoid heavy weights
Pattern: Beginners tend to prefer cardio over weights
Generalization: Recommend cardio-focused plans for beginners
```

---

#### **C. Probabilistic Reasoning**
```
Bayesian Inference for Uncertainty
```

**Formula:**
```
P(H|E) = P(E|H) × P(H) / P(E)

where:
- P(H|E) = Posterior (updated belief)
- P(E|H) = Likelihood
- P(H) = Prior (initial belief)
- P(E) = Evidence probability
```

**Example:**
```
H: User will succeed with difficult workout
E: User has high energy and no injuries

P(H) = 0.6 (prior)
P(E|H) = 0.8 (likelihood)
P(E) = 0.5 (evidence)

P(H|E) = 0.8 × 0.6 / 0.5 = 0.96 (96% success)
```

---

### 4️⃣ **State-Space Search Formulation**

**Components:**
- **State:** Complete description of workout progress
- **Initial State:** User profile (age, weight, goals)
- **Goal State:** Desired outcome (duration, calories, muscles)
- **Actions:** Adding exercises to workout plan
- **Transition Model:** Result(state, action) → new_state
- **Path Cost:** Sum of exercise difficulty/fatigue
- **Solution:** Sequence of exercises achieving goal

**Code Representation:**
```python
@dataclass
class State:
    """Represents workout state"""
    user_id: str
    fitness_goal: FitnessGoal
    experience_level: ExperienceLevel
    worked_muscle_groups: FrozenSet[str]
    total_duration: float
    calories_burned: float
    exercises_completed: int
    current_fatigue: float
```

---

## 🏗️ System Architecture

### Clean Architecture (4 Layers)

```
┌─────────────────────────────────────────┐
│     PRESENTATION LAYER                  │
│   (Streamlit UI, Components)            │
│   - app.py                              │
│   - ui_components.py                    │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│     APPLICATION LAYER                   │
│   (Use Cases, Business Logic)           │
│   - workout_recommendation_usecase.py   │
│   - workout_plan_generator.py           │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│     DOMAIN LAYER (AI Core)              │
│   - Agents (Reflex, Goal, Utility)      │
│   - Search (A*, BFS, DFS, UCS)          │
│   - Reasoning (Deductive, Inductive)    │
│   - Models (State, Action, Exercise)    │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│     INFRASTRUCTURE LAYER                │
│   - Data Loader (CSV processing)        │
│   - Config Loader (YAML)                │
│   - Logging System                      │
└─────────────────────────────────────────┘
```

**Benefits:**
- ✅ Separation of Concerns
- ✅ Testable Code
- ✅ Easy to Maintain
- ✅ Independent Layers

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step-by-Step Installation

**1. Navigate to Project Directory**
```bash
cd Ai_Fitness_Plan
```

**2. Create Virtual Environment (Recommended)**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Verify Installation**
```bash
python -c "import streamlit; import pandas; import numpy; print('✅ All dependencies installed!')"
```

---

## ▶️ How to Run

### Method 1: Using Streamlit Command
```bash
streamlit run app.py
```

### Method 2: Using Batch File (Windows)
```bash
run.bat
```

### Method 3: Direct Python
```bash
python -m streamlit run app.py
```

**Application will open at:** `http://localhost:8501`

---

## 📁 Code Structure

```
Ai_Fitness_Plan/
│
├── app.py                          # Main application entry point
├── requirements.txt                # Python dependencies
├── run.bat                         # Windows batch file
├── config/
│   └── config.yaml                 # Configuration settings
│
├── data/
│   └── GymDataset.csv              # Exercise dataset
│
├── docs/                           # Documentation
│   ├── ALGORITHMS.md               # Algorithm explanations
│   ├── ARCHITECTURE.md             # Architecture docs
│   ├── SIMPLIFIED_ARCHITECTURE.md  # Simplified guide
│   └── USAGE_GUIDE.md              # User guide
│
├── src/
│   ├── presentation/               # UI Layer
│   │   ├── ui_components.py        # UI components
│   │   ├── ui_state.py             # State management
│   │   └── custom_css.py           # Styling
│   │
│   ├── application/                # Application Layer
│   │   ├── workout_recommendation_usecase.py
│   │   ├── workout_plan_generator.py
│   │   ├── pdf_generator.py
│   │   └── reasoning_explainer.py
│   │
│   ├── domain/                     # Domain Layer (AI Core)
│   │   ├── agents/                 # Intelligent Agents
│   │   │   ├── agent.py
│   │   │   ├── simple_reflex_agent.py
│   │   │   ├── goal_based_agent.py
│   │   │   └── utility_based_agent.py
│   │   │
│   │   ├── search/                 # Search Algorithms
│   │   │   ├── search_problem.py
│   │   │   ├── search_strategy.py
│   │   │   └── astar.py
│   │   │
│   │   ├── reasoning/              # Reasoning Systems
│   │   │   ├── deductive_reasoner.py
│   │   │   ├── inductive_reasoner.py
│   │   │   ├── probability_calculator.py
│   │   │   └── heuristic_function.py
│   │   │
│   │   └── models/                 # Domain Models
│   │       ├── state.py
│   │       ├── action.py
│   │       ├── exercise.py
│   │       ├── search_node.py
│   │       └── workout_plan.py
│   │
│   ├── infrastructure/             # Infrastructure Layer
│   │   ├── data/
│   │   │   ├── data_loader.py
│   │   │   ├── data_preprocessor.py
│   │   │   └── data_validator.py
│   │   ├── config_loader.py
│   │   └── logging_config.py
│   │
│   └── utils/                      # Utilities
│       ├── error_handler.py
│       └── performance_optimizer.py
│
└── tests/                          # Unit tests
    ├── test_integration.py
    └── __init__.py
```

---

## 🔍 Algorithms Explained

### 1. A* Search Algorithm

**Pseudocode:**
```
function A_STAR(problem):
    frontier ← priority queue ordered by f(n)
    frontier.add(initial_node)
    explored ← empty set
    
    while frontier is not empty:
        node ← frontier.pop()  # lowest f(n)
        
        if problem.is_goal(node.state):
            return SOLUTION(node)
        
        explored.add(node.state)
        
        for each action in problem.actions(node.state):
            child ← CHILD-NODE(node, action)
            
            if child.state not in explored:
                g ← child.path_cost
                h ← problem.heuristic(child.state)
                f ← g + h
                frontier.add(child, priority=f)
    
    return FAILURE
```

**Key Concepts:**
- **Frontier:** Priority queue of nodes to explore
- **Explored Set:** Visited states (avoid cycles)
- **f(n) = g(n) + h(n):** Evaluation function
- **Admissible Heuristic:** Guarantees optimality

---

### 2. Utility Function Optimization

**Multi-Objective Optimization:**
```
Objective: Maximize U(exercise)

U(e) = Σ wi × fi(e)

Components:
f1(e) = Effectiveness Score  (w1 = 0.4)
f2(e) = Safety Score        (w2 = 0.3)
f3(e) = Time Efficiency     (w3 = 0.2)
f4(e) = User Preference     (w4 = 0.1)
```

---

## 📚 Libraries Used

### Core Libraries

| Library | Version | Purpose | Concepts |
|---------|---------|---------|----------|
| **Python** | 3.8+ | Programming Language | OOP, Functional Programming |
| **Streamlit** | 1.28+ | Web UI Framework | Interactive UI |
| **Pandas** | 2.1+ | Data Processing | DataFrames |
| **NumPy** | 1.24+ | Numerical Computing | Arrays |
| **PyYAML** | 6.0+ | Configuration | YAML Parsing |
| **ReportLab** | 4.0+ | PDF Generation | PDF Creation |

### Standard Library Modules

| Module | Purpose |
|--------|---------|
| `dataclasses` | Structured data classes |
| `typing` | Type hints |
| `abc` | Abstract base classes |
| `enum` | Enumerations |
| `heapq` | Priority queue |
| `collections` | Deque, defaultdict |
| `datetime` | Timestamps |
| `logging` | Application logging |

---

## ⚡ Complexity Analysis

### Agent Complexity

| Agent Type | Time | Space | Explanation |
|------------|------|-------|-------------|
| Simple Reflex | O(n) | O(1) | Iterates through n exercises |
| Goal-Based | O(1) | O(1) | Direct goal lookup |
| Utility-Based | O(n) | O(n) | Calculates utility for n exercises |

### Search Algorithm Complexity

| Algorithm | Time | Space | Complete | Optimal |
|-----------|------|-------|----------|---------|
| BFS | O(b^d) | O(b^d) | ✅ Yes | ✅ Yes |
| DFS | O(b^m) | O(bm) | ❌ No | ❌ No |
| UCS | O(b^(C*/ε)) | O(b^(C*/ε)) | ✅ Yes | ✅ Yes |
| A* | O(b^d) | O(b^d) | ✅ Yes | ✅ Yes |

**Legend:**
- b = branching factor
- d = depth of optimal solution
- m = maximum depth
- C* = optimal solution cost

---

## 🎓 Viva Questions & Answers

### **Q1: Why did you choose intelligent agents?**
**Answer:**
Intelligent agents provide a modular architecture where each agent has a specific responsibility:
- **Simple Reflex Agent** handles safety (reactive)
- **Goal-Based Agent** defines objectives (goal-oriented)
- **Utility-Based Agent** optimizes choices (rational)

This separation makes the system easier to explain and maintain.

---

### **Q2: Why A* algorithm instead of BFS or DFS?**
**Answer:**
- **BFS:** Optimal but explores all nodes (slow)
- **DFS:** Fast but not optimal
- **A*:** Both optimal and efficient with heuristics

A* combines the optimality of BFS with informed search efficiency.

---

### **Q3: What makes your heuristic admissible?**
**Answer:**
Our heuristic **never overestimates** the actual cost. It uses:
```python
h(n) = max(
    remaining_time,
    time_for_calories,
    time_for_muscles
)
```

By using optimistic estimates (max calorie burn, min durations), we ensure h(n) ≤ actual cost.

---

### **Q4: Explain the utility function.**
**Answer:**
```
U(exercise) = 0.4·Effectiveness + 0.3·Safety + 0.2·TimeEfficiency + 0.1·Preference
```

**Components:**
1. **Effectiveness (40%):** Goal achievement
2. **Safety (30%):** Injury prevention
3. **Time Efficiency (20%):** Results per minute
4. **User Preference (10%):** Personal likes

Weights reflect importance priorities.

---

### **Q5: Difference between deductive and inductive reasoning?**
**Answer:**

**Deductive:** General → Specific (logically certain)
```
Rule: All beginners avoid advanced exercises
Fact: User is beginner
Conclusion: Avoid advanced exercises
```

**Inductive:** Specific → General (probabilistic)
```
Observations: Multiple beginners prefer cardio
Pattern: Beginners tend to prefer cardio
Generalization: Recommend cardio for beginners
```

---

## ✨ Features

### Current Features
- ✅ 4 types of intelligent agents
- ✅ Multiple search algorithms (A*, BFS, DFS, UCS)
- ✅ Reasoning systems (Deductive, Inductive, Probabilistic)
- ✅ Heuristic functions with optimality guarantees
- ✅ Interactive web interface
- ✅ PDF export of workout plans
- ✅ Performance metrics and analysis
- ✅ Safety filtering and injury prevention
- ✅ Multi-objective optimization

---

## 📊 Example Usage

### Input
```
User Profile:
- Age: 25 years
- Weight: 70 kg
- Goal: Weight Loss
- Time: 45 minutes
- Level: Beginner
```

### Output
```
🏋️ WORKOUT PLAN

1. Warm-Up (5 min) - 20 cal
2. Running (15 min) - 150 cal
3. Jump Rope (10 min) - 100 cal
4. Burpees (8 min) - 80 cal
5. Cool-Down (2 min) - 10 cal

Total: 45 min, 360 calories ✓

AI Metrics:
- Algorithm: A* Search
- Nodes Explored: 127
- Optimality: Guaranteed ✓
```

---

## 🔧 Configuration

### config/config.yaml
```yaml
application:
  name: "AI Gym Workout Recommendation System"
  version: "1.0.0"

agents:
  utility_based:
    weights:
      effectiveness: 0.4
      safety: 0.3
      time_efficiency: 0.2
      preference: 0.1

search:
  algorithm: "astar"
  max_iterations: 10000
```

---

## 🐛 Troubleshooting

**Issue: ModuleNotFoundError**
```bash
pip install -r requirements.txt
```

**Issue: Port already in use**
```bash
streamlit run app.py --server.port 8502
```

**Issue: Dataset not loading**
- Check file path in config.yaml
- Ensure `data/GymDataset.csv` exists

---

## 📖 Additional Documentation

- [`docs/ALGORITHMS.md`](docs/ALGORITHMS.md) - Detailed algorithms
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) - Architecture
- [`docs/USAGE_GUIDE.md`](docs/USAGE_GUIDE.md) - User guide

---

## 🎯 Learning Outcomes

### AI Concepts
✅ Intelligent Agents (Reflex, Goal-Based, Utility-Based)
✅ Search Algorithms (A*, BFS, DFS, UCS)
✅ Heuristic Functions
✅ State-Space Search
✅ Reasoning Systems
✅ Utility Optimization

### Software Engineering
✅ Clean Architecture
✅ SOLID Principles
✅ Design Patterns
✅ Code Organization
✅ Type Hints
✅ Error Handling

---

## 📝 License

Educational purposes and academic presentations.

---

## 👨‍💻 Author

**AI Gym Development Team**
- Project Type: Academic AI Project
- Purpose: Viva Presentation & Learning
- Date: January 2026

---

## 🎓 Perfect for Viva!

This project demonstrates:
- ✅ Clear AI concepts
- ✅ Well-commented code
- ✅ Comprehensive documentation
- ✅ Step-by-step explanations
- ✅ Complexity analysis
- ✅ Question bank with answers

**Good luck with your viva presentation!** 🎯💪

---
