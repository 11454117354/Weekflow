# API Overview

## User

POST /api/users
- Get users registered

POST /api/login
- User login

GET /api/me
- Get users' info for frontend

POST /api/logout
- User logout

## Weeks

GET /api/weeks/current
- Get current week data

## Tasks

POST /api/tasks
- Create a new task

GET /api/weeks/<week_id>/tasks
- Get tasks for a week

## Schedules

POST /api/schedules
- Assign time block to a task

DELETE /api/schedules/<id>
- Remove a scheduled time block