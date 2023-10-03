from uuid import uuid4
from flask import Blueprint, g, jsonify, request
from sqlalchemy.orm import noload

from ..db import db
from ..models import List, Task
from ..middlewares.protected_route_middleware import protected_route


blueprint_list = Blueprint("list", __name__)

"""
Retrieve a specific list in a board route endpoint
"""
@blueprint_list.route("/lists/<int:list_id>", methods=["GET"])
@protected_route
def get_list(list_id):
    user_id = g.user.get("id")

    requested_list = List.query.filter_by(id=list_id, user_id=user_id).first()

    if not requested_list:
        return jsonify(msg="List not found or you cannot perform this operation"), 404
    
    list_tasks = [
        {
            "id": task.id,
            "title": task.title,
        }

        for task in requested_list.tasks
    ]
    
    response_list = {
        "id": requested_list.id,
        "title": requested_list.title,
        "board": requested_list.board_id,
        "tasks": list_tasks
    }

    return jsonify(response_list), 200



"""
Erase a specific list in a board route endpoint
"""
@blueprint_list.route("/lists/<int:list_id>", methods=["DELETE"])
@protected_route
def delete_list(list_id):
    user_id = g.user.get("id")

    requested_list = List.query.filter_by(id=list_id, user_id=user_id).first()

    if not requested_list:
        return jsonify(msg="List not found or you cannot perform this action"), 404

    db.session.delete(requested_list)
    db.session.commit()
    
    return jsonify(msg="List and all its tasks deleted successfully."), 200



@blueprint_list.route("/lists/<int:list_id>/title", methods=["PATCH"])
@protected_route
def edit_list_title(list_id):
    user_id = g.user.get("id")

    request_data = request.get_json()
    title = request_data.get("title")

    requested_list = List.query.options(noload("tasks")).filter_by(id=list_id, user_id=user_id).first()

    if not requested_list:
        return jsonify(msg="List not found or you cannot perform this action"), 404
    
    if requested_list.title == title:
        return jsonify("New title cannot be the same as the current title"), 400
    
    requested_list.title = title

    db.session.commit()

    return jsonify(msg="Title updated successfully"), 200



"""
Create a new list task route endpoint
"""
@blueprint_list.route("/lists/<int:list_id>/task", methods=["POST"])
@protected_route
def create_list_task(list_id):
    user_id = g.user.get("id")

    request_data = request.get_json()
    task_title = request_data.get("title")

    if not task_title or list_id:
        return jsonify(msg="Missing required parameters"), 400
    
    requested_list = List.query.filter_by(id=list_id, user_id=user_id).first()

    if not requested_list:
        return jsonify(msg="List not found"), 404
    
    new_task = Task(user_id=user_id, list_id=list_id, title=task_title, uid=str(uuid4()))

    db.session.add(new_task)
    db.session.commit()

    response_new_task = {
        "id": new_task.id,
        "uid": new_task.uid,
        "title": new_task.title,
    }  

    return jsonify(response_new_task), 200



"""
Sorting list tasks route endpoints
"""
@blueprint_list.route("/lists/<int:list_id>/sort", methods=["POST"])
@protected_route
def sort_list_tasks(list_id):
    user_id = g.user.get("id")

    request_data = request.get_json()
    order = request_data.get("order")

    if not order:
        return jsonify(msg="Missing required parameters"), 400
    
    requested_list_tasks = Task.query.options(noload("priority")).filter_by(list_id=list_id, user_id=user_id).all()

    task_order_map = {
        str(task.id): position for position,
        task in enumerate(order)
    }

    for task in requested_list_tasks:
        task.position = task_order_map.get(str(task.id), len(order))

    db.session.commit()

    return jsonify(msg="Tasks sorted by position successfully"), 200


 







