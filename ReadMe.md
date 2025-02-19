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

This API uses JWT (JSON Web Tokens) for authentication. Users can obtain an access token by providing their username and password to the `/token` endpoint. This token can then be used to access protected endpoints.

### Obtaining an Access Token

Send a `POST` request to the `/token` endpoint with the username and password in the request body, using the `application/x-www-form-urlencoded` format.

**Request:**

POST /token
Content-Type: application/x-www-form-urlencoded

username=your_username&password=your_password

**Response (Success - 200 OK):**

```json
{
  "access_token": "your_access_token",
  "token_type": "bearer"
}
```

### Error Handling

The API will return appropriate HTTP status codes and JSON error responses for authentication-related issues. Common errors include:

401 Unauthorized: Incorrect credentials, invalid token, or missing token.
404 Not Found: User not found.

**Response (Error - 401 Unauthorized):**

```json
{
  "detail": "Incorrect username or password",
  "headers": {
    "WWW-Authenticate": "Bearer"
  }
}
```

Accessing Protected Endpoints
To access a protected endpoint, include the access token in the Authorization header of your request, using the Bearer scheme.

**Request:**

GET /users/me (or any other protected endpoint)
Authorization: Bearer your_access_token
Response (Success - 200 OK):

```json
{
  "id": "user_id",
  "username": "your_username"
  // ... other user data
}
```

**Response (Error - 401 Unauthorized - Invalid or Expired Token):**

```json
{
  "detail": "Invalid token"
}
```

## Refreshing Tokens

Send a `POST` request to the `/refresh_token` endpoint with the refresh token in the `Authorization` header, using the `Bearer` scheme.

**Request:**
POST /refresh_token
Authorization: Bearer your_refresh_token

**Response (Success - 200 OK):**

```json
{
  "access_token": "your_new_access_token",
  "token_type": "bearer"
}
```

**Response (Error - 401 Unauthorized):**

```json
{
  "detail": "Invalid refresh token"
}
```

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
