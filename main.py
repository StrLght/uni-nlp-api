from flask import Flask
from flask import request
from flask import jsonify
from textblob import TextBlob

app = Flask(__name__)

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
             self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route("/sentiment")
def sentiment():
    text = request.args.get('text')
    if text is not None and len(text) > 0:
        blob = TextBlob(text)
	result = {"polarity": blob.sentiment.polarity, "subjectivity": blob.sentiment.subjectivity}
    	return jsonify(result)
    else:
        raise InvalidUsage("text cannot be empty")

@app.route("/tag")
def tag():
    text = request.args.get('text')
    if text is not None and len(text) > 0:
        blob = TextBlob(text)
	result = []
        for tag in blob.tags:
            result.append({"word": tag[0], "tag": tag[1]})
    	return jsonify({"result": result})
    else:
        raise InvalidUsage("text cannot be empty")

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080)
