from pathlib import Path
import sys
from datetime import date, timedelta

sys.path.append(str(Path(__file__).resolve().parents[1]))

from pawpal_system import Owner, Pet, Scheduler, Task


def make_task(**kwargs) -> Task:
    defaults = dict(
        title="Morning walk",
        time="07:00",
        duration_minutes=30,
        priority="high",
        frequency="once",
        pet_name="Mochi",
        due_date=date.today(),
    )
    return Task(**{**defaults, **kwargs})


def test_mark_complete_sets_completed_flag():
    task = make_task()
    assert not task.completed
    task.mark_complete()
    assert task.completed


def test_mark_complete_returns_next_task_for_daily():
    task = make_task(frequency="daily")
    next_task = task.mark_complete()
    assert next_task is not None
    assert next_task.due_date == task.due_date + timedelta(days=1)
    assert not next_task.completed


def test_mark_complete_returns_none_for_once():
    task = make_task(frequency="once")
    next_task = task.mark_complete()
    assert next_task is None


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog")
    assert len(pet.tasks) == 0
    pet.add_task(make_task())
    assert len(pet.tasks) == 1


def test_add_multiple_tasks_to_pet():
    pet = Pet(name="Luna", species="cat")
    pet.add_task(make_task(title="Feed breakfast"))
    pet.add_task(make_task(title="Brush fur"))
    assert len(pet.tasks) == 2


def test_scheduler_sorting_returns_chronological_order():
    owner = Owner(name="Alex")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    late = make_task(title="Evening walk", time="19:30", pet_name="Mochi")
    early = make_task(title="Breakfast", time="07:15", pet_name="Mochi")
    mid = make_task(title="Lunch check", time="12:00", pet_name="Mochi")
    pet.add_task(late)
    pet.add_task(early)
    pet.add_task(mid)

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.get_todays_schedule()

    assert [t.time for t in sorted_tasks] == ["07:15", "12:00", "19:30"]


def test_scheduler_mark_daily_task_complete_creates_next_day_task():
    owner = Owner(name="Alex")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    daily_task = make_task(
        title="Evening meds",
        frequency="daily",
        pet_name="Mochi",
        due_date=date.today(),
    )
    pet.add_task(daily_task)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(daily_task)

    assert daily_task.completed is True
    assert len(pet.tasks) == 2

    recurring_copy = pet.tasks[1]
    assert recurring_copy.title == daily_task.title
    assert recurring_copy.frequency == "daily"
    assert recurring_copy.completed is False
    assert recurring_copy.due_date == daily_task.due_date + timedelta(days=1)


def test_detect_conflicts_flags_tasks_with_duplicate_start_times():
    owner = Owner(name="Alex")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    pet.add_task(
        make_task(
            title="Breakfast",
            time="08:00",
            duration_minutes=20,
            pet_name="Mochi",
        )
    )
    pet.add_task(
        make_task(
            title="Morning meds",
            time="08:00",
            duration_minutes=10,
            pet_name="Mochi",
        )
    )

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "Breakfast" in conflicts[0]
    assert "Morning meds" in conflicts[0]
    assert "Mochi" in conflicts[0]
