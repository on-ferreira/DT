from flask import Flask
from blueprints.manager_bp import manager_bp

# maybe will be used later
# from datetime import datetime
# from datetime import timedelta
# from datetime import timezone

app = Flask(__name__)
app.register_blueprint(manager_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5095)

