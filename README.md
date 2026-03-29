# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

The scheduler goes beyond a simple task list. Key algorithmic features built into `pawpal_system.py`:

**Time-aware sorting**
Tasks are sorted by converting `"HH:MM"` strings to total minutes since midnight (`start_minutes()`), making the sort correct for all valid 24-hour times rather than relying on string comparison.

**Overlap-aware conflict detection**
`detect_conflicts()` uses a standard interval-overlap test — `a.start < b.end AND b.start < a.end` — to catch tasks that collide even when they don't share an exact start time (e.g. a 30-minute walk at 07:00 conflicts with feeding at 07:20). Tasks are sorted first so the inner loop can exit early once no further overlap is possible.

**Flexible filtering**
`filter_tasks()` accepts any combination of `pet_name`, `completed`, and `priority`, letting the UI show exactly the slice a user needs without fetching all tasks.

**Automatic recurrence**
Marking a `daily` or `weekly` task complete automatically spawns the next occurrence (`due_date + timedelta(days=1)` or `timedelta(weeks=1)`) and adds it to the correct pet's task list — no manual re-entry required.

**Input validation**
`Task.__post_init__` rejects malformed data at construction time: times must be zero-padded `HH:MM`, priority must be `low/medium/high`, and frequency must be `once/daily/weekly`.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
        
        Owner

        Attributes: name, available_minutes (time budget for the day)
        Methods: add_pet(), get_pets()
        Pet

        Attributes: name, species, tasks (list of Task)
        Methods: add_task(), remove_task(), get_tasks()
        Task

        Attributes: title, duration_minutes, priority (low/medium/high), notes (optional)
        Methods: is_high_priority(), __repr__()
        Scheduler

        Attributes: owner, tasks
        Methods: generate_plan() → returns a DailyPlan; _filter_by_time(), _sort_by_priority()
        DailyPlan

        Attributes: scheduled_tasks (list of Task), total_duration, reasoning (dict mapping task → reason string)
        Methods: add_task(), summarize(), display()
        Key relationships:

        Owner → has → Pet(s)
        Pet → has → Task(s)
        Scheduler → consumes Owner + Tasks → produces DailyPlan -->

2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Testing PawPal+

Run the automated test suite with:

python -m pytest

Current tests cover core scheduler reliability checks, including:
- Task completion state changes and recurrence behavior (`once` vs `daily`)
- Pet task-list behavior when adding one or multiple tasks
- Sorting correctness for daily schedules in chronological time order
- Recurrence logic through `Scheduler.mark_task_complete()` creating the next-day task for daily tasks
- Conflict detection when two tasks share duplicate start times for the same pet

Confidence Level: ★★★★☆ (4/5)

Reasoning: All current tests pass (8 passed), and they exercise the most important happy paths plus key edge cases in sorting, recurrence, and conflict detection. Additional confidence could come from more boundary-time and multi-pet conflict scenarios.
