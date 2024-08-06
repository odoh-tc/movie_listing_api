# Database Design

## Users Table

| Column   | Type    | Description   |
| -------- | ------- | ------------- |
| id       | INTEGER | Primary Key   |
| email    | TEXT    | User email    |
| password | TEXT    | User password |

- **Relationships:**
  - `movies`: Relationship to `Movie` model, representing movies listed by the user.
  - `ratings`: Relationship to `Rating` model, representing ratings given by the user.
  - `comments`: Relationship to `Comment` model, representing comments made by the user.

## Movies Table

| Column      | Type    | Description          |
| ----------- | ------- | -------------------- |
| id          | INTEGER | Primary Key          |
| title       | TEXT    | Movie title          |
| description | TEXT    | Movie description    |
| owner_id    | INTEGER | Foreign Key to Users |

- **Relationships:**
  - `owner`: Relationship to `User` model, representing the user who listed the movie.
  - `ratings`: Relationship to `Rating` model, representing ratings associated with the movie.
  - `comments`: Relationship to `Comment` model, representing comments associated with the movie.

## Ratings Table

| Column   | Type    | Description                        |
| -------- | ------- | ---------------------------------- |
| id       | INTEGER | Primary Key                        |
| movie_id | INTEGER | Foreign Key to Movies              |
| user_id  | INTEGER | Foreign Key to Users               |
| score    | INTEGER | Rating score ("1 start"-"5 stars") |

- **Relationships:**
  - `movie`: Relationship to `Movie` model, representing the movie being rated.
  - `user`: Relationship to `User` model, representing the user who gave the rating.

## Comments Table

| Column            | Type    | Description                                |
| ----------------- | ------- | ------------------------------------------ |
| id                | INTEGER | Primary Key                                |
| content           | TEXT    | Comment content                            |
| movie_id          | INTEGER | Foreign Key to Movies                      |
| parent_comment_id | INTEGER | Foreign Key to Comments (self-referential) |
| user_id           | INTEGER | Foreign Key to Users                       |

- **Relationships:**
  - `user`: Relationship to `User` model, representing the user who made the comment.
  - `movie`: Relationship to `Movie` model, representing the movie associated with the comment.
  - `parent_comment`: Relationship to `Comment` model, representing the parent comment if nested.
  - `replies`: Relationship to `Comment` model, representing replies to the comment.
