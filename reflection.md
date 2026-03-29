# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

I initially drafted a broader architecture, but the final implementation focused on four core classes that keep responsibilities clear:

- `Owner`: owns pets and provides cross-pet task access.
- `Pet`: owns the task list for one pet.
- `Task`: stores schedule metadata (time, duration, priority, recurrence, status, due date) and task-level behaviors.
- `Scheduler`: performs scheduling operations over the owner's task graph (sorting, filtering, conflict checks, summaries, recurrence handling).

**b. Design changes**

My UML and code changed to stay clean and realistic:

1. I removed early concepts like `DailyPlan` that were not needed for this iteration.
2. I moved recurrence behavior to `Task.mark_complete()` and let `Scheduler.mark_task_complete()` orchestrate owner/pet updates.
3. I added explicit validation in `Task.__post_init__` (time format, priority set, frequency set) so bad data is blocked at object creation.

These changes improved cohesion: task rules live on `Task`, aggregation lives on `Owner`, and coordination lives on `Scheduler`.

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler currently considers:

- Due date (today/upcoming windows)
- Time ordering (`HH:MM` converted to minutes)
- Priority (`high`, `medium`, `low`)
- Completion status
- Pet ownership/scope
- Recurrence (`once`, `daily`, `weekly`)

I prioritized constraints that directly affect user trust in a planner: correct order, recurring continuity, and conflict visibility.

**b. Tradeoffs**

I chose overlap detection using sorted tasks plus an early-break nested loop in `detect_conflicts()`.

Tradeoff accepted:

- Pros: clearer performance behavior and fewer unnecessary comparisons once overlap is impossible.
- Cons: loop logic is a bit less obvious than a brute-force all-pairs approach.

I kept this because it balances readability with practical efficiency and matches how schedules are naturally processed chronologically.

## 3. AI Collaboration (VS Code Copilot)

**a. Most effective Copilot features for this scheduler**

The most helpful features were:

- Copilot Chat with file context (`#file` and `#codebase`) to reason about edge cases and missing tests.
- Test drafting support for fast `pytest` scaffolding, then manual tightening of assertions.
- Refactor assistance when aligning UI behavior to scheduler methods (`sort_by_time`, `filter_tasks`, `detect_conflicts`).

Prompts worked best when they were concrete, such as asking for "most important edge cases for recurring tasks and conflicts" rather than broad "improve my code" requests.

**b. One AI suggestion I rejected/modified**

I rejected keeping outdated architecture ideas (like a separate `DailyPlan` object) once the actual implementation made that layer unnecessary. Instead, I simplified to direct scheduler outputs (`get_todays_schedule`, `daily_summary`, `get_upcoming_tasks`) to avoid over-engineering and duplicated state.

I also treated generated test code as drafts, then adjusted it to match real business logic and naming conventions.

**c. How separate chat sessions helped**

Using separate sessions by phase (design, implementation, testing, UI, docs) made the project easier to manage:

- Design chats stayed focused on UML and class boundaries.
- Build chats focused on methods and correctness.
- Testing chats focused on happy paths and edge cases.
- Documentation chats focused on README/reflection quality.

This prevented context mixing and reduced the risk of blindly applying suggestions that belonged to a previous phase.

## 4. Testing and Verification

**a. What I tested and why**

I tested:

- Task completion toggling
- Daily recurrence creation (+1 day)
- One-time tasks not recurring
- Pet task list growth
- Chronological schedule sorting
- Scheduler-level recurrence integration (`mark_task_complete`)
- Conflict detection for duplicate start times

These tests are important because they cover both expected workflows and high-risk scheduling logic where small bugs can break user trust.

**b. Confidence**

Confidence level: 4/5.

Reasoning: core behaviors pass current tests and key edge cases are covered. With more time, I would add boundary tests (back-to-back tasks, midnight-like times), multi-pet conflict isolation, and invalid-input parameterized tests.

## 5. Reflection

**a. What went well**

The strongest outcome was keeping the backend model clean while making the UI actually expose scheduler intelligence (sorted tables, conflict warnings, and recurrence effects).

**b. What I would improve**

Next iteration, I would reduce duplicated explanatory sections in documentation, add stronger UI flows for editing/removing tasks, and expand test coverage for date boundaries and weekly recurrence behavior.

**c. Key takeaway: being the "lead architect" with AI**

I learned that AI is most powerful as a force multiplier, not a decision-maker. As lead architect, my job is to define boundaries, verify correctness, and reject suggestions that add complexity without value. The best results came from treating Copilot like a fast collaborator while keeping final ownership of design choices, tradeoffs, and quality gates.
