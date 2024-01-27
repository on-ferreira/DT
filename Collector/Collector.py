from urllib import response

import requests
import threading
import time
from DT.Common import MonitoringProject

class Collector:
    def __init__(self, global_count=0, manager_url="http://manager-container:5000"):
        """
        Constructor for the Collector class.

        Parameters:
            global_count (int): Integer starting at 0.
            manager_url (str): URL for the Manager container with Flask.
        """
        self.project_list = []  # Initialize an empty list
        self.global_count = global_count
        self.manager_url = manager_url

        # Call get_project_list to initialize the project_list within the max of 10 retries.
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

        # Set up a flag for stopping the periodic data collection
        self.stop_data_collection = threading.Event()

        # Start a separate thread for periodic data collection
        self.data_collection_thread = threading.Thread(target=self._periodic_data_collection)
        self.data_collection_thread.start()

    def _periodic_data_collection(self):
        """
        Periodically call collect_data every 15 seconds in a separate thread.
        """
        while not self.stop_data_collection.is_set():
            self.collect_data()
            time.sleep(15)

    def stop_periodic_data_collection(self):
        """
        Stop the periodic data collection thread.
        """
        self.stop_data_collection.set()
        self.data_collection_thread.join()

    def get_project_list(self):
        """
        Retrieve the projects from another container with Flask ("/get_active_projects" route).
        """
        response = requests.get(f"{self.manager_url}/get_active_projects")
        if response.status_code == 200:
            self.project_list = response.json()
            print("Project list updated successfully.")
        else:
            print(f"Error updating project list. Status code: {response.status_code}")

    def update_project_list(self, flag, project_id):
        """
        Update the project_list based on the given flag.

        Parameters:
            flag (int): Flag indicating the operation (1 for insertion, 2 for deletion, 3 for update).
            project: The project to be inserted, deleted, or updated.
        """
        match flag:
            case 1:
                self.project_list.append(MonitoringProject(project_id))
            case 2:
                if project_id in self.project_list:
                    self.project_list.remove(project)
            case 3:
                for i, existing_project in enumerate(self.project_list):
                    if existing_project.id == project.id:
                        self.project_list[i] = project
                        break
            case _:
                print(f"Error updating project list. Status code: {response}")


    def collect_data(self):
        """
        Loop through the project_list, calling get_data() for all DataSources in data.
        """
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
        """
        Helper method to call get_data() for a specific DataSource.
        """
        data = data_source.get_data()
        self.post_data(data)

    def post_data(self, data):
        """
        Send the collected data to the Manager container ("/receive_data_from_collector" route).

        Parameters:
            data: The collected data.
        """
        response = requests.post(f"{self.manager_url}/receive_data_from_collector", json=data)
        if response.status_code == 200:
            print("Data posted to Manager successfully.")
        else:
            print(f"Error posting data to Manager. Status code: {response.status_code}")
