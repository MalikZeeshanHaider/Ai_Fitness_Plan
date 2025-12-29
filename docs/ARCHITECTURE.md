# 🏗️ System Architecture

## Table of Contents

- [Overview](#overview)
- [Architecture Principles](#architecture-principles)
- [Layer Details](#layer-details)
- [Design Patterns](#design-patterns)
- [Data Flow](#data-flow)
- [Component Interactions](#component-interactions)
- [Scalability & Extensibility](#scalability--extensibility)

---

## Overview

The **AI Gym Workout Recommendation System** is built using **Clean Architecture** principles, ensuring separation of concerns, testability, and maintainability. The system is divided into four distinct layers, each with specific responsibilities.

### Architecture Diagram

```
┌───────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │  app.py     │  │ UI Components│  │  Custom CSS │           │
│  │ (Streamlit) │  │   & State   │  │   Styling   │           │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘           │
│         │                │                │                    │
└─────────┼────────────────┼────────────────┼────────────────────┘
          │                │                │
┌─────────▼────────────────▼────────────────▼────────────────────┐
│                    APPLICATION LAYER                            │
│  ┌──────────────────┐  ┌──────────────────┐                   │
│  │ Recommendation   │  │ Workout Plan     │                   │
│  │ Use Case         │  │ Generator        │                   │
│  └────────┬─────────┘  └────────┬─────────┘                   │
│  ┌────────┴─────────┐  ┌────────┴─────────┐                   │
│  │ Reasoning        │  │ PDF              │                   │
│  │ Explainer        │  │ Generator        │                   │
│  └────────┬─────────┘  └────────┬─────────┘                   │
└───────────┼──────────────────────┼─────────────────────────────┘
            │                      │
┌───────────▼──────────────────────▼─────────────────────────────┐
│                      DOMAIN LAYER                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   MODELS     │  │   SEARCH     │  │   AGENTS     │         │
│  │              │  │              │  │              │         │
│  │ • State      │  │ • BFS        │  │ • Reflex     │         │
│  │ • Exercise   │  │ • DFS        │  │ • Model      │         │
│  │ • Action     │  │ • UCS        │  │ • Goal       │         │
│  │ • Plan       │  │ • Greedy     │  │ • Utility    │         │
│  │              │  │ • A*         │  │ • Learning   │         │
│  └──────────────┘  │ • AND/OR     │  └──────────────┘         │
│                    └──────────────┘                            │
│  ┌──────────────────────────────────────────────────┐         │
│  │              REASONING SYSTEMS                    │         │
│  │  • Deductive Reasoner (rule engine)              │         │
│  │  • Inductive Reasoner (pattern learning)         │         │
│  │  • Probability Calculator (Bayesian)             │         │
│  └──────────────────────────────────────────────────┘         │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│                 INFRASTRUCTURE LAYER                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Data Loader  │  │ Data         │  │ Config       │          │
│  │              │  │ Validator    │  │ Loader       │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │ Data         │  │ Logger       │                            │
│  │ Preprocessor │  │              │                            │
│  └──────────────┘  └──────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼
                  ┌───────────────┐
                  │  GymDataset   │
                  │    .csv       │
                  └───────────────┘
```

---

## Architecture Principles

### 1. Clean Architecture

Based on Robert C. Martin's Clean Architecture:

- **Independence of Frameworks**: Business logic doesn't depend on Streamlit
- **Testability**: Business rules can be tested without UI or database
- **Independence of UI**: UI can change without affecting business logic
- **Independence of Database**: Can swap data sources without affecting logic
- **Independence of External Agencies**: Business rules don't know about external interfaces

### 2. SOLID Principles

#### Single Responsibility Principle (SRP)
- Each class has one reason to change
- Example: `WorkoutPlanGenerator` only generates plans, doesn't handle UI or data loading

#### Open/Closed Principle (OCP)
- Open for extension, closed for modification
- Example: New agents can be added by extending `Agent` base class

#### Liskov Substitution Principle (LSP)
- Derived classes are substitutable for base classes
- Example: Any `Agent` subclass can be used where `Agent` is expected

#### Interface Segregation Principle (ISP)
- Clients shouldn't depend on interfaces they don't use
- Example: Separate interfaces for different search strategies

#### Dependency Inversion Principle (DIP)
- Depend on abstractions, not concretions
- Example: Use cases depend on abstract `SearchProblem`, not concrete implementations

### 3. Separation of Concerns

Each layer has distinct responsibilities:
- **Presentation**: User interaction
- **Application**: Use case orchestration
- **Domain**: Business logic and algorithms
- **Infrastructure**: External dependencies

---

## Layer Details

### 1. Presentation Layer

**Responsibility**: User interface and interaction

**Components**:

```
src/presentation/
├── ui_components.py      # Reusable UI widgets
├── ui_state.py           # Session state management
└── custom_css.py         # Styling

app.py                    # Main application entry point
```

**Key Functions**:
- `render_header()`: Display application header
- `render_user_input_form()`: Collect user profile
- `render_workout_plan()`: Display generated plan
- `render_reasoning_explanations()`: Show AI reasoning
- `render_pdf_download()`: Download functionality

**Technologies**: Streamlit, HTML/CSS

**Dependencies**: Application Layer (Use Cases)

---

### 2. Application Layer

**Responsibility**: Orchestrate use cases and coordinate domain objects

**Components**:

```
src/application/
├── workout_recommendation_usecase.py   # Main use case
├── workout_plan_generator.py           # Plan generation service
├── reasoning_explainer.py              # AI explanation service
└── pdf_generator.py                    # Report generation service
```

#### WorkoutRecommendationUseCase

**Purpose**: Orchestrate the entire recommendation workflow

**Workflow**:
```python
1. Load exercise dataset
2. Apply safety reasoning (Deductive Reasoner)
3. Filter exercises based on equipment and safety
4. Select appropriate agent based on strategy
5. Generate workout plan (Search or Agent)
6. Calculate success probability
7. Generate alternative plans
8. Create reasoning explanations
```

**Input**: `RecommendationRequest`
- User state
- Available time
- Equipment
- Preferences
- Strategy
- Max exercises

**Output**: `RecommendationResponse`
- Workout plan
- Exercises list
- Safety warnings
- Success probability
- AI reasoning
- Alternatives

#### WorkoutPlanGenerator

**Purpose**: Generate workout plans using multiple algorithms

**Algorithms**:
1. **Greedy**: Maximize calories burned
2. **Balanced**: Round-robin across exercise types
3. **Variety-Optimized**: Maximum exercise diversity
4. **Time-Optimized**: Best calories/minute ratio
5. **Progressive**: Easy to hard difficulty progression

**Configuration**: `PlanGenerationConfig`
- Min/max exercises
- Target duration/calories
- Algorithm selection
- Variety enforcement
- Progressive difficulty

#### ReasoningExplainer

**Purpose**: Generate human-readable AI explanations

**Explanation Types**:
1. **Deductive**: Rule-based reasoning steps
2. **Inductive**: Learned patterns and confidence
3. **Probabilistic**: Probability calculations
4. **Search**: Search algorithm statistics
5. **Agent**: Agent decision rationale
6. **Plan**: Workout plan breakdown

**Detail Levels**:
- `BRIEF`: Short summary (1-2 sentences)
- `SUMMARY`: Key points (3-5 sentences)
- `DETAILED`: Comprehensive explanation (multiple paragraphs)
- `TECHNICAL`: Algorithm details and metrics

#### PDFGenerator

**Purpose**: Create downloadable workout reports

**Report Sections**:
1. Summary (goal, level, duration, calories, success probability)
2. Plan Table (exercise list with details)
3. Exercises (detailed descriptions, muscles, safety)
4. Reasoning (AI explanations)
5. Safety (warnings and guidelines)
6. Tips (goal-specific advice)

**Styles**: Professional, Colorful, Minimal, Detailed

---

### 3. Domain Layer

**Responsibility**: Core business logic and AI algorithms

#### 3.1 Models

```
src/domain/models/
├── state.py          # User fitness state (immutable)
├── action.py         # Workout actions
├── exercise.py       # Exercise model with metadata
└── workout_plan.py   # Workout plan with exercises
```

##### State
- **Immutable**: Uses `@dataclass(frozen=True)`
- **Attributes**: age, weight, height, fitness_level, energy, goal, injuries
- **Methods**: 
  - `apply_action()`: Returns new state after action
  - `calculate_bmi()`: Body Mass Index calculation
  - `get_target_heart_rate()`: Max heart rate calculation

##### Exercise
- **Attributes**: name, type, difficulty, duration, calories, equipment, muscles, description, safety_notes
- **Types**: CARDIO, STRENGTH, FLEXIBILITY, HIIT, CORE, BALANCE
- **Difficulty**: EASY, MEDIUM, HARD

##### WorkoutPlan
- **Composition**: List of exercises + metadata
- **Methods**:
  - `calculate_total_duration()`: Sum of exercise durations
  - `calculate_total_calories()`: Sum of calories burned
  - `calculate_variety_score()`: Type diversity (0-1)
  - `get_exercise_types()`: Unique exercise types
  - `validate()`: Check plan constraints

#### 3.2 Search Algorithms

```
src/domain/search/
├── search_problem.py      # Abstract SearchProblem base
├── uninformed_search.py   # BFS, DFS, UCS
├── informed_search.py     # Greedy, A*
└── and_or_tree.py         # AND/OR tree for alternatives
```

##### SearchProblem (Abstract Base)
```python
class SearchProblem(ABC):
    @abstractmethod
    def get_initial_state(self) -> State: ...
    
    @abstractmethod
    def is_goal_state(self, state: State) -> bool: ...
    
    @abstractmethod
    def get_actions(self, state: State) -> List[Action]: ...
    
    @abstractmethod
    def get_result(self, state: State, action: Action) -> State: ...
    
    @abstractmethod
    def get_cost(self, state: State, action: Action) -> float: ...
    
    @abstractmethod
    def heuristic(self, state: State) -> float: ...
```

##### BFS (Breadth-First Search)
- **Strategy**: FIFO queue
- **Complete**: ✅ Yes
- **Optimal**: ✅ Yes (unweighted graphs)
- **Time**: O(b^d)
- **Space**: O(b^d)

##### DFS (Depth-First Search)
- **Strategy**: LIFO stack
- **Complete**: ❌ No (infinite paths)
- **Optimal**: ❌ No
- **Time**: O(b^m)
- **Space**: O(bm)

##### UCS (Uniform Cost Search)
- **Strategy**: Priority queue (lowest path cost)
- **Complete**: ✅ Yes
- **Optimal**: ✅ Yes
- **Time**: O(b^(1+⌊C*/ε⌋))
- **Space**: O(b^(1+⌊C*/ε⌋))

##### Greedy Best-First Search
- **Strategy**: Priority queue (lowest heuristic)
- **Complete**: ❌ No
- **Optimal**: ❌ No
- **Time**: O(b^m)
- **Space**: O(b^m)

##### A* Search
- **Strategy**: Priority queue (f(n) = g(n) + h(n))
- **Complete**: ✅ Yes
- **Optimal**: ✅ Yes (with admissible heuristic)
- **Time**: O(b^d)
- **Space**: O(b^d)
- **Heuristic**: Must be admissible (never overestimate)

#### 3.3 Intelligent Agents

```
src/domain/agents/
├── agent.py                # Abstract Agent base
├── reflex_agent.py         # SimpleReflexAgent
├── model_based_agent.py    # ModelBasedAgent
├── goal_based_agent.py     # GoalBasedAgent
├── utility_based_agent.py  # UtilityBasedAgent
└── learning_agent.py       # LearningAgent
```

##### Agent Hierarchy

```
Agent (ABC)
├── SimpleReflexAgent
│   └── Uses: if-then rules
│   └── Example: Safety checks
│
├── ModelBasedAgent
│   └── Maintains: Internal world model
│   └── Example: Track user progress
│
├── GoalBasedAgent
│   └── Uses: Goal-directed planning
│   └── Example: Achieve fitness goal
│
├── UtilityBasedAgent
│   └── Uses: Utility function maximization
│   └── Example: Optimize multiple objectives
│
└── LearningAgent
    └── Uses: Experience-based improvement
    └── Example: Learn from workout history
```

##### SimpleReflexAgent
```python
def choose_action(self, percept: State) -> Action:
    # Rule-based decisions
    if percept.has_injury("knee"):
        return self._avoid_knee_exercises()
    if percept.current_energy < 5:
        return self._low_intensity_action()
    ...
```

##### ModelBasedAgent
```python
def choose_action(self, percept: State) -> Action:
    self._update_internal_model(percept)
    return self._select_action_from_model()
```

##### GoalBasedAgent
```python
def choose_action(self, percept: State) -> Action:
    goal = self._extract_goal(percept)
    return self._plan_to_achieve_goal(goal)
```

##### UtilityBasedAgent
```python
def choose_action(self, percept: State) -> Action:
    actions = self._get_possible_actions(percept)
    return max(actions, key=lambda a: self._utility(a, percept))
```

##### LearningAgent
```python
def choose_action(self, percept: State) -> Action:
    if self._should_explore():
        return self._explore()
    return self._exploit_learned_policy(percept)
```

#### 3.4 Reasoning Systems

```
src/domain/reasoning/
├── deductive_reasoner.py      # Forward chaining
├── inductive_reasoner.py      # Pattern learning
└── probability_calculator.py  # Bayesian inference
```

##### Deductive Reasoner
- **Type**: Forward chaining inference engine
- **Input**: Facts + Rules
- **Output**: Derived conclusions
- **Algorithm**: Modus Ponens
- **Example**:
  ```
  Fact: has_injury("knee")
  Rule: IF has_injury("knee") THEN avoid("squats")
  Conclusion: avoid("squats")
  ```

##### Inductive Reasoner
- **Type**: Pattern learning from data
- **Input**: Historical workout data
- **Output**: Patterns with confidence scores
- **Algorithm**: Frequency analysis
- **Example**:
  ```
  Pattern: "weight_loss" users → cardio (confidence: 0.85)
  Pattern: "muscle_gain" users → strength (confidence: 0.92)
  ```

##### Probability Calculator
- **Type**: Bayesian probability calculations
- **Formulas**:
  - P(A|B) = P(B|A) * P(A) / P(B)
  - P(A∪B) = P(A) + P(B) - P(A∩B)
- **Use Cases**:
  - Success probability calculation
  - Risk assessment
  - Confidence scoring

---

### 4. Infrastructure Layer

**Responsibility**: External dependencies and technical concerns

```
src/infrastructure/
├── config/
│   └── config_loader.py       # Load config.yaml
├── data/
│   ├── data_loader.py         # Load GymDataset.csv
│   ├── data_validator.py      # Validate data integrity
│   └── data_preprocessor.py   # Clean and transform data
└── logging/
    └── logger.py              # Logging configuration
```

#### DataLoader
- Loads exercise dataset from CSV
- Caches data for performance
- Validates data format
- Converts to Exercise objects

#### DataValidator
- Schema validation
- Range checks (age, weight, etc.)
- Required field validation
- Data type validation

#### DataPreprocessor
- Remove duplicates
- Handle missing values
- Normalize data
- Feature engineering

---

## Design Patterns

### 1. Strategy Pattern
**Used in**: Agent selection
```python
class RecommendationStrategy(Enum):
    SIMPLE_REFLEX = "simple_reflex"
    MODEL_BASED = "model_based"
    GOAL_BASED = "goal_based"
    UTILITY_BASED = "utility_based"
    LEARNING = "learning"
```

### 2. Factory Pattern
**Used in**: Agent creation
```python
def _select_agent(strategy: RecommendationStrategy) -> Agent:
    if strategy == RecommendationStrategy.SIMPLE_REFLEX:
        return SimpleReflexAgent()
    elif strategy == RecommendationStrategy.MODEL_BASED:
        return ModelBasedAgent()
    # ...
```

### 3. Builder Pattern
**Used in**: WorkoutPlan construction
```python
plan = WorkoutPlan(
    exercises=[],
    user_goal="weight_loss",
    target_duration=60
)
```

### 4. Singleton Pattern
**Used in**: DataLoader (cache)
```python
class DataLoader:
    _instance = None
    _cache = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### 5. Repository Pattern
**Used in**: Data access abstraction
```python
class ExerciseRepository:
    def get_by_id(self, exercise_id: int) -> Exercise: ...
    def get_by_type(self, ex_type: ExerciseType) -> List[Exercise]: ...
    def get_by_difficulty(self, difficulty: DifficultyLevel) -> List[Exercise]: ...
```

### 6. Use Case Pattern
**Used in**: Application layer orchestration
```python
class WorkoutRecommendationUseCase:
    def execute(self, request: RecommendationRequest) -> RecommendationResponse:
        # Orchestrate domain objects
        pass
```

---

## Data Flow

### End-to-End Flow

```
1. User Input (Presentation)
   └─> Form submission with user profile
   
2. Request Creation (Application)
   └─> Create RecommendationRequest
   
3. Use Case Execution (Application)
   ├─> Load exercises (Infrastructure)
   ├─> Apply safety reasoning (Domain - Reasoning)
   ├─> Filter exercises (Domain - Models)
   ├─> Select agent (Domain - Agents)
   ├─> Generate plan (Domain - Search/Agents)
   ├─> Calculate probability (Domain - Reasoning)
   └─> Create response
   
4. Explanation Generation (Application)
   └─> Generate natural language explanations
   
5. PDF Generation (Application)
   └─> Create downloadable report
   
6. Display Results (Presentation)
   └─> Render workout plan, metrics, explanations
```

### Data Transformation Pipeline

```
CSV Data → Exercise Objects → Filtered Exercises → Workout Plan → User Display

Raw CSV
  ↓ DataLoader.load()
Exercise Objects
  ↓ _filter_exercises()
Safe Exercises
  ↓ Agent.choose_action() / A*.search()
Selected Exercises
  ↓ WorkoutPlanGenerator.generate()
Workout Plan
  ↓ ReasoningExplainer.explain()
Explanations
  ↓ PDFGenerator.create_report()
PDF Report
  ↓ UI Components
User Interface
```

---

## Component Interactions

### Sequence Diagram: Generate Workout Plan

```
User → UI → UseCase → DataLoader → Domain → UI

1. User fills form
2. UI creates RecommendationRequest
3. UseCase receives request
4. UseCase loads exercises from DataLoader
5. UseCase applies DeductiveReasoner for safety
6. UseCase filters exercises
7. UseCase selects Agent based on strategy
8. Agent/Search generates exercise sequence
9. UseCase creates WorkoutPlan
10. UseCase calculates success probability
11. ReasoningExplainer generates explanations
12. PDFGenerator creates report
13. UseCase returns RecommendationResponse
14. UI displays results
```

### Class Diagram: Core Components

```
┌─────────────────────┐
│ RecommendationUseCase│
├─────────────────────┤
│ + execute()         │
│ - _filter_exercises()│
│ - _select_agent()   │
└──────┬──────────────┘
       │ uses
       ├────────┐
       ▼        ▼
┌──────────┐ ┌────────┐
│ Agent    │ │ Search │
├──────────┤ ├────────┤
│ +choose()│ │ +solve()│
└──────────┘ └────────┘
       │         │
       └────┬────┘
            ▼
     ┌──────────────┐
     │ WorkoutPlan  │
     ├──────────────┤
     │ +exercises[] │
     │ +validate()  │
     └──────────────┘
```

---

## Scalability & Extensibility

### Adding New Search Algorithms

1. Create new class extending `SearchProblem` or implement search function
2. Register in `informed_search.py` or `uninformed_search.py`
3. Add to strategy enum
4. No changes required to UI or Use Cases

### Adding New Agents

1. Create new class extending `Agent`
2. Implement `choose_action()` method
3. Add to `RecommendationStrategy` enum
4. Update `_select_agent()` in UseCase
5. No changes required to UI

### Adding New Exercise Types

1. Add to `ExerciseType` enum
2. Update CSV dataset
3. Update UI form options
4. No changes required to business logic

### Adding New Generation Algorithms

1. Add to `GenerationAlgorithm` enum
2. Implement selection method in `WorkoutPlanGenerator`
3. Update UI algorithm selector
4. No changes required to Use Cases

### Performance Optimization Points

1. **Caching**: Exercise dataset cached in DataLoader
2. **Lazy Loading**: Load only required data
3. **Parallel Processing**: Generate alternatives in parallel
4. **Memoization**: Cache search results
5. **Database**: Replace CSV with database for large datasets

---

## Testing Strategy

### Unit Tests
- Test each layer independently
- Mock dependencies
- Test edge cases

### Integration Tests
- Test layer interactions
- Verify data flow
- Test use cases end-to-end

### UI Tests
- Test form validation
- Test user interactions
- Test error handling

---

## Security Considerations

1. **Input Validation**: Validate all user inputs
2. **Data Sanitization**: Clean data before processing
3. **Error Handling**: Don't expose internal errors
4. **Session Management**: Secure session state
5. **Dependency Updates**: Keep dependencies updated

---

## Deployment Architecture

```
┌─────────────────────────────────────┐
│         Load Balancer               │
└───────┬─────────────┬───────────────┘
        │             │
┌───────▼─────┐ ┌────▼──────────┐
│ Streamlit   │ │ Streamlit     │
│ Instance 1  │ │ Instance 2    │
└───────┬─────┘ └────┬──────────┘
        │             │
┌───────▼─────────────▼───────────┐
│      Shared Data Store           │
│  (PostgreSQL / MongoDB)          │
└──────────────────────────────────┘
```

---

**This architecture ensures maintainability, testability, and scalability while adhering to SOLID principles and Clean Architecture.**
