# Linkstore API Documentation

## Overview

This API was developed with the assistance of AI tools (Gemini and Claude 3.5 Sonnet (Copilot Version)) to serve as the backend for a Flutter application. It provides user management and link storage functionality.

## Base Command

uvicorn main:app --reload --host 10.0.0.102 --port 8000

## Base URL

`http://10.0.0.102:8000`

## Live Demo URL

https://linkstore-api.vercel.app/docs

## Authentication

Basic authentication using username and password.

## Endpoints

### Users

- `POST /users/` - Create new user
- `GET /users/` - Get all users
- `GET /users/{user_id}` - Get specific user
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user
- `POST /users/validate` - Validate user data
- `POST /users/{user_id}/profile-pic` - Upload profile picture
- `POST /login` - User login

### Links

- `POST /users/{user_id}/links/` - Create new link
- `GET /users/{user_id}/links` - Get user's links
- `GET /links/{link_id}` - Get specific link
- `PUT /links/{link_id}` - Update link
- `DELETE /links/{link_id}` - Delete link

## Technologies Used

- FastAPI
- SQLAlchemy
- SQLLite

## Flutter Integration

This API is designed to work seamlessly with Flutter applications for cross-platform mobile development.
