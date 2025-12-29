# 📖 Usage Guide

## Table of Contents

- [Getting Started](#getting-started)
- [Basic Usage](#basic-usage)
- [Advanced Examples](#advanced-examples)
- [API Reference](#api-reference)
- [Tips & Best Practices](#tips--best-practices)
- [Troubleshooting](#troubleshooting)

---

## Getting Started

### Prerequisites

Ensure you have completed the installation steps from [README.md](../README.md).

### Running the Application

```bash
# Navigate to project directory
cd AI_GYM_PROJECT

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Run the application
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

---

## Basic Usage

### Example 1: First-Time Beginner

**Scenario**: 25-year-old beginner wants to start fitness journey.

#### Step 1: Fill Profile
```
Personal Information:
- Age: 25
- Weight: 80 kg
- Height: 175 cm
- Experience: Beginner
- Energy Level: 7/10

Fitness Goals:
- Primary Goal: General Fitness

Workout Preferences:
- Available Time: 30 minutes
- Maximum Exercises: 4

Available Equipment:
- Resistance Bands
- Include Bodyweight Exercises: ✓

Health Considerations:
- No injuries
```

#### Step 2: Configure Settings (Sidebar)
```
Generation Algorithm: Balanced
AI Strategy: Simple Reflex
Explanation Detail: Summary
Report Style: Professional
```

#### Step 3: Generate Plan
Click "Generate Workout Plan 🚀"

#### Expected Output
```
Success Probability: 78.5%

Metrics:
- 4 Exercises
- 30 Minutes
- 250 Calories
- 75% Variety

Exercises:
1. Jumping Jacks (Cardio, Easy, 5 min, 50 cal)
2. Push-ups (Strength, Easy, 10 min, 80 cal)
3. Bodyweight Squats (Strength, Easy, 10 min, 70 cal)
4. Cat-Cow Stretch (Flexibility, Easy, 5 min, 50 cal)
```

---

### Example 2: Weight Loss Focus

**Scenario**: 35-year-old with weight loss goal.

#### Profile
```python
from src.application.workout_recommendation_usecase import (
    WorkoutRecommendationUseCase,
    RecommendationRequest,
    RecommendationStrategy
)
from src.domain.models.state import State
from src.infrastructure.data.data_loader import DataLoader

# Initialize
data_loader = DataLoader()
use_case = WorkoutRecommendationUseCase(data_loader)

# Create user profile
state = State(
    age=35,
    weight=85.0,
    height=170.0,
    fitness_level="intermediate",
    current_energy=8,
    goal="weight_loss",
    injuries=None,
    exercise_history=[]
)

# Create request
request = RecommendationRequest(
    current_state=state,
    available_time=45,
    available_equipment=["Dumbbells", "Treadmill", "None"],
    preferences={"intensity": "high"},
    strategy=RecommendationStrategy.GREEDY_BEST_FIRST,
    max_exercises=6
)

# Generate recommendation
response = use_case.execute(request)

# Display results
print(f"✅ Success Probability: {response.success_probability * 100:.1f}%")
print(f"📊 Total Calories: {response.workout_plan.calculate_total_calories()}")
print(f"⏱️  Duration: {response.workout_plan.calculate_total_duration()} minutes")

for idx, exercise in enumerate(response.workout_plan.exercises, 1):
    print(f"{idx}. {exercise.name} ({exercise.calories_burned} cal)")
```

#### Output
```
✅ Success Probability: 82.3%
📊 Total Calories: 520
⏱️  Duration: 45 minutes

1. Running (250 cal)
2. Burpees (150 cal)
3. Mountain Climbers (80 cal)
4. Jump Rope (40 cal)
```

---

### Example 3: Muscle Gain with Equipment

**Scenario**: Advanced lifter with full gym access.

#### Configuration
```python
state = State(
    age=28,
    weight=75.0,
    height=180.0,
    fitness_level="advanced",
    current_energy=9,
    goal="muscle_gain",
    injuries=None,
    exercise_history=["bench_press", "squats", "deadlifts"]
)

request = RecommendationRequest(
    current_state=state,
    available_time=90,
    available_equipment=[
        "Barbell",
        "Dumbbells",
        "Bench",
        "Pull-up Bar",
        "Squat Rack"
    ],
    preferences={
        "split": "upper_body",
        "progressive_overload": True
    },
    strategy=RecommendationStrategy.UTILITY_BASED,
    max_exercises=8
)

response = use_case.execute(request)
```

#### Result
```
Workout Plan: Upper Body Hypertrophy
Success Probability: 91.2%

Exercises:
1. Barbell Bench Press (Strength, Hard, 15 min, 180 cal)
2. Pull-ups (Strength, Hard, 12 min, 150 cal)
3. Overhead Press (Strength, Medium, 12 min, 140 cal)
4. Dumbbell Rows (Strength, Hard, 15 min, 160 cal)
5. Bicep Curls (Strength, Medium, 10 min, 100 cal)
6. Tricep Dips (Strength, Hard, 12 min, 130 cal)
7. Lateral Raises (Strength, Medium, 10 min, 90 cal)
8. Face Pulls (Strength, Medium, 4 min, 50 cal)

Total: 90 minutes, 1000 calories
```

---

### Example 4: Safety-First with Injuries

**Scenario**: User with knee and lower back injuries.

#### Profile with Injuries
```python
state = State(
    age=45,
    weight=70.0,
    height=168.0,
    fitness_level="intermediate",
    current_energy=6,
    goal="general_fitness",
    injuries=["Lower Back", "Knee"],  # ⚠️ Current injuries
    exercise_history=[]
)

request = RecommendationRequest(
    current_state=state,
    available_time=30,
    available_equipment=["Resistance Bands", "None"],
    preferences={"priority": "safety"},
    strategy=RecommendationStrategy.SIMPLE_REFLEX,  # Safety-first
    max_exercises=5
)

response = use_case.execute(request)

# Check safety warnings
print("⚠️ Safety Warnings:")
for warning in response.safety_warnings:
    print(f"  - {warning}")

print("\n✅ Safe Exercises:")
for exercise in response.workout_plan.exercises:
    print(f"  - {exercise.name}")
```

#### Output
```
⚠️ Safety Warnings:
  - Avoid: Squats (knee stress)
  - Avoid: Deadlifts (lower back stress)
  - Avoid: Running (knee impact)
  - Recommended: Low-impact exercises

✅ Safe Exercises:
  - Swimming (Full body, no impact)
  - Resistance Band Pulls (Upper body, safe)
  - Plank (Core, no back stress)
  - Seated Leg Extensions (Knee-friendly)
  - Arm Circles (Mobility, low intensity)

Success Probability: 85.7%
```

---

## Advanced Examples

### Example 5: Multiple Algorithms Comparison

Compare different generation algorithms for the same profile.

```python
from src.application.workout_plan_generator import (
    WorkoutPlanGenerator,
    PlanGenerationConfig,
    GenerationAlgorithm
)

# Create generator
generator = WorkoutPlanGenerator()

# User state
state = State(
    age=30,
    weight=75.0,
    height=175.0,
    fitness_level="intermediate",
    current_energy=7,
    goal="weight_loss",
    injuries=None,
    exercise_history=[]
)

# Load exercises
data_loader = DataLoader()
exercises = data_loader.load_exercises()

# Test all algorithms
algorithms = [
    GenerationAlgorithm.GREEDY,
    GenerationAlgorithm.BALANCED,
    GenerationAlgorithm.VARIETY_OPTIMIZED,
    GenerationAlgorithm.TIME_OPTIMIZED,
    GenerationAlgorithm.PROGRESSIVE
]

print("Algorithm Comparison:\n")

for algo in algorithms:
    config = PlanGenerationConfig(
        min_exercises=4,
        max_exercises=6,
        target_duration=45,
        algorithm=algo
    )
    
    plan = generator.generate(exercises, state, config)
    
    print(f"{algo.value.upper()}:")
    print(f"  Exercises: {len(plan.exercises)}")
    print(f"  Duration: {plan.calculate_total_duration()} min")
    print(f"  Calories: {plan.calculate_total_calories()}")
    print(f"  Variety: {plan.calculate_variety_score():.2f}\n")
```

#### Output
```
Algorithm Comparison:

GREEDY:
  Exercises: 4
  Duration: 45 min
  Calories: 500
  Variety: 0.50

BALANCED:
  Exercises: 5
  Duration: 45 min
  Calories: 420
  Variety: 0.80

VARIETY_OPTIMIZED:
  Exercises: 6
  Duration: 45 min
  Calories: 380
  Variety: 1.00

TIME_OPTIMIZED:
  Exercises: 3
  Duration: 45 min
  Calories: 550
  Variety: 0.67

PROGRESSIVE:
  Exercises: 5
  Duration: 45 min
  Calories: 400
  Variety: 0.60
```

---

### Example 6: Custom Heuristic Function

Create a custom heuristic for A* search.

```python
from src.domain.search.search_problem import SearchProblem
from src.domain.search.informed_search import a_star_search
from src.domain.models.state import State
from src.domain.models.action import Action

class CustomWorkoutProblem(SearchProblem):
    def __init__(self, initial_state, goal_calories=500):
        self.initial = initial_state
        self.goal_calories = goal_calories
    
    def get_initial_state(self) -> State:
        return self.initial
    
    def is_goal_state(self, state: State) -> bool:
        total_calories = sum(e.calories_burned for e in state.exercise_history)
        return total_calories >= self.goal_calories
    
    def get_actions(self, state: State) -> List[Action]:
        # Return available exercises as actions
        return [Action(ex) for ex in self.available_exercises]
    
    def get_result(self, state: State, action: Action) -> State:
        # Apply action to get new state
        return state.apply_action(action)
    
    def get_cost(self, state: State, action: Action) -> float:
        # Cost = time (minimize duration)
        return action.exercise.duration_minutes
    
    def heuristic(self, state: State) -> float:
        """
        Custom heuristic: Estimate remaining exercises needed.
        
        h(n) = (remaining_calories / max_calories_per_exercise)
        """
        current_calories = sum(e.calories_burned for e in state.exercise_history)
        remaining = max(0, self.goal_calories - current_calories)
        
        # Assume best exercise burns 200 calories
        max_cal_per_exercise = 200
        
        estimated_exercises = remaining / max_cal_per_exercise
        avg_exercise_duration = 15  # minutes
        
        return estimated_exercises * avg_exercise_duration

# Use custom problem
problem = CustomWorkoutProblem(initial_state, goal_calories=600)
solution = a_star_search(problem)

if solution:
    print("Found optimal solution!")
    print(f"Path cost: {solution.path_cost} minutes")
    print(f"Exercises: {len(solution.path)}")
```

---

### Example 7: Learning Agent with Feedback

Use learning agent with feedback loop.

```python
from src.domain.agents.learning_agent import LearningAgent

# Initialize agent with dataset
data_loader = DataLoader()
dataset = data_loader.load_dataset()
agent = LearningAgent(dataset)

# Simulate workout sessions with feedback
sessions = []

for session_num in range(10):
    # User state
    state = State(
        age=30,
        weight=75.0 - (session_num * 0.5),  # Progressive weight loss
        height=175.0,
        fitness_level="intermediate",
        current_energy=7 + (session_num % 3),
        goal="weight_loss",
        injuries=None,
        exercise_history=sessions
    )
    
    # Agent chooses action
    action = agent.choose_action(state)
    
    # Simulate workout
    success = random() > 0.3  # 70% success rate
    result = 1.0 if success else 0.0
    
    # Provide feedback
    agent.update(state, action, result)
    
    sessions.append({
        'session': session_num + 1,
        'exercise': action.exercise.name,
        'success': success,
        'weight': state.weight
    })
    
    print(f"Session {session_num + 1}: {action.exercise.name} - {'✅' if success else '❌'}")

print(f"\nAgent learned from {len(sessions)} sessions")
print(f"Success rate: {sum(s['success'] for s in sessions) / len(sessions) * 100:.1f}%")
```

---

### Example 8: Explanation Generation

Generate detailed AI explanations.

```python
from src.application.reasoning_explainer import (
    ReasoningExplainer,
    DetailLevel
)

explainer = ReasoningExplainer()

# After generating workout plan
response = use_case.execute(request)

# Generate comprehensive explanation
explanations = explainer.create_comprehensive_explanation(
    workout_plan=response.workout_plan,
    success_probability=response.success_probability,
    detail_level=DetailLevel.DETAILED
)

# Display each explanation type
for explanation in explanations:
    print(f"\n{'='*60}")
    print(f"📋 {explanation.title}")
    print(f"{'='*60}")
    print(explanation.content)
    
    if explanation.reasoning_steps:
        print("\nReasoning Steps:")
        for i, step in enumerate(explanation.reasoning_steps, 1):
            print(f"  {i}. {step}")
    
    if explanation.confidence:
        print(f"\nConfidence: {explanation.confidence * 100:.1f}%")

# Export to Markdown
markdown = explanation.to_markdown()
with open("workout_explanation.md", "w") as f:
    f.write(markdown)
print("\n✅ Explanation saved to workout_explanation.md")
```

---

### Example 9: PDF Report Generation

Create and customize PDF reports.

```python
from src.application.pdf_generator import PDFGenerator, PDFStyle

pdf_gen = PDFGenerator()

# Generate report
report = pdf_gen.create_workout_report(
    workout_plan=response.workout_plan,
    user_state=state,
    explanations=explanations,
    safety_warnings=response.safety_warnings,
    success_probability=response.success_probability,
    style=PDFStyle.PROFESSIONAL
)

# Save as PDF
pdf_bytes = pdf_gen.generate_pdf(report)
with open("workout_plan.pdf", "wb") as f:
    f.write(pdf_bytes)

# Save as Markdown
markdown_content = pdf_gen.generate_markdown(report)
with open("workout_plan.md", "w") as f:
    f.write(markdown_content)

print("✅ Reports generated:")
print("  - workout_plan.pdf")
print("  - workout_plan.md")
```

---

### Example 10: Batch Processing

Generate plans for multiple users.

```python
import pandas as pd

# User profiles
users = [
    {"age": 25, "weight": 80, "goal": "weight_loss"},
    {"age": 35, "weight": 70, "goal": "muscle_gain"},
    {"age": 45, "weight": 75, "goal": "endurance"},
    {"age": 55, "weight": 68, "goal": "flexibility"},
]

results = []

for user in users:
    state = State(
        age=user["age"],
        weight=user["weight"],
        height=170.0,
        fitness_level="intermediate",
        current_energy=7,
        goal=user["goal"],
        injuries=None,
        exercise_history=[]
    )
    
    request = RecommendationRequest(
        current_state=state,
        available_time=45,
        available_equipment=["Dumbbells", "None"],
        strategy=RecommendationStrategy.BALANCED
    )
    
    response = use_case.execute(request)
    
    results.append({
        'age': user['age'],
        'goal': user['goal'],
        'exercises': len(response.workout_plan.exercises),
        'duration': response.workout_plan.calculate_total_duration(),
        'calories': response.workout_plan.calculate_total_calories(),
        'success_prob': response.success_probability
    })

# Create DataFrame
df = pd.DataFrame(results)
print(df)

# Save results
df.to_csv("batch_results.csv", index=False)
print("\n✅ Results saved to batch_results.csv")
```

---

## API Reference

### Core Classes

#### State
```python
@dataclass(frozen=True)
class State:
    age: int
    weight: float
    height: float
    fitness_level: str
    current_energy: int
    goal: str
    injuries: Optional[List[str]]
    exercise_history: List[Exercise]
    
    def apply_action(self, action: Action) -> 'State': ...
    def calculate_bmi(self) -> float: ...
    def get_target_heart_rate(self) -> Tuple[int, int]: ...
```

#### RecommendationRequest
```python
@dataclass
class RecommendationRequest:
    current_state: State
    available_time: int
    available_equipment: List[str]
    preferences: Dict[str, Any]
    strategy: RecommendationStrategy
    max_exercises: int = 6
```

#### RecommendationResponse
```python
@dataclass
class RecommendationResponse:
    workout_plan: WorkoutPlan
    exercises: List[Exercise]
    reasoning: List[str]
    safety_warnings: List[str]
    success_probability: float
    alternatives: List[WorkoutPlan]
    agent_used: str
    search_stats: Dict[str, Any]
```

---

## Tips & Best Practices

### 1. Choosing the Right Strategy

- **Simple Reflex**: Safety-first, injuries present
- **Model-Based**: Track progress over time
- **Goal-Based**: Long-term fitness planning
- **Utility-Based**: Multiple objectives (balance goals)
- **Learning**: Personalized, adaptive recommendations

### 2. Algorithm Selection

- **Greedy**: Maximize single objective (calories, duration)
- **Balanced**: Diverse exercise types
- **Variety-Optimized**: Maximum variety (prevent boredom)
- **Time-Optimized**: Limited time, maximum efficiency
- **Progressive**: Gradual difficulty increase

### 3. Optimal Time Ranges

- **15-30 min**: Quick workout, high intensity
- **30-45 min**: Standard workout, balanced
- **45-60 min**: Comprehensive workout, multiple types
- **60-90 min**: Advanced, muscle-building focus

### 4. Success Probability Interpretation

- **> 80%**: Highly achievable
- **60-80%**: Moderately challenging
- **40-60%**: Challenging, consider modifications
- **< 40%**: Consider reducing intensity/duration

### 5. Injury Management

Always specify injuries in the profile. The system will:
- Filter out contraindicated exercises
- Suggest alternatives
- Provide safety warnings
- Adjust difficulty level

---

## Troubleshooting

### Issue: No exercises generated

**Solution**:
- Check equipment availability
- Verify goal is valid
- Ensure time > 15 minutes
- Try different strategy

### Issue: Success probability too low

**Solution**:
- Reduce workout duration
- Lower difficulty level
- Increase energy level in profile
- Remove conflicting constraints

### Issue: Limited exercise variety

**Solution**:
- Use VARIETY_OPTIMIZED algorithm
- Increase max_exercises
- Add more equipment types
- Try BALANCED strategy

### Issue: Application won't start

**Solution**:
```bash
# Verify installation
pip install -r requirements.txt

# Check Streamlit installation
streamlit --version

# Clear cache
streamlit cache clear

# Restart application
streamlit run app.py
```

### Issue: Data loading errors

**Solution**:
- Verify `data/GymDataset.csv` exists
- Check file permissions
- Validate CSV format
- Re-download dataset if corrupted

---

## Additional Resources

- [README.md](../README.md): Project overview
- [ARCHITECTURE.md](ARCHITECTURE.md): System architecture
- [ALGORITHMS.md](ALGORITHMS.md): Algorithm details
- Inline documentation: Check docstrings in code

---

**For more examples and updates, check the project repository and documentation.**
