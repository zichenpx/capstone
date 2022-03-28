# Capstone/ Casting Agency project (Full Stack Project)
https://tranquil-ridge-30288.herokuapp.com/

## 1. Motivations

This is the final project of Udacity Full Stack Web Developer Nanodegree Program. This is an opportunity for me to reinforce those skills and walk away very confident in them.

- Coding in Python 3
- Relational Database Architecture
- Modeling Data Objects with SQLAlchemy
- Internet Protocols and Communication
- Developing a Flask API
- Authentication and Access
- Authentication with Auth0
- Authentication in Flask
- Role-Based Access Control (RBAC)
- Testing Flask Applications
- Deploying Applications

## 2. Casting Agency Project Specifications
The Casting Agency project an application that is responsible for creating movies and managing and assigning actors to those movies.

- Models:
    - Movies with attributes title, release date, duration, cast, amd imdb rating
    - Actors with attributes name, birthdate, and gender

- Endpoints:
    - GET /actors and /movies
    - DELETE /actors/ and /movies/
    - POST /actors and /movies and
    - PATCH /actors/ and /movies/

- Roles:
    - Agency
        - Can view actors and movies
        - Add or delete an actor from the database
        - Modify actors or movies
    - User
        - Can view actors and movies

## 3. Getting Started

### 3.1. Installing Dependencies

#### Python 3.9
Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment
Working within a virtual environment whenever using Python for projects is recommended. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform are the following:

Initialize and activate a virtualenv:
```bash
$ cd YOUR_PROJECT_DIRECTORY_PATH/
$ python -m venv env
$ env/Scripts/activate
```

More instructions can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages this project selected within the `requirements.txt` file.

##### Key Dependencies
- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### 3.2. Running the server
From within the root directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
flask run --reload
```

or

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

The `--reload` flag will detect file changes and restart the server automatically.

## 4. API Reference

### 4.1. Getting Started
Base URL: At present this app can be run locally and may not be hosted as a base URL. If hosted, the hosted version is at https://tranquil-ridge-30288.herokuapp.com/. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.

Authentication: This application requires authentication to perform various actions. All the endpoints require various permissions, except the root (or health) endpoint, that are passed via the Bearer token.

The application has two types of roles:
- Agency:
    - Agency
        - can only view the list of artist and movies and can view complete information for any actor or movie
        - can also create an actor and movie and also modify respective information
        - can also delete an actor or a movie
        - has `get:movies, get:movies-detail, post:movie, patch:movie, delete:movie, get:actors, get:actors-detail, post:actor, patch:actor, delete:actor` permissions
    - User
        - can only view the list of artist and movies and can view complete information for any actor or movie
        - has `get:movies, get:movies-detail, get:actors, get:actors-detail` permissions
- User:
    - Agency
        - Can view actors and movies
        - Add or delete an actor from the database
        - Modify actors or movies
    - User
        - Can view actors and movies

### 4.2. Error Handling
Errors are returned as JSON objects in the following format:

```json
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```

The API will return these error types when requests fail:

- 400: Bad Request
- 401: Unauthorized
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable
- 500: Internal Server Error

### 4.3. Endpoints 
#### GET /
- A public root endpoint, no authentication required, can also check if the API is running or not.

**Sample Request**
`http://127.0.0.1:5000`

<details>
<summary>Sample Response</summary>

```json
{
    "health": "Good!!",
    "message": "Welcome to My Full Stack Capstone Project",
    "state": "Running!!",
    "success": true
}
```

#### GET /movies
- Returns a list of all the movies.
- `get:movies` permission required.

**Sample Request**
`http://127.0.0.1:5000/movies`


<details>
<summary>Sample Response</summary>

