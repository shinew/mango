"""
API endpoints for the server
"""

import sys
from flask import request, jsonify, abort, Flask
from database.setup import Session, Base, engine
from validator import Validator
from processor import Processor
from scorer import Scorer
from authenticator import Authenticator
from measurer import Measurer

Base.metadata.create_all(engine)
app = Flask(__name__)
scorer = Scorer(app.logger)
authenticator = Authenticator(app.logger)
validator = Validator(app.logger, authenticator)
processor = Processor(app.logger, scorer, authenticator)
measurer = Measurer(app.logger)

# set up logging (for linux)
if sys.platform == "linux2":
    from logging import FileHandler, INFO
    handler = FileHandler("/tmp/mylogs.txt")
    handler.setLevel(INFO)
    app.logger.addHandler(handler)


@app.route("/")
def hello():
    return "Hello, world!"


@app.route("/v2.0/users/<int:userID>/sensors", methods=["POST"])
def addSensorData(userID):
    """
    Receives and processes HR and HRV inputs from users.
    """

    session = Session()
    if not validator.addSensorData(request, session):
        session.close()
        abort(400)
    processor.addSensorData(userID, request.json, session)
    session.close()
    return jsonify({}), 200

@app.route("/v2.0/users/<int:userID>/sensors", methods=["POST"])
def getScore(userID):
    """
    Returns a stress score.
    """

    session = Session()
    if not validator.getScore(request, session):
        session.close()
        abort(400)
    result = processor.getScore(userID, request.json, session)
    session.close()
    return jsonify(result), 200

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)

