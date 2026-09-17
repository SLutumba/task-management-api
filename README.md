# Task Management API

A Python and Flask API for managing user-owned tasks. Users register, sign in and manage their tasks through JWT-protected endpoints backed by SQLAlchemy and SQLite.

**Status:** the core authenticated CRUD workflow is implemented. Error handling, date consistency and an automated regression suite are the next work items. See [API_SPEC.md](API_SPEC.md) for the implemented API, including its current limitations.

## Features

- Registration and login with bcrypt password hashing and signed JWT access tokens.
- JWT protection on task creation, listing, retrieval, updates and deletion.
- Ownership checks in database queries: users can access only their own tasks.
- Pydantic validation for user and task input, including allowed status and priority values.
- Partial updates that preserve omitted fields and allow optional fields to be cleared.
- Separate routes, schemas, services, models and serialization helpers.
- Database transaction rollback on failed writes and session cleanup in routes.

## Run locally

Tested with Python 3.12. Commands below use Bash, including Git Bash on Windows.

```bash
git clone https://github.com/SLutumba/task-management-api.git
cd task-management-api
python -m venv venv
```

Activate the environment in **Git Bash on Windows**:

```bash
source venv/Scripts/activate
```

On **Linux or macOS**:

```bash
source venv/bin/activate
```

Install the dependencies, create a development secret and start the server from the repository root:

```bash
python -m pip install -r requirements.txt
export JWT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
python -m flask --app main run
```

The server listens at `http://127.0.0.1:5000`. The application reads `JWT_SECRET_KEY` from the shell environment; it does not load a `.env` file automatically. Run the export command again in a new shell session. Changing the secret invalidates tokens signed with the previous value.

SQLite tables are created on application import, and local data is stored in `app/database.db`, relative to the working directory. Table creation does not migrate an existing schema. Schema migrations have not been added yet.

Check that the application responds:

```bash
curl -i http://127.0.0.1:5000/tasks/health
```

Expected: `200 OK` with `{"status":"healthy"}`. The health route is public and is not a database connectivity check.

## Try the task workflow

Register a new account:

```bash
curl -i -X POST http://127.0.0.1:5000/users/register \
  -H 'Content-Type: application/json' \
  -d '{"username":"demo_user","email":"demo@example.com","password":"DemoPassword123!"}'
```

Registration returns `201` and an `access_token`. For an existing account, sign in instead:

```bash
curl -i -X POST http://127.0.0.1:5000/users/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"demo@example.com","password":"DemoPassword123!"}'
```

Copy the returned token into a shell variable. Tokens currently expire after 15 minutes; sign in again for a new token.

```bash
export TOKEN='paste-access-token-here'

curl -i -X POST http://127.0.0.1:5000/tasks/create \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"title":"Review API docs","description":"Check examples","status":"To-Do","priority":"Medium","due_date":null}'

curl -i http://127.0.0.1:5000/tasks/ \
  -H "Authorization: Bearer $TOKEN"
```

Use the task ID returned by creation in the remaining requests:

```bash
TASK_ID=1 # Replace with the returned id.

curl -i "http://127.0.0.1:5000/tasks/$TASK_ID" \
  -H "Authorization: Bearer $TOKEN"

curl -i -X PATCH "http://127.0.0.1:5000/tasks/$TASK_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"status":"Complete","description":null}'

curl -i -X DELETE "http://127.0.0.1:5000/tasks/$TASK_ID" \
  -H "Authorization: Bearer $TOKEN"
```

Deletion returns `204` with no body. Accessing a missing task or another user's task returns `404`.

## Endpoint overview

Paths have no `/api` prefix. The table shows the current implementation's success codes.

| Method | Path | Authentication | Success |
|---|---|---|---|
| POST | `/users/register` | Public | `201`, access token |
| POST | `/users/login` | Public | `200`, access token |
| POST | `/tasks/create` | Bearer token | `200`, task object |
| GET | `/tasks/` | Bearer token | `201`, task array |
| GET | `/tasks/{task_id}` | Bearer token | `200`, task object |
| PATCH | `/tasks/{task_id}` | Bearer token | `200`, updated task |
| DELETE | `/tasks/{task_id}` | Bearer token | `204`, empty body |
| GET or POST | `/users/health`, `/tasks/health` | Public | `200`, health object |

The create/list codes need correction to `201`/`200` respectively. They are documented as implemented here so examples do not promise different behaviour from the code.

## Implementation

| Location | Responsibility |
|---|---|
| `main.py` | Flask application, blueprint registration and JWT configuration |
| `app/api/` | HTTP handling, token identity, validation and application-error responses |
| `app/schemas/` | Pydantic request models and field validation |
| `app/services/` | Task ownership queries, business rules and database writes |
| `app/models/` | SQLAlchemy user/task tables and relationships |
| `app/database.py` | SQLite engine, session factory and initial table creation |
| `app/utils/` | Password hashing and task serialization helpers |

Each task has one owner through `user_id`; a user can own many tasks. Ownership is taken from the authenticated token, not a request body. Single-task queries filter by both task ID and owner ID, so missing and inaccessible tasks produce the same status code.

For PATCH requests, `model_dump(exclude_unset=True)` distinguishes an omitted field from an explicit `null`. This allows a description or due date to be cleared without overwriting unrelated fields.

## Verification and remaining work

A review of application commit `b937cb5` exercised registration, login, task CRUD, missing/expired tokens, two-user ownership isolation and partial-update behaviour using an isolated SQLite database. It also reproduced the issues below. That review is not a committed automated test suite.

- Correct create/list success codes and use a validation-error response for past due dates instead of `406`.
- Choose a consistent datetime policy. Timezone-aware input currently causes `500`; returned date strings also differ from accepted input strings.
- Handle duplicate usernames as conflicts, validate bcrypt's password byte limit and remove submitted input from authentication validation errors.
- Apply consistent title rules to creation and updates, and normalise error responses.
- Add regression tests and run them in CI, prioritising ownership isolation and failed requests.

Filtering, pagination, refresh tokens, deployment and database migrations are not implemented. These are separate enhancements; the current task workflow does not depend on them.

## License

A license has not yet been selected.
