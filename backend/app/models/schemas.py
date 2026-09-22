from pydantic import BaseModel, Field
from typing import Any, Literal

class RequirementRequest(BaseModel):
    requirement: str = Field(min_length=10)
    project_name: str | None = None

class ProjectCreateResponse(BaseModel):
    project_id: str
    project_name: str
    status: str

class ProjectState(BaseModel):
    project_id: str
    project_name: str
    requirement: str
    status: str
    specification: dict[str, Any] = {}
    architecture: dict[str, Any] = {}
    tasks: list[dict[str, Any]] = []
    current_task: str | None = None
    test_results: dict[str, Any] = {}
    security_results: dict[str, Any] = {}
    deployment: dict[str, Any] = {}
    events: list[dict[str, Any]] = []
