from flask import Blueprint, g, jsonify, request
from sqlalchemy.orm import noload
from sqlalchemy.exc import IntegrityError

from ..db import db
from ..middlewares.protected_route_middleware import protected_route
from ..models import Board, List


blueprint_board = Blueprint("board", __name__)

"""
Retrieve all boards route endpoint 
"""
@blueprint_board.route("/boards", methods=["GET"])
@protected_route
def get_boards():
    # The decoded and stored user information in the Flask g object, allows access to the protected route.
    # Directly access the `g.user` dictionary to extract userID(`id`=`user_id`) from it. This simplifies the code and avoids unnecessary dictionary access.
    user_id = g.user.get("id")

    # Use `noload` to avoid loading unnecessary relationships
    boards = Board.query.options(noload("lists")).filter_by(user_id=user_id)

    # Use a list comprehension for a more concise and readable response data
    response_boards = [
        {
            "id": board.id,
            "title": board.title,
        }
        
        for board in boards
    ]

    # Use HTTP 200 OK success status response code to indicate that the request was successful.
    return jsonify(response_boards), 200



"""
Create a new board route endpoint
"""
@blueprint_board.route("/boards", methods=["POST"])
@protected_route
def create_board():
    user_id = g.user.get("id")

    # Extract and parse JSON data from an incoming HTTP request.
    request_data = request.get_json()
    board_name = request_data.get("boardName")

    # Use `not board_name` to check for the missing parameter, which is more concise.
    if not board_name:
        return jsonify(msg="Missing required parameter: boardName"), 400
    
    # Specify the keyword arguments (user_id and title) explicitly for clarity.
    new_board = Board(user_id=user_id, title=board_name)

    # Use `try` and `except` to check if `new_board` was successfully added to the database before returning a response.
    try: 
        db.session.add(new_board)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

        # Status code `400 Bad Request` indicate a client error.
        return jsonify(msg="Board name already exists"), 400
    
    # The response is constructed as a dictionary
    response_new_board = {
        "msg": "New board created",
        "boardId": new_board.id,
        "boardName": new_board.title,
    }
    
    # Use `201 Created` status code, which is the standard status code for indicating that a resource has been successfully created.
    return jsonify(response_new_board), 201 
    


"""
Retrieve a specific board route endpoint
"""
@blueprint_board.route("/boards/<int:board_id>", methods=["GET"])
@protected_route
def get_board(board_id):
    user_id = g.user.get("id")

    # `not board_id` handle the case where board_id is missing or zero, returning a 400 Bad Request response in such cases.
    if not board_id:
        return jsonify(msg="Missing required parameter: board_id"), 400

    # Use `filter_by` with both `id` and `user_id` to ensure that the board with the given board_id belongs to the authenticated user.
    board = Board.query.filter_by(id=board_id, user_id=user_id).first()

    # If not, it returns a `404 Not Found` or `403 Forbidden` response as appropriate.
    if not board:
        return jsonify(msg="Board not found or you cannot perform this action"), 404

    # Use list comprehensions for building both `list_tasks` and `board_lists`, making the code more concise and readable.
    board_lists = []

    for list in board.lists:
        list_tasks = [
            {
                "id": task.id,
                "title": task.title,
                "position": task.position,
                "priority": task.priority.value if task.priority else None,
            }

            for task in list.tasks 
        ]

        # Construct a list of dictionaries where each dictionary represents a board's details, including its lists and associated tasks.
        board_lists.append({
            "id": list.id,
            "title": list.title,
            "created_at": list.created_at,
            "tasks": list_tasks
        })

    response_board_lists = {
        "id": board.id,
        "title": board.title,
        "lists": board_lists
    }

    return jsonify(response_board_lists), 200



"""
Erase a specific board route endpoint
"""
@blueprint_board.route("/boards/<int:board_id>", methods=["DELETE"])
@protected_route
def delete_board(board_id):
    user_id = g.user.get("id")

    board = Board.query.filter_by(id=board_id, user_id=user_id).first()

    if not board: 
        return jsonify(msg="Board not found or you cannot perform this action"), 404
    
    try: 
        db.session.delete(board)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

        return jsonify(msg="Board deletion failed due to integrity constraints"), 400

    return jsonify(msg="Board, all its lists and tasks were deleted successfully"), 200



"""
Retrieve a specific board, with its lists and corresponding tasks route endpoint
"""
@blueprint_board.route("/boards/<int:board_id>/lists", methods=["GET"])
@protected_route
def get_board_lists(board_id):
    user_id = g.user.get("id")

    board = Board.query.filter_by(id=board_id, user_id=user_id).first()

    if not board:
        return jsonify(msg="Board not found or you cannot perform this action"), 404
    
    board_lists = [
        {
            "id": list.id,
            "title": list.title,
        }

        for list in board.lists 
    ]

    response_board_lists = {
        "id": board.id,
        "title": board.title,
        "lists": board_lists
    }

    return jsonify(response_board_lists), 200



"""
Create a new board list route endpoint
"""
@blueprint_board.route("/boards/<int:board_id>/lists", methods=["POST"])
@protected_route
def create_board_list(board_id):
    user_id = g.user.get("id")

    request_data = request.get_json()
    title = request_data.get("title")

    if not title:
        return jsonify(msg="Missing required parameter: title"), 400
    
    requested_board = Board.query.filter_by(id=board_id, user_id=user_id).first()

    if not requested_board:
        return jsonify(msg="Board not found or you cannot perform this action"), 404
    
    new_list = List(board_id=board_id, user_id=user_id, title=title)

    
    db.session.add(new_list)
    db.session.commit()
    db.session.rollback()
    
    response_new_list = {
        "id": new_list.id,
        "title": new_list.title,
        "tasks": []
    }

    return jsonify(response_new_list), 201