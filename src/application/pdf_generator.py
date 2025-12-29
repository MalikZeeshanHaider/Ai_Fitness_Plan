"""
PDF Generator Service.

This service generates professional PDF reports for workout plans
with explanations, visualizations, and detailed information.

Features:
- Professional PDF layout
- Workout plan tables
- Exercise details with images placeholders
- Reasoning explanations
- Progress tracking sections
- Safety warnings
- Customizable branding

Uses reportlab for PDF generation.

Time Complexity: O(n) where n is content elements
Space Complexity: O(n) for document storage
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import io

from ..domain.models.workout_plan import WorkoutPlan
from ..domain.models.exercise import Exercise
from ..domain.models.state import State
from .reasoning_explainer import Explanation


class PDFStyle(Enum):
    """PDF document style."""
    PROFESSIONAL = "professional"
    COLORFUL = "colorful"
    MINIMAL = "minimal"
    DETAILED = "detailed"


@dataclass
class PDFSection:
    """
    A section in the PDF document.
    
    Attributes:
        title: Section title
        content: Section content (text, table, list)
        section_type: Type of content (text, table, list)
        style: Style attributes
        page_break: Add page break after section
    """
    title: str
    content: Any
    section_type: str = "text"  # text, table, list, heading
    style: Dict[str, Any] = field(default_factory=dict)
    page_break: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "title": self.title,
            "content": str(self.content),
            "section_type": self.section_type,
            "style": self.style,
            "page_break": self.page_break
        }


@dataclass
class PDFReport:
    """
    A complete PDF report.
    
    Attributes:
        title: Report title
        subtitle: Report subtitle
        sections: List of sections
        metadata: Report metadata
        style: Document style
        generated_at: Generation timestamp
    """
    title: str
    subtitle: str = ""
    sections: List[PDFSection] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    style: PDFStyle = PDFStyle.PROFESSIONAL
    generated_at: datetime = field(default_factory=datetime.now)
    
    def add_section(self, section: PDFSection) -> None:
        """Add a section to the report."""
        self.sections.append(section)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "title": self.title,
            "subtitle": self.subtitle,
            "sections": [s.to_dict() for s in self.sections],
            "metadata": self.metadata,
            "style": self.style.value,
            "generated_at": self.generated_at.isoformat()
        }


class PDFGenerator:
    """
    Service for generating PDF workout reports.
    
    This generator creates professional PDF documents containing:
    1. Workout plan overview
    2. Exercise details with instructions
    3. AI reasoning explanations
    4. Safety warnings and tips
    5. Progress tracking sections
    6. Personalization details
    
    PDF Structure:
    - Cover page with title and branding
    - Executive summary
    - Workout plan details (table)
    - Exercise breakdowns (one per page optional)
    - AI reasoning explanations
    - Safety and tips section
    - Footer with generation info
    
    Design Pattern: Builder
    - Builds complex PDF documents step by step
    - Allows customization at each stage
    - Produces final PDF output
    
    Example Usage:
    ```python
    generator = PDFGenerator()
    
    report = generator.create_workout_report(
        workout_plan=plan,
        user_state=state,
        explanations=explanations,
        style=PDFStyle.PROFESSIONAL
    )
    
    pdf_bytes = generator.generate_pdf(report)
    
    with open("workout_plan.pdf", "wb") as f:
        f.write(pdf_bytes)
    ```
    
    Time Complexity: O(n) where n is content elements
    Space Complexity: O(n) for document storage
    """
    
    def __init__(self, name: str = "PDF Generator"):
        """
        Initialize PDF generator.
        
        Args:
            name: Generator name
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._name = name
        self._reports_generated = 0
    
    @property
    def name(self) -> str:
        """Get generator name."""
        return self._name
    
    def create_workout_report(
        self,
        workout_plan: WorkoutPlan,
        user_state: State,
        explanations: Optional[List[Explanation]] = None,
        safety_warnings: Optional[List[str]] = None,
        success_probability: float = 0.0,
        style: PDFStyle = PDFStyle.PROFESSIONAL
    ) -> PDFReport:
        """
        Create complete workout report.
        
        Args:
            workout_plan: Workout plan to document
            user_state: User's fitness state
            explanations: AI reasoning explanations
            safety_warnings: Safety warnings
            success_probability: Predicted success probability
            style: PDF style
            
        Returns:
            Complete PDF report
            
        Time Complexity: O(n) where n is exercises + explanations
        Space Complexity: O(n)
        """
        # Create report
        report = PDFReport(
            title="Personalized Workout Plan",
            subtitle=f"Plan ID: {workout_plan.plan_id}",
            style=style,
            metadata={
                "user_level": user_state.experience_level.value,
                "fitness_goal": user_state.fitness_goal.value,
                "duration": workout_plan.total_duration_minutes,
                "exercises": len(workout_plan.exercises)
            }
        )
        
        # Add executive summary section
        summary_section = self._create_summary_section(
            workout_plan,
            user_state,
            success_probability
        )
        report.add_section(summary_section)
        
        # Add workout plan table section
        plan_section = self._create_plan_table_section(workout_plan)
        report.add_section(plan_section)
        
        # Add exercise details section
        exercises_section = self._create_exercises_section(workout_plan.exercises)
        report.add_section(exercises_section)
        
        # Add AI reasoning section if explanations provided
        if explanations:
            reasoning_section = self._create_reasoning_section(explanations)
            report.add_section(reasoning_section)
        
        # Add safety warnings section
        if safety_warnings:
            safety_section = self._create_safety_section(safety_warnings)
            report.add_section(safety_section)
        
        # Add tips and guidelines section
        tips_section = self._create_tips_section(user_state)
        report.add_section(tips_section)
        
        self._reports_generated += 1
        
        return report
    
    def _create_summary_section(
        self,
        workout_plan: WorkoutPlan,
        user_state: State,
        success_probability: float
    ) -> PDFSection:
        """Create executive summary section."""
        content = [
            f"**Goal:** {user_state.fitness_goal.value.replace('_', ' ').title()}",
            f"**Experience Level:** {user_state.experience_level.value.title()}",
            f"**Total Duration:** {workout_plan.total_duration_minutes} minutes",
            f"**Total Exercises:** {len(workout_plan.exercises)}",
            f"**Estimated Calories:** {workout_plan.total_calories:.0f} kcal",
            f"**Success Probability:** {success_probability:.1%}",
            "",
            f"This personalized workout plan was generated using advanced AI algorithms "
            f"that analyzed your fitness profile, goals, and constraints. The plan is "
            f"designed to be safe, effective, and aligned with your {user_state.fitness_goal.value} goals."
        ]
        
        return PDFSection(
            title="Executive Summary",
            content="\n".join(content),
            section_type="text"
        )
    
    def _create_plan_table_section(self, workout_plan: WorkoutPlan) -> PDFSection:
        """Create workout plan table section."""
        # Create table data
        table_data = [
            ["#", "Exercise", "Type", "Difficulty", "Duration", "Calories"]
        ]
        
        for i, ex_in_plan in enumerate(workout_plan.exercises, 1):
            exercise = ex_in_plan.exercise
            row = [
                str(i),
                exercise.name,
                exercise.category.value,
                exercise.difficulty,
                f"{exercise.duration_minutes} min",
                f"{exercise.calories_per_minute * exercise.duration_minutes:.0f} kcal"
            ]
            table_data.append(row)
        
        # Add totals row
        table_data.append([
            "",
            "**TOTAL**",
            "",
            "",
            f"**{workout_plan.total_duration_minutes} min**",
            f"**{workout_plan.total_calories:.0f} kcal**"
        ])
        
        return PDFSection(
            title="Workout Plan Overview",
            content=table_data,
            section_type="table"
        )
    
    def _create_exercises_section(self, exercises_in_plan) -> PDFSection:
        """Create detailed exercises section."""
        content = []
        
        for i, ex_in_plan in enumerate(exercises_in_plan, 1):
            exercise = ex_in_plan.exercise
            exercise_detail = [
                f"## Exercise {i}: {exercise.name}",
                "",
                f"**Type:** {exercise.category.value.title()}",
                f"**Difficulty:** {exercise.difficulty.title()}",
                f"**Duration:** {exercise.duration_minutes} minutes",
                f"**Target Muscles:** {', '.join(exercise.primary_muscles) if exercise.primary_muscles else 'Full body'}",
                f"**Equipment:** {', '.join(exercise.equipment) if exercise.equipment else 'None'}",
                "",
                "**Description:**",
                exercise.description if exercise.description else "Standard exercise technique applies.",
                "",
                "**Safety Notes:**",
                "- Warm up before starting this exercise",
                "- Maintain proper form throughout",
                "- Stop if you experience pain",
                "- Stay hydrated",
                "",
                "---",
                ""
            ]
            content.extend(exercise_detail)
        
        return PDFSection(
            title="Exercise Details",
            content="\n".join(content),
            section_type="text"
        )
    
    def _create_reasoning_section(self, explanations: List[Explanation]) -> PDFSection:
        """Create AI reasoning explanations section."""
        content = ["## How This Workout Was Generated", ""]
        
        for explanation in explanations:
            content.append(f"### {explanation.title}")
            content.append("")
            content.append(explanation.content)
            content.append("")
            
            if explanation.reasoning_steps:
                content.append("**Reasoning Steps:**")
                for step in explanation.reasoning_steps[:5]:  # Limit to 5
                    content.append(f"- {step}")
                content.append("")
            
            if explanation.details:
                content.append("**Details:**")
                for detail in explanation.details[:5]:  # Limit to 5
                    content.append(f"- {detail}")
                content.append("")
            
            content.append("---")
            content.append("")
        
        return PDFSection(
            title="AI Reasoning & Analysis",
            content="\n".join(content),
            section_type="text",
            page_break=True
        )
    
    def _create_safety_section(self, safety_warnings: List[str]) -> PDFSection:
        """Create safety warnings section."""
        content = [
            "Please review the following safety considerations before starting your workout:",
            ""
        ]
        
        for warning in safety_warnings:
            content.append(f"⚠️ {warning}")
        
        content.extend([
            "",
            "**General Safety Guidelines:**",
            "- Always consult with a healthcare provider before starting a new exercise program",
            "- Start slowly and gradually increase intensity",
            "- Listen to your body and stop if you experience pain",
            "- Ensure proper form to prevent injuries",
            "- Stay hydrated throughout your workout",
            "- Allow adequate rest between workout sessions"
        ])
        
        return PDFSection(
            title="Safety & Warnings",
            content="\n".join(content),
            section_type="text"
        )
    
    def _create_tips_section(self, user_state: State) -> PDFSection:
        """Create tips and guidelines section."""
        content = [
            "## Tips for Success",
            "",
            "**Preparation:**",
            "- Warm up for 5-10 minutes before starting",
            "- Prepare all necessary equipment in advance",
            "- Wear appropriate workout clothing",
            "- Have water readily available",
            "",
            "**During Workout:**",
            "- Focus on proper form over speed",
            "- Breathe consistently (don't hold your breath)",
            "- Take rest periods as needed",
            "- Monitor your heart rate and exertion level",
            "",
            "**After Workout:**",
            "- Cool down with light stretching",
            "- Rehydrate and replenish electrolytes",
            "- Log your workout for progress tracking",
            "- Allow 24-48 hours for muscle recovery",
            ""
        ]
        
        # Add goal-specific tips
        goal = user_state.fitness_goal.value
        if goal == "weight_loss":
            content.extend([
                "**Weight Loss Tips:**",
                "- Maintain a calorie deficit through diet and exercise",
                "- Combine cardio with strength training",
                "- Aim for 150-300 minutes of moderate activity per week",
                "- Track your progress weekly"
            ])
        elif goal == "muscle_gain":
            content.extend([
                "**Muscle Gain Tips:**",
                "- Consume adequate protein (1.6-2.2g per kg body weight)",
                "- Progressive overload: gradually increase weights",
                "- Allow 48-72 hours between training same muscle groups",
                "- Get 7-9 hours of sleep for recovery"
            ])
        elif goal == "endurance":
            content.extend([
                "**Endurance Tips:**",
                "- Gradually increase workout duration",
                "- Vary intensity with interval training",
                "- Fuel properly before long sessions",
                "- Monitor heart rate zones"
            ])
        
        return PDFSection(
            title="Tips & Guidelines",
            content="\n".join(content),
            section_type="text"
        )
    
    def generate_pdf(self, report: PDFReport) -> bytes:
        """
        Generate PDF document from report using reportlab.
        
        Args:
            report: PDF report to generate
            
        Returns:
            PDF as bytes
            
        Time Complexity: O(n) where n is sections
        Space Complexity: O(n)
        """
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        from io import BytesIO
        
        # Create PDF buffer
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1E88E5'),
            alignment=TA_CENTER,
            spaceAfter=12
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#424242'),
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1E88E5'),
            spaceAfter=10
        )
        
        # Title and subtitle
        story.append(Paragraph(report.title, title_style))
        story.append(Paragraph(report.subtitle, subtitle_style))
        story.append(Spacer(1, 0.2 * inch))
        
        # Metadata
        meta_text = f"Generated: {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')} | Style: {report.style.value}"
        story.append(Paragraph(meta_text, styles['Normal']))
        story.append(Spacer(1, 0.3 * inch))
        
        # Add sections
        for section in report.sections:
            # Section title
            story.append(Paragraph(section.title, heading_style))
            story.append(Spacer(1, 0.1 * inch))
            
            if section.section_type == "text":
                # Parse text content with better formatting
                content_text = section.content if isinstance(section.content, str) else "\n".join(section.content)
                
                # Split by lines and process each
                lines = content_text.split('\n')
                for line in lines:
                    line = line.strip()
                    if not line:
                        story.append(Spacer(1, 0.05 * inch))
                        continue
                    
                    # Handle headers (##)
                    if line.startswith('## '):
                        exercise_title_style = ParagraphStyle(
                            'ExerciseTitle',
                            parent=styles['Heading3'],
                            fontSize=12,
                            textColor=colors.HexColor('#1976D2'),
                            spaceAfter=6,
                            spaceBefore=10
                        )
                        story.append(Paragraph(line[3:], exercise_title_style))
                    # Handle separators
                    elif line == '---':
                        story.append(Spacer(1, 0.15 * inch))
                    # Handle bold (**text**) - proper replacement
                    elif '**' in line:
                        # Replace pairs of ** with <b> and </b>
                        import re
                        line = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', line)
                        story.append(Paragraph(line, styles['Normal']))
                    # Regular text
                    else:
                        story.append(Paragraph(line, styles['Normal']))
            
            elif section.section_type == "table" and section.content:
                # Create table with better styling
                table = Table(section.content, colWidths=[0.5*inch, 2*inch, 1.2*inch, 1.2*inch, 1*inch, 1*inch])
                table.setStyle(TableStyle([
                    # Header row
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976D2')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('TOPPADDING', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                    # Data rows
                    ('BACKGROUND', (0, 1), (-1, -2), colors.HexColor('#E3F2FD')),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.HexColor('#E3F2FD'), colors.white]),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('TOPPADDING', (0, 1), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                    # Total row
                    ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#BBDEFB')),
                    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                    # Grid
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#1976D2')),
                ]))
                story.append(table)
            
            elif section.section_type == "list" and section.content:
                bullet_style = ParagraphStyle(
                    'BulletList',
                    parent=styles['Normal'],
                    leftIndent=20,
                    bulletIndent=10
                )
                for item in section.content:
                    story.append(Paragraph(f"• {item}", bullet_style))
            
            story.append(Spacer(1, 0.25 * inch))
            
            if section.page_break:
                story.append(PageBreak())
        
        # Add footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        story.append(Spacer(1, 0.5 * inch))
        story.append(Paragraph("AI Gym Workout Recommendation System", footer_style))
        story.append(Paragraph("Powered by Advanced AI Algorithms", footer_style))
        
        # Build PDF
        doc.build(story)
        
        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def _format_table(self, table_data: List[List[str]]) -> List[str]:
        """Format table data as text."""
        if not table_data:
            return []
        
        # Calculate column widths
        col_widths = [max(len(str(row[i])) for row in table_data) for i in range(len(table_data[0]))]
        
        lines = []
        
        # Header row
        header = table_data[0]
        lines.append(" | ".join(str(header[i]).ljust(col_widths[i]) for i in range(len(header))))
        lines.append("-+-".join("-" * w for w in col_widths))
        
        # Data rows
        for row in table_data[1:]:
            lines.append(" | ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(row))))
        
        return lines
    
    def generate_markdown(self, report: PDFReport) -> str:
        """
        Generate Markdown document from report.
        
        Args:
            report: PDF report to generate
            
        Returns:
            Markdown as string
            
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        md_lines = [
            f"# {report.title}",
            f"## {report.subtitle}",
            "",
            f"*Generated: {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}*",
            "",
            "---",
            ""
        ]
        
        # Add sections
        for section in report.sections:
            md_lines.append(f"## {section.title}")
            md_lines.append("")
            
            if section.section_type == "text":
                md_lines.append(str(section.content))
            elif section.section_type == "table":
                md_lines.extend(self._format_markdown_table(section.content))
            
            md_lines.append("")
            md_lines.append("---")
            md_lines.append("")
        
        return "\n".join(md_lines)
    
    def _format_markdown_table(self, table_data: List[List[str]]) -> List[str]:
        """Format table as Markdown."""
        if not table_data:
            return []
        
        lines = []
        
        # Header
        lines.append("| " + " | ".join(str(cell) for cell in table_data[0]) + " |")
        lines.append("|" + "|".join("---" for _ in table_data[0]) + "|")
        
        # Rows
        for row in table_data[1:]:
            lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
        
        return lines
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get generator statistics.
        
        Returns:
            Statistics dictionary
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return {
            "name": self._name,
            "reports_generated": self._reports_generated
        }
    
    def __str__(self) -> str:
        """String representation."""
        return f"PDFGenerator(reports_generated={self._reports_generated})"


# Example usage
if __name__ == "__main__":
    print("PDF Generator Service")
    print("====================")
    print()
    
    from ..domain.models.state import State, ExperienceLevel, FitnessGoal
    from ..domain.models.exercise import Exercise, ExerciseType
    from ..domain.models.action import Difficulty
    from ..domain.models.workout_plan import WorkoutPlan
    
    # Create generator
    generator = PDFGenerator()
    
    # Create sample workout plan
    exercises = [
        Exercise(
            exercise_id="ex1",
            name="Running",
            exercise_type=ExerciseType.CARDIO,
            difficulty=Difficulty.INTERMEDIATE,
            duration_minutes=20,
            calories_per_minute=10.0,
            description="Moderate pace running"
        ),
        Exercise(
            exercise_id="ex2",
            name="Push-ups",
            exercise_type=ExerciseType.STRENGTH,
            difficulty=Difficulty.INTERMEDIATE,
            duration_minutes=10,
            calories_per_minute=7.0,
            description="Standard push-ups"
        )
    ]
    
    workout_plan = WorkoutPlan(
        plan_id="test_plan_1",
        plan_name="30-Min Weight Loss Workout",
        exercises=exercises,
        target_goal=FitnessGoal.WEIGHT_LOSS,
        difficulty_level=ExperienceLevel.INTERMEDIATE
    )
    
    user_state = State(
        experience_level=ExperienceLevel.INTERMEDIATE,
        fitness_goal=FitnessGoal.WEIGHT_LOSS,
        strength_level=50.0,
        endurance_level=55.0,
        flexibility_level=45.0
    )
    
    # Create report
    report = generator.create_workout_report(
        workout_plan=workout_plan,
        user_state=user_state,
        success_probability=0.85,
        style=PDFStyle.PROFESSIONAL
    )
    
    # Generate PDF (text format)
    pdf_bytes = generator.generate_pdf(report)
    
    print("PDF Generated (text format):")
    print("=" * 80)
    print(pdf_bytes.decode('utf-8')[:500])  # Print first 500 chars
    print("...")
    print("=" * 80)
    
    print(f"\nTotal length: {len(pdf_bytes)} bytes")
    print(f"Sections: {len(report.sections)}")
