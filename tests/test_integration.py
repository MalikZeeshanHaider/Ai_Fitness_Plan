"""
Integration Tests for AI Gym Workout Recommendation System.

Tests the complete workflow from user input to recommendation output.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.domain.models.state import State
from src.domain.models.exercise import ExerciseCategory, IntensityLevel
from src.infrastructure.data.data_loader import DataLoader
from src.application.workout_recommendation_usecase import (
    WorkoutRecommendationUseCase,
    RecommendationRequest,
    RecommendationStrategy
)
from src.application.workout_plan_generator import PlanGenerationConfig, GenerationAlgorithm
from src.application.reasoning_explainer import ReasoningExplainer, DetailLevel
from src.application.pdf_generator import PDFGenerator, PDFStyle


class TestEndToEndWorkflow:
    """Test complete workflow from input to output."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.data_loader = DataLoader()
        self.use_case = WorkoutRecommendationUseCase(self.data_loader)
    
    def test_basic_workout_generation(self):
        """Test basic workout generation for beginner."""
        # Create user state
        state = State(
            age=25,
            weight=70.0,
            height=175.0,
            fitness_level="beginner",
            current_energy=7,
            goal="general_fitness",
            injuries=None,
            exercise_history=[]
        )
        
        # Create request
        request = RecommendationRequest(
            current_state=state,
            available_time=30,
            available_equipment=["None"],
            preferences={},
            strategy=RecommendationStrategy.SIMPLE_REFLEX,
            max_exercises=5
        )
        
        # Execute
        response = self.use_case.execute(request)
        
        # Assertions
        assert response is not None
        assert response.workout_plan is not None
        assert len(response.workout_plan.exercises) > 0
        assert len(response.workout_plan.exercises) <= 5
        assert response.workout_plan.calculate_total_duration() <= 35  # Allow 5min buffer
        assert 0 <= response.success_probability <= 1.0
        
        print(f"✅ Basic workout generation: {len(response.workout_plan.exercises)} exercises")
    
    def test_weight_loss_workout(self):
        """Test weight loss focused workout."""
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
        
        request = RecommendationRequest(
            current_state=state,
            available_time=45,
            available_equipment=["Dumbbells", "None"],
            preferences={"intensity": "high"},
            strategy=RecommendationStrategy.GREEDY_BEST_FIRST,
            max_exercises=6
        )
        
        response = self.use_case.execute(request)
        
        # Weight loss should prioritize cardio
        cardio_count = sum(1 for ex in response.workout_plan.exercises 
                          if ex.category == ExerciseCategory.CARDIO)
        
        assert response.workout_plan.calculate_total_calories() > 300
        assert cardio_count > 0  # Should have some cardio exercises
        
        print(f"✅ Weight loss workout: {response.workout_plan.calculate_total_calories()} calories")
    
    def test_muscle_gain_workout(self):
        """Test muscle gain focused workout."""
        state = State(
            age=28,
            weight=75.0,
            height=180.0,
            fitness_level="advanced",
            current_energy=9,
            goal="muscle_gain",
            injuries=None,
            exercise_history=[]
        )
        
        request = RecommendationRequest(
            current_state=state,
            available_time=60,
            available_equipment=["Barbell", "Dumbbells", "Bench"],
            preferences={},
            strategy=RecommendationStrategy.UTILITY_BASED,
            max_exercises=7
        )
        
        response = self.use_case.execute(request)
        
        # Muscle gain should prioritize strength
        strength_count = sum(1 for ex in response.workout_plan.exercises 
                            if ex.category == ExerciseCategory.STRENGTH)
        
        assert strength_count >= len(response.workout_plan.exercises) / 2
        
        print(f"✅ Muscle gain workout: {strength_count} strength exercises")
    
    def test_injury_safety(self):
        """Test workout generation with injuries."""
        state = State(
            age=45,
            weight=70.0,
            height=168.0,
            fitness_level="intermediate",
            current_energy=6,
            goal="general_fitness",
            injuries=["Lower Back", "Knee"],
            exercise_history=[]
        )
        
        request = RecommendationRequest(
            current_state=state,
            available_time=30,
            available_equipment=["Resistance Bands", "None"],
            preferences={"priority": "safety"},
            strategy=RecommendationStrategy.SIMPLE_REFLEX,
            max_exercises=5
        )
        
        response = self.use_case.execute(request)
        
        # Should have safety warnings
        assert len(response.safety_warnings) > 0
        
        # All exercises should be safe (verified by agent)
        assert len(response.workout_plan.exercises) > 0
        
        print(f"✅ Safety test: {len(response.safety_warnings)} warnings, {len(response.workout_plan.exercises)} safe exercises")
    
    def test_all_strategies(self):
        """Test all agent strategies."""
        state = State(
            age=30,
            weight=75.0,
            height=175.0,
            fitness_level="intermediate",
            current_energy=7,
            goal="general_fitness",
            injuries=None,
            exercise_history=[]
        )
        
        strategies = [
            RecommendationStrategy.SIMPLE_REFLEX,
            RecommendationStrategy.MODEL_BASED,
            RecommendationStrategy.GOAL_BASED,
            RecommendationStrategy.UTILITY_BASED,
            RecommendationStrategy.LEARNING
        ]
        
        for strategy in strategies:
            request = RecommendationRequest(
                current_state=state,
                available_time=30,
                available_equipment=["None"],
                preferences={},
                strategy=strategy,
                max_exercises=5
            )
            
            response = self.use_case.execute(request)
            
            assert response is not None
            assert len(response.workout_plan.exercises) > 0
            
            print(f"✅ Strategy {strategy.value}: {len(response.workout_plan.exercises)} exercises")
    
    def test_all_algorithms(self):
        """Test all generation algorithms."""
        from src.application.workout_plan_generator import WorkoutPlanGenerator
        
        state = State(
            age=30,
            weight=75.0,
            height=175.0,
            fitness_level="intermediate",
            current_energy=7,
            goal="general_fitness",
            injuries=None,
            exercise_history=[]
        )
        
        generator = WorkoutPlanGenerator()
        exercises = self.data_loader.load_exercises()
        
        algorithms = [
            GenerationAlgorithm.GREEDY,
            GenerationAlgorithm.BALANCED,
            GenerationAlgorithm.VARIETY_OPTIMIZED,
            GenerationAlgorithm.TIME_OPTIMIZED,
            GenerationAlgorithm.PROGRESSIVE
        ]
        
        for algo in algorithms:
            config = PlanGenerationConfig(
                min_exercises=3,
                max_exercises=6,
                target_duration=30,
                algorithm=algo
            )
            
            plan = generator.generate(exercises, state, config)
            
            assert plan is not None
            assert len(plan.exercises) >= 3
            
            print(f"✅ Algorithm {algo.value}: {len(plan.exercises)} exercises, variety={plan.calculate_variety_score():.2f}")


