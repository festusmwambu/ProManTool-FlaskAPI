# Pro-Man-Tool

`ProManTool` is an open-source project management software that is specifically developed to support the `kanban methodology`, which is a way of organizing and managing projects to improve efficiency and effectiveness.
It is build using `Python-Flask` for backend/server, `React-Typescript` for frontend/client, `Sass`as the CSS preprocessor, `Redux` for centralized state management, and `PostgreSQL` as a relational database. The tests for backend are done on `pytest` and the tests for the frontend are done on `jest`.
The project also incorporates `GitHub OAuth` for authentication and authorization, `Google Analytics 4` which collects event-based and page view data from websites, web applications and mobile applications, and `Google reCAPTCHA v2` to protect sites from fraudulent activities, spam, and abuse.

## Installation for the backend/server

#### Requirements to run this project
- **Python** 3.9.5
- **Flask** 3.0.0
- **SQLAlchemy (ORM)** 2.0.21
- **PostgreSQL** 12

#### How to initialize the project in development environment mode

To initialize Python-Flask development environment, install backend dependencies:

```
../ProManTool-FlaskAPI
$ pip3.9 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
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

#### How to run tests

❗ Make sure you installed all the dependencies and activated the python development environment

Tests are made with Pytest library, 

```
../ProManTool-FlaskAPI

$ pytest
```

#### Documentation (Swagger)

Swagger is available at: [localhost:5000/api](http://localhost:5000/api)