import flask
from flask import jsonify, Response, send_from_directory
from apidoc import InfoResponse, spec
import os
import json


# Setup using environment variables: This can be used to configure the service when running in Docker


service_url = str(os.environ.get("SERVICE_URL", "http://127.0.0.1"))
"""SERVICE_URL: url where the service can be accessed.
Normally, it's somehow set when running the flask dev server
but it needs to be adapted, when one wants to access the docker container
default is "localhost".
"""

port = int(os.environ.get("SERVICE_PORT", 5000))
"""SERVICE_PORT: Port of the running service. 
flask's default is 5000
"""

# Debug Mode: Activates the flask Debug Mode
if os.environ.get("SERVICE_DEBUG", "TRUE") == "FALSE":
    debug = False
else:
    debug = True


# Setup of flask API
api = flask.Flask(__name__)
# enable UTF-8 support
api.config["JSON_AS_ASCII"] = False


@api.route("/api", methods=["GET"])
def swagger_ui():
    """Displays the OpenAPI Documentation of the API"""
    return send_from_directory("static/swagger-ui", "index.html")


@api.route("/api/info", methods=["GET"])
def get_info():
    """Information about the API
    ---
    get:
        summary: About the service
        description: Returns information about the service's API
        responses:
            200:
                description: Information about the API
                content:
                    application/json:
                        schema: InfoResponse
    """
    return jsonify({"status": "OK"})


# Generate the OpenAPI Specification
with api.test_request_context():
    spec.path(view=get_info)

# write the OpenAPI Specification as YAML to the root folder
with open('openapi.yaml', 'w') as f:
    f.write(spec.to_yaml())

# Write the Specification to the /static folder to use in the Swagger UI
with open('static/swagger-ui/openapi.json', 'w') as f:
    json.dump(spec.to_dict(), f)

# Run the Service:
api.run(debug=debug, host='0.0.0.0', port=port)
