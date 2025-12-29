"""
Application Layer Package.

This layer contains use cases and application services that orchestrate
domain logic to fulfill business requirements.

Components:
- StreamlinedWorkoutUseCase: Simplified use case with 3 agents + A* search
- (Legacy components available but not used in streamlined workflow)

The application layer:
- Orchestrates domain objects
- Implements use cases
- Coordinates between layers
- Remains independent of UI and infrastructure details
"""

from .streamlined_workout_usecase import (
    StreamlinedWorkoutUseCase,
    StreamlinedRequest,
    StreamlinedResponse
)

__all__ = [
    'StreamlinedWorkoutUseCase',
    'StreamlinedRequest',
    'StreamlinedResponse',
]
