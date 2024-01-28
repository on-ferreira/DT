from flask import Blueprint, request, jsonify

manager_bp = Blueprint('manager', __name__)


class Manager:
    def __init__(self):
        """
        Constructor for the Manager class.
        """
        # self.projects = self.get_all_projects()

    def get_active_projects(self):
        """
        Retrieve the active projects from the database.
        """
        pass

    def get_all_projects():
        """
        Retrieve all projects from the database.
        """
        projects = []

        return projects

    def get_project_by_id(project_id):
        """
        Retrieve a project from the database by its ID.
        """

        project = None

        return project

    def get_all_tags():
        """
        Retrieve all tags from the database.
        """

        tags = []

        return tags

    def get_tag_by_id(tag_id):
        """
        Retrieve a tag from the database by its ID.
        """

        tag = None

        return tag

    def get_recent_value_for_project_and_tag(self, project_id, tag_id):
        """
        Retrieve the most recent value for a project and a tag.
        """
        pass

    def get_oldest_value_for_project_and_tag(project_id, tag_id):
        """
        Retrieve the oldest value for a project and a tag.
        """
        pass

    def get_project_tag_values_older_than(timestamp):
        """
        Retrieve the records from the table ProjectTag with timestamp older than the specified timestamp.
        """

        pass

    def delete_project_tag_values_older_than(timestamp):
        """
        Delete the records from the table ProjectTag with timestamp older than the specified timestamp.
        """

        pass


@manager_bp.route('/get_active_projects', methods=['GET'])
def get_active_projects():
    """
    Retrieve the active projects from the database.
    """
    # Implement the logic to retrieve active projects
    # You can use the Manager class or a database connection here
    manager_instance = Manager()
    active_projects = manager_instance.get_active_projects() or {"project_id": 1, "data": {'type': 'ExternalDataSource',
                                                                                           "source": "www.google.com",
                                                                                           "tags": ["tag1", "tag2"]}}

    return jsonify(active_projects)


@manager_bp.route('/receive_data_from_collector', methods=['POST'])
def receive_data_from_collector():
    """
    Receive data from Collector and save in the database.
    """
    # Implement the logic to receive all data
    # You can use the Manager class or a database connection here

    return jsonify({"status": "success"}), 200
