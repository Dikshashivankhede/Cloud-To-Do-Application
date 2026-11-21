"""Streamlit UI for Cloud To-Do Application."""
from datetime import date
import streamlit as st
from app.database import initialize_database
from app.task_manager import create_task, delete_task, get_tasks, set_task_status, update_task


st.set_page_config(page_title="Cloud To-Do", page_icon="☁️", layout="wide")
initialize_database()


st.title("☁️ Cloud To-Do")
st.caption("A simple task manager with persistent SQLite storage.")


all_tasks = get_tasks()
total = len(all_tasks)
completed = sum(task["status"] == "Completed" for task in all_tasks)
pending = total - completed

c1, c2, c3 = st.columns(3)
c1.metric("Total tasks", total)
c2.metric("Pending", pending)
c3.metric("Completed", completed)
st.divider()

with st.expander("➕ Add a task", expanded=True):
    with st.form("add_task_form", clear_on_submit=True):
        title = st.text_input("Task title *", placeholder="e.g., Review API integration")
        description = st.text_area("Description", placeholder="Optional details")
        col1, col2 = st.columns(2)
        priority = col1.selectbox("Priority", ["Low", "Medium", "High"], index=1)
        due = col2.date_input("Due date (optional)", value=None)
        submitted = st.form_submit_button("Add task", type="primary")
        if submitted:
            if not title.strip():
                st.error("Please enter a task title.")
            else:
                create_task(title, description, priority, due.isoformat() if due else None)
                st.success("Task added.")
                st.rerun()

st.subheader("Your tasks")
filter_col1, filter_col2, filter_col3 = st.columns([1, 1, 2])
status_filter = filter_col1.selectbox("Status", ["All", "Pending", "Completed"])
priority_filter = filter_col2.selectbox("Priority", ["All", "High", "Medium", "Low"])
search_text = filter_col3.text_input("Search", placeholder="Search task title or description")
tasks = get_tasks(status_filter, priority_filter, search_text)
if not tasks:
    st.info("No tasks match these filters. Add a task or adjust the filters.")
else:
    for task in tasks:
        with st.container(border=True):
            title_col, status_col, action_col = st.columns([4, 1, 1])
            title_col.markdown(f"**{task['title']}**")
            title_col.caption(f"{task['priority']} priority · Due: {task['due_date'] or 'Not set'}")
            if task["description"]:
                title_col.write(task["description"])
            status_col.write(task["status"])
            toggle_label = "Mark pending" if task["status"] == "Completed" else "Complete"
            if status_col.button(toggle_label, key=f"status_{task['id']}"):
                new_status = "Pending" if task["status"] == "Completed" else "Completed"
                set_task_status(task["id"], new_status)
                st.rerun()
            if action_col.button("Delete", key=f"delete_{task['id']}"):
                delete_task(task["id"])
                st.rerun()

with st.expander("✏️ Edit a task"):
    if all_tasks:
        selected_id = st.selectbox("Choose task", [task["id"] for task in all_tasks], format_func=lambda task_id: next((f"#{task_id} — {t['title']}" for t in all_tasks if t["id"] == task_id), str(task_id)))
        selected = next(task for task in all_tasks if task["id"] == selected_id)
        with st.form("edit_task_form"):
            edit_title = st.text_input("Title", value=selected["title"])
            edit_description = st.text_area("Description", value=selected["description"] or "")
            edit_priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(selected["priority"]))
            edit_due = st.date_input("Due date", value=date.fromisoformat(selected["due_date"]) if selected["due_date"] else None)
            edit_status = st.selectbox("Status", ["Pending", "Completed"], index=["Pending", "Completed"].index(selected["status"]))
            save_edit = st.form_submit_button("Save changes")
            if save_edit:
                if not edit_title.strip():
                    st.error("Title cannot be empty.")
                else:
                    update_task(selected_id, edit_title, edit_description, edit_priority, edit_due.isoformat() if edit_due else None, edit_status)
                    st.success("Task updated.")
                    st.rerun()
    else:
        st.caption("Add a task first to enable editing.")


st.caption("Tasks are stored locally in a SQLite database. Cloud deployment and database persistence configuration will be handled in a later step.")
