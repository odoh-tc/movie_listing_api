# Database Design

## Users Table

| Column                    | Type     | Description                               |
| ------------------------- | -------- | ----------------------------------------- |
| id                        | UUID     | Primary Key                               |
| email                     | String   | User email address                        |
| first_name                | String   | User's first name                         |
| last_name                 | String   | User's last name                          |
| hashed_password           | String   | Hashed password for authentication        |
| is_verified               | Boolean  | Indicates if the user's email is verified |
| verification_token        | String   | Token used for email verification         |
| verification_token_expiry | DateTime | Expiry date for the verification token    |

- **Relationships:**
  - `movies`: Relationship to `Movie` model, representing movies listed by the user.
  - `ratings`: Relationship to `Rating` model, representing ratings given by the user.
  - `comments`: Relationship to `Comment` model, representing comments made by the user.

## Movies Table

| Column       | Type    | Description                      |
| ------------ | ------- | -------------------------------- |
| id           | UUID    | Primary Key                      |
| title        | String  | Movie title                      |
| description  | String  | Movie description                |
| duration     | Integer | Duration of the movie in minutes |
| release_date | Date    | Release date of the movie        |
| poster_url   | String  | URL of the movie poster          |
| owner_id     | UUID    | Foreign Key to Users (owner)     |

- **Relationships:**
  - `owner`: Relationship to `User` model, representing the user who listed the movie.
  - `ratings`: Relationship to `Rating` model, representing ratings associated with the movie.
  - `comments`: Relationship to `Comment` model, representing comments associated with the movie.

## Ratings Table

| Column   | Type    | Description                    |
| -------- | ------- | ------------------------------ |
| id       | UUID    | Primary Key                    |
| score    | Integer | Rating score (e.g., 1-5 stars) |
| review   | String  | Optional review text           |
| movie_id | UUID    | Foreign Key to Movies          |
| user_id  | UUID    | Foreign Key to Users           |

- **Relationships:**
  - `movie`: Relationship to `Movie` model, representing the movie being rated.
  - `user`: Relationship to `User` model, representing the user who gave the rating.

## Comments Table

| Column            | Type   | Description                                |
| ----------------- | ------ | ------------------------------------------ |
| id                | UUID   | Primary Key                                |
| content           | String | Comment content                            |
| movie_id          | UUID   | Foreign Key to Movies                      |
| parent_comment_id | UUID   | Foreign Key to Comments (self-referential) |
| user_id           | UUID   | Foreign Key to Users                       |

- **Relationships:**
  - `user`: Relationship to `User` model, representing the user who made the comment.
  - `movie`: Relationship to `Movie` model, representing the movie associated with the comment.
  - `parent_comment`: Relationship to `Comment` model, representing the parent comment if nested.
  - `replies`: Relationship to `Comment` model, representing replies to the comment.
