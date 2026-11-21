"""CRUD functions for the task table."""
from app.database import get_connection



VALID_PRIORITIES = {"Low", "Medium", "High"}
VALID_STATUSES = {"Pending", "Completed"}



def create_task(title: str, description: str = "", priority: str = "Medium", due_date: str | None = None) -> None:
    title = title.strip()
    if not title:
        raise ValueError("Task title cannot be empty.")
    if priority not in VALID_PRIORITIES:
        raise ValueError("Choose a valid priority.")
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO tasks (title, description, priority, due_date) VALUES (?, ?, ?, ?)",
            (title, description.strip(), priority, due_date or None),
        )
        conn.commit()



def get_tasks(status: str = "All", priority: str = "All", search: str = "") -> list[dict]:
    query = "SELECT * FROM tasks WHERE 1=1"
    params: list[str] = []
    if status != "All":
        query += " AND status = ?"
        params.append(status)
    if priority != "All":
        query += " AND priority = ?"
        params.append(priority)
    if search.strip():
        query += " AND (title LIKE ? OR description LIKE ?)"
        params.extend([f"%{search.strip()}%", f"%{search.strip()}%"])
    query += " ORDER BY CASE status WHEN 'Pending' THEN 0 ELSE 1 END, CASE priority WHEN 'High' THEN 0 WHEN 'Medium' THEN 1 ELSE 2 END, due_date IS NULL, due_date, id DESC"
    with get_connection() as conn:
        return [dict(row) for row in conn.execute(query, params).fetchall()]



def update_task(task_id: int, title: str, description: str, priority: str, due_date: str | None, status: str) -> None:
    if not title.strip():
        raise ValueError("Task title cannot be empty.")
    if priority not in VALID_PRIORITIES or status not in VALID_STATUSES:
        raise ValueError("Invalid task priority or status.")
    with get_connection() as conn:
        conn.execute(
            "UPDATE tasks SET title=?, description=?, priority=?, due_date=?, status=? WHERE id=?",
            (title.strip(), description.strip(), priority, due_date or None, status, task_id),
        )
        conn.commit()



def delete_task(task_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()



def set_task_status(task_id: int, status: str) -> None:
    if status not in VALID_STATUSES:
        raise ValueError("Invalid status.")
    with get_connection() as conn:
        conn.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
        conn.commit()
