# Movie Listing API

Welcome to the **Movie Listing API**! This API allows you to manage movies, including adding, viewing, updating, and deleting movies. It also features user authentication, rating systems, and comment management.

## Table of Contents

- [Movie Listing API](#movie-listing-api)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Environment Variables](#environment-variables)
  - [Middleware](#middleware)
  - [Local Development Setup](#local-development-setup)
  - [Docker Deployment](#docker-deployment)
  - [Testing](#testing)
    - [Testing Locally](#testing-locally)
    - [Testing with Docker Compose](#testing-with-docker-compose)
  - [API Endpoints](#api-endpoints)
    - [Authentication](#authentication)
    - [User](#user)
    - [Movies](#movies)
    - [Ratings](#ratings)
    - [Comments](#comments)
  - [License](#license)

## Features

- **User Authentication:** Secure user registration and login with JWT-based authentication.
- **Email Verification:** Upon registration, users receive an email containing a verification link. This link includes a unique token that is valid for a specific period. Users should click this link to verify their email address. If the token expires, users can request a new verification email.
- **Movie Listing:** Users can browse a collection of movies, including details like title, description, release date, duration, and poster. Advanced search, filtering, and sorting options are available.
- **Movie Ratings and Comments:** Users can rate movies and leave comments, which can be viewed by others. Ratings and comments can be filtered and sorted based on user preferences.
- **Secure API:** JWT authentication ensures that only authorized users can access certain endpoints.
- **Logging:** Logs are sent to both the terminal and Papertrail for centralized logging and monitoring, providing insights into application performance and issues.
- **Rate Limiting:** SlowAPI is used to apply rate limits to API endpoints to prevent abuse and ensure fair usage.
- **Cloud Deployment:** The API is deployed on a cloud platform, ensuring high availability and scalability.
- **Comprehensive Testing:** Unit and integration tests are implemented to ensure the reliability of the API.
- **Documentation:** The API is documented using OpenAPI/Swagger for an interactive interface to explore endpoints, complemented by a detailed README for easy setup, deployment, and usage instructions.

## Requirements

- Python 3.8+
- PostgreSQL 13+
- Docker and Docker Compose

## Environment Variables

Create a `.env` file in the root directory of your project and add the following:

```env
DATABASE_URL=postgresql://<db_user>:<db_password>@<db_host>:<db_port>/<db_name>
TEST_DATABASE_URL=
TESTING=false
SECRET_KEY=<your_secret_key>
ACCESS_TOKEN_EXPIRE_MINUTES=
ALGORITHM=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
SMTP_SERVER=
SMTP_PORT=
SMTP_SENDER=
SMTP_PASSWORD=
BASE_URL=<your_base_url>
VERIFICATION_TOKEN_EXPIRE_HOURS=
PAPERTRAIL_URL=
PAPERTRAIL_PORT=
```

## Middleware

- **ErrorHandlingMiddleware:** Catches and handles errors across the API to provide consistent error responses.
- **LoggingMiddleware:** Logs requests and responses for debugging and monitoring purposes.
- **AuthMiddleware:** Manages authentication for protected routes, excluding specific public paths and authentication routes.
- **SlowAPIMiddleware:** Applies rate limiting to manage API request rates and prevent abuse.
- **CORS Middleware:** Manages Cross-Origin Resource Sharing (CORS) to control access based on the origin of requests.

## Local Development Setup

1. Clone the repository

   ```sh
   git clone https://github.com/username/movie_listing_api.git

   cd movie_listing_api
   ```

2. Create and activate a virtual environment

   ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies

   ```sh
    pip install -r requirements.txt
   ```

4. Set up the database
   Ensure PostgreSQL is installed and running. Then, create the database:

   ```sh
    psql -U <your_postgres_user> -c "CREATE DATABASE <your_db_name>;"
   ```

5. Start the FastAPI server

```sh
 uvicorn app.main:app --reload
```

The server should now be running at `http://localhost:8000`.

## Docker Deployment

To deploy the application using Docker Compose:

1. Build and start the containers

Ensure Docker and Docker Compose are installed, then run:

```sh
docker-compose up --build -d
```

1. Access the API
   The API will be accessible at `http://localhost:8000`.

2. Stopping the containers
   To stop the containers, run:

```sh
docker-compose down
```

## Testing

### Testing Locally

You can run the tests using pytest. To do this, execute the following command:

```bash
pytest
```

Ensure that the TEST_DATABASE_URL is properly configured in your .env file before running the tests.

### Testing with Docker Compose

To run tests within a Docker environment using Docker Compose, follow these steps:

1. Make sure your Docker containers are up and running. You can do this with:

```sh
docker-compose up --build
```

2. Run the Tests:
   Execute the tests within the Docker container by running:

```sh
docker-compose exec <service_name> pytest
```

Replace <service_name> with the name of the service defined in your docker-compose.yml file where pytest should be run (typically, this would be the service running your FastAPI application).

Ensure that the TEST_DATABASE_URL and other environment variables are correctly set in your Docker environment.

## API Endpoints

<!-- Detailed API documentation is available through Swagger UI at `http://localhost:8000/docs` or Redoc at `http://localhost:8000/redoc`. -->

<!-- ### Authentication

- **POST /auth/register**: Register a new user.
- **POST /auth/login**: Authenticate and get an access token.
- **POST /auth/login/token**: Obtain an access token using email and password. This is an alternative way to get a token.
- **POST /auth/resend-verification**: Resend verification email.
- **GET /auth/verify-email**: Verify a user's email using a token.

### User

- **GET /users/me**: Retrieve current user details. -->

### Authentication

- **POST /auth/register**

  - **Description**: Register a new user.
  - **Request Body**:
    ```json
    {
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "password": "password123"
    }
    ```
  - **Response**:
    ```json
    {
      "success": true,
      "status_code": 201,
      "message": "User registered successfully. Please check your email for verification link.",
      "data": {
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "is_verified": false
      }
    }
    ```
  - **Error Response**:
    ```json
    {
    "success": false,
    "status_code": <status_code>,
    "message": "<error_message>"
    }
    ```

- **POST /auth/login**

  - **Description**: Authenticate and get an access token.
  - **Request Body**:

    ```json
    {
      "email": "user@example.com",
      "password": "password123"
    }
    ```

  - **Response**:
    ```json
    {
      "success": true,
      "status_code": 200,
      "message": "Login successful",
      "data": {
        "user": {
          "email": "user@example.com",
          "id": "123e4567-e89b-12d3-a456-426614174000",
          "first_name": "John",
          "last_name": "Doe",
          "is_verified": false,
          "created_at": "2024-08-14T12:34:56Z"
        },
        "access_token": "your_access_token_here",
        "token_type": "bearer"
      }
    }
    ```
  - **Error Response**:
    ```json
    {
      "success": false,
      "status_code": 401,
      "message": "Incorrect email or password"
    }
    ```

- **POST /auth/login/token**

  - **Description**: Obtain an access token using email and password. This is an alternative way to get a token.
  - **Request Body**:
    ```json
    {
      "email": "user@example.com",
      "password": "password123"
    }
    ```
  - **Response**:
    ```json
    {
      "access_token": "your_access_token_here",
      "token_type": "bearer"
    }
    ```

- **POST /auth/resend-verification**

  - **Description**: Resend verification email.
  - **Request Body**:
    ```json
    {
      "email": "user@example.com"
    }
    ```
  - **Response**:
    ```json
    {
      "success": true,
      "status_code": 200,
      "message": "Verification email resent. Please check your email."
    }
    ```

- **GET /auth/verify-email**

  - **Description**: Verify a user's email using a token.
  - **Query Parameters**:
    - `token` (string): The email verification token.
  - **Response**:

    ```json
    {
      "success": true,
      "status_code": 200,
      "message": "Email verified successfully"
    }
    ```

  - **Error Response**:
    ```json
    {
      "success": false,
      "status_code": 400,
      "message": "Invalid or expired token"
    }
    ```

### User

- **GET /users/me**
  - **Description**: Retrieve current user details.
  - **Response**:
    ```json
    {
      "success": true,
      "status_code": 200,
      "message": "User data fetched successfully",
      "data": {
        "email": "user@example.com",
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "first_name": "John",
        "last_name": "Doe",
        "is_verified": true,
        "created_at": "2024-08-14T12:34:56Z"
      }
    }
    ```

<!-- ### Movies

- **POST /movies/**: Add a new movie.
- **GET /movies/{movie_id}**: Retrieve a specific movie.
- **GET /movies/**: List movies with optional search, pagination, etc.
- **PUT /movies/{movie_id}**: Update a specific movie.
- **DELETE /movies/{movie_id}**: Delete a specific movie. -->

### Movies

**POST /movies/**

**Description:**  
This endpoint allows an authenticated user to add a new movie.

**Request:**

- **Headers:**

  - `Authorization: Bearer <JWT_TOKEN>`

- **Body:**

  ```json
  {
    "title": "Inception",
    "description": "A mind-bending thriller about dreams within dreams.",
    "duration": 148,
    "release_date": "2010-07-16",
    "poster_url": "https://example.com/poster.jpg"
  }
  ```

- **Response**:

  - **Success**:

    ```json
    {
      "success": true,
      "status_code": 201,
      "message": "Movie added successfully",
      "data": {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "title": "Inception",
        "description": "A mind-bending thriller about dreams within dreams.",
        "duration": 148,
        "release_date": "2010-07-16",
        "poster_url": "https://example.com/poster.jpg",
        "owner_id": "123e4567-e89b-12d3-a456-426614174001",
        "created_at": "2024-08-14T12:00:00Z",
        "updated_at": "2024-08-14T12:00:00Z"
      }
    }
    ```

  - **Failure**:

    ```json
      {
      "success": false,
      "status_code": <status_code>,
      "message": "<error_message>"
      }
    ```

**GET /movies/{movie_id}**

Retrieve a specific movie.

- **Path Parameters**:

  - `movie_id`: The unique identifier of the movie.

- **Responses**:

  - **Success**:

    ```json
    {
      "success": true,
      "status_code": 200,
      "message": "Movie retrieved successfully",
      "data": {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "title": "Inception",
        "description": "A mind-bending thriller about dreams within dreams.",
        "duration": 148,
        "release_date": "2010-07-16",
        "poster_url": "https://example.com/poster.jpg",
        "owner_id": "123e4567-e89b-12d3-a456-426614174001",
        "created_at": "2024-08-14T12:00:00Z",
        "updated_at": "2024-08-14T12:00:00Z"
      }
    }
    ```

  - **Failure**:

    ```json
    {
      "success": false,
      "status_code": 404,
      "message": "Movie not found"
    }
    ```

**GET /movies/**

List movies with optional search, pagination, and sorting.

- **Query Parameters**:

  - `skip`: Number of items to skip (default: 0).
  - `limit`: Maximum number of items to return (default: 10).
  - `search`: Search term for filtering movies (optional).
  - `sort_by`: Sort criteria (options: most_rated, most_recent, most_rated_and_recent).

- **Responses**:

  - **Success**:

    ```json
    {
      "success": true,
      "status_code": 200,
      "message": "Movies retrieved successfully",
      "data": {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "title": "Inception",
        "description": "A mind-bending thriller about dreams within dreams.",
        "duration": 148,
        "release_date": "2010-07-16",
        "poster_url": "https://example.com/poster.jpg",
        "owner_id": "123e4567-e89b-12d3-a456-426614174001",
        "created_at": "2024-08-14T12:00:00Z",
        "updated_at": "2024-08-14T12:00:00Z"
      }
    }
    ```

  **PUT /movies/{movie_id}**

Update a specific movie.

- **Path Parameters**:

  - `movie_id`: The unique identifier of the movie.

- **Headers**:

  - `Authorization: Bearer <JWT_TOKEN>`

- **Request Body**:

  ```json
  {
    "title": "Inception",
    "description": "An updated description for the movie.",
    "duration": 148,
    "release_date": "2010-07-16",
    "poster_url": "https://example.com/new_poster.jpg"
  }
  ```

- **Responses**:

  - **Success**:

    ```json
    {
      "success": true,
      "status_code": 200,
      "message": "Movie updated successfully",
      "data": {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "title": "Inception",
        "description": "An updated description for the movie.",
        "duration": 148,
        "release_date": "2010-07-16",
        "poster_url": "https://example.com/new_poster.jpg",
        "owner_id": "123e4567-e89b-12d3-a456-426614174001",
        "created_at": "2024-08-14T12:00:00Z",
        "updated_at": "2024-08-14T12:00:00Z"
      }
    }
    ```

  - **Failure**:

    ```json
    {
      "success": false,
      "status_code": 404,
      "message": "Movie not found"
    }
    ```

**DELETE /movies/{movie_id}**

Delete a specific movie.

- **Path Parameters**:

  - `movie_id`: The unique identifier of the movie.

- **Headers**:

  - `Authorization: Bearer <JWT_TOKEN>`

- **Responses**:

  - **Success**:

    ```json
    {
      "success": true,
      "status_code": 204,
      "message": "Movie deleted successfully"
    }
    ```

  - **Failure**:

    ```json
    {
      "success": false,
      "status_code": 404,
      "message": "Movie not found"
    }
    ```

<!-- ### Ratings

- **POST /ratings/**: Rate a movie.
- **GET /ratings/{movie_id}**: View ratings for a specific movie. -->

### Ratings

- **POST /ratings/**: Rate a movie.

  - **Description**: This endpoint allows an authenticated user to rate a movie. If the user has already rated the movie, their rating will be updated.

  - **Request**:

    - **Headers**:

      - `Authorization: Bearer <JWT_TOKEN>`

    - **Body**:

      ```json
      {
        "movie_id": "123e4567-e89b-12d3-a456-426614174000",
        "score": 5,
        "review": "Amazing movie!"
      }
      ```

  - **Response**:

    - **Success**:

      ```json
      {
        "success": true,
        "status_code": 201,
        "message": "Movie rated successfully",
        "data": {
          "id": "123e4567-e89b-12d3-a456-426614174001",
          "movie_id": "123e4567-e89b-12d3-a456-426614174000",
          "user_id": "123e4567-e89b-12d3-a456-426614174002",
          "score": 5,
          "review": "Amazing movie!",
          "created_at": "2024-08-14T12:00:00Z",
          "updated_at": "2024-08-14T12:00:00Z"
        }
      }
      ```

    - **Failure**:

      ```json
      {
        "success": false,
        "status_code": 404,
        "message": "Movie with id 123e4567-e89b-12d3-a456-426614174000 not found"
      }
      ```

- **GET /ratings/{movie_id}**: View ratings for a specific movie.

  - **Description**: This endpoint allows users to view all ratings for a specific movie, along with an aggregated average score.

  - **Parameters**:

    - **Path Parameter**:

      - `movie_id`: The unique identifier of the movie.

    - **Query Parameters** (optional):

      - `skip`: Number of items to skip for pagination. Default is 0.
      - `limit`: Maximum number of items to return. Default is 10.
      - `rating_score`: Filter ratings by a specific score (e.g., 1-5).

  - **Response**:

    - **Success**:

      ```json
      {
        "success": true,
        "status_code": 200,
        "message": "Ratings retrieved successfully",
        "data": {
          "aggregated_rating": {
            "average_score": 5
          },
          "ratings": [
            {
              "id": "123e4567-e89b-12d3-a456-426614174001",
              "user_id": "123e4567-e89b-12d3-a456-426614174002",
              "score": 5,
              "review": "Amazing movie!",
              "created_at": "2024-08-14T12:00:00Z",
              "updated_at": "2024-08-14T12:00:00Z"
            }
          ]
        }
      }
      ```

    - **Failure**:

      ```json
      {
        "success": false,
        "status_code": 404,
        "message": "Movie with id 123e4567-e89b-12d3-a456-426614174000 not found"
      }
      ```

### Comments

- **POST /comments/**

  - **Description**: Allows an authenticated user to add a new comment to a specific movie.

  - **Request**:

    - **Headers**:

      - `Authorization: Bearer <JWT_TOKEN>`

    - **Body**:

      ```json
      {
        "content": "This movie was absolutely mind-blowing!",
        "movie_id": "123e4567-e89b-12d3-a456-426614174000"
      }
      ```

  - **Response**:

    - **Success**:

      ```json
      {
        "success": true,
        "status_code": 201,
        "message": "Comment added successfully",
        "data": [
          {
            "id": "123e4567-e89b-12d3-a456-426614174001",
            "content": "This movie was absolutely mind-blowing!",
            "movie_id": "123e4567-e89b-12d3-a456-426614174000",
            "user_id": "123e4567-e89b-12d3-a456-426614174002",
            "parent_comment_id": null,
            "created_at": "2024-08-14T12:00:00Z",
            "updated_at": "2024-08-14T12:00:00Z"
          }
        ]
      }
      ```

    - **Failure**:

      ```json
          {
          "success": false,
          "status_code": <status_code>,
          "message": "<error_message>"
        }
      ```

- **GET /comments/{movie_id}**: Retrieve comments for a specific movie.

  - **Parameters**:

    - **Path Parameter**:

      - `movie_id`: The unique identifier of the movie.

    - **Query Parameters** (optional):

      - `skip`: Number of items to skip for pagination. Default is 0.
      - `limit`: Maximum number of items to return. Default is 10.
      - `sort_order`: Sort order for comments (options: most_recent, from_oldest).

  - **Response**:

    - **Success**:

      ```json
      {
        "success": true,
        "status_code": 200,
        "message": "Comments retrieved successfully",
        "data": [
          {
            "id": "123e4567-e89b-12d3-a456-426614174001",
            "content": "This movie was absolutely mind-blowing!",
            "movie_id": "123e4567-e89b-12d3-a456-426614174000",
            "user_id": "123e4567-e89b-12d3-a456-426614174002",
            "parent_comment_id": null,
            "created_at": "2024-08-14T12:00:00Z",
            "updated_at": "2024-08-14T12:00:00Z",
            "replies": [
              {
                "id": "123e4567-e89b-12d3-a456-426614174003",
                "content": "I agree! The special effects were stunning.",
                "movie_id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "123e4567-e89b-12d3-a456-426614174004",
                "parent_comment_id": "123e4567-e89b-12d3-a456-426614174001",
                "created_at": "2024-08-14T12:05:00Z",
                "updated_at": "2024-08-14T12:05:00Z"
              }
            ]
          }
        ]
      }
      ```

    - **Failure**:

      ```json
      {
        "success": false,
        "status_code": 404,
        "message": "Movie with id 123e4567-e89b-12d3-a456-426614174000 not found"
      }
      ```

- **POST /comments/nested**

  - **Description**: Allows an authenticated user to add a nested reply to an existing comment.

  - **Request**:

    - **Headers**:

      - `Authorization: Bearer <JWT_TOKEN>`

    - **Body**:

      ```json
      {
        "content": "I agree! The special effects were stunning.",
        "parent_comment_id": "123e4567-e89b-12d3-a456-426614174001"
      }
      ```

  - **Response**:

    - **Success**:

      ```json
      {
        "success": true,
        "status_code": 201,
        "message": "Nested comment added successfully",
        "data": [
          {
            "id": "123e4567-e89b-12d3-a456-426614174003",
            "content": "I agree! The special effects were stunning.",
            "movie_id": null,
            "user_id": "123e4567-e89b-12d3-a456-426614174004",
            "parent_comment_id": "123e4567-e89b-12d3-a456-426614174001",
            "created_at": "2024-08-14T12:05:00Z",
            "updated_at": "2024-08-14T12:05:00Z"
          }
        ]
      }
      ```

    - **Failure**:

      ```json
          {
          "success": false,
          "status_code": <status_code>,
          "message": "<error_message>"
        }
      ```

<!-- - **POST /comments/**: Add a comment to a movie.
- **GET /comments/{movie_id}**: View comments for a specific movie.
- **POST /comments/nested**: Add a nested comment. -->

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
