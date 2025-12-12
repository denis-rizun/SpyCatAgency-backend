# Spy Cat Agency - Backend API

Backend application for managing spy cats and their missions. Built with FastAPI and PostgreSQL.

## Requirements

- Python 3.13
- PostgreSQL 16
- Docker and Docker Compose (optional, for containerized setup)

## Installation

### Using Docker (Recommended)

1. Clone the repository
2. Create a `.env` file in the root directory with the following variables:

```env
INNER_API_PORT=8000
OUTER_API_PORT=8000
API_WORKERS_AMOUNT=1
POSTGRES_USER=user
POSTGRES_PASSWORD=user
POSTGRES_DB=db
POSTGRES_HOST=database
INNER_POSTGRES_PORT=5432
OUTER_POSTGRES_PORT=5432
BREED_VALIDATOR_API_URL=https://api.thecatapi.com/v1/breeds
```

3. Start the application using Docker Compose:

```bash
make run
```
or
```bash
docker-compose --env-file=.env -f deploy/dockers/compose.yml up --build -d
```

This will start:
- PostgreSQL database
- API server
- Database migrations

The API will be available at `http://0.0.0.0:8000` (or another port which you set)


## API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://0.0.0.0:8000/docs
- **ReDoc**: http://0.0.0.0:8000/redoc

## API Endpoints

### Health Check

- `GET /health` - Check if the API is running

### Cats

- `POST /api/v1/cats` - Create a new spy cat
- `GET /api/v1/cats` - Get all spy cats
- `GET /api/v1/cats/{id}` - Get a spy cat by ID
- `PATCH /api/v1/cats/{id}` - Update a spy cat's salary
- `DELETE /api/v1/cats/{id}` - Delete a spy cat

### Missions

- `POST /api/v1/missions` - Create a new mission with targets (1-3 targets)
- `GET /api/v1/missions` - Get all missions
- `GET /api/v1/missions/{id}` - Get a mission by ID
- `POST /api/v1/missions/{id}/assign` - Assign a cat to a mission
- `PATCH /api/v1/missions/{id}/targets` - Update mission targets
- `DELETE /api/v1/missions/{id}` - Delete a mission

## Postman Collection

All API endpoints are documented in the Postman collection file: `postman_collection.json`

**To import the collection:**

1. Open Postman
2. Click "Import" button
3. Select the `postman_collection.json` file from the project root
4. The collection will be imported with all endpoints

**To configure the base URL:**

1. Select the collection in Postman
2. Go to the "Variables" tab
3. Set the `base_url` variable to `http://localhost:8000` (or your server URL)
4. Save the collection

The collection includes:
- All API endpoints organized by category (Health, Cats, Missions)
- Example request bodies for POST and PATCH requests
- Pre-configured headers
- Environment variable for easy URL switching

## Business Rules

### Cats
- A cat can have only one active mission at a time
- You cannot delete a cat if it has an active mission
- Only the salary can be updated

### Missions
- A mission must have between 1 and 3 targets
- You cannot delete a mission if it is assigned to a cat
- When all targets are completed, the mission is automatically marked as completed
- Targets are deleted automatically when a mission is deleted

### Targets
- You cannot update notes if the target or mission is completed
- Notes are frozen once a target is completed

### Breed Validation
- Cat breeds are validated using TheCatAPI
- Only valid breeds from the API are accepted

## Response Format

All API responses follow this format:

```json
{
  "statusCode": 200,
  "message": "ok",
  "data": ...
}
```

## Error Handling

The API returns appropriate HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation errors)
- `404` - Not Found
- `500` - Internal Server Error

Error responses include a message describing what went wrong.


## Project Structure

```
backend/
├── src/
│   ├── api/              # API routes and handlers
│   ├── application/      # Business logic services
│   ├── core/             # Core configuration and exceptions
│   ├── domain/           # Domain models and enums
│   ├── infra/            # Infrastructure (database, schemas, DI)
│   └── main.py           # Application entry point
├── deploy/               # Docker configuration
├── alembic.ini           # Alembic configuration
├── requirements.txt      # Python dependencies
└── postman_collection.json
```

## Troubleshooting

### Database Connection Issues
- Check that PostgreSQL is running
- Verify database credentials in `.env` file
- Ensure the database exists

### Migration Issues
- Make sure you're using the correct database URL
- Check that all previous migrations are applied

### Port Already in Use
- Change the port in the compose.yml
- Check if another process is using port 8000

