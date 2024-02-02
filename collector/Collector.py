from urllib import response
from abc import ABC, abstractmethod

import requests
import threading
import time
import os

import sys

sys.path.append('../')
from DT.common.MonitoringProject import MonitoringProject
from DT.common.DataSource import DataSource


class Collector(ABC):
    def __init__(self, project_list, global_count, manager_url):
        """
          Constructor for the Collector class.

          Parameters:
              project_list (list<MonitoringProject>): List of active projects
              global_count (int): Integer starting at 0.
              manager_url (str): URL for the manager container with Flask.
        """
        self.project_list = project_list
        self.global_count = global_count
        self.manager_url = manager_url

    @abstractmethod
    def _periodic_data_collection(self, X):
        """
        Periodically call collect_data every 'X' seconds in a separate thread.
        """
        pass

    @abstractmethod
    def stop_periodic_data_collection(self):
        """
        Stop the periodic data collection thread.
        """
        pass

    @abstractmethod
    def get_project_list(self):
        """
        Retrieve the projects from another container with Flask ("/get_active_projects" route).
        """
        pass

    @abstractmethod
    def update_project_list(self, flag, project_id, mp_dict):
        """
        Update the project_list based on the given flag.

        Parameters:
            flag (int): Flag indicating the operation (1 for insertion, 2 for deletion, 3 for update).
            project: The project to be inserted, deleted, or updated.
        """
        pass

    @abstractmethod
    def collect_data(self):
        """
        Loop through the project_list, calling get_data() for all DataSources in data.
        """
        pass

    @abstractmethod
    def _collect_data_for_source(self, data_source):
        """
        Helper method to call get_data() for a specific DataSource.
        """
        pass

    @abstractmethod
    def post_data(self, data):
        """
        Send the collected data to the manager container ("/receive_data_from_collector" route).

        Parameters:
            data: The collected data.
        """
        pass


class DTCollector(Collector):
    def __init__(self):
        super().__init__(project_list=[], global_count=0, manager_url=os.getenv("URL_MANAGER", "http://localhost:5000"))

        max_retries = 10
        for retry_count in range(1, max_retries + 1):
            try:
                self.get_project_list()
                break
            except requests.exceptions.ConnectionError as e:
                print(f"Attempt {retry_count}/{max_retries}: {e}. Trying again in 5 seconds...")
                time.sleep(5)
        else:
            raise RuntimeError(f"Unable to retrieve project list after {max_retries} attempts. Aborting application.")

        self.stop_data_collection = threading.Event()
        self.data_collection_thread = threading.Thread(target=self._periodic_data_collection)
        self.data_collection_thread.start()

    def _periodic_data_collection(self, X=30):
        while not self.stop_data_collection.is_set():
            self.collect_data()
            time.sleep(X)

    def stop_periodic_data_collection(self):
        self.stop_data_collection.set()
        self.data_collection_thread.join()

    def get_project_list(self):
        response = requests.get(f"{self.manager_url}/get_active_projects")
        if response.status_code == 200:
            mp_dicts_list = response.json()

            print(mp_dicts_list)

            self.project_list = [MonitoringProject(**mp_dict) for mp_dict in mp_dicts_list]

        else:
            print(f"Error updating project list. Status code: {response.status_code}")

    def update_project_list(self, flag, project_id, mp_dict):
        match flag:
            case 1:
                self.project_list.append(MonitoringProject(**mp_dict))
            case 2:
                self.project_list = [project for project in self.project_list if project.project_id != project_id]
            case 3:
                for i, existing_project in enumerate(self.project_list):
                    if existing_project.project_id == project_id:
                        updated_project = MonitoringProject(**mp_dict)
                        self.project_list[i] = updated_project
                        break
            case _:
                print(f"Error updating project list. Status code: {response}")

    def collect_data(self):
        processes = []
        for project in self.project_list:
            for data_source in project.data:
                process = threading.Thread(target=self._collect_data_for_source, args=(data_source,))
                processes.append(process)

        for process in processes:
            process.start()

        for process in processes:
            process.join()

    def _collect_data_for_source(self, data_source):
        try:
            if (isinstance(data_source, DataSource)):
                data = data_source.get_data()
                data["project_id"] = data_source.get_project_id()
                self.post_data(data)
        except Exception as e:
            print(f"Error in _collect_data_for_source: {e}")

    def post_data(self, data):
        print(f"post_data - {data}")
        response = requests.post(f"{self.manager_url}/receive_data_from_collector", json=data)
        if response.status_code == 200:
            print("Data posted to manager successfully.")
        else:
            print(f"Error posting data to manager. Status code: {response.status_code}")
