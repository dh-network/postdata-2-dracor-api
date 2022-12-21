from marshmallow import Schema, fields
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
import json
from api import this_service_url, this_server_desc, api, get_info


class InfoResponse(Schema):
    """Schema of the response of the 'api/info' endpoint"""
    baseurl = fields.Str()
    description = fields.Str()
    name = fields.Str()
    version = fields.Str()


# construct the currently running server object for the OpenAPI Documentation:
# if running in docker, .env will be evaluated
this_service_server_desc = dict(
        description=this_server_desc,
        url=this_service_url
)

spec = APISpec(
    title="Poecor POSTDATA connector",
    version="1.0",
    openapi_version="3.0.3",
    info=dict(
        description="""
Middleware to connect POSTDATA to a DraCor-like frontend.""",
        version="1.0",
        contact=dict(
            name="Ingo Börner",
            email="ingo.boerner@uni-potsdam.de"
        ),
        license=dict(
            name="GPL-3.0 license",
            url="https://www.gnu.org/licenses/gpl-3.0.html"
        )
    ),
    servers=[
        this_service_server_desc,
        dict(
            description="Production",
            url="https://poecor.org"
        ),
        dict(
            description="Staging",
            url="https://staging.poecor.org"
        )
    ],
    externalDocs=dict(
        description="Code on Github",
        url="https://github.com/dh-network/postdata-2-dracor-api"
    ),
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)


def generate_apidoc():
    """Generate the Open API Documentation.
    Writes YAML openapi.yaml to root directory and openapi.json to the Swagger UI folder in /static
    """
    with api.test_request_context():
        spec.path(view=get_info)

    # write the OpenAPI specification as YAML
    with open("openapi.yaml", "w") as yaml_file:
        yaml_file.write(spec.to_yaml())

    # Write the OpenAPI as JSON to the static swagger dictionary
    with open("static/swagger-ui/openapi.json", "w") as json_file:
        json.dump(spec.to_dict(), json_file)
