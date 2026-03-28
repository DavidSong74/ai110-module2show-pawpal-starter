from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    notes: Optional[str] = None

    def is_high_priority(self) -> bool:
        pass


@dataclass
class Pet:
    name: str
    species: str  # "dog", "cat", "other"
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass


@dataclass
class Owner:
    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass


@dataclass
class DailyPlan:
    scheduled_tasks: list[Task] = field(default_factory=list)
    total_duration: int = 0
    reasoning: dict[str, str] = field(default_factory=dict)

    def add_task(self, task: Task, reason: str) -> None:
        pass

    def summarize(self) -> str:
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_plan(self) -> DailyPlan:
        pass

    def _sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        pass

    def _filter_by_time(self, tasks: list[Task], available_minutes: int) -> list[Task]:
        pass
