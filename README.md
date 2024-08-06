# Movie Listing API

## Overview

The **Movie Listing API** is a comprehensive API designed to manage a movie catalog. It allows you to add, view, update, and delete movies, as well as rate and comment on them. This project is built with FastAPI and utilizes Docker Compose for deployment.

## Features

- **User Authentication**

  - User registration
  - User login
  - JWT token generation

- **Movie Listing**

  - View a movie added (public access)
  - Add a movie (authenticated access)
  - View all movies (public access)
  - Edit a movie (only by the user who listed it)
  - Delete a movie (only by the user who listed it)

- **Movie Rating**

  - Rate a movie (authenticated access)
  - Get ratings for a movie (public access)

- **Comments**
  - Add a comment to a movie (authenticated access)
  - View comments for a movie (public access)
  - Add comment to a comment (nested comments, authenticated access)

## Getting Started

To get started with this project, follow these steps:

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/movie-listing-api.git
   cd movie-listing-api
   ```

## Installation

1. Clone the repository:
   ```sh
   git clone <repository-url>
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up the database:
   ```sh
   alembic upgrade head
   ```
4. Run the application:
   ```sh
   uvicorn app.main:app --reload
   ```

## Running Tests

Run the tests using pytest:

```sh
pytest
```

Create a .env File

Copy the .env.example file to .env and update the environment variables as needed.

bash
Copy code
cp .env.example .env
Build and Start the Containers

Use Docker Compose to build and start the containers.

bash
Copy code
docker-compose up --build
