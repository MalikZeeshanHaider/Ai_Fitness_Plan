# 💪 AI Gym Workout Recommendation System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)

> **A simplified, easy-to-explain AI workout recommendation system using three intelligent agents and A* search algorithm.**

---

## 🎯 Overview

Generates **personalized workout plans** using a 4-step AI workflow:

1. 🛡️ **Simple Reflex Agent** - Safety filtering
2. 🎯 **Goal-Based Agent** - Goal definition
3. ⚖️ **Utility-Based Agent** - Exercise scoring  
4. 🔍 **A* Search** - Optimal plan generation

**Perfect for viva presentations!** ✅ Simple ✅ Academic ✅ Production-ready

---

## 🚀 Quick Start

```bash
# Install
pip install -r requirements.txt

# Run
streamlit run app.py
# OR
run.bat
```

Opens at `http://localhost:8501`

---

## 🤖 AI Components

### 1. Simple Reflex Agent (Safety)
- **Purpose**: Filter unsafe exercises
- **Method**: If-then rules
- **Example**: `IF knee injury THEN remove squats`
- **O(n) time**

### 2. Goal-Based Agent (Planning)
- **Purpose**: Define fitness goal
- **Goals**: Weight loss, muscle gain, endurance, general
- **Output**: Target state + direction
- **O(1) time**

### 3. Utility-Based Agent (Optimization)
- **Purpose**: Score exercises  
- **Formula**: `U = 0.4·Eff + 0.3·Safety + 0.2·Time + 0.1·Pref`
- **Output**: Ranked exercises
- **O(n log n) time**

### 4. A* Search (Optimal Solution)
- **Purpose**: Generate workout sequence
- **Formula**: `f(n) = g(n) + h(n)`
- **Properties**: Complete & Optimal
- **O(b^d) time**

---

## 📊 Example

**Input:**
- Goal: Weight Loss
- Level: Beginner
- Time: 45 min

**Output:**
```
1. Warm-up (5 min)
2. Running (15 min) - 150 kcal
3. Jump Rope (10 min) - 100 kcal
4. Burpees (8 min) - 80 kcal
5. Cool-down (2 min)

Total: 45 min, ~330 calories
```

---

## 🏗️ Architecture

```
UI (Streamlit)
    ↓
Application (Use Case)
    ↓
Domain (Agents + Search)
    ↓
Infrastructure (Data)
```

---

## 📁 Key Files

```
AI_GYM/
├── app.py                           # Main app
├── src/application/
│   └── streamlined_workout_usecase.py  # Workflow
├── src/domain/agents/
│   ├── simple_reflex_agent.py       # Safety filter
│   ├── goal_based_agent.py          # Goal planner
│   └── utility_based_agent.py       # Optimizer
└── src/domain/search/
    └── astar.py                      # A* search
```

---

## 🎓 Viva Q&A

**Q: Why these 3 agents?**
> - **Reflex**: Simple safety rules (if-then)
> - **Goal**: Define target to achieve
> - **Utility**: Balance multiple objectives

**Q: Why A*?**
> - Complete & optimal
> - Efficient with good heuristic
> - Better than BFS/DFS

**Q: Workflow order?**
> 1. Safety first (filter)
> 2. Define goal (plan)
> 3. Score options (rank)
> 4. Optimize (search)

---

## 📚 Docs

📖 [SIMPLIFIED_ARCHITECTURE.md](docs/SIMPLIFIED_ARCHITECTURE.md) - Full details  
📖 [ALGORITHMS.md](docs/ALGORITHMS.md) - AI algorithms  
📖 [USAGE_GUIDE.md](docs/USAGE_GUIDE.md) - User guide  

---

## ✅ AI Concepts

✅ Simple Reflex Agent  
✅ Goal-Based Agent  
✅ Utility-Based Agent  
✅ A* Search  
✅ Heuristic Functions  
✅ Clean Architecture  

---

## 🌟 Why This Project?

1. **Simple to explain** in viva
2. **Academic excellence** - maps to AI concepts
3. **Production quality** - clean code
4. **Well documented** - complete guides

**Perfect for AI course projects! 💯**

---

**Author**: AI Gym Team | December 2025
