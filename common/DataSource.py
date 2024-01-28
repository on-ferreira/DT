import requests
from abc import ABC, abstractmethod


class DataSource(ABC):
    def __init__(self, source, tags=[]):
        """
        Constructor for the DataSource class.

        Parameters:
            source (str): The source of the data.
            tags (list): List of tags associated with the data (default is an empty list).
        """
        self.source = source
        self.tags = tags

    def display_info(self):
        """
        Displays information about the data source, including the source and tags.
        """
        print(f"Source: {self.source}")
        print(f"Tags: {self.tags}")

    @abstractmethod
    def get_data(self):
        """
        Abstract method that must be implemented by child classes.
        Raises:
            NotImplementedError: To enforce implementation in child classes.
        """
        raise NotImplementedError("get_data() method must be implemented in child classes.")

    def edit_source(self, new_source):
        """
        Modifies the source of the data.

        Parameters:
            new_source (str): The new source to set.
        """
        self.source = new_source

    def edit_tags(self, operation_code, new_tag, old_tag):
        """
        Edits the tags associated with the data.

        Parameters:
            operation_code (int): Code indicating the type of operation to perform (1 for insert, 2 for remove, 3 for update).
            new_tag (str): The tag to insert, remove, or update.
            old_tag (str): The existing tag to remove or update.
        """
        match int(operation_code):
            case 1:
                self.tags.append(new_tag)
            case 2:
                if new_tag in self.tags:
                    self.tags.remove(new_tag)
                    print(f"Tag '{new_tag}' removed from tags.")
                else:
                    print(f"Tag '{new_tag}' not found. Unable to remove.")
            case 3:
                if old_tag in self.tags:
                    index = self.tags.index(old_tag)
                    self.tags[index] = new_tag
                    print(f"Tag '{old_tag}' updated to '{new_tag}'.")
                else:
                    print(f"Tag '{old_tag}' not found. Unable to update.")
            case _:
                print("Not Recognized operation_code. Use 1 for inserting a tag on tags. "
                      "Use 2 for removing a tag from tags."
                      "Use 3 for updating a tag from tags")

    @abstractmethod
    def to_dict(self):
        """
        Abstract method that must be implemented by child classes.
        Raises:
            NotImplementedError: To enforce implementation in child classes.
        """
        raise NotImplementedError("to_dict() method must be implemented in child classes.")


class DatabaseDataSource(DataSource):
    def __init__(self, type, source, tags=[], proj_id=None, connection_string=None):
        """
        Constructor for the DatabaseDataSource class.

        Parameters:
            source (str): The source of the data.
            tags (list): List of tags associated with the data (default is an empty list).
            proj_id (any): Identifier for the associated project.
            connection_string (str): Connection string for the database.
        """
        super().__init__(source, tags)
        self.proj_id = proj_id
        self.connection_string = connection_string
        self.type = type


    def get_data(self):
        """
        Queries data from the database specified in the connection_string within the project specified by proj_id.

        Returns:
            The queried data or performs any necessary actions.
        """
        print(f"Querying data from the database: {self.source}")
        # Implement here the specific logic for querying data from a database within the proj_id
        # Use self.connection_string to establish a connection
        # Return the data or perform any necessary actions

    def to_dict(self):
        return {'type': self.type,
                "source": self.source, "tags": self.tags, "proj_id": self.proj_id,
                "connection_string": self.connection_string}


class ExcelDataSource(DataSource):
    def __init__(self, type, source, tags=[]):
        """
        Constructor for the ExcelDataSource class.

        Parameters:
            source (str): The source of the data.
            tags (list): List of tags associated with the data (default is an empty list).
        """
        super().__init__(source, tags)
        self.type = type

    def get_data(self):
        """
        Reads data from the specified Excel file.

        Returns:
            The read data or performs any necessary actions.
        """
        print(f"Reading data from Excel file: {self.source}")
        # Implement here the specific logic for reading data from an Excel file
        # Use self.sheet_name to specify the sheet
        # Return the data or perform any necessary actions

    def to_dict(self):
        return {'type': self.type,
                "source": self.source, "tags": self.tags}


class ExternalDataSource(DataSource):
    def __init__(self, type, source, tags=[]):
        """
        Constructor for the ExternalDataSource class.

        Parameters:
            source (str): The source of the data.
            tags (list): List of tags associated with the data (default is an empty list).
        """
        super().__init__(source, tags)
        self.type = type

    def get_data(self):
        """
        Fetches data from the specified external API using the requests library.

        Returns:
            The fetched data if successful; otherwise, prints an error message and returns None.
        """
        print(f"Fetching data from external source using API: {self.source}")
        # Implement here the specific logic for making a request to an external API
        # Use self.api_url to specify the API endpoint
        response = requests.get(self.source)
        if response.status_code == 200:
            data = response.json()  # Assuming the response is in JSON format
            return data
        else:
            print(f"Error: Unable to fetch data. Status code: {response.status_code}")
            return None

    def to_dict(self):
        return {'type': self.type,
                "source": self.source, "tags": self.tags}
