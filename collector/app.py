from Collector import Collector
from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    collector_instance = Collector()
    app.run(host='0.0.0.0', port=5095)
