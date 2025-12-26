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

PUT /api/task/time

GET /api/tasks/<task_id>

GET /api/weeks/<week_id>/tasks
- Get tasks for a week

DELETE /api/tasks/<task_id>

## Category

POST /api/category/create

GET /api/categories/<category_id>

DELETE /api/categories/<category_id>