from DataSource import DataSource

class MonitoringProject:
    def __init__(self, project_id, data=[]):
        self.project_id = project_id
        self.data = data

    def add_data_source(self, data_source):
        """
        Add a DataSource instance to the project's data list.

        Parameters:
            data_source (DataSource): An instance of the DataSource class.
        """
        self.data.append(data_source)

    def display_project_info(self):
        """
        Display information about the monitoring project.
        """
        print(f"Project ID: {self.project_id}")
        print("Data Sources:")
        for i, data_source in enumerate(self.data, start=1):
            print(f"  {i}. {data_source}")
