from datetime import date
from pawpal_system import Pet, Task


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
    assert next_task.due_date == task.due_date + __import__("datetime").timedelta(days=1)
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
