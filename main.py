"""Demo: recurring task auto-creation and overlap conflict detection."""
from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner("Jordan")
mochi = Pet("Mochi", "dog")
luna  = Pet("Luna", "cat")
owner.add_pet(mochi)
owner.add_pet(luna)

mochi.add_task(Task(
    title="Morning walk",
    time="07:00", duration_minutes=30,
    priority="high", frequency="daily",
    pet_name="Mochi", due_date=date.today(),
))
mochi.add_task(Task(
    title="Feed breakfast",
    time="07:20",           # overlaps "Morning walk" (07:00–07:30)
    duration_minutes=10,
    priority="high", frequency="daily",
    pet_name="Mochi", due_date=date.today(),
))
mochi.add_task(Task(
    title="Evening walk",
    time="18:00", duration_minutes=20,
    priority="medium", frequency="weekly",
    pet_name="Mochi", due_date=date.today(),
))
luna.add_task(Task(
    title="Give medication",
    time="08:00", duration_minutes=5,
    priority="high", frequency="daily",
    pet_name="Luna", due_date=date.today(),
))
luna.add_task(Task(
    title="Clean litter box",
    time="08:03",           # overlaps "Give medication" (08:00–08:05)
    duration_minutes=10,
    priority="medium", frequency="daily",
    pet_name="Luna", due_date=date.today(),
))

scheduler = Scheduler(owner)

# ── 1. Conflict detection ─────────────────────────────────────────────────────
print("=" * 56)
print("CONFLICT DETECTION (overlap-aware):")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for c in conflicts:
        print(f"  ⚠  {c}")
else:
    print("  No conflicts detected.")

# ── 2. Today's schedule before completing anything ────────────────────────────
print("\n" + "=" * 56)
print("TODAY'S SCHEDULE (before):")
today_tasks = scheduler.get_todays_schedule()
for t in today_tasks:
    print(f"  ○ [{t.priority.upper():6}] {t.time}  {t.title}  ({t.pet_name})")
print(f"  Total tasks today: {len(today_tasks)}")

# ── 3. Mark daily tasks complete → auto-creates next occurrence ───────────────
print("\n" + "=" * 56)
print("MARKING RECURRING TASKS COMPLETE:")

walk = mochi.tasks[0]           # Morning walk — daily
med  = luna.tasks[0]            # Give medication — daily
ew   = mochi.tasks[2]           # Evening walk — weekly

for task in [walk, med, ew]:
    before = len(owner.get_all_tasks())
    scheduler.mark_task_complete(task)
    after = len(owner.get_all_tasks())
    spawned = after - before
    next_due = task.due_date.strftime("%Y-%m-%d") if not task.completed else "—"
    print(
        f"  ✓ {task.title:<20} ({task.frequency})"
        f"  → {'new occurrence spawned' if spawned else 'no recurrence (once)'}"
    )

# ── 4. Schedule after completion — recurring tasks appear for tomorrow ─────────
print("\n" + "=" * 56)
print("ALL TASKS AFTER COMPLETION (today + future):")
for t in scheduler.get_upcoming_tasks(days=8):
    print(f"  {'✓' if t.completed else '○'} {t.due_date}  {t.time}  {t.pet_name}: {t.title}")

# ── 5. timedelta summary ──────────────────────────────────────────────────────
print("\n" + "=" * 56)
print("RECURRENCE DATES GENERATED:")
from datetime import timedelta
print(f"  daily  → today + timedelta(days=1)  = {date.today() + timedelta(days=1)}")
print(f"  weekly → today + timedelta(weeks=1) = {date.today() + timedelta(weeks=1)}")
