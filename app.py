"""PawPal+ Streamlit dashboard — clinic-inspired pet care planner."""
from collections import defaultdict
from datetime import date, timedelta

import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

# ── CSS (injected once at module level) ───────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', system-ui, sans-serif !important;
    background-color: #F8F7F4 !important;
    color: #334155 !important;
}
.stApp { background-color: #F8F7F4 !important; }

input, textarea { border: 1.5px solid #CBD5E1 !important; border-radius: 8px !important;
    background: #FFFFFF !important; font-family: 'Inter', sans-serif !important;
    color: #334155 !important; font-size: 13px !important; }
[data-baseweb="select"] > div { border: 1.5px solid #CBD5E1 !important;
    border-radius: 8px !important; background: #FFFFFF !important; }
[data-testid="stForm"] { background: transparent !important; border: none !important;
    padding: 0 !important; }

.stButton > button, .stFormSubmitButton > button {
    background-color: #3B82C4 !important; color: #FFFFFF !important;
    border: none !important; border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important; font-weight: 600 !important;
    font-size: 13px !important; padding: 8px 18px !important;
    transition: background 0.15s !important;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    background-color: #2563A8 !important;
}

[data-testid="stCheckbox"] label { font-size: 13px !important; color: #334155 !important; }
[data-testid="stCheckbox"] { margin-bottom: 2px !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.2rem !important; padding-bottom: 2rem !important; }

.app-header { font-family: 'Inter', sans-serif; font-size: 24px; font-weight: 700;
    color: #1E3A5F; display: flex; align-items: center; gap: 10px; margin-bottom: 2px; }
.app-sub { font-size: 12px; color: #94A3B8; margin-bottom: 16px; font-weight: 400; }
.col-label { font-size: 11px; font-weight: 700; letter-spacing: 1.5px;
    text-transform: uppercase; color: #94A3B8; margin: 0 0 10px 0;
    padding-bottom: 6px; border-bottom: 2px solid #E2E8F0; }
.section-title { font-size: 13px; font-weight: 700; color: #1E3A5F;
    margin: 16px 0 8px 0; display: flex; align-items: center; gap: 6px; }
.card { background: #FFFFFF; border: 1.5px solid #E2E8F0; border-radius: 12px;
    padding: 14px 16px; margin-bottom: 10px; }
.card-critical { border-left: 4px solid #3B82C4; }
.card-nice     { border-left: 4px solid #F5A623; }
.card-done     { border-left: 4px solid #86EFAC; opacity: 0.75; }

.priority-chip { display: inline-block; font-size: 10px; font-weight: 700;
    padding: 2px 8px; border-radius: 10px; margin-left: 6px;
    text-transform: uppercase; letter-spacing: 0.5px; }
.chip-high   { background: #FEE2E2; color: #DC2626; }
.chip-medium { background: #FEF3C7; color: #D97706; }
.chip-low    { background: #DCFCE7; color: #16A34A; }
.chip-done   { background: #F1F5F9; color: #94A3B8; }

.stress-banner { background: linear-gradient(90deg, #F0FDF4, #DCFCE7);
    border: 1.5px solid #86EFAC; border-radius: 10px; padding: 10px 16px;
    font-size: 13px; font-weight: 500; color: #15803D; margin-bottom: 12px; }
.warn-banner { background: #FFF7ED; border: 1.5px solid #FED7AA;
    border-radius: 10px; padding: 10px 16px; font-size: 13px;
    font-weight: 500; color: #C2410C; margin-bottom: 12px; }

.week-day { font-size: 11px; font-weight: 700; color: #94A3B8;
    text-transform: uppercase; letter-spacing: 1px; margin: 12px 0 4px 0; }
.week-today-label { display: inline-block; background: #3B82C4; color: #FFFFFF;
    font-size: 10px; font-weight: 700; border-radius: 6px;
    padding: 1px 7px; margin-left: 6px; vertical-align: middle; }
.week-task-row { background: #FFFFFF; border: 1.5px solid #E2E8F0;
    border-radius: 8px; padding: 6px 10px; margin-bottom: 4px;
    font-size: 12px; color: #334155;
    display: flex; justify-content: space-between; align-items: center; }
.week-overdue { border-left: 3px solid #DC2626; background: #FFF5F5; }
.overdue-dot { display: inline-block; width: 7px; height: 7px;
    background: #DC2626; border-radius: 50%; margin-right: 5px;
    vertical-align: middle; animation: pulse 1.2s ease-in-out infinite; }
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(0.7); }
}
.stat-box { background: #FFFFFF; border: 1.5px solid #E2E8F0; border-radius: 10px;
    padding: 10px 12px; text-align: center; font-size: 11px; color: #64748B; }
.stat-num { font-size: 22px; font-weight: 700; color: #1E3A5F; line-height: 1.1; }
.empty-state { text-align: center; color: #94A3B8; font-size: 13px;
    padding: 24px 10px; border: 1.5px dashed #E2E8F0;
    border-radius: 10px; margin: 8px 0; }
</style>
""", unsafe_allow_html=True)


# ── Module-level helpers (pure functions, no Streamlit state) ─────────────────

def chip(priority: str, done: bool = False) -> str:
    """Return an HTML priority chip span for a task."""
    if done:
        return '<span class="priority-chip chip-done">done</span>'
    cls_map = {"high": "chip-high", "medium": "chip-medium", "low": "chip-low"}
    css_cls = cls_map.get(priority, "chip-low")
    return f'<span class="priority-chip {css_cls}">{priority}</span>'


def task_icon(title: str) -> str:
    """Return a flat emoji icon based on keywords in the task title."""
    title_lc = title.lower()
    keyword_map = [
        (["med", "pill", "drug", "vaccine"],            "💊"),
        (["feed", "food", "meal", "breakfast", "dinner"], "🍽️"),
        (["walk", "leash", "run", "jog"],               "🦮"),
        (["brush", "groom", "bath"],                    "🪮"),
        (["play", "toy", "fetch", "train"],              "🦴"),
        (["vet", "check", "exam", "appt"],               "🩺"),
        (["litter", "clean", "scoop"],                  "🧹"),
    ]
    for keywords, ico in keyword_map:
        if any(w in title_lc for w in keywords):
            return ico
    return "🐾"


def render_task_row(
    task: Task,
    key_prefix: str,
    scheduler: Scheduler,
) -> None:
    """Render a single task as an icon + checkbox row."""
    ico = task_icon(task.title)
    col_a, col_b = st.columns([0.08, 0.92])
    with col_a:
        st.markdown(
            f'<div style="padding-top:5px;font-size:15px">{ico}</div>',
            unsafe_allow_html=True,
        )
    with col_b:
        label = (
            f"**{task.title}** — {task.pet_name}"
            f" · {task.time} · {task.duration_minutes} min"
        )
        checked = st.checkbox(
            label,
            value=task.completed,
            key=f"{key_prefix}_{task.pet_name}_{task.title}_{task.time}",
        )
        if checked and not task.completed:
            scheduler.mark_task_complete(task)
            st.rerun()


# ── Main app ──────────────────────────────────────────────────────────────────

def main() -> None:
    """Render the PawPal+ planner dashboard."""

    # Session state
    if "owner" not in st.session_state:
        st.session_state.owner = Owner("Jordan")
    if "active_pet" not in st.session_state:
        st.session_state.active_pet = None

    owner: Owner = st.session_state.owner
    scheduler = Scheduler(owner)
    active: str | None = st.session_state.active_pet

    # Header
    today = date.today()
    st.markdown(
        '<div class="app-header">🐾 PawPal+</div>'
        f'<div class="app-sub">{today.strftime("%A, %B %d %Y")}'
        f' &nbsp;·&nbsp; Good to see you, <b>{owner.name}</b></div>',
        unsafe_allow_html=True,
    )

    left, mid, right = st.columns([1, 2.2, 1.4])

    # ── LEFT ─────────────────────────────────────────────────────────────────
    with left:
        st.markdown('<div class="col-label">Pets</div>', unsafe_allow_html=True)

        # Pet selector buttons
        if st.button(
            f"{'✓ ' if active is None else ''}All pets",
            key="btn_all",
            use_container_width=True,
        ):
            st.session_state.active_pet = None
            st.rerun()

        for pet in owner.pets:
            is_active = active == pet.name
            btn_label = f"{'✓ ' if is_active else ''}{pet.name}"
            if st.button(btn_label, key=f"btn_{pet.name}", use_container_width=True):
                st.session_state.active_pet = None if is_active else pet.name
                st.rerun()

        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

        # Stats
        today_tasks_all = scheduler.get_todays_schedule()
        view_tasks = (
            [t for t in today_tasks_all if t.pet_name == active]
            if active else today_tasks_all
        )
        done_count = sum(1 for t in view_tasks if t.completed)
        total_count = len(view_tasks)
        mins_left = sum(
            t.duration_minutes for t in view_tasks if not t.completed
        )

        s1, s2 = st.columns(2)
        with s1:
            st.markdown(
                f'<div class="stat-box">'
                f'<div class="stat-num">{done_count}/{total_count}</div>'
                f'done today</div>',
                unsafe_allow_html=True,
            )
        with s2:
            st.markdown(
                f'<div class="stat-box">'
                f'<div class="stat-num">{mins_left}</div>'
                f'min left</div>',
                unsafe_allow_html=True,
            )

        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)

        with st.expander("➕ Add a pet"):
            with st.form("add_pet_form", clear_on_submit=True):
                new_pet_name = st.text_input("Name", placeholder="Mochi")
                new_pet_species = st.selectbox("Species", ["dog", "cat", "other"])
                if st.form_submit_button("Add pet", use_container_width=True):
                    if new_pet_name.strip():
                        owner.add_pet(
                            Pet(name=new_pet_name.strip(), species=new_pet_species)
                        )
                        st.rerun()
                    else:
                        st.warning("Enter a pet name.")

        if owner.pets:
            with st.expander("➕ Log a task"):
                with st.form("add_task_form", clear_on_submit=True):
                    task_title = st.text_input("Task", placeholder="Morning walk")
                    task_time = st.text_input("Time (HH:MM)", value="08:00")
                    task_dur = st.number_input(
                        "Duration (min)", min_value=1, max_value=240, value=20
                    )
                    task_pet = st.selectbox("Pet", [p.name for p in owner.pets])
                    task_prio = st.selectbox("Priority", ["high", "medium", "low"])
                    task_freq = st.selectbox("Repeats", ["once", "daily", "weekly"])
                    if st.form_submit_button("Log task", use_container_width=True):
                        if task_title.strip():
                            owner.get_pet(task_pet).add_task(Task(
                                title=task_title.strip(),
                                time=task_time,
                                duration_minutes=int(task_dur),
                                priority=task_prio,
                                frequency=task_freq,
                                pet_name=task_pet,
                                due_date=today,
                            ))
                            st.rerun()
                        else:
                            st.warning("Enter a task name.")

        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        new_name = st.text_input("Your name", value=owner.name)
        if new_name.strip() and new_name.strip() != owner.name:
            owner.name = new_name.strip()

    # ── MIDDLE ───────────────────────────────────────────────────────────────
    with mid:
        st.markdown('<div class="col-label">Today</div>', unsafe_allow_html=True)

        must_do = [
            t for t in view_tasks if not t.completed and t.priority == "high"
        ]
        nice_do = [
            t for t in view_tasks
            if not t.completed and t.priority in ("medium", "low")
        ]
        done_list = [t for t in view_tasks if t.completed]

        # Banner
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            for conflict in conflicts:
                st.markdown(
                    f'<div class="warn-banner">⚠️ {conflict}</div>',
                    unsafe_allow_html=True,
                )
        elif total_count > 0 and done_count == total_count:
            pet_name = active if active else "your pets"
            st.markdown(
                f'<div class="stress-banner">✅ You\'ve covered all the essentials'
                f' for <b>{pet_name}</b> today. Great job!</div>',
                unsafe_allow_html=True,
            )
        elif done_count > 0 and not must_do:
            pet_name = active if active else "your pets"
            st.markdown(
                f'<div class="stress-banner">✅ Non-negotiables done for'
                f' <b>{pet_name}</b>. Only nice-to-haves remain.</div>',
                unsafe_allow_html=True,
            )

        # Non-negotiables
        st.markdown(
            '<div class="section-title">💊 Daily non-negotiables'
            '<span style="font-size:11px;color:#94A3B8;font-weight:400;'
            'margin-left:4px;">— meds, meals, walks</span></div>',
            unsafe_allow_html=True,
        )
        if must_do:
            st.markdown('<div class="card card-critical">', unsafe_allow_html=True)
            for task in must_do:
                render_task_row(task, "must", scheduler)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="empty-state">🎉 All non-negotiables done for today.</div>',
                unsafe_allow_html=True,
            )

        # Nice-to-haves
        st.markdown(
            '<div class="section-title">🦴 If you have 10 minutes'
            '<span style="font-size:11px;color:#94A3B8;font-weight:400;'
            'margin-left:4px;">— enrichment, play, grooming</span></div>',
            unsafe_allow_html=True,
        )
        if nice_do:
            st.markdown('<div class="card card-nice">', unsafe_allow_html=True)
            for task in nice_do:
                render_task_row(task, "nice", scheduler)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="empty-state" style="border-color:#FED7AA;color:#D97706;">'
                '— No optional tasks logged for today.</div>',
                unsafe_allow_html=True,
            )

        # Completed
        if done_list:
            with st.expander(f"✓ Completed today ({len(done_list)})"):
                st.markdown('<div class="card card-done">', unsafe_allow_html=True)
                for task in done_list:
                    st.markdown(
                        f'<span style="color:#94A3B8;'
                        f'text-decoration:line-through;font-size:13px;">'
                        f'{task_icon(task.title)} {task.title}'
                        f' — {task.pet_name}</span>',
                        unsafe_allow_html=True,
                    )
                st.markdown('</div>', unsafe_allow_html=True)

        if not owner.pets:
            st.markdown(
                '<div class="empty-state">'
                'Add a pet in the left panel to get started.</div>',
                unsafe_allow_html=True,
            )

    # ── RIGHT ────────────────────────────────────────────────────────────────
    with right:
        st.markdown('<div class="col-label">This Week</div>', unsafe_allow_html=True)

        upcoming = scheduler.get_upcoming_tasks(days=7)
        if active:
            upcoming = [t for t in upcoming if t.pet_name == active]

        if not upcoming:
            st.markdown(
                '<div class="empty-state">'
                'No upcoming tasks in the next 7 days.</div>',
                unsafe_allow_html=True,
            )
        else:
            by_date: dict[date, list[Task]] = defaultdict(list)
            for task in upcoming:
                by_date[task.due_date].append(task)

            for day_offset in range(8):
                day = today + timedelta(days=day_offset)
                tasks_on_day = by_date.get(day, [])
                if not tasks_on_day:
                    continue

                is_today = day == today
                day_label = "Today" if is_today else day.strftime("%a %d")
                today_badge = (
                    '<span class="week-today-label">TODAY</span>'
                    if is_today else ""
                )
                st.markdown(
                    f'<div class="week-day">{day_label}{today_badge}</div>',
                    unsafe_allow_html=True,
                )

                for task in tasks_on_day:
                    ov_dot = (
                        '<span class="overdue-dot"></span>'
                        if task.due_date < today else ""
                    )
                    ov_cls = "week-overdue" if task.due_date < today else ""
                    ch_html = chip(task.priority)
                    row_html = (
                        f'<div class="week-task-row {ov_cls}">'
                        f'<span>{ov_dot}{task_icon(task.title)}'
                        f' {task.title[:20]}'
                        f'<span style="color:#94A3B8;font-size:11px;">'
                        f' · {task.pet_name}</span></span>'
                        f'<span style="white-space:nowrap">{ch_html}'
                        f'<span style="font-size:11px;color:#94A3B8;'
                        f'margin-left:4px;">{task.time}</span>'
                        f'</span></div>'
                    )
                    st.markdown(row_html, unsafe_allow_html=True)


main()
