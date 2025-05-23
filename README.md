# Latam Users API

A RESTful FastAPI service for managing users and roles, following best practices for API design, validation, testing, and cloud deployment.

---

## Features

- **User & Role Management:** CRUD operations for users and roles.
- **Validation & Error Handling:** Pydantic models and proper HTTP error codes.
- **OpenAPI/Swagger Docs:** Auto-generated at `/docs`.
- **Dockerized:** Ready for containerized deployment.
- **Cloud Ready:** Includes `cloudbuild.yaml` for Google Cloud Build & Run.
- **Unit Tested:** Comprehensive tests for all endpoints.

---

## API Endpoints

### List Roles

**GET** `/roles`

**Response Example:**
```json
[
  {"id": 1, "name": "admin", "description": "Administrator"},
  {"id": 2, "name": "user", "description": "Regular user"},
  {"id": 3, "name": "guest", "description": "Guest user"}
]
```

---

### List Users

**GET** `/users`

**Response Example:**
```json
[
  {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "first_name": "Alice",
    "last_name": "Smith",
    "active": true,
    "created_at": "2023-10-01T12:00:00",
    "updated_at": "2023-10-01T12:00:00"
  }
]
```

---

### Retrieve User

**GET** `/users/{id}`

**Response Example:**
```json
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com",
  "first_name": "Alice",
  "last_name": "Smith",
  "active": true,
  "created_at": "2023-10-01T12:00:00",
  "updated_at": "2023-10-01T12:00:00",
  "role": {"id": 1, "name": "admin", "description": "Administrator"}
}
```
**404 Example:**
```json
{"detail": "User not found"}
```

---

### Create User

**POST** `/users`

**Request Example:**
```json
{
  "username": "charlie",
  "email": "charlie@example.com",
  "first_name": "Charlie",
  "last_name": "Brown",
  "active": true,
  "created_at": "2023-10-01T12:00:00",
  "updated_at": "2023-10-01T12:00:00",
  "role_id": 2
}
```
**Response Example:**
```json
{
  "id": 3,
  "username": "charlie",
  "email": "charlie@example.com",
  "first_name": "Charlie",
  "last_name": "Brown",
  "active": true,
  "created_at": "2023-10-01T12:00:00",
  "updated_at": "2023-10-01T12:00:00",
  "role": {"id": 2, "name": "user", "description": "Regular user"}
}
```
**422 Example:**
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

### Update User

**PUT** `/users/{id}`

**Request Example:**
```json
{
  "username": "alice",
  "email": "alice@newdomain.com",
  "first_name": "Alice",
  "last_name": "Smith",
  "active": true,
  "created_at": "2023-10-01T12:00:00",
  "updated_at": "2023-10-01T12:00:00",
  "role_id": 1
}
```
**Response Example:**
```json
{
  "id": 1,
  "username": "alice",
  "email": "alice@newdomain.com",
  "first_name": "Alice",
  "last_name": "Smith",
  "active": true,
  "created_at": "2023-10-01T12:00:00",
  "updated_at": "2023-10-01T12:00:00",
  "role": {"id": 1, "name": "admin", "description": "Administrator"}
}
```
**404 Example:**
```json
{"detail": "User not found"}
```

---

### Delete User

**DELETE** `/users/{id}`

**Response Example:**
```json
true
```
**404 Example:**
```json
{"detail": "User not found"}
```

---

## How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd latam_users_api
   ```

2. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Access the API docs:**
   - Open [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Loading Initial Data

To load initial roles or other seed data, run:

```bash
python loader.py
```

This will populate the database with default roles and any other initial data defined in `loader.py`.

---

## Running Unit Tests

Unit tests are located in `users/tests_controllers.py` and cover all API endpoints, including both success and failure cases.

**To run tests:**
```bash
pytest users/tests_controllers.py
```

**Test coverage includes:**
- Listing roles and users
- Retrieving, creating, updating, and deleting users
- Handling not found and validation errors

---

## Cloud Deployment

To deploy to Google Cloud Run using Cloud Build:

1. Push your code to GitHub.
2. Ensure `cloudbuild.yaml` is in the project root.
3. Connect your repo to Google Cloud Build triggers.
4. Cloud Build will build the Docker image and deploy to Cloud Run automatically.

---

## License

MIT

---
