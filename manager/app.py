from flask import Flask
from blueprints.manager_bp import manager_bp

import sys
sys.path.append('../')
from DT.common.db.db_setup import db
sys.path.append('manager')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://DTuser:DTuser@db-DT/DTsistemas'
db.init_app(app)

app.register_blueprint(manager_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5095, debug=True)
