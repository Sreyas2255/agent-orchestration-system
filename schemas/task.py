from typing import List
from pydantic import BaseModel, Field


class Subtask(BaseModel):
    description: str = Field(
        description="What needs to be done"
    )

    assigned_specialist: str = Field(
        description="Specialist agent responsible for the task"
    )

    required_inputs: List[str] = Field(
        description="Inputs required to complete the task"
    )

    expected_output: str = Field(
        description="Expected result from the specialist"
    )

    complexity: str = Field(
        description="Task complexity: Low, Medium, or High"
    )


class ExecutionPlan(BaseModel):
    subtasks: List[Subtask] = Field(
        description="Ordered list of subtasks"
    )