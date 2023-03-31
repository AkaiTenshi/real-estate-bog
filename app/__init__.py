from flask import Flask
from utils.logger import Logger
from utils.db import DB

# Initialize logger
logger = Logger()

# Initialize database
logger.info("Initializing DB")
db = DB()

# Initialize Flask app
app = Flask(__name__)

# Test route
@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
