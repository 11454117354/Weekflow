# API Overview

## User

POST /api/register
- Get users registered
    ```json
    {
        "username": "chen",
        "password": "1",
        "password_confirm": "1"
    }

POST /api/login
- User login
    ```json
    {
        "username": "chen",
        "password": "1"
    }

GET /api/me
- Get users' info for frontend

POST /api/logout
- User logout

## Weeks

POST /api/week/create
- Create a new "week"
    ```json
    {
    "name": "week1",
    "start_time": "2025-12-26T15:30:00",
    "end_time": "2025-12-26T16:30:00"
    }

GET /api/weeks/<week_id>
- Get specific week name and info

GET /api/weeks/last
- Get the last week the user has ever viewed

DELETE /api/weeks/delete
- Delete a week

## Tasks

POST /api/task/create
- Create a new task in specific week
    ```json
    {
        "title":"cs50 final project",
        "ddl":"2025-12-30T12:00:00",
        "category_id":"1",
        "remark":"",
        "week_id":"1"
    }

PATCH /api/task/<task_id>/time
- Add the start time and end time of a task
    ```json
    {
        "start_time":"2025-12-29T12:00:00",
        "end_time":"2025-12-29T13:00:00"
    }

GET /api/tasks/<task_id>
- Get a certain task

GET /api/weeks/<week_id>/tasks
- Get tasks for a week

DELETE /api/tasks/<task_id>
- Delete a task

## Categories

POST /api/category/create
- Add a category

GET /api/categories/<category_id>
- Get info of a category

DELETE /api/categories/<category_id>
- Delete a category