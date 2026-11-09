import html

import streamlit as st

# ---------------------------------------------------------------
# Student Grade Manager (Streamlit version of the Day 2 program)
#
# Storage: a list of dictionaries kept in st.session_state.
# Why session_state: Streamlit reruns this whole script on every
# click, so a plain `students = []` would be wiped each time.
# Why a list of dictionaries: it keeps the order students were
# added and allows two students with the same name.
#
# Note: the table and the grade chart are drawn with plain HTML,
# because pandas is blocked on this computer.
# ---------------------------------------------------------------

st.set_page_config(
    page_title="Student Grade Manager",
    page_icon="🎓",
    layout="wide",
)

# ---------- Styling ----------
st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; max-width: 1100px;}
    .hero {
        background: linear-gradient(90deg, #8B1A24, #C0202F);
        padding: 1.6rem 2rem;
        border-radius: 14px;
        margin-bottom: 1.5rem;
    }
    .hero h1 {color: #ffffff; margin: 0; font-size: 2rem;}
    .hero p {color: #ffffff; margin: 0.3rem 0 0 0; opacity: 0.9;}
    .grade-table {width: 100%; border-collapse: collapse; font-size: 1rem;}
    .grade-table th {
        text-align: left; padding: 0.75rem 1rem;
        background: #8B1A24; color: #ffffff;
    }
    .grade-table td {
        padding: 0.7rem 1rem;
        border-bottom: 1px solid rgba(128, 128, 128, 0.25);
    }
    .grade-table tr:nth-child(even) td {background: rgba(128, 128, 128, 0.07);}
    .badge {
        display: inline-block; min-width: 2.2rem; text-align: center;
        padding: 0.15rem 0.7rem; border-radius: 999px;
        color: #ffffff; font-weight: 700;
    }
    .g-A {background: #2E7D32;}
    .g-B {background: #1E88E5;}
    .g-C {background: #F9A825;}
    .g-D {background: #EF6C00;}
    .g-E {background: #C62828;}
    .bar-row {display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.7rem;}
    .bar-label {width: 1.5rem; font-weight: 700;}
    .bar-track {
        flex: 1; height: 1.1rem; border-radius: 999px; overflow: hidden;
        background: rgba(128, 128, 128, 0.18);
    }
    .bar-fill {height: 100%; border-radius: 999px;}
    .bar-count {width: 2rem; text-align: right;}
    .scale-title {font-weight: 700; margin: 0.25rem 0 0.5rem 0;}
    .scale-table {width: 100%; border-collapse: collapse;}
    .scale-table td {
        padding: 0.3rem 0.4rem; border: none;
        background: transparent; vertical-align: middle;
    }
    .scale-table td:first-child {width: 3rem;}

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- Logic (get_grade is unchanged from Day 2) ----------
def get_grade(mark):
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "E"


# ---------- Storage that survives reruns ----------
if "students" not in st.session_state:
    st.session_state.students = []

# ---------- Header ----------
st.markdown(
    """
    <div class="hero">
        <h1>🎓 Student Grade Manager</h1>
        <p>Add students, see their grades, and track class performance.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Sidebar: add-student form ----------
with st.sidebar:
    st.header("➕ Add a student")
    with st.form("add", clear_on_submit=True):
        name = st.text_input("Name", placeholder="e.g. Priya")
        mark = st.number_input(
            "Mark (0 to 100)", min_value=0, max_value=100, value=0, step=1
        )
        submitted = st.form_submit_button("Add student")

    st.divider()
    if st.button("🗑️ Clear all students", disabled=not st.session_state.students):
        st.session_state.students = []

    scale = [
        ("A", "90 to 100"),
        ("B", "80 to 89"),
        ("C", "70 to 79"),
        ("D", "60 to 69"),
        ("E", "Below 60"),
    ]
    scale_rows = ""
    for grade_letter, mark_range in scale:
        scale_rows += (
            f"<tr><td><span class='badge g-{grade_letter}'>{grade_letter}</span></td>"
            f"<td>{mark_range}</td></tr>"
        )
    st.markdown(
        "<div class='scale-title'>Grading scale</div>"
        f"<table class='scale-table'>{scale_rows}</table>",
        unsafe_allow_html=True,
    )

# ---------- Handle the form ----------
if submitted:
    clean_name = name.strip()
    if clean_name == "":
        st.sidebar.error("Name cannot be empty.")
    elif mark < 0 or mark > 100:
        st.sidebar.error("Mark must be between 0 and 100.")
    else:
        st.session_state.students.append({"name": clean_name, "mark": int(mark)})
        st.sidebar.success(f"Added {clean_name} with mark {int(mark)}.")

# ---------- Main page ----------
students = st.session_state.students

if not students:
    st.info("No students yet. Use the form in the sidebar to add your first student.")
else:
    marks = [s["mark"] for s in students]
    average = sum(marks) / len(marks)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Students", len(marks))
    c2.metric("Class average", f"{average:.1f}")
    c3.metric("Highest", max(marks))
    c4.metric("Lowest", min(marks))

    st.write("")
    left, right = st.columns([3, 2])

    with left:
        st.subheader("Results")
        rows = ""
        for s in students:
            grade = get_grade(s["mark"])
            rows += (
                f"<tr><td>{html.escape(s['name'])}</td>"
                f"<td>{s['mark']}</td>"
                f"<td><span class='badge g-{grade}'>{grade}</span></td></tr>"
            )
        st.markdown(
            "<table class='grade-table'>"
            "<tr><th>Name</th><th>Mark</th><th>Grade</th></tr>"
            f"{rows}</table>",
            unsafe_allow_html=True,
        )

    with right:
        st.subheader("Grade distribution")
        counts = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0}
        for s in students:
            counts[get_grade(s["mark"])] += 1
        biggest = max(counts.values())
        bars = ""
        for grade, count in counts.items():
            width = count / biggest * 100
            bars += (
                f"<div class='bar-row'><span class='bar-label'>{grade}</span>"
                f"<div class='bar-track'>"
                f"<div class='bar-fill g-{grade}' style='width:{width}%'></div>"
                f"</div><span class='bar-count'>{count}</span></div>"
            )
        st.markdown(bars, unsafe_allow_html=True)