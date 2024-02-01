from abc import ABC, abstractmethod
from flask import jsonify, current_app
import sys

sys.path.append('../')
from DT.common.db.db_setup import db
from DT.common.db.models import Project, DataSource, Tag


class Manager(ABC):
    def __init__(self):
        """
        Constructor for the Manager class.
        """

    @abstractmethod
    def get_active_projects(self):
        """
        Retrieve the active projects from the database.
        """
        pass

    @abstractmethod
    def receive_data_from_collector(self):
        """
        Process and save the data from the collector in the database
        :return: Status 200
        """
        pass


class DTManager(Manager):
    def __init__(self):
        super().__init__()

    def get_active_projects(self):
        projects = Project.query.all()
        projects_return = []
        for project in projects:
            projects_return.append({'project_id': project.id, 'data': project.data})

        return projects_return

    def receive_data_from_collector(self, data):
        for key, value in data.items():
            if key != 'project_id':
                tag = Tag(tag_name=key, value=value, project_id=data['project_id'])
                db.session.add(tag)

        db.session.commit()

        return jsonify({"status": "ok"}), 200
