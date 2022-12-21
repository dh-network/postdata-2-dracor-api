import flask
from flask import jsonify, Response, send_from_directory
from apidoc import InfoResponse, spec
import os
import json


# Setup using environment variables: This can be used to configure the service when running in Docker
service_version = str(os.environ.get("SERVICE_VERSION", "0.0"))
"""SERVICE_VERSION: Version of the service. Will be set with the env file and conform to a github release
"""

service_url = str(os.environ.get("SERVICE_URL", "http://localhost"))
"""SERVICE_URL: url where the service can be accessed.
Normally, it's somehow set when running the flask dev server
but it needs to be adapted, when one wants to access the docker container
default is "localhost".
"""

service_port = int(os.environ.get("SERVICE_PORT", 5000))
"""SERVICE_PORT: Port of the running service. 
flask's default is 5000
"""

# Debug Mode: Activates the flask Debug Mode
if os.environ.get("SERVICE_DEBUG", "TRUE") == "FALSE":
    debug = False
else:
    debug = True

# Triple Store Connection Details are retrieved from environment variables

triplestore_name = str(os.environ.get("PD_TRIPLESTORE", "stardog"))
"""PD_TRIPLESTORE: Name of the Triple Store.
Default implementation is based on Stardog.
"""

triplestore_protocol = os.environ.get("PD_PROTOCOL", "http")
"""PD_PROTOCOL: Postdata's current implementation uses http only."""

triplestore_url = os.environ.get("PD_URL", "localhost")
"""PD_URL: Url of the Triple Store. Defaults to localhost, but is overwritten with the env file when using Docker.
"""

triplestore_port = int(os.environ.get("PD_PORT", 5820))
"""PD_PORT: Port of the Triple Store. 
Stardog Default is 5820
"""

triplestore_db = os.environ.get("PD_DATABASE", "PD_KG")
"""PD_DATABASE: Name of the Database in the Triple Store
"""

triplestore_user = os.environ.get("PD_USER", "admin")
"""PD_USER: User name to use to connect to Triplestore
"""

triplestore_pwd = os.environ.get("PD_PASSWORD", "admin")
"""PD_PASSWORD: User name to use to connect to Triplestore
"""


# Setup of flask API
api = flask.Flask(__name__)
# enable UTF-8 support
api.config["JSON_AS_ASCII"] = False


@api.route("/", methods=["GET"])
def swagger_ui():
    """Displays the OpenAPI Documentation of the API"""
    return send_from_directory("static/swagger-ui", "index.html")


@api.route("/info", methods=["GET"])
def get_info():
    """Information about the API
    ---
    get:
        summary: About the service
        description: Returns information about the service's API
        operationId: get_info
        responses:
            200:
                description: Information about the API
                content:
                    application/json:
                        schema: InfoResponse
    """

    data = dict(
        name="POSTDATA 2 DraCor API",
        version=service_version,
        description="Connects POSTDATA to a DraCor-like Frontend"
    )
    # To make sure, that the response matches the schema defined in the OpenAPI
    # we validate this data using the InfoResponse Schema.
    schema = InfoResponse()
    schema.load(data)

    return jsonify(schema.dump(data))


# Generate the OpenAPI Specification
# This can not be moved to the apidoc module,
# because to generate the Documentation, we need the flask API to be runnable
with api.test_request_context():
    spec.path(view=get_info)

# write the OpenAPI Specification as YAML to the root folder
with open('openapi.yaml', 'w') as f:
    f.write(spec.to_yaml())

# Write the Specification to the /static folder to use in the Swagger UI
with open('static/swagger-ui/openapi.json', 'w') as f:
    json.dump(spec.to_dict(), f)

# Run the Service:
api.run(debug=debug, host='0.0.0.0', port=service_port)