class TestExplanationGeneration:
    """Test reasoning explanation generation."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.explainer = ReasoningExplainer()
        self.data_loader = DataLoader()
        self.use_case = WorkoutRecommendationUseCase(self.data_loader)
    
    def test_explanation_generation(self):
        """Test comprehensive explanation generation."""
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
        
        request = RecommendationRequest(
            current_state=state,
            available_time=45,
            available_equipment=["Dumbbells", "None"],
            preferences={},
            strategy=RecommendationStrategy.UTILITY_BASED,
            max_exercises=6
        )
        
        response = self.use_case.execute(request)
        
        # Generate explanations
        explanations = self.explainer.create_comprehensive_explanation(
            workout_plan=response.workout_plan,
            success_probability=response.success_probability,
            detail_level=DetailLevel.SUMMARY
        )
        
        assert len(explanations) > 0
        
        for explanation in explanations:
            assert explanation.title is not None
            assert explanation.content is not None or len(explanation.reasoning_steps) > 0
        
        print(f"✅ Generated {len(explanations)} explanations")
    
    def test_all_detail_levels(self):
        """Test all explanation detail levels."""
        from src.domain.models.workout_plan import WorkoutPlan
        from src.domain.models.exercise import Exercise
        
        exercise = Exercise(
            exercise_id="ex_running",
            name="Running",
            category=ExerciseCategory.CARDIO,
            difficulty="medium",
            typical_duration_minutes=20,
            calories_per_minute=10.0,
            equipment=["None"],
            primary_muscles=["Legs"],
            description="Cardio exercise",
            contraindications=["knee injury"]
        )
        
        plan = WorkoutPlan(
            exercises=[exercise],
            user_goal="weight_loss",
            target_duration=20
        )
        
        levels = [DetailLevel.BRIEF, DetailLevel.SUMMARY, DetailLevel.DETAILED, DetailLevel.TECHNICAL]
        
        for level in levels:
            explanations = self.explainer.create_comprehensive_explanation(
                workout_plan=plan,
                success_probability=0.8,
                detail_level=level
            )
            
            assert len(explanations) > 0
            print(f"✅ Detail level {level.value}: {len(explanations)} explanations")


class TestPDFGeneration:
    """Test PDF report generation."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.pdf_gen = PDFGenerator()
        self.data_loader = DataLoader()
        self.use_case = WorkoutRecommendationUseCase(self.data_loader)
        self.explainer = ReasoningExplainer()
    
    def test_pdf_report_creation(self):
        """Test PDF report creation."""
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
        
        request = RecommendationRequest(
            current_state=state,
            available_time=45,
            available_equipment=["Dumbbells"],
            preferences={},
            strategy=RecommendationStrategy.BALANCED,
            max_exercises=5
        )
        
        response = self.use_case.execute(request)
        
        explanations = self.explainer.create_comprehensive_explanation(
            workout_plan=response.workout_plan,
            success_probability=response.success_probability,
            detail_level=DetailLevel.SUMMARY
        )
        
        # Create report
        report = self.pdf_gen.create_workout_report(
            workout_plan=response.workout_plan,
            user_state=state,
            explanations=explanations,
            safety_warnings=response.safety_warnings,
            success_probability=response.success_probability,
            style=PDFStyle.PROFESSIONAL
        )
        
        assert report is not None
        assert report.title is not None
        assert len(report.sections) > 0
        
        print(f"✅ PDF report created with {len(report.sections)} sections")
    
    def test_all_pdf_styles(self):
        """Test all PDF styles."""
        from src.domain.models.workout_plan import WorkoutPlan
        from src.domain.models.exercise import Exercise
        
        state = State(
            age=30,
            weight=75.0,
            height=175.0,
            fitness_level="intermediate",
            current_energy=7,
            goal="general_fitness",
            injuries=None,
            exercise_history=[]
        )
        
        exercise = Exercise(
            exercise_id="ex_pushups",
            name="Push-ups",
            category=ExerciseCategory.STRENGTH,
            difficulty="medium",
            typical_duration_minutes=10,
            calories_per_minute=8.0,
            equipment=["None"],
            primary_muscles=["Chest", "Arms"],
            description="Upper body exercise",
            contraindications=[]
        )
        
        plan = WorkoutPlan(
            exercises=[exercise],
            user_goal="general_fitness",
            target_duration=10
        )
        
        styles = [PDFStyle.PROFESSIONAL, PDFStyle.COLORFUL, PDFStyle.MINIMAL, PDFStyle.DETAILED]
        
        for style in styles:
            report = self.pdf_gen.create_workout_report(
                workout_plan=plan,
                user_state=state,
                explanations=[],
                safety_warnings=[],
                success_probability=0.85,
                style=style
            )
            
            assert report is not None
            print(f"✅ PDF style {style.value}: {len(report.sections)} sections")
    
    def test_pdf_and_markdown_generation(self):
        """Test both PDF and Markdown generation."""
        from src.domain.models.workout_plan import WorkoutPlan
        from src.domain.models.exercise import Exercise
        
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
        
        exercise = Exercise(
            exercise_id="ex_running_2",
            name="Running",
            category=ExerciseCategory.CARDIO,
            difficulty="medium",
            typical_duration_minutes=20,
            calories_per_minute=10.0,
            equipment=["None"],
            primary_muscles=["Legs"],
            description="Cardio",
            contraindications=[]
        )
        
        plan = WorkoutPlan(
            exercises=[exercise],
            user_goal="weight_loss",
            target_duration=20
        )
        
        report = self.pdf_gen.create_workout_report(
            workout_plan=plan,
            user_state=state,
            explanations=[],
            safety_warnings=[],
            success_probability=0.8,
            style=PDFStyle.PROFESSIONAL
        )
        
        # Generate PDF
        pdf_bytes = self.pdf_gen.generate_pdf(report)
        assert pdf_bytes is not None
        assert len(pdf_bytes) > 0
        
        # Generate Markdown
        markdown = self.pdf_gen.generate_markdown(report)
        assert markdown is not None
        assert len(markdown) > 0
        assert "# " in markdown  # Should have markdown headers
        
        print(f"✅ PDF: {len(pdf_bytes)} bytes, Markdown: {len(markdown)} chars")


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.data_loader = DataLoader()
        self.use_case = WorkoutRecommendationUseCase(self.data_loader)
    
    def test_very_short_time(self):
        """Test with very short available time."""
        state = State(
            age=25,
            weight=70.0,
            height=175.0,
            fitness_level="beginner",
            current_energy=7,
            goal="general_fitness",
            injuries=None,
            exercise_history=[]
        )
        
        request = RecommendationRequest(
            current_state=state,
            available_time=15,  # Very short
            available_equipment=["None"],
            preferences={},
            strategy=RecommendationStrategy.TIME_OPTIMIZED,
            max_exercises=3
        )
        
        response = self.use_case.execute(request)
        
        assert response is not None
        assert len(response.workout_plan.exercises) > 0
        assert response.workout_plan.calculate_total_duration() <= 20  # Allow buffer
        
        print(f"✅ Short time test: {len(response.workout_plan.exercises)} exercises in {response.workout_plan.calculate_total_duration()} min")
    
    def test_low_energy(self):
        """Test with low energy level."""
        state = State(
            age=30,
            weight=75.0,
            height=175.0,
            fitness_level="intermediate",
            current_energy=3,  # Very low
            goal="general_fitness",
            injuries=None,
            exercise_history=[]
        )
        
        request = RecommendationRequest(
            current_state=state,
            available_time=30,
            available_equipment=["None"],
            preferences={},
            strategy=RecommendationStrategy.SIMPLE_REFLEX,
            max_exercises=5
        )
        
        response = self.use_case.execute(request)
        
        # Should recommend lower intensity
        easy_count = sum(1 for ex in response.workout_plan.exercises 
                        if ex.difficulty.lower() in ["easy", "beginner"])
        
        assert easy_count > 0
        print(f"✅ Low energy test: {easy_count} easy exercises recommended")
    
    def test_no_equipment(self):
        """Test with no equipment available."""
        state = State(
            age=25,
            weight=70.0,
            height=175.0,
            fitness_level="beginner",
            current_energy=7,
            goal="general_fitness",
            injuries=None,
            exercise_history=[]
        )
        
        request = RecommendationRequest(
            current_state=state,
            available_time=30,
            available_equipment=["None"],  # Bodyweight only
            preferences={},
            strategy=RecommendationStrategy.BALANCED,
            max_exercises=5
        )
        
        response = self.use_case.execute(request)
        
        assert response is not None
        assert len(response.workout_plan.exercises) > 0
        
        # All exercises should be bodyweight
        for exercise in response.workout_plan.exercises:
            assert exercise.equipment == "None" or exercise.equipment is None
        
        print(f"✅ No equipment test: {len(response.workout_plan.exercises)} bodyweight exercises")
    
    def test_multiple_injuries(self):
        """Test with multiple injuries."""
        state = State(
            age=50,
            weight=80.0,
            height=170.0,
            fitness_level="beginner",
            current_energy=6,
            goal="general_fitness",
            injuries=["Lower Back", "Knee", "Shoulder"],  # Multiple
            exercise_history=[]
        )
        
        request = RecommendationRequest(
            current_state=state,
            available_time=30,
            available_equipment=["Resistance Bands", "None"],
            preferences={"priority": "safety"},
            strategy=RecommendationStrategy.SIMPLE_REFLEX,
            max_exercises=4
        )
        
        response = self.use_case.execute(request)
        
        assert response is not None
        assert len(response.safety_warnings) >= len(state.injuries)
        assert len(response.workout_plan.exercises) > 0
        
        print(f"✅ Multiple injuries test: {len(response.safety_warnings)} warnings, {len(response.workout_plan.exercises)} safe exercises")


def run_all_tests():
    """Run all integration tests."""
    import traceback
    
    test_classes = [
        TestEndToEndWorkflow,
        TestExplanationGeneration,
        TestPDFGeneration,
        TestEdgeCases
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    print("=" * 70)
    print("RUNNING INTEGRATION TESTS")
    print("=" * 70)
    
    for test_class in test_classes:
        print(f"\n{'='*70}")
        print(f"Testing: {test_class.__name__}")
        print(f"{'='*70}\n")
        
        test_instance = test_class()
        test_methods = [method for method in dir(test_instance) if method.startswith('test_')]
        
        for method_name in test_methods:
            total_tests += 1
            
            try:
                # Setup
                if hasattr(test_instance, 'setup_method'):
                    test_instance.setup_method()
                
                # Run test
                method = getattr(test_instance, method_name)
                method()
                
                passed_tests += 1
                print()
                
            except Exception as e:
                failed_tests += 1
                print(f"❌ FAILED: {method_name}")
                print(f"   Error: {str(e)}")
                traceback.print_exc()
                print()
    
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Total Tests: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    print("=" * 70)
    
    return failed_tests == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
