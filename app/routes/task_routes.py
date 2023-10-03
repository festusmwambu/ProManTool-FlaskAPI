from flask import Blueprint, g, jsonify, request
from sqlalchemy.orm import noload

from ..db import db
from ..middlewares.protected_route_middleware import protected_route
from ..models import List, Priority, Task


blueprint_task = Blueprint("task", __name__)

"""
Retrieve a task by its id route endpoint
"""
@blueprint_task.route("/tasks/<int:task_id>", methods=["GET"])
@protected_route
def get_task(task_id):
    user_id = g.user.get("id")

    requested_task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not requested_task:
        return jsonify(msg="Task not found or you cannot perform this action"), 404
    
    response_task = {
        "id": requested_task.id,
        "uid": requested_task.uid,
        "title": requested_task.title,
        "description": requested_task.description,
        "created_at": requested_task.created_at,
        "list": requested_task.list_id
    }

    if requested_task.priority:
        response_task["priority"] = requested_task.priority.value

    return jsonify(response_task), 200



"""
Erase a task by its id route endpoint
"""
@blueprint_task.route("/tasks/<int:task_id>", methods=["DELETE"])
@protected_route
def delete_task(task_id):
    user_id = g.user.get("id")

    requested_task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not requested_task:
        return jsonify(msg="Task not found or you cannot perform this action"), 404
    
    db.session.delete(requested_task)
    db.session.commit()

    return jsonify(msg="Task deleted successfully"), 200



"""
Partial update of a task list route endpoint
"""
@blueprint_task.route("/tasks/<int:task_id>/list", methods=["PATCH"])
@protected_route
def update_task_list(task_id):
    user_id = g.user.get("id")

    request_data = request.get_json()
    list_id = request_data.get("list_id")
    new_position = request_data.get("position")

    if not (list_id and task_id and new_position):
        return jsonify(msg="Missing required parameters"), 400
    
    task_id = int(task_id)
    list_id = int(list_id)
    new_position = int(new_position)
    
    # Query for the requested task and its list
    requested_task = Task.query.get(task_id)

    if not requested_task:
        return jsonify(msg="Task not found."), 404
    
    requested_task_list = List.query.get(list_id)

    if not requested_task_list:
        return jsonify(msg="List not found."), 404
    
    # Check if the user has permission to perform this action
    if requested_task_list.user_id != user_id:
        return jsonify(msg="You cannot perform this action"), 403
    
    # Move the task to the new position in the list
    task_in_list = Task.query.filter_by(list_id=list_id).order_by(Task.position).all()

    if new_position < 0:
        new_position = 0
    elif new_position >= len(task_in_list):
        new_position = len(task_in_list) - 1

    task_in_list.remove(requested_task)
    task_in_list.insert(new_position, requested_task)

    # Update the positions of all tasks in the list
    for i, requested_task in enumerate(task_in_list):
        requested_task.position = i

    db.session.commit()

    return jsonify(msg="Task list updated successfully"), 200



"""
Partial update of a task description route endpoint
"""
@blueprint_task.route("/tasks/<int:task_id>/description", methods=["PATCH"])
@protected_route
def update_task_description(task_id):
    user_id = g.user.get("id")

    request_data = request.get_json()
    new_description = request_data.get("description")

    if not new_description:
        return jsonify(msg="Missing required parameter: description"), 400
    
    requested_task = Task.query.options(noload("priority")).filter_by(id=task_id, user_id=user_id).first()

    if not requested_task: 
        return jsonify(msg="Task not found"), 404
    
    if requested_task.user_id != user_id:
        return jsonify(msg="You cannot perform this action"), 403

    if requested_task.description == new_description:
        return jsonify(msg="New description cannot be the same as the current description"), 400
    
    requested_task.description = new_description
    db.session.commit()

    return jsonify(msg="Task description updated successfully"), 200



"""
Partial update of task prioriy route endpoint
"""
@blueprint_task.route("/tasks/<int:task_id>/priority", methods=["PATCH"])
@protected_route
def update_task_priority(task_id):
    user_id = g.user.get("id")

    request_data = request.get_json()
    new_priority = request_data.get("priority")

    if not new_priority:
        return jsonify(msg="Missing required parameter: priority"), 400
    

    requested_task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not requested_task:
        return jsonify(msg="Task not found"), 404
    
    if requested_task.user_id != user_id:
        return jsonify(msg="You cannot perform this action"), 403
    
    if requested_task.priority == new_priority:
        return jsonify(msg="New priority cannot be the same as the current priority"), 403


    requested_priority = Priority.query.get(new_priority)

    if not requested_priority: 
        return jsonify(msg="Priority not found"), 404
    

    requested_task.priority = new_priority
    db.session.commit()

    return jsonify(msg="Task priority updated successfully"), 200



"""
Partial update of task title route endpoint
"""
@blueprint_task.route("/tasks/<int:task_id>/title", methods=["PATCH"])
@protected_route
def update_task_title(task_id):
    user_id = g.user.get("id")

    request_data = request.get_json()
    new_title = request_data.get("title")

    if not new_title:
        return jsonify(msg="Missing required parameter: title"), 400
    

    requested_task = Task.query.options(noload("priority")).filter_by(id=task_id, user_id=user_id).first()

    if not requested_task: 
        return jsonify(msg="Task not found"), 404
    
    if requested_task.user_id != user_id:
        return jsonify(msg="You cannot perform this task action"), 403
    
    if requested_task.title == new_title:
        return jsonify(msg="New title cannot be the same as the current title"), 400
    
    requested_task.title = new_title
    db.session.commit()

    return jsonify(msg="Task title updated successfully"), 200

