from flask import Flask
from blueprints.manager_bp import manager_bp

import sys

sys.path.append('../')
from DT.common.db.db_setup import db
from DT.common.db.models import Project

sys.path.append('manager')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://DTuser:DTuser@db-DT/DTsistemas'

if __name__ == '__main__':
    with app.app_context():
        app.register_blueprint(manager_bp)

        db.init_app(app)
        db.create_all()

        if db.session.query(Project).count() == 0:
            initial_project = Project(id=1, data=[{'type': 'ExternalDataSource',
                                                   "source": "https://api.chucknorris.io/jokes/random",
                                                   "tags": ["url", "value"], "project_id": 1}])
            db.session.add(initial_project)
            db.session.commit()

        app.run(host='0.0.0.0', port=5095, debug=True)
