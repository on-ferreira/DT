from DT.common.DataSource import DataSource, DatabaseDataSource, ExternalDataSource, ExcelDataSource


class MonitoringProject:
    def __init__(self, project_id, data=None):
        self.project_id = project_id
        self.data = data or []
        if data:
            for i in range(len(data)):
                self.add_data_source(data[i])

    def add_data_source(self, data_source):
        """
        Add a DataSource instance or a dictionary representing a DataSource to the project's data list.

        Parameters:
            data_source (Union[DataSource, dict]): An instance of the DataSource class or a dictionary representing a DataSource.
        """
        if isinstance(data_source, DataSource):
            self.data.append(data_source)
        elif isinstance(data_source, dict):
            data_source_type = data_source.get('type', None)
            match data_source_type:
                case 'DatabaseDataSource':
                    self.data.append(DatabaseDataSource(**data_source))
                case 'ExcelDataSource':
                    self.data.append(ExcelDataSource(**data_source))
                case 'ExternalDataSource':
                    self.data.append(ExternalDataSource(**data_source))
                case _:
                    raise ValueError(f"Unknown data source type: {data_source_type}")
        else:
            raise ValueError("Input must be an instance of DataSource or a dictionary representing a DataSource.")

    def display_project_info(self):
        """
        Display information about the monitoring project.
        """
        print(f"Project ID: {self.project_id}")
        print("Data Sources:")
        for i, data_source in enumerate(self.data, start=1):
            print(f"  {i}. {data_source}")

    def to_dict(self):
        data_sources = []
        for source in self.data:
            data_sources.append(source.to_dict())
        return {"project_id": self.project_id, "data": data_sources}

