# 🧠 AI Algorithms Documentation

## Table of Contents

- [Overview](#overview)
- [Search Algorithms](#search-algorithms)
- [Intelligent Agents](#intelligent-agents)
- [Reasoning Systems](#reasoning-systems)
- [Heuristic Functions](#heuristic-functions)
- [Performance Analysis](#performance-analysis)

---

## Overview

This document provides detailed explanations of all AI algorithms implemented in the system. Each algorithm includes theoretical background, implementation details, complexity analysis, and practical examples.

---

## Search Algorithms

Search algorithms find optimal sequences of exercises to create workout plans. The system implements both uninformed and informed search strategies.

### 1. Breadth-First Search (BFS)

#### Theory
BFS explores the search tree level by level, guaranteeing the shortest path in unweighted graphs.

#### Algorithm
```
function BFS(problem):
    frontier = Queue()
    frontier.enqueue(problem.initial_state)
    explored = Set()
    
    while frontier is not empty:
        node = frontier.dequeue()
        
        if problem.is_goal(node.state):
            return solution(node)
        
        explored.add(node.state)
        
        for action in problem.actions(node.state):
            child = create_child_node(node, action)
            if child.state not in explored and child not in frontier:
                frontier.enqueue(child)
    
    return failure
```

#### Implementation Details
```python
def breadth_first_search(problem: SearchProblem, 
                        graph_search: bool = True) -> Optional[SearchNode]:
    """
    Breadth-First Search implementation.
    
    Args:
        problem: SearchProblem instance
        graph_search: If True, avoid revisiting states
    
    Returns:
        Goal node or None if no solution
    """
    frontier = deque([SearchNode(problem.get_initial_state())])
    explored = set() if graph_search else None
    
    while frontier:
        node = frontier.popleft()  # FIFO
        
        if problem.is_goal_state(node.state):
            return node
        
        if graph_search:
            explored.add(node.state)
        
        for action in problem.get_actions(node.state):
            child = node.expand(action, problem)
            
            if graph_search:
                if child.state not in explored and child not in frontier:
                    frontier.append(child)
            else:
                frontier.append(child)
    
    return None
```

#### Complexity Analysis
- **Time Complexity**: O(b^d)
  - b = branching factor (avg actions per state)
  - d = depth of shallowest goal
- **Space Complexity**: O(b^d)
  - Must store all nodes at current level
- **Completeness**: ✅ Complete (finds solution if exists)
- **Optimality**: ✅ Optimal for unweighted graphs

#### Use Case in Workout System
- Finding minimal exercise sequence
- Exploring all exercise type combinations
- Ensuring diverse workout types

#### Example
```
Initial State: No exercises selected
Goal State: 60 minutes of exercises

Level 0: []
Level 1: [Cardio], [Strength], [Flexibility]
Level 2: [Cardio, Strength], [Cardio, Flexibility], [Strength, Cardio], ...
...
Solution: Shortest path to 60-minute workout
```

---

### 2. Depth-First Search (DFS)

#### Theory
DFS explores as deep as possible along each branch before backtracking.

#### Algorithm
```
function DFS(problem):
    frontier = Stack()
    frontier.push(problem.initial_state)
    explored = Set()
    
    while frontier is not empty:
        node = frontier.pop()
        
        if problem.is_goal(node.state):
            return solution(node)
        
        explored.add(node.state)
        
        for action in problem.actions(node.state):
            child = create_child_node(node, action)
            if child.state not in explored and child not in frontier:
                frontier.push(child)
    
    return failure
```

#### Implementation Details
```python
def depth_first_search(problem: SearchProblem,
                      graph_search: bool = True,
                      depth_limit: Optional[int] = None) -> Optional[SearchNode]:
    """
    Depth-First Search implementation with optional depth limit.
    
    Args:
        problem: SearchProblem instance
        graph_search: If True, avoid revisiting states
        depth_limit: Maximum depth to explore
    
    Returns:
        Goal node or None
    """
    frontier = [SearchNode(problem.get_initial_state())]
    explored = set() if graph_search else None
    
    while frontier:
        node = frontier.pop()  # LIFO
        
        if depth_limit and node.depth > depth_limit:
            continue
        
        if problem.is_goal_state(node.state):
            return node
        
        if graph_search:
            explored.add(node.state)
        
        for action in problem.get_actions(node.state):
            child = node.expand(action, problem)
            
            if graph_search:
                if child.state not in explored:
                    frontier.append(child)
            else:
                frontier.append(child)
    
    return None
```

#### Complexity Analysis
- **Time Complexity**: O(b^m)
  - m = maximum depth (can be infinite)
- **Space Complexity**: O(bm)
  - Only stores path from root to current node
- **Completeness**: ❌ Incomplete (infinite paths)
- **Optimality**: ❌ Not optimal

#### Use Case in Workout System
- Quick exploration of exercise combinations
- Memory-efficient for large search spaces
- Limited depth search for time constraints

#### Example
```
Initial: []
Explore: [Cardio] → [Cardio, Strength] → [Cardio, Strength, Core] → ...
(Goes deep before trying [Cardio, Flexibility])
```

---

### 3. Uniform Cost Search (UCS)

#### Theory
UCS expands the node with the lowest path cost, guaranteeing optimal solutions.

#### Algorithm
```
function UCS(problem):
    frontier = PriorityQueue(by=path_cost)
    frontier.insert(problem.initial_state, cost=0)
    explored = Set()
    
    while frontier is not empty:
        node = frontier.pop()  # Lowest cost
        
        if problem.is_goal(node.state):
            return solution(node)
        
        explored.add(node.state)
        
        for action in problem.actions(node.state):
            child = create_child_node(node, action)
            if child.state not in explored and child not in frontier:
                frontier.insert(child, child.path_cost)
            elif child in frontier with higher cost:
                replace with child
    
    return failure
```

#### Implementation Details
```python
def uniform_cost_search(problem: SearchProblem) -> Optional[SearchNode]:
    """
    Uniform Cost Search using priority queue.
    
    Expands nodes in order of increasing path cost.
    
    Returns:
        Goal node with optimal cost or None
    """
    frontier = PriorityQueue()
    initial = SearchNode(problem.get_initial_state())
    frontier.put((initial.path_cost, id(initial), initial))
    
    explored = set()
    frontier_states = {initial.state: initial.path_cost}
    
    while not frontier.empty():
        _, _, node = frontier.get()
        
        if problem.is_goal_state(node.state):
            return node
        
        explored.add(node.state)
        del frontier_states[node.state]
        
        for action in problem.get_actions(node.state):
            child = node.expand(action, problem)
            
            if child.state not in explored:
                if child.state not in frontier_states:
                    frontier.put((child.path_cost, id(child), child))
                    frontier_states[child.state] = child.path_cost
                elif child.path_cost < frontier_states[child.state]:
                    # Replace with lower cost path
                    frontier.put((child.path_cost, id(child), child))
                    frontier_states[child.state] = child.path_cost
    
    return None
```

#### Complexity Analysis
- **Time Complexity**: O(b^(1+⌊C*/ε⌋))
  - C* = optimal solution cost
  - ε = minimum step cost
- **Space Complexity**: O(b^(1+⌊C*/ε⌋))
- **Completeness**: ✅ Complete
- **Optimality**: ✅ Optimal

#### Use Case in Workout System
- Minimize total workout duration
- Optimize calorie expenditure
- Balance multiple cost factors

#### Example
```
Cost = Duration in minutes

Initial: [] (cost=0)
Expand: [Cardio(10min)] (cost=10)
        [Strength(15min)] (cost=15)
Expand: [Cardio(10min), Flexibility(5min)] (cost=15)
...
Finds lowest total duration to goal
```

---

### 4. Greedy Best-First Search

#### Theory
Greedy search expands nodes that appear closest to the goal based on a heuristic function.

#### Algorithm
```
function GreedySearch(problem):
    frontier = PriorityQueue(by=heuristic)
    frontier.insert(problem.initial_state, h(initial))
    explored = Set()
    
    while frontier is not empty:
        node = frontier.pop()  # Lowest h(n)
        
        if problem.is_goal(node.state):
            return solution(node)
        
        explored.add(node.state)
        
        for action in problem.actions(node.state):
            child = create_child_node(node, action)
            if child.state not in explored and child not in frontier:
                frontier.insert(child, h(child.state))
    
    return failure
```

#### Implementation Details
```python
def greedy_best_first_search(problem: SearchProblem) -> Optional[SearchNode]:
    """
    Greedy Best-First Search using heuristic function.
    
    Expands nodes with lowest h(n) value.
    
    Returns:
        Goal node or None
    """
    frontier = PriorityQueue()
    initial = SearchNode(problem.get_initial_state())
    h_value = problem.heuristic(initial.state)
    frontier.put((h_value, id(initial), initial))
    
    explored = set()
    
    while not frontier.empty():
        _, _, node = frontier.get()
        
        if problem.is_goal_state(node.state):
            return node
        
        explored.add(node.state)
        
        for action in problem.get_actions(node.state):
            child = node.expand(action, problem)
            
            if child.state not in explored:
                h_value = problem.heuristic(child.state)
                frontier.put((h_value, id(child), child))
    
    return None
```

#### Complexity Analysis
- **Time Complexity**: O(b^m)
- **Space Complexity**: O(b^m)
- **Completeness**: ❌ Incomplete
- **Optimality**: ❌ Not optimal

#### Heuristic Function
```python
def heuristic(state: State) -> float:
    """
    Estimate remaining cost to goal.
    
    Lower value = closer to goal
    """
    current_duration = state.total_exercise_time
    target_duration = 60  # minutes
    
    remaining = max(0, target_duration - current_duration)
    return remaining
```

#### Use Case in Workout System
- Fast goal-directed search
- Good for time-limited scenarios
- Prioritize exercises that quickly meet goals

#### Example
```
Goal: 60 minutes total
h(n) = 60 - current_duration

State: [Cardio(20min)] → h=40
State: [Cardio(20min), Strength(30min)] → h=10
State: [Cardio(20min), Strength(30min), Core(10min)] → h=0 (GOAL)
```

---

### 5. A* Search

#### Theory
A* combines UCS and Greedy, using f(n) = g(n) + h(n) where:
- g(n) = actual cost from start to n
- h(n) = estimated cost from n to goal
- f(n) = estimated total cost through n

#### Algorithm
```
function A_Star(problem):
    frontier = PriorityQueue(by=f(n))
    frontier.insert(problem.initial, f=0+h(initial))
    explored = Set()
    
    while frontier is not empty:
        node = frontier.pop()  # Lowest f(n)
        
        if problem.is_goal(node.state):
            return solution(node)
        
        explored.add(node.state)
        
        for action in problem.actions(node.state):
            child = create_child_node(node, action)
            f_value = child.path_cost + h(child.state)
            
            if child.state not in explored and child not in frontier:
                frontier.insert(child, f_value)
            elif child in frontier with higher f:
                replace with child
    
    return failure
```

#### Implementation Details
```python
def a_star_search(problem: SearchProblem) -> Optional[SearchNode]:
    """
    A* Search using f(n) = g(n) + h(n).
    
    Optimal if heuristic is admissible (never overestimates).
    
    Returns:
        Optimal goal node or None
    """
    frontier = PriorityQueue()
    initial = SearchNode(problem.get_initial_state())
    
    g = initial.path_cost  # Actual cost
    h = problem.heuristic(initial.state)  # Estimated cost
    f = g + h  # Total estimated cost
    
    frontier.put((f, id(initial), initial))
    
    explored = set()
    frontier_states = {initial.state: f}
    
    while not frontier.empty():
        _, _, node = frontier.get()
        
        if problem.is_goal_state(node.state):
            return node
        
        explored.add(node.state)
        del frontier_states[node.state]
        
        for action in problem.get_actions(node.state):
            child = node.expand(action, problem)
            
            g = child.path_cost
            h = problem.heuristic(child.state)
            f = g + h
            
            if child.state not in explored:
                if child.state not in frontier_states:
                    frontier.put((f, id(child), child))
                    frontier_states[child.state] = f
                elif f < frontier_states[child.state]:
                    frontier.put((f, id(child), child))
                    frontier_states[child.state] = f
    
    return None
```

#### Complexity Analysis
- **Time Complexity**: O(b^d)
- **Space Complexity**: O(b^d)
- **Completeness**: ✅ Complete
- **Optimality**: ✅ Optimal (with admissible h)

#### Admissible Heuristics

**Heuristic 1: Remaining Time**
```python
def h_remaining_time(state: State) -> float:
    """Never overestimates (admissible)."""
    target = 60
    current = sum(e.duration for e in state.exercises)
    return max(0, target - current)
```

**Heuristic 2: Minimum Exercises Needed**
```python
def h_min_exercises(state: State) -> float:
    """Assumes shortest exercises available."""
    target = 60
    current = sum(e.duration for e in state.exercises)
    remaining = target - current
    
    if remaining <= 0:
        return 0
    
    shortest_exercise = 5  # Minimum exercise duration
    return remaining / shortest_exercise
```

**Heuristic 3: Calorie Deficit**
```python
def h_calorie_deficit(state: State) -> float:
    """Estimate exercises needed for calorie goal."""
    target_calories = 500
    current_calories = sum(e.calories for e in state.exercises)
    deficit = max(0, target_calories - current_calories)
    
    avg_calories_per_exercise = 100
    return deficit / avg_calories_per_exercise
```

#### Use Case in Workout System
- **Primary search algorithm** for workout generation
- Balances optimality and efficiency
- Guarantees best solution with admissible heuristic

#### Example
```
Goal: 60 minutes, high-calorie workout

Initial: [] (g=0, h=60, f=60)
Expand: [Cardio(20,200cal)] (g=20, h=40, f=60)
Expand: [Cardio, Strength(30,250cal)] (g=50, h=10, f=60)
Expand: [Cardio, Strength, Core(10,50cal)] (g=60, h=0, f=60) ✓

Optimal: 500 calories in 60 minutes
```

---

### 6. AND/OR Tree Search

#### Theory
AND/OR trees represent problems where:
- **OR nodes**: Choose one alternative
- **AND nodes**: Must satisfy all children

#### Structure
```
         Goal: Complete Workout
                 (OR)
          /       |        \
    Cardio     Strength   Flexibility
      (AND)      (AND)       (AND)
     /  \       /  |  \      /  \
   Run Cycle  Push Pull Squat Yoga Stretch
```

#### Implementation Details
```python
class ANDORNode:
    def __init__(self, exercise: Exercise, node_type: str):
        self.exercise = exercise
        self.type = node_type  # 'AND' or 'OR'
        self.children: List[ANDORNode] = []
        self.solved = False
    
def solve_and_or_tree(node: ANDORNode) -> bool:
    """
    Recursively solve AND/OR tree.
    
    Returns:
        True if node is solvable
    """
    if node.type == 'OR':
        # Try each alternative
        for child in node.children:
            if solve_and_or_tree(child):
                node.solved = True
                return True
        return False
    
    elif node.type == 'AND':
        # All children must be satisfied
        for child in node.children:
            if not solve_and_or_tree(child):
                return False
        node.solved = True
        return True
```

#### Use Case in Workout System
- Exercise alternatives (OR: Running OR Cycling)
- Compound requirements (AND: Warmup AND Main AND Cooldown)
- Flexible workout planning

#### Example
```
Goal: Upper Body Workout (OR)
├─ Option 1 (AND)
│  ├─ Push-ups (20 reps)
│  └─ Pull-ups (10 reps)
└─ Option 2 (AND)
   ├─ Bench Press (3 sets)
   └─ Rows (3 sets)

Solution: Choose Option 1 or Option 2
```

---

## Intelligent Agents

Agents are entities that perceive their environment and take actions to achieve goals.

### Agent Architecture

```
    Percept
       ↓
  ┌─────────┐
  │  Agent  │
  └─────────┘
       ↓
    Action
```

### 1. Simple Reflex Agent

#### Theory
Directly maps percepts to actions using if-then rules.

#### Architecture
```
Percept → Rules → Action
```

#### Implementation
```python
class SimpleReflexAgent(Agent):
    def __init__(self):
        self.rules = self._initialize_rules()
    
    def choose_action(self, percept: State) -> Action:
        """Choose action based on current percept."""
        # Check injuries
        if "knee" in (percept.injuries or []):
            return self._avoid_knee_exercises(percept)
        
        # Check energy level
        if percept.current_energy < 5:
            return self._low_intensity_action(percept)
        
        # Check goal
        if percept.goal == "weight_loss":
            return self._cardio_action(percept)
        
        return self._default_action(percept)
    
    def _avoid_knee_exercises(self, state: State) -> Action:
        """Return action that avoids knee-intensive exercises."""
        safe_exercises = [
            e for e in self.available_exercises
            if "knee" not in e.target_muscles.lower()
        ]
        return Action(choice(safe_exercises)) if safe_exercises else None
```

#### Use Case
- **Safety-first recommendations**
- Fast response time
- Rule-based constraints

#### Example Rules
```
IF has_injury("knee") THEN avoid(squats, lunges, running)
IF current_energy < 5 THEN recommend(low_intensity)
IF goal = "weight_loss" THEN recommend(cardio)
IF age > 60 THEN avoid(high_impact)
```

---

### 2. Model-Based Agent

#### Theory
Maintains internal model of the world state.

#### Architecture
```
Percept → Update Model → Rules → Action
            ↓
     Internal State
```

#### Implementation
```python
class ModelBasedAgent(Agent):
    def __init__(self):
        self.internal_state = None
        self.model = WorldModel()
    
    def choose_action(self, percept: State) -> Action:
        """
        Choose action based on internal model.
        """
        # Update internal model
        self.internal_state = self._update_state(
            self.internal_state,
            percept
        )
        
        # Predict effects of actions
        best_action = None
        best_predicted_state = None
        
        for action in self._get_possible_actions(percept):
            predicted = self.model.predict_next_state(
                self.internal_state,
                action
            )
            
            if self._is_better(predicted, best_predicted_state):
                best_action = action
                best_predicted_state = predicted
        
        return best_action
    
    def _update_state(self, current, percept):
        """Update internal world model."""
        return {
            'user_state': percept,
            'exercise_history': self.internal_state['exercise_history'] + [percept],
            'fatigue_level': self._estimate_fatigue(percept),
            'progress': self._calculate_progress(percept)
        }
```

#### Use Case
- Track workout progress
- Adjust recommendations based on history
- Progressive difficulty planning

#### Example
```
Initial Internal State:
- Exercise History: []
- Fatigue: 0
- Progress: 0%

After 3 Workouts:
- Exercise History: [workout1, workout2, workout3]
- Fatigue: 3.5
- Progress: 30%

Recommendation: Lower intensity due to fatigue
```

---

### 3. Goal-Based Agent

#### Theory
Uses goal information to guide planning.

#### Architecture
```
Percept + Goal → Planning → Action Sequence
```

#### Implementation
```python
class GoalBasedAgent(Agent):
    def __init__(self):
        self.goal = None
    
    def choose_action(self, percept: State) -> Action:
        """
        Plan actions to achieve goal.
        """
        self.goal = self._extract_goal(percept)
        
        # Create search problem
        problem = WorkoutSearchProblem(
            initial_state=percept,
            goal=self.goal
        )
        
        # Plan using A* search
        solution = a_star_search(problem)
        
        if solution:
            # Return first action in plan
            return solution.path[0] if solution.path else None
        
        return None
    
    def _extract_goal(self, state: State) -> Dict:
        """Extract concrete goal from user state."""
        if state.goal == "weight_loss":
            return {
                'calories_burned': 500,
                'duration': 60,
                'exercise_types': ['cardio', 'hiit']
            }
        elif state.goal == "muscle_gain":
            return {
                'calories_burned': 400,
                'duration': 75,
                'exercise_types': ['strength']
            }
        # ... more goals
```

#### Use Case
- Long-term fitness planning
- Multi-week workout programs
- Goal-oriented exercise selection

#### Example
```
Goal: Lose 10 pounds in 12 weeks

Sub-goals:
1. Burn 500 calories per workout
2. 4 workouts per week
3. Progressive intensity increase

Actions:
Week 1-4: Moderate cardio + light strength
Week 5-8: High-intensity cardio + moderate strength
Week 9-12: HIIT + intensive strength
```

---

### 4. Utility-Based Agent

#### Theory
Selects actions that maximize utility function.

#### Architecture
```
Percept → Utility Function → Action with Max Utility
```

#### Implementation
```python
class UtilityBasedAgent(Agent):
    def choose_action(self, percept: State) -> Action:
        """
        Choose action that maximizes utility.
        """
        actions = self._get_possible_actions(percept)
        
        # Calculate utility for each action
        utilities = [
            (action, self._utility(action, percept))
            for action in actions
        ]
        
        # Return action with maximum utility
        return max(utilities, key=lambda x: x[1])[0]
    
    def _utility(self, action: Action, state: State) -> float:
        """
        Calculate utility score for action.
        
        Utility = weighted sum of multiple factors
        """
        exercise = action.exercise
        
        # Multiple objective scores
        calorie_score = exercise.calories_burned / 100.0
        time_efficiency = exercise.calories_burned / exercise.duration_minutes
        safety_score = self._safety_score(exercise, state)
        goal_alignment = self._goal_alignment(exercise, state)
        variety_score = self._variety_score(exercise, state)
        
        # Weighted combination
        utility = (
            0.3 * calorie_score +
            0.2 * time_efficiency +
            0.25 * safety_score +
            0.15 * goal_alignment +
            0.1 * variety_score
        )
        
        return utility
    
    def _safety_score(self, exercise: Exercise, state: State) -> float:
        """Score based on safety for user's condition."""
        if state.injuries:
            for injury in state.injuries:
                if injury.lower() in exercise.name.lower():
                    return 0.0
        return 1.0
```

#### Use Case
- Multi-objective optimization
- Balanced recommendations
- Trade-off between competing goals

#### Utility Function Example
```
U(exercise) = 0.3*calories + 0.2*efficiency + 0.25*safety + 
              0.15*goal_fit + 0.1*variety

Exercise: Running (30 min, 300 cal)
- Calories: 300/100 = 3.0 → 0.3*3.0 = 0.90
- Efficiency: 300/30 = 10 → 0.2*10 = 2.00
- Safety: No conflicts → 0.25*1.0 = 0.25
- Goal Fit: Perfect for weight loss → 0.15*1.0 = 0.15
- Variety: Not done recently → 0.1*0.8 = 0.08

Total Utility = 0.90 + 2.00 + 0.25 + 0.15 + 0.08 = 3.38
```

---

### 5. Learning Agent

#### Theory
Improves performance based on experience.

#### Architecture
```
    Percept
       ↓
  Performance Element
       ↓
    Action
       ↓
  Learning Element
       ↓
Updated Knowledge
```

#### Implementation
```python
class LearningAgent(Agent):
    def __init__(self, dataset: pd.DataFrame):
        self.experience = []
        self.patterns = {}
        self.dataset = dataset
        self._learn_from_dataset()
    
    def choose_action(self, percept: State) -> Action:
        """
        Choose action based on learned patterns.
        """
        # Exploit learned knowledge
        if random() > 0.1:  # 90% exploitation
            return self._exploit(percept)
        else:  # 10% exploration
            return self._explore(percept)
    
    def _exploit(self, state: State) -> Action:
        """Use learned patterns."""
        patterns = self.patterns.get(state.goal, [])
        
        if not patterns:
            return self._default_action(state)
        
        # Find pattern matching current state
        matching = [
            p for p in patterns
            if self._matches(p, state)
        ]
        
        if matching:
            best_pattern = max(matching, key=lambda p: p['success_rate'])
            return Action(best_pattern['exercise'])
        
        return self._default_action(state)
    
    def _learn_from_dataset(self):
        """Learn patterns from historical data."""
        for goal in self.dataset['goal'].unique():
            goal_data = self.dataset[self.dataset['goal'] == goal]
            
            # Calculate success rates for each exercise
            patterns = []
            for exercise in goal_data['exercise'].unique():
                ex_data = goal_data[goal_data['exercise'] == exercise]
                success_rate = ex_data['success'].mean()
                
                patterns.append({
                    'exercise': exercise,
                    'success_rate': success_rate,
                    'avg_duration': ex_data['duration'].mean(),
                    'avg_calories': ex_data['calories'].mean()
                })
            
            self.patterns[goal] = patterns
    
    def update(self, state: State, action: Action, result: float):
        """Update knowledge based on feedback."""
        self.experience.append({
            'state': state,
            'action': action,
            'result': result
        })
        
        # Relearn patterns periodically
        if len(self.experience) % 10 == 0:
            self._update_patterns()
```

#### Use Case
- Personalized recommendations
- Adapt to user preferences
- Continuous improvement

#### Learning Example
```
Initial Knowledge (from dataset):
- Weight Loss → Cardio (85% success)
- Weight Loss → Strength (65% success)

After 10 User Workouts:
- User prefers Strength
- User success: Strength (90%), Cardio (70%)

Updated Recommendations:
- Prioritize Strength for this user
- Personalized pattern learned
```

---

## Reasoning Systems

### 1. Deductive Reasoning

#### Theory
Derive conclusions from known facts and rules using logical inference.

#### Forward Chaining Algorithm
```
function ForwardChaining(KB, query):
    inferred = {}
    
    repeat until no new facts added:
        for each rule in KB:
            if premises of rule are satisfied:
                add conclusion to inferred
                add conclusion to KB
        
        if query in inferred:
            return True
    
    return False
```

#### Implementation
```python
class DeductiveReasoner:
    def __init__(self):
        self.facts: Set[Fact] = set()
        self.rules: List[Rule] = []
        self.inference_chain: List[str] = []
    
    def add_fact(self, fact: Fact):
        """Add a known fact."""
        self.facts.add(fact)
    
    def add_rule(self, rule: Rule):
        """Add inference rule."""
        self.rules.append(rule)
    
    def infer(self) -> Set[Fact]:
        """
        Apply forward chaining to derive new facts.
        """
        new_facts = set()
        changed = True
        
        while changed:
            changed = False
            
            for rule in self.rules:
                if self._can_apply(rule):
                    conclusion = rule.apply(self.facts)
                    
                    if conclusion not in self.facts:
                        self.facts.add(conclusion)
                        new_facts.add(conclusion)
                        changed = True
                        
                        self.inference_chain.append(
                            f"{rule} → {conclusion}"
                        )
        
        return new_facts
    
    def _can_apply(self, rule: Rule) -> bool:
        """Check if rule premises are satisfied."""
        return all(
            premise in self.facts
            for premise in rule.premises
        )
```

#### Example Rules
```python
# Safety Rules
Rule("IF has_injury(knee) AND exercise(squats) THEN unsafe(squats)")
Rule("IF age > 60 AND exercise_intensity(high) THEN recommend(moderate)")
Rule("IF current_energy < 5 THEN recommend(light_exercise)")

# Goal Rules
Rule("IF goal(weight_loss) AND time(60min) THEN recommend(cardio)")
Rule("IF goal(muscle_gain) THEN recommend(strength)")

# Progression Rules
Rule("IF fitness_level(beginner) THEN start_with(easy)")
Rule("IF completed(easy) AND success THEN progress_to(medium)")
```

#### Use Case
- Safety constraint enforcement
- Rule-based recommendations
- Logical consistency checking

---

### 2. Inductive Reasoning

#### Theory
Learn patterns from observations and generalize to new situations.

#### Pattern Learning Algorithm
```
function LearnPatterns(data):
    patterns = {}
    
    for each goal in data:
        goal_data = filter(data, goal)
        
        for each feature_combination:
            count = frequency(feature_combination, goal_data)
            confidence = count / total(goal_data)
            
            if confidence > threshold:
                patterns.add(feature_combination, confidence)
    
    return patterns
```

#### Implementation
```python
class InductiveReasoner:
    def __init__(self, min_confidence: float = 0.7):
        self.patterns: List[Pattern] = []
        self.min_confidence = min_confidence
    
    def learn_patterns(self, data: pd.DataFrame):
        """
        Learn patterns from historical workout data.
        """
        # Group by goal
        for goal in data['goal'].unique():
            goal_data = data[data['goal'] == goal]
            
            # Find frequent exercise types
            exercise_counts = goal_data['exercise_type'].value_counts()
            total = len(goal_data)
            
            for ex_type, count in exercise_counts.items():
                confidence = count / total
                
                if confidence >= self.min_confidence:
                    pattern = Pattern(
                        condition={'goal': goal},
                        conclusion={'exercise_type': ex_type},
                        confidence=confidence,
                        support=count
                    )
                    self.patterns.append(pattern)
        
        # Learn feature correlations
        self._learn_correlations(data)
    
    def _learn_correlations(self, data: pd.DataFrame):
        """Learn correlations between features."""
        # Age vs difficulty preference
        age_groups = pd.cut(data['age'], bins=[0, 30, 50, 100])
        for age_group in age_groups.unique():
            age_data = data[data['age'].isin(age_group)]
            preferred_difficulty = age_data['difficulty'].mode()[0]
            confidence = len(age_data[age_data['difficulty'] == preferred_difficulty]) / len(age_data)
            
            if confidence >= self.min_confidence:
                self.patterns.append(Pattern(
                    condition={'age_group': str(age_group)},
                    conclusion={'preferred_difficulty': preferred_difficulty},
                    confidence=confidence
                ))
    
    def predict(self, features: Dict) -> List[Tuple[str, float]]:
        """
        Predict likely outcomes based on learned patterns.
        """
        matches = []
        
        for pattern in self.patterns:
            if self._matches(pattern.condition, features):
                matches.append((
                    pattern.conclusion,
                    pattern.confidence
                ))
        
        return sorted(matches, key=lambda x: x[1], reverse=True)
```

#### Learned Patterns Example
```
From 1000 workouts:

Pattern 1:
- Condition: goal = "weight_loss"
- Conclusion: prefer exercise_type = "cardio"
- Confidence: 0.87 (87% of weight loss users do cardio)
- Support: 870 instances

Pattern 2:
- Condition: age_group = "50-100"
- Conclusion: prefer difficulty = "easy"
- Confidence: 0.75
- Support: 225 instances

Pattern 3:
- Condition: goal = "muscle_gain" AND fitness_level = "advanced"
- Conclusion: prefer duration > 75 minutes
- Confidence: 0.82
- Support: 164 instances
```

---

### 3. Probabilistic Reasoning

#### Theory
Use probability theory to handle uncertainty.

#### Bayes' Theorem
```
P(A|B) = P(B|A) * P(A) / P(B)

P(A|B): Posterior probability
P(B|A): Likelihood
P(A): Prior probability
P(B): Evidence
```

#### Implementation
```python
class ProbabilityCalculator:
    def __init__(self):
        self.probabilities: Dict[str, float] = {}
        self.conditional_probs: Dict[Tuple[str, str], float] = {}
    
    def calculate_conditional(self, 
                            event_a: str,
                            event_b: str) -> float:
        """
        Calculate P(A|B) using Bayes' theorem.
        """
        # P(A|B) = P(B|A) * P(A) / P(B)
        
        p_a = self.probabilities.get(event_a, 0.5)
        p_b = self.probabilities.get(event_b, 0.5)
        p_b_given_a = self.conditional_probs.get((event_b, event_a), 0.5)
        
        if p_b == 0:
            return 0.0
        
        p_a_given_b = (p_b_given_a * p_a) / p_b
        
        return p_a_given_b
    
    def calculate_success_probability(self,
                                     workout_plan: WorkoutPlan,
                                     user_state: State) -> float:
        """
        Calculate probability of workout success.
        """
        # Factors affecting success
        energy_factor = self._energy_probability(user_state.current_energy)
        difficulty_factor = self._difficulty_match(workout_plan, user_state)
        injury_factor = self._injury_compatibility(workout_plan, user_state)
        experience_factor = self._experience_match(user_state.fitness_level)
        
        # Combined probability (assuming independence)
        success_prob = (
            energy_factor *
            difficulty_factor *
            injury_factor *
            experience_factor
        )
        
        return min(1.0, success_prob)
    
    def _energy_probability(self, energy_level: int) -> float:
        """Probability of completing workout given energy."""
        # Energy scale: 1-10
        return energy_level / 10.0
    
    def _difficulty_match(self, plan: WorkoutPlan, state: State) -> float:
        """Probability based on difficulty alignment."""
        level_map = {
            'beginner': DifficultyLevel.EASY,
            'intermediate': DifficultyLevel.MEDIUM,
            'advanced': DifficultyLevel.HARD
        }
        
        preferred = level_map.get(state.fitness_level, DifficultyLevel.MEDIUM)
        
        matches = sum(
            1 for ex in plan.exercises
            if ex.difficulty == preferred
        )
        
        return matches / len(plan.exercises)
```

#### Probability Calculations Example
```
Success Probability Calculation:

Given:
- User Energy: 7/10 → P(complete|energy=7) = 0.70
- Difficulty Match: 4/5 exercises match level → P(complete|difficulty) = 0.80
- No Injury Conflicts → P(complete|no_injury) = 1.00
- Experience: Intermediate → P(complete|experience) = 0.85

Success Probability = 0.70 * 0.80 * 1.00 * 0.85 = 0.476 = 47.6%

Interpretation: 47.6% chance of completing the workout successfully
```

---

## Heuristic Functions

### Requirements for Admissibility

A heuristic h(n) is **admissible** if:
```
h(n) ≤ h*(n)

where h*(n) is the true cost from n to goal
```

### Heuristic 1: Time Remaining
```python
def h_time(state: State) -> float:
    """
    Estimate time needed to reach goal.
    
    Admissible: Uses minimum possible time.
    """
    target_duration = 60
    current_duration = sum(e.duration for e in state.exercises)
    remaining = max(0, target_duration - current_duration)
    
    # Assume shortest available exercise (5 min)
    min_exercise_duration = 5
    return remaining / min_exercise_duration
```

### Heuristic 2: Exercise Count
```python
def h_exercises(state: State) -> float:
    """
    Estimate exercises needed.
    
    Admissible: Never overestimates needed exercises.
    """
    target_exercises = 6
    current_count = len(state.exercises)
    return max(0, target_exercises - current_count)
```

### Heuristic 3: Calorie Goal
```python
def h_calories(state: State) -> float:
    """
    Estimate cost to reach calorie goal.
    
    Admissible: Uses maximum calorie per exercise.
    """
    target_calories = 500
    current_calories = sum(e.calories for e in state.exercises)
    deficit = max(0, target_calories - current_calories)
    
    # Assume best calorie-burning exercise
    max_calories = 200
    return deficit / max_calories
```

### Combining Heuristics
```python
def h_combined(state: State) -> float:
    """
    Combine multiple heuristics.
    
    Use max() to maintain admissibility.
    """
    h1 = h_time(state)
    h2 = h_exercises(state)
    h3 = h_calories(state)
    
    # Max maintains admissibility
    return max(h1, h2, h3)
```

---

## Performance Analysis

### Search Algorithm Comparison

| Algorithm | Time | Space | Optimal | Use Case |
|-----------|------|-------|---------|----------|
| BFS | O(b^d) | O(b^d) | ✅ | Shortest path |
| DFS | O(b^m) | O(bm) | ❌ | Memory limited |
| UCS | O(b^C*/ε) | O(b^C*/ε) | ✅ | Minimize cost |
| Greedy | O(b^m) | O(b^m) | ❌ | Fast solution |
| A* | O(b^d) | O(b^d) | ✅ | Best overall |

### Agent Performance

| Agent Type | Response Time | Adaptability | Optimality |
|------------|--------------|--------------|------------|
| Simple Reflex | Fast (ms) | Low | Low |
| Model-Based | Medium (ms) | Medium | Medium |
| Goal-Based | Slow (seconds) | High | High |
| Utility-Based | Medium (ms) | High | Medium |
| Learning | Fast (ms) | Very High | High |

### Reasoning System Comparison

| System | Certainty | Learning | Computational Cost |
|--------|-----------|----------|-------------------|
| Deductive | Absolute | No | Low |
| Inductive | Probabilistic | Yes | Medium |
| Probabilistic | Quantified | No | Low |

---

**This comprehensive guide covers all AI algorithms implemented in the system with theoretical foundations, implementation details, and practical examples.**
