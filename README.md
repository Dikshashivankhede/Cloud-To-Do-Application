# Cloud To-Do Application

A task management web app built with Python and Streamlit, using SQLite for persistent local storage. Planned deployment target: AWS EC2.

## Features
- Create tasks with descriptions, priority, and optional due dates
- View, search, and filter tasks
- Mark tasks as pending or completed
- Edit task details and delete tasks
- Dashboard counters for total, pending, and completed tasks
- SQLite-backed storage

## Tech stack
Python, Streamlit, SQLite/SQL, Git/GitHub. AWS EC2 and Linux are planned for deployment.

## Local setup
1. Install Python 3.10 or newer.
2. Create and activate a virtual environment.
   - Windows PowerShell: `python -m venv .venv` then ` .\.venv\Scripts\Activate.ps1`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the app from the project root: `streamlit run app/main.py`
5. Open the local URL Streamlit prints in the terminal.


## Project structure
```text
Cloud-To-Do-Application/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── task_manager.py
│   └── main.py
├── data/                 # created automatically; SQLite database is local and gitignored
├── screenshots/           # add project screenshots here
├── .streamlit/config.toml
├── .gitignore
├── requirements.txt
└── README.md
```

## Notes
- The SQLite database is created automatically in `data/tasks.db` when the app starts.
- `data/*.db` is excluded from Git to avoid committing local task data.
- Cloud deployment and production database persistence are not configured yet.
