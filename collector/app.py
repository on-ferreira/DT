from Collector import DTCollector
from flask import Flask, jsonify, request

app = Flask(__name__)
collector_instance = DTCollector()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5096, debug=True)


@app.route('/update_project_list', methods=['POST'])
def update_project_list():
    """
    Receive updates for the project list.

    Expects JSON data in the request body:
    {
        "flag": 1,  # Flag indicating the operation (1 for insertion, 2 for deletion, 3 for update)
        "project_id": 123,  # Project ID to be inserted, deleted, or updated
        "mp_dict": {"project_id": 123, "data": [{"type": "ExternalDataSource", "source": "www.example.com",
                                                                                "tags": ["tag1","tag2"]}]}
    }

    Calls the function update_project_list of the Collector class to update the list of projects in the collector_instance

    Returns:
        JSON response indicating the success or failure of the update.
    """
    try:
        data = request.json
        flag = data.get("flag", None)
        project_id = data.get("project_id", None)
        mp_dict = data.get("mp_dict", {})

        if flag is None or project_id is None:
            raise ValueError("Missing required fields in JSON data.")

        collector_instance.update_project_list(flag, project_id, mp_dict)

        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500