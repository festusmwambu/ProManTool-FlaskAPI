import datetime

from .db import db


"""
Import SQLAlchemy database instance `from .db import db`.
Each model class inherits from `db.Model`.
We use `db.Column` to define the table columns, specifying the data types and constraints.
Relationships between tables are defined using `db.relationship`, and foreign keys are declared with `db.ForeignKey`.
We follow the PEP8 naming convention for class names, using singular forms like `User`, `Board`, `List`, `Task`, and `Priority`.
Updated column names to follow Pythonic naming conventions (e.g., `created_at` instead of `createdAt`).
"""
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))
    strategy = db.Column(db.String(100), nullable=False, default="AUTH")
    created_at = db.Column(db.DateTime()) # `DateTime` data type is used to store date and time

    def __init__(self, username, strategy, **kwargs):
        self.username = username
        self.password = kwargs.get("password", None)
        self.email = kwargs.get("email", None)
        self.strategy = strategy
        self.created_at = int(datetime.datetime.now().timestamp())


class Board(db.Model):
    __tablename__ = "boards"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    title = db.Column(db.String(100))
    lists = db.relationship("List", cascade="all, delete", backref="board", order_by="List.created_at", lazy="joined")

    def __init__(self, user_id, title):
        self.user_id = user_id
        self.title = title


class List(db.Model):
    __tablename__ = "lists"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    board_id = db.Column(db.Integer(), db.ForeignKey("boards.id"))
    title = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(), default=int(datetime.datetime.now().timestamp()))
    tasks = db.relationship("Task", cascade="all, delete", backref="list", order_by="Task.position", lazy="joined")

    def __init__(self, user_id, board_id, title):
        self.user_id = user_id
        self.board_id = board_id
        self.title = title


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    list_id = db.Column(db.Integer(), db.ForeignKey("lists.id"))
    priority_id = db.Column(db.Integer(), db.ForeignKey("priorities.id"))
    title = db.Column(db.String(100))
    uid = db.Column(db.String(100))
    description = db.Column(db.String(250))
    position = db.Column(db.Integer(), db.Sequence("tasks_position_sequence"))
    created_at = db.Column(db.DateTime())
    priority = db.relationship("Priority", backref="task", lazy="joined")

    def __init__(self, user_id, list_id, title, uid, description=""):
        self.user_id = user_id
        self.list_id = list_id
        self.title = title
        self.uid = uid
        self.description = description
        self.created_at = int(datetime.datetime.now().timestamp())


class Priority(db.Model):
    __tablename__ = 'priorities'

    id = db.Column(db.Integer(), primary_key=True)
    value = db.Column(db.String())

    def __init__(self, value):
        self.value = value
