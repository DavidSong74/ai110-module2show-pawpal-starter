from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
owner = Owner("Jordan")

mochi = Pet("Mochi", "dog")
luna = Pet("Luna", "cat")

owner.add_pet(mochi)
owner.add_pet(luna)

# --- Tasks for Mochi ---
mochi.add_task(Task(
    title="Morning walk",
    time="07:00",
    duration_minutes=30,
    priority="high",
    frequency="daily",
    pet_name="Mochi",
    due_date=date.today(),
))
mochi.add_task(Task(
    title="Feed breakfast",
    time="08:00",
    duration_minutes=5,
    priority="high",
    frequency="daily",
    pet_name="Mochi",
    due_date=date.today(),
))

# --- Tasks for Luna ---
luna.add_task(Task(
    title="Clean litter box",
    time="09:30",
    duration_minutes=10,
    priority="medium",
    frequency="daily",
    pet_name="Luna",
    due_date=date.today(),
))
luna.add_task(Task(
    title="Brush fur",
    time="18:00",
    duration_minutes=15,
    priority="low",
    frequency="weekly",
    pet_name="Luna",
    due_date=date.today(),
))

# --- Run Scheduler ---
scheduler = Scheduler(owner)
print(scheduler.daily_summary())
