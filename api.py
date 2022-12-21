import flask
from flask import jsonify, Response, send_from_directory
from apidoc import generate_apidoc, InfoResponse
import os


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


this_server_desc = str(os.environ.get("OPENAPI_SERVER_DESC", "local flask development"))
"""OPENAPI_SERVER_DESC: description that is used to describe the server in the openapi documentation
"""

# get cleaned service url, depending, if the port works or not
if ":" + str(port) in service_url:
    # port is also in the url
    this_service_url = service_url
else:
    this_service_url = service_url + ":" + str(port)


# Setup of flask API
api = flask.Flask(__name__)
# enable UTF-8 support
api.config["JSON_AS_ASCII"] = False


@api.route("/", methods=["GET"])
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
    pass


# Generate the Documentation:
generate_apidoc()

# Run the Service:
api.run(debug=debug, host='0.0.0.0', port=port)
