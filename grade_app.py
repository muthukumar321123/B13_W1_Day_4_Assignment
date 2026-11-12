import streamlit as st

# Page configuration
st.set_page_config(page_title="Student Grade Manager", layout="centered")
st.title("Student Grade Manager")


# Grading logic from Day 2
def get_grade(mark: float) -> str:
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "F"


# Initialize session_state so data survives script reruns
if "students" not in st.session_state:
    st.session_state.students = []

# Form to add a student
with st.form("add_student_form", clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        name = st.text_input("Name")
    with col2:
        # Rejects marks outside 0 to 100 in the interface
        mark = st.number_input("Mark", min_value=0, max_value=100, step=1)

    submitted = st.form_submit_button("Add")

    if submitted:
        clean_name = name.strip()
        if not clean_name:
            st.warning("Please enter a valid student name.")
        elif mark < 0 or mark > 100:
            st.error("Mark must be between 0 and 100.")
        else:
            grade = get_grade(mark)
            st.session_state.students.append({
                "Name": clean_name,
                "Mark": int(mark),
                "Grade": grade
            })
            st.success(f"Added {clean_name} (Mark: {int(mark)}, Grade: {grade})")

# Display table and class metrics when students exist
if st.session_state.students:
    st.subheader("Results")
    st.table(st.session_state.students)

    # Calculate class figures using pure Python
    marks = [student["Mark"] for student in st.session_state.students]
    avg_mark = sum(marks) / len(marks)
    highest_mark = max(marks)
    lowest_mark = min(marks)

    # Display class metrics in 3 columns
    m1, m2, m3 = st.columns(3)
    m1.metric("Average", f"{avg_mark:.1f}")
    m2.metric("Highest", highest_mark)
    m3.metric("Lowest", lowest_mark)
else:
    st.info("No students added yet. Use the form above to add your first student.")