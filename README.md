# Weekly Time Manager

A weekly-based time management tool for tracking deadlines and scheduling work time.

This project was built as my CS50 Final Project.
I wanted to create a tool that fits my owm study habits: managing deadlines and planning word on a weekly basis rather than daily task lists.

## Features

- User authentication
- View tasks and deadlines by week
- Add deadlines with due dates and estimated time
- Assign specific time blocks to tasks within a week
- Auto-delaying for unfinished work to the next week

## Tech Stack

- Backend: Flask(Python)
- Database: SQLite
- Frontend: HTML, CSS, Javascript, Jinja2
- API: REST-style JSON APIs

## How to Run

1. Clone the repository
2. Create a virtual environment and install dependencies:
    ```bash
    pip install -r requirements.txt
3. Initialize the database:
    ```bash
    python3 ./create_db.py
4. Run the application:
    ```bash
    flask run
5. Open the browser at http://127.0.0.1:5000
   
## Future Improvememts
- iOS client using the same API
- Visually-appealing calender with task blocks and class schedule
- A build-in focus timer 
  
