from flask import Blueprint, jsonify, request
from Manager import Manager

manager_bp = Blueprint('manager', __name__)
manager_instance = Manager()

@manager_bp.route('/get_active_projects', methods=['GET'])
def get_active_projects():
    """
    Retrieve the active projects from the database.
    """
    # Implement the logic to retrieve active projects
    # You can use the Manager class or a database connection here
    active_projects = manager_instance.get_active_projects() or [
        {"project_id": 1, "data": [{'type': 'ExternalDataSource',
                                    "source": "http://worldtimeapi.org/api/timezone/America/Sao_Paulo",
                                    "tags": ["utc_datetime", "unixtime"]}]}]

    return jsonify(active_projects)


@manager_bp.route('/receive_data_from_collector', methods=['POST'])
def receive_data_from_collector():
    """
    Receive data from Collector and save in the database.
    """
    
    try:
        # data = request.json
        result = manager_instance.receive_data_from_collector()

        return result

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
