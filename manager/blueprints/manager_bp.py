from flask import Blueprint, jsonify, request, current_app
from Manager import DTManager

import sys
sys.path.append('../')
from DT.common.db.models import Project, DataSource, Tag

manager_bp = Blueprint('manager', __name__)
manager_instance = DTManager()

#current_app.logger.info("")


@manager_bp.route('/get_active_projects', methods=['GET'])
def get_active_projects():
    """
    Retrieve the active projects from the database.
    """
    # Implement the logic to retrieve active projects
    # You can use the Manager class or a database connection here
    active_projects = manager_instance.get_active_projects()

    return jsonify(active_projects)


@manager_bp.route('/receive_data_from_collector', methods=['POST'])
def receive_data_from_collector():
    """
    Receive data from Collector and save in the database.
    """

    try:
        data = request.json
        result = manager_instance.receive_data_from_collector(data)

        return result

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

