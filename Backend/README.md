# 🚀 Backend – FastAPI Chat Service

This folder contains the backend service for the real-time chat app, built using **FastAPI** with **Socket.IO** for real-time communication and **JWT** for authentication.

## ⚙️ Tech Stack

- Python 3.11+
- FastAPI
- python-socketio
- PostgreSQL (via SQLAlchemy + AsyncPG)
- JWT (via PyJWT)
- Pydantic for data validation
- Alembic for database migrations
- Cloudinary for image uploads

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL database
- Cloudinary account (for image uploads)

### Installation

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Copy `.env` file and update with your values:
   ```bash
   DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/chatapp
   JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
   NODE_ENV=development
   PORT=8000
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   ```

4. **Initialize database**
   ```bash
   python init_db.py
   ```

5. **Run the server**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/v1/endpoints/     # API route definitions
│   ├── controllers/          # Business logic handlers
│   ├── core/                 # Core configurations (DB, Socket.IO)
│   ├── middleware/           # Authentication middleware
│   ├── models/               # SQLAlchemy database models
│   ├── schemas/              # Pydantic request/response schemas
│   └── db/                   # Database connection utilities
├── alembic/                  # Database migration files
├── main.py                   # FastAPI application entry point
├── init_db.py               # Database initialization script
└── requirements.txt          # Python dependencies
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `PUT /api/auth/update-profile` - Update profile picture
- `GET /api/auth/check` - Check authentication status

### Messages
- `GET /api/messages/users` - Get users for sidebar
- `GET /api/messages/{id}` - Get conversation history
- `POST /api/messages/send/{id}` - Send message

### WebSocket
- `WS /ws` - Socket.IO connection for real-time messaging

## 🗄️ Database Models

### User
- `id` (String, Primary Key)
- `full_name` (String)
- `email` (String, Unique)
- `password` (String, Hashed)
- `profile_pic` (String, Optional)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Message
- `id` (String, Primary Key)
- `sender_id` (String, Foreign Key)
- `receiver_id` (String, Foreign Key)
- `text` (String, Optional)
- `image` (String, Optional)
- `created_at` (DateTime)

## 🔧 Development

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Downgrade migration
alembic downgrade -1
```

### Running Tests
```bash
# Add your test commands here
pytest
```

## 🐳 Docker

Build and run with Docker:
```bash
docker build -t chat-backend .
docker run -p 8000:8000 chat-backend
```

## 🔒 Security Features

- JWT authentication with HTTP-only cookies
- Password hashing with bcrypt
- CORS configuration for frontend
- Protected routes middleware
- Input validation with Pydantic

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://postgres:1234@localhost:5432/chatapp` |
| `JWT_SECRET` | Secret key for JWT tokens | Required |
| `NODE_ENV` | Environment mode | `development` |
| `PORT` | Server port | `8000` |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name | Required |
| `CLOUDINARY_API_KEY` | Cloudinary API key | Required |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret | Required |
