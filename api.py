from flask import Flask, jsonify, make_response, abort, request
from functools import wraps
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

def authorize(f):
    @wraps(f)
    def decorated_function():
        key = request.args.get('api_key')
        if key == 'abc123':
            return f()
        return jsonify({"statusCode":401, "message":"Un authorised access"})
    return decorated_function

@app.route("/employees", methods = ['GET'])
@authorize
def getAllEmployees():
    """
    endpoint returns list of employees
    ---
    parameters:
      - name: api_key
        in: query
        type: string
    responses:
      200:
        description: A list of employees
        examples:
          [{"name" : "Roy"},{"name" : "Sam"}]
    """
    response = make_response(jsonify([{"name" : "James"},{"name" : "Johnson"}]))
    response.headers['Accept-version'] = 'v1'
    return response
@app.errorhandler(404)
def route_not_found(e):
    return jsonify({"error" : "Invalid route","statusCode" : 404})
