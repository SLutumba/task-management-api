# Endpoints
- Register User
- Login
- Get Tasks
- Create Task
- Update Task
- Delete Task

## Register User
### Request:
POST /api/auth/register
{
    "username": "name",
    "email": "email@stuff.com",
    "password": "supersecretpassword"
}
### Response:
####  Success
- Code: 201
- Body:
{
    "message": "User successfully registered."
}

#### Failures
- Code: 500
{
    "Internal server issue, please try again"
}
- Code: 400
{
    "error": "Missing email/username/password"
}
- Code: 409
{
    "error": "email/username already exists"
}

## Login
### Request:
POST /api/auth/login
{
    "username": "name",
    "password": "supersecretpassword"
}

### Response:
####  Success
- Code: 200
- Body:
{
    "token": "jwt_token."
}

#### Failures
- Code: 500
{
    "Internal server issue, please try again"
}
- Code: 400
{
    "error": "Missing email/username/password"
}
- Code: 404
{
    "error": "User with username not found"
}
- Code: 401
{
    "error": "Invalid password"
}

## Create Task
### Request:
POST /api/tasks/
{

    "title": "title",
    "description": "describeit",
    "status": "created",
    "priority": "low",
    "due_date": ?
}

### Response:
####  Success
- Code: 201
- Body:
{
    "task_id", 1
    "user_id", 1
    "title": "title",
    "description": "describeit",
    "status": "created",
    "priority": "low",
    "due_date": ?
}

#### Failures
- Code: 500
{
    "Internal server issue, please try again"
}
- Code: 400
{
    "error": "Missing details (title, status, or priority)"
}
- Code: 401
{
    "error": "You're not logged in, you can't create any tasks"
}

## Get Tasks
### Request:
GET /api/tasks/

### Response:
####  Success
- Code: 200
- Body:
{
    {"title": "title",
    "description": "describeit",
    "status": "created",
    "priority": "low",
    "due_date": ?},

    {"title": "title2",
    "description": "describeit2",
    "status": "created",
    "priority": "low",
    "due_date": ?}
}

#### Failures
- Code: 500
{
    "Internal server issue, please try again"
}

- Code: 401
{
    "error": "You're not logged in, you can't access any tasks"
}
- Code: 403
{
    "error": "the tasks you're trying to retrieve don't belong to you"
}
## Get Task
### Request:
GET /api/tasks/{id}

### Response:
####  Success
- Code: 200
- Body:
{
    {"title": "title",
    "description": "describeit",
    "status": "created",
    "priority": "low",
    "due_date": ?}
}

#### Failures
- Code: 500
{
    "Internal server issue, please try again"
}

- Code: 401
{
    "error": "You're not logged in, you can't access any tasks"
}
- Code: 403
{
    "error": "the tasks you're trying to retrieve don't belong to you"
}
- Code: 404
{
    "error": "no such task exists"
}

## Update Task
### Request:
PUT /api/tasks/{task_id}
{
    "title": "title",
    "description": "describeit",
    "status": "created",
    "priority": "low",
    "due_date": ?
}

### Response:
####  Success
- Code: 200
- Body:
{
    "title": "title",
    "description": "describeit",
    "status": "created",
    "priority": "low",
    "due_date": ?
}

#### Failures
- Code: 500
{
    "Internal server issue, please try again"
}
- Code: 400
{
    "error": "Missing details (title, status, or priority)"
}
- Code: 401
{
    "error": "You're not logged in, you can't access any tasks"
}
- Code: 403
{
    "error": "the tasks you're trying to edit don't belong to you"
}

## Delete Task
### Request:
DELETE /api/tasks/{task_id}


### Response:
####  Success
- Code: 204
- Body:
{
   "success": "deletion was successful"
}

#### Failures
- Code: 500
{
    "Internal server issue, please try again"
}
- Code: 400
{
    "error": "Missing task id"
}
- Code: 401
{
    "error": "You're not logged in, you can't delete any tasks"
}
- Code: 403
{
    "error": "the tasks you're trying to delete don't belong to you"
}