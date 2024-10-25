# fastapi

[Edit in StackBlitz next generation editor ⚡️](https://stackblitz.com/~/github.com/zinxon/fastapi)

# MoonReader API

A FastAPI-based microservice for managing MoonReader highlights with PostgreSQL storage.

## Features

- ✨ Async API endpoints using FastAPI
- 🗃️ PostgreSQL database integration
- 📝 CRUD operations for highlights
- 🔐 Token-based authentication
- 📁 File-based storage backup
- 🧪 Comprehensive test suite

## Prerequisites

- Python 3.8+
- PostgreSQL
- Poetry (recommended) or pip

## Installation

1. Clone the repository:

```bash
git clone git@github.com:zinxon/fastapi.git moonreader-api
cd moonreader-api
```

2. Create and activate virtual environment & install dependencies:

```bash
python3 -m venv fastapi
source fastapi/bin/activate
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```
APP_ENV=development
LOG_LEVEL=debug
PORT=8000
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fastapi_db
MOONREADER_TOKEN=your_moonreader_token_here
```

4. Initialize the database:

```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

5. Build docker image:

```bash
docker build -t fastapi-app .
```

6. Run docker container:

```bash
docker run -p 8000:8000 fastapi-app
# docker run -p 8000:8000 -w /app/src fastapi-app
```

## Running the Application

Start the development server:

```bash
python src/main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Highlights

- `POST /highlights` - Create a new highlight
- `GET /highlights` - List all highlights
- `GET /highlights/{highlight_id}` - Get a specific highlight
- `GET /highlights/by-title/{title}` - Get highlights by book title
- `PUT /highlights/{highlight_id}` - Update a highlight
- `DELETE /highlights/{highlight_id}` - Delete a highlight

## Testing

Run the test suite:

```bash
python -m pytest tests
```

## Project Structure

```
├── src/
│   ├── main.py           # FastAPI application
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── crud.py          # Database operations
│   ├── database.py      # Database configuration
│   └── services/        # Business logic services
├── tests/               # Test suite
├── alembic/             # Database migrations
└── requirements.txt     # Project dependencies
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
