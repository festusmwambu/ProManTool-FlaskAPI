# Pro-Man-Tool

`ProManTool` is an open-source project management software that is specifically developed to support the `kanban methodology`, which is a way of organizing and managing projects to improve efficiency and effectiveness.
It is build using `Python-Flask` for backend/server, `React-Typescript` for frontend/client, `Sass`as the CSS preprocessor, `Redux` for centralized state management, and `PostgreSQL` as a relational database. The tests for backend are done on `pytest` and the tests for the frontend are done on `jest`.
The project also incorporates `GitHub OAuth` for authentication and authorization, `Google Analytics 4` which collects event-based and page view data from websites, web applications and mobile applications, and `Google reCAPTCHA v2` to protect sites from fraudulent activities, spam, and abuse.

## Installation

#### Requirements to run this project
- **NodeJS** v14.21.3
- **Python** 3.9.5
- **Flask** 2.3.3
- **SQLAlchemy (ORM)** 2.0.20
- **PostgreSQL** 12

#### How to initialize the project in development environment mode

To initialize Python-Flask development environment, install backend dependencies:

```
../ProManTool-FlaskAPI
$ pip3.9 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

To initialize React-Typescript development environment, install frontend dependencies:

```
../ProManTool-React
$ npm install
```

#### How to run the application in development environment mode

To execute/run the backend Python-Flask development environment:

```
../ProManTool-FlaskAPI
$ source venv/bin/activate
$ python run.py or python3 run.py
```
And

```
../ProManTool-FlaskAPI
$ source venv/bin/activate
$ redis-server
```

To execute/run the frontend React-Typescript development environment:

```
../ProManTool-React/
$ npm start
```

#### How to run tests

❗ Make sure you installed all the dependencies and activated the python development environment

Tests are made with Pytest library, 

```
../pro-man-tool/backend

$ pytest
```

#### Documentation (Swagger)

Swagger is available at: [localhost:5000/api](http://localhost:5000/api)