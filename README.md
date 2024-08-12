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
  - [API Endpoints](#api-endpoints)
    - [Authentication](#authentication)
    - [User](#user)
    - [Movies](#movies)
    - [Ratings](#ratings)
    - [Comments](#comments)
  - [Testing](#testing)
    - [Testing Locally](#testing-locally)
    - [Testing with Docker Compose](#testing-with-docker-compose)
  - [License](#license)

## Features

- **User Authentication:** Secure user registration and login with JWT-based authentication.
- **Email Verification:** Upon registration, users receive an email containing a verification link. This link includes a unique token that is valid for a specific period. Users should click this link to verify their email address. If the token expires, users can request a new verification email.
- **Movie Listing:** Users can browse a collection of movies, including details like title, description, release date, duration, and poster.
- **Movie Ratings and Comments:** Users can rate movies and leave comments, which can be viewed by others.
- **Secure API:** JWT authentication ensures that only authorized users can access certain endpoints.
- **Logging:** Logs are sent to both the terminal and Papertrail for centralized logging and monitoring, providing insights into application performance and issues.
- **Rate Limiting:** SlowAPI is used to apply rate limits to API endpoints to prevent abuse and ensure fair usage.
- **Cloud Deployment:** The API is deployed on a cloud platform, ensuring high availability and scalability.
- **Comprehensive Testing:** Unit and integration tests are implemented to ensure the reliability of the API.
- **Documentation:** The API is documented using OpenAPI/Swagger, providing an interactive interface for exploring the endpoints.

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
   git clone https://github.com/yourusername/movielistingapi.git

   cd movielistingapi
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

This will start the following services:

- **db**: PostgreSQL database.
- **app**: FastAPI application.
- **adminer**: Adminer for database management, accessible at `http://localhost:8080`.
- **npm**: Nginx Proxy Manager, accessible at `http://localhost:81`.

2. Access the API
   The API will be accessible at `http://localhost:8000`.

3. Stopping the containers
   To stop the containers, run:

```sh
docker-compose down
```

## API Endpoints

Detailed API documentation is available through Swagger UI at `http://localhost:8000/docs` or Redoc at `http://localhost:8000/redoc`.

### Authentication

- **POST /auth/register**: Register a new user.
- **POST /auth/login**: Authenticate and get an access token.
- **POST /auth/login/token**: Obtain an access token using email and password. This is an alternative way to get a token.
- **POST /auth/resend-verification**: Resend verification email.
- **GET /auth/verify-email**: Verify a user's email using a token.

### User

- **GET /users/me**: Retrieve current user details.

### Movies

- **POST /movies/**: Add a new movie.
- **GET /movies/{movie_id}**: Retrieve a specific movie.
- **GET /movies/**: List movies with optional search, pagination, etc.
- **PUT /movies/{movie_id}**: Update a specific movie.
- **DELETE /movies/{movie_id}**: Delete a specific movie.

### Ratings

- **POST /ratings/**: Rate a movie.
- **GET /ratings/{movie_id}**: View ratings for a specific movie.

### Comments

- **POST /comments/**: Add a comment to a movie.
- **GET /comments/{movie_id}**: View comments for a specific movie.
- **POST /comments/nested**: Add a nested comment.

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

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