```json
{
    "movies": [
        {
            "id": 1,
            "imdb_rating": 7.7,
            "release_year": 1954,
            "title": "Sabrina"
        },
        {
            "id": 2,
            "imdb_rating": 7.8,
            "release_year": 2017,
            "title": "Dunkirk"
        },
        {
            "id": 3,
            "imdb_rating": 6.8,
            "release_year": 2019,
            "title": "Spies in Disguise"
        },
        {
            "id": 4,
            "imdb_rating": 7.0,
            "release_year": 2000,
            "title": "Majian"
        },
        {
            "id": 6,
            "imdb_rating": 7.0,
            "release_year": 2000,
            "title": "Majian2"
        },
        {
            "id": 7,
            "imdb_rating": 6.3,
            "release_year": 2001,
            "title": "The Princess Diaries"
        },
        {
            "id": 8,
            "imdb_rating": 5.8,
            "release_year": 2004,
            "title": "The Princess Diaries 2： Royal Engagement"
        },
        {
            "id": 9,
            "imdb_rating": 8.0,
            "release_year": 2006,
            "title": "The Devil Wears Prada"
        },
        {
            "id": 10,
            "imdb_rating": 6.9,
            "release_year": 2006,
            "title": "The Devil Wears Prada"
        },
        {
            "id": 11,
            "imdb_rating": 6.9,
            "release_year": 2006,
            "title": "The Devil Wears Prada"
        },
        {
            "id": 12,
            "imdb_rating": 8.4,
            "release_year": 2022,
            "title": "The Batman"
        },
        {
            "id": 14,
            "imdb_rating": 8.4,
            "release_year": 2022,
            "title": "The Batman"
        },
        {
            "id": 15,
            "imdb_rating": 8.4,
            "release_year": 2022,
            "title": "The Batman"
        }
    ],
    "success": true
}
```

### GET /movies/{movie_id}
- Returns details of a certain movies with its cast, duration, id, imdb rating, release year, title and success message.
- `get:movies/<int:movie_id>` permission required.

**Sample Request**
`http://127.0.0.1:5000/movies/14`


<details>
<summary>Sample Response</summary>

```json
{
    "movie": {
        "cast": [
            "Robert Pattinson",
            "Zoë Isabella Kravitz"
        ],
        "duration": 176,
        "id": 14,
        "imdb_rating": 8.4,
        "release_year": 2022,
        "title": "The Batman"
    },
    "success": true
}
```

#### POST /movies
- Creates a new movie using the title and release year, duration, cast, imdb rating. 
- Returns the ID of the created movie, success message, and a movie list with the created movie and the number of total movies.
- `post:movies` permission required.

**Sample Request**
`POST` `http://127.0.0.1:5000/movies`
`raw json`
```json
{
    "title": "Majian2",
    "release_year": 2000,
    "duration": 100,
    "cast": [
        "Louis Koo"
    ],
    "imdb_rating": 7.0
}
```

<details>
<summary>Sample Response</summary>

```json
{
    "movie": [
        {
            "cast": [
                "Louis Koo"
            ],
            "duration": 100,
            "id": 16,
            "imdb_rating": 7.0,
            "release_year": 2000,
            "title": "Majian2"
        }
    ],
    "success": true,
    "total_movies": 14
}
```

#### PATCH /movies/{movie_id}
- Updates the movie based on the given movie ID using the updated title, release year, imdb rating, duration, casts.
- Returns the success message and a detailed with the updated movie.
- `patch:movies` permission required.

**Sample Request**
`PATCH` `http://127.0.0.1:5000/movies/2`
`raw json`

```json
{
    "imdb_rating": 8.0
}
```

<details>
<summary>Sample Response</summary>

```json
{
    "movie_info": {
        "cast": [
            "Tom Hardy"
        ],
        "duration": 106,
        "id": 2,
        "imdb_rating": 8.0,
        "release_year": 2017,
        "title": "Dunkirk"
    },
    "success": true
}
```

#### DELETE /movies/{movie_id}
- Deletes the movie based on the given movie ID.
- Returns the success message, the ID of the deleted movie, and the number of total movies.
- `patch:movies` permission required.

**Sample Request**
`DELETE` `http://127.0.0.1:5000/movies/10`

<details>
<summary>Sample Response</summary>

```json
{
    "deleted": 10,
    "success": true,
    "total_movies": 13
}
```

#### GET /actors
- Returns a list of all the actors.
- `get:actors` permission required.

**Sample Request**
`http://127.0.0.1:5000/actors`

<details>
<summary>Sample Response</summary>

