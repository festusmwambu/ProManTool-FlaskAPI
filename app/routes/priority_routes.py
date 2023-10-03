from flask import Blueprint, jsonify

from ..middlewares.protected_route_middleware import protected_route
from ..models import Priority


blueprint_priority = Blueprint("priority", __name__)

"""
Retrieve all priorities route endpoint
"""
@blueprint_priority.route("/priorities", methods=["GET"])
@protected_route
def priorities():
    # Get all priorities from the database
    priorities = Priority.query.all()

    # Map priorities to a list of dictionaries with "id" and "value" keys
    requested_priorities = [
        {
            "id": priority.id,
            "value": priority.value,
        }
        for priority in priorities
    ]

    # Create the response dictionary
    response_data = {
        "result": requested_priorities
    }
    
    return jsonify(response_data), 200
