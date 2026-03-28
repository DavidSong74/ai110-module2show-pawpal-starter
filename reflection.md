Review the diagram. Ensure relationships (like "Owner has Pets") make sense and that you haven't included unnecessary complexity.

# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

I designed five classes:

- **`Owner`** — stores name and daily available time (minutes); owns one or more pets.
- **`Pet`** — stores name and species; holds a list of tasks assigned to that pet.
- **`Task`** — stores title, duration (minutes), priority (low/medium/high), and optional notes; knows whether it is high priority.
- **`Scheduler`** — takes an owner, walks the owner→pet→task chain, sorts by priority, filters to fit the time budget, and produces a `DailyPlan`.
- **`DailyPlan`** — the output: an ordered list of scheduled tasks, total duration, and a reasoning note for each task.

**b. Design changes**

Yes, the design changed in three ways after reviewing the skeleton:

1. **`Scheduler` no longer holds a `tasks` list.** The initial design stored tasks directly on the scheduler, but tasks already live on `Pet` which belongs to `Owner`. Keeping a separate list would require syncing two sources of truth. I removed it and had `Scheduler` walk `owner → pet → tasks` instead.

2. **`Priority` became an enum.** The initial design used raw strings (`"low"`, `"medium"`, `"high"`), which are easy to mistype and hard to sort. Switching to `Priority(Enum)` with integer values (`LOW=1`, `MEDIUM=2`, `HIGH=3`) made sorting natural and caught typos at assignment time.

3. **`DailyPlan.total_duration` became a computed property.** Storing it as a plain `int` risked going stale if tasks were added without updating it. Making it a `@property` that sums `scheduled_tasks` on demand means it's always accurate.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