```json
{
    "actors": [
        {
            "gender": "F",
            "id": 1,
            "name": "Audrey Hepburn"
        },
        {
            "gender": "M",
            "id": 2,
            "name": "Louis Koo"
        },
        {
            "gender": "M",
            "id": 3,
            "name": "Tom Hardy"
        },
        {
            "gender": "M",
            "id": 4,
            "name": "Tom Holland"
        },
        {
            "gender": "F",
            "id": 5,
            "name": "Anne Hethaway"
        },
        {
            "gender": "M",
            "id": 6,
            "name": "Robert Pattinson"
        },
        {
            "gender": "F",
            "id": 7,
            "name": "Zoë Isabella Kravitz"
        },
        {
            "gender": "F",
            "id": 8,
            "name": "Julie Andrews"
        },
        {
            "gender": "M",
            "id": 9,
            "name": "Hector Elizondo"
        },
        {
            "gender": "F",
            "id": 10,
            "name": "Heather Matarazzo"
        },
        {
            "gender": "F",
            "id": 11,
            "name": "Meryl Streep"
        },
        {
            "gender": "F",
            "id": 12,
            "name": "Emily Blunt"
        },
        {
            "gender": "M",
            "id": 13,
            "name": "Stanley Tucci"
        },
        {
            "gender": "M",
            "id": 14,
            "name": "Stanley Tucci"
        },
        {
            "gender": "F",
            "id": 15,
            "name": "Meryl Streep"
        }
    ],
    "success": true
}
```

### GET /actors/id
- Returns details of a certain actor with its birthday, gender, id, movies, name and success message.
- `get:actors/<int:actor_id>` permission required.

**Sample Request**
`http://127.0.0.1:5000/actors/1`


<details>
<summary>Sample Response</summary>

```json
{
    "actor": {
        "date_of_birth": "May 04, 1929",
        "gender": "F",
        "id": 1,
        "movies": [
            "Sabrina"
        ],
        "name": "Audrey Hepburn"
    },
    "success": true
}
```

#### POST /actors
- Creates a new actor using the name, birthday, and gender. 
- Returns the ID of the created actors, success message, and a cumber of total actors.
- `post:actors` permission required.

**Sample Request**
`post` `http://127.0.0.1:5000/actors`
```json
{
    "name": "Sarah Gray Rafferty",
    "date_of_birth": "December 6, 1972",
    "gender": "F"
}
```

<details>
<summary>Sample Response</summary>

```json
{
    "actor": [
        {
            "date_of_birth": "December 06, 1972",
            "gender": "F",
            "id": 17,
            "movies": [],
            "name": "Sarah Gray Rafferty"
        }
    ],
    "success": true,
    "total_actors": 16
}
```

#### PATCH /actors/{actor_id}
- Updates the actor based on the given actor ID using the updated name, birthday, or gender.
- Returns the success message and birthday, gender, id, movies, name of the updated actor, and the given ID.
- `patch:actors/<int:actor_id>` permission required.

**Sample Request**
`patch` `http://127.0.0.1:5000/actors/5`
```json
{
    "date_of_birth": "June 12, 1972"
}
```

<details>
<summary>Sample Response</summary>

```json
{
    "actor_info": {
        "date_of_birth": "June 12, 1972",
        "gender": "F",
        "id": 5,
        "movies": [
            "The Princess Diaries",
            "The Princess Diaries 2： Royal Engagement"
        ],
        "name": "Anne Hethaway"
    },
    "success": true,
    "updated": 5
}
```

#### DELETE /actors/{actor_id}
- Deletes the actor based on the given actor ID.
- Returns the success message, the ID of the deleted actor, and the number of total actors.
- `delete:actors/<int:actor_id>` permission required.

**Sample Request**
`delete` `http://127.0.0.1:5000/actors/5`

<details>
<summary>Sample Response</summary>

```json
{
    "deleted": 5,
    "success": true,
    "total_actors": 17
}
```

## 5. Testing
There two test files - one for role agency, one for role user.

For testing the backend.To run the agency test, run
```bash
dropdb capstone_test
createdb capstone_test
psql -U postgres capstone_test < capstone.sql
OR psql capstone_test < capstone_no_owner.sql
python test_app_agency.py
```

To run the user test, run
```bash
dropdb capstone_test
createdb capstone_test
psql -U postgres capstone_test < capstone.sql
OR psql capstone_test < capstone_no_owner.sql
python test_app_user.py
```