from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional


@dataclass
class Task:
    title: str
    time: str               # "HH:MM" 24-hour format
    duration_minutes: int
    priority: str           # "low" | "medium" | "high"
    frequency: str          # "once" | "daily" | "weekly"
    pet_name: str
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> Optional["Task"]:
        """Mark complete; return next Task if recurring, else None."""
        self.completed = True
        if self.frequency == "daily":
            return Task(
                title=self.title,
                time=self.time,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                frequency=self.frequency,
                pet_name=self.pet_name,
                due_date=self.due_date + timedelta(days=1),
            )
        elif self.frequency == "weekly":
            return Task(
                title=self.title,
                time=self.time,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                frequency=self.frequency,
                pet_name=self.pet_name,
                due_date=self.due_date + timedelta(weeks=1),
            )
        return None

    def is_high_priority(self) -> bool:
        """Return True if this task's priority is 'high'."""
        return self.priority == "high"


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return a shallow copy of this pet's task list."""
        return list(self.tasks)

    def get_incomplete_tasks(self) -> list[Task]:
        """Return only tasks that have not been completed."""
        return [t for t in self.tasks if not t.completed]


class Owner:
    def __init__(self, name: str) -> None:
        self.name = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def get_pet(self, name: str) -> Optional[Pet]:
        """Look up a pet by name; return None if not found."""
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None

    def get_all_tasks(self) -> list[Task]:
        """Return a flat list of all tasks across every pet."""
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks())
        return tasks


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def get_todays_schedule(self) -> list[Task]:
        """Return all tasks due today, sorted by time."""
        today = date.today()
        todays = [t for t in self.owner.get_all_tasks() if t.due_date == today]
        return self.sort_by_time(todays)

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks chronologically using 'HH:MM' string comparison."""
        return sorted(tasks, key=lambda t: t.time)

    def filter_tasks(
        self,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> list[Task]:
        """Filter by pet name and/or completion status."""
        tasks = self.owner.get_all_tasks()
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet_name == pet_name]
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        return tasks

    def detect_conflicts(self) -> list[str]:
        """Return warning strings for tasks on the same pet at the same time."""
        groups: dict[tuple[str, str], list[str]] = defaultdict(list)
        for task in self.owner.get_all_tasks():
            groups[(task.pet_name, task.time)].append(task.title)
        conflicts = []
        for (pet, time), titles in groups.items():
            if len(titles) > 1:
                names = " & ".join(f'"{t}"' for t in titles)
                conflicts.append(f"Conflict: {names} at {time} for {pet}")
        return conflicts

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks high → medium → low."""
        order = {"high": 0, "medium": 1, "low": 2}
        return sorted(tasks, key=lambda t: order.get(t.priority, 3))

    def get_upcoming_tasks(self, days: int = 7) -> list[Task]:
        """Return incomplete tasks due within the next `days` days, sorted by date then time."""
        today = date.today()
        cutoff = today + timedelta(days=days)
        upcoming = [
            t for t in self.owner.get_all_tasks()
            if not t.completed and today <= t.due_date <= cutoff
        ]
        return sorted(upcoming, key=lambda t: (t.due_date, t.time))

    def daily_summary(self) -> str:
        """Return a human-readable summary of today's schedule."""
        tasks = self.get_todays_schedule()
        if not tasks:
            return "No tasks scheduled for today."
        lines = [f"Schedule for {date.today().strftime('%A, %B %d')}:"]
        for t in tasks:
            status = "✓" if t.completed else "○"
            lines.append(
                f"  {status} [{t.priority.upper()}] {t.time} — {t.title} ({t.pet_name}, {t.duration_minutes} min)"
            )
        total = sum(t.duration_minutes for t in tasks)
        lines.append(f"Total: {len(tasks)} task(s), {total} min")
        return "\n".join(lines)

    def mark_task_complete(self, task: Task) -> None:
        """Mark complete; auto-add next occurrence if recurring."""
        next_task = task.mark_complete()
        if next_task is not None:
            pet = self.owner.get_pet(task.pet_name)
            if pet is not None:
                pet.add_task(next_task)