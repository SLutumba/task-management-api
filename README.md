# Task Management API

A REST-style backend API for managing user-owned tasks, built with Flask and SQLAlchemy.

The project is being developed as a hands-on backend engineering project rather than a simple CRUD exercise. The goal is to build the API while practising clear application boundaries, database design, authentication, authorization, validation, error handling, and maintainable code structure.

## Project Status

**In development.**

Currently implemented:

- User registration
- User login
- Password hashing and verification with bcrypt
- Request validation with Pydantic
- JWT access-token generation
- SQLAlchemy `User` and `Task` models
- Shared SQLAlchemy declarative base and database session setup
- Application-specific authentication exceptions

Currently in progress:

- JWT-protected Task endpoints
- User-scoped task retrieval
- Task creation, update, and deletion
- Object-level authorization so users can only access their own tasks
- Task request/response schemas
- Automated testing

## Architecture

The project follows a layered structure so that each part of the application has a focused responsibility:

```text
Client
  ↓
Route / API layer
  ↓
Schema / validation layer
  ↓
Service layer
  ↓
ORM / database layer
```

### Responsibilities

- **Routes** — handle HTTP requests, responses, status codes, JWT/framework concerns, and translate known application errors into HTTP responses.
- **Schemas** — validate and structure incoming request data.
- **Services** — contain application and business logic while coordinating database operations.
- **Models** — map Python objects to relational database tables through SQLAlchemy.
- **Database** — stores application data and enforces persistence-level constraints.

A key design principle for the project is:

> Each layer should know only what it needs to know to perform its responsibility.

## Tech Stack

- Python
- Flask
- Flask-JWT-Extended
- SQLAlchemy ORM
- Pydantic
- bcrypt
- SQLite for local development

## Project Structure

```text
task-management-api/
├── app/
│   ├── api/
│   │   ├── tasks.py
│   │   └── users.py
│   ├── models/
│   │   ├── base.py
│   │   ├── task.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── task.py
│   │   └── user.py
│   ├── services/
│   │   └── user.py
│   ├── utils/
│   │   └── security.py
│   ├── database.py
│   └── exceptions.py
├── API_SPEC.md
├── main.py
├── requirements.txt
└── README.md
```

## Data Model

### User

A user has a unique username and email, a securely stored password hash, audit timestamps, and can own multiple tasks.

### Task

A task belongs to one user and contains:

- title
- optional description
- status
- priority
- optional due date
- created and updated timestamps

The relationship is:

```text
User 1 ──────── * Task
```

Each Task stores a `user_id` foreign key referencing its owner.

## Authentication

Passwords are never stored directly. Registration hashes the supplied password with bcrypt and stores only the resulting password hash.

Login verifies the supplied credentials and, when authentication succeeds, returns a signed JWT access token.

The user ID is used as the JWT identity so protected routes can determine which authenticated user is making the request.

## Current API

### Health Checks

```http
GET /users/health
GET /tasks/health
```

### Register

```http
POST /users/register
```

Example request:

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "strongpassword123"
}
```

Successful registration creates the account and immediately returns an access token:

```json
{
  "access_token": "<jwt>"
}
```

Status: `201 Created`

### Login

```http
POST /users/login
```

Example request:

```json
{
  "email": "test@example.com",
  "password": "strongpassword123"
}
```

Successful response:

```json
{
  "access_token": "<jwt>"
}
```

Status: `200 OK`

Known authentication failures are translated into appropriate HTTP responses, including `400 Bad Request`, `401 Unauthorized`, and `409 Conflict`.

> Task endpoints are still being developed and secured. Their public contract may change until the authentication and authorization flow is complete.

## Running Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd task-management-api
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/Scripts/activate
```

The activation command above is for Git Bash on Windows. On Linux/macOS, use:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

The dependency file is being cleaned up as part of the current development work. The application currently depends on Flask, SQLAlchemy, Pydantic, email-validator, bcrypt, and Flask-JWT-Extended.

### 4. Configure the JWT secret

The application expects `JWT_SECRET_KEY` to exist in the environment and intentionally fails to start when it is missing.

Generate a development secret:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Then export it in Bash:

```bash
export JWT_SECRET_KEY="your-generated-secret"
```

Do not commit the JWT secret to the repository.

### 5. Start the application

```bash
flask --app main run --debug
```

The local SQLite database is created from the registered SQLAlchemy model metadata during development.

## Engineering Goals

This project is also being used to practise several backend engineering principles:

- Keep HTTP/framework concerns out of the service layer.
- Separate structural validation from database-dependent business rules.
- Inject database sessions rather than creating them inside services.
- Roll back failed transactions before propagating errors.
- Store password hashes rather than recoverable passwords.
- Use application-specific exceptions for known business failures.
- Apply authorization directly to database queries where possible.
- Prefer simple designs until additional complexity solves a real problem.

## Roadmap

- [x] Design initial relational model
- [x] Build SQLAlchemy models and relationships
- [x] Add database session infrastructure
- [x] Add registration and password hashing
- [x] Add login and credential verification
- [x] Add JWT access-token creation
- [ ] Protect Task routes with JWT authentication
- [ ] Extract authenticated user identity
- [ ] Implement user-scoped Task queries
- [ ] Add create/update/delete Task operations
- [ ] Add object-level authorization
- [ ] Finalize Task schemas and serialization
- [ ] Add automated tests
- [ ] Improve configuration and environment management
- [ ] Add database migrations

## API Specification

`API_SPEC.md` contains the original API design notes. The implementation is evolving as the project is developed, so the README and running application should be treated as the more current representation of implemented behaviour until the API specification is revised.

## License

This project is currently intended for learning and portfolio development. A license has not yet been selected.
