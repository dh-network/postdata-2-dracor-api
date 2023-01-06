from marshmallow import Schema, fields
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin


class InfoResponse(Schema):
    """Schema of the response of the 'api/info' endpoint"""
    name = fields.Str()
    version = fields.Str()
    description = fields.Str()


class CorpusMetrics(Schema):
    """Schema of the corpus metrics included in the corpus metadata"""
    poems = fields.Int()
    authors = fields.Int()
    stanzas = fields.Int()
    verses = fields.Int()
    words = fields.Int()
    grammatical_syllables = fields.Int()
    metrical_syllables = fields.Int()


class CorpusMetadata(Schema):
    name = fields.Str()
    title = fields.Str()
    description = fields.Str()
    metrics = fields.Nested(CorpusMetrics, required=False)


spec = APISpec(
    title="Poecor POSTDATA connector",
    version="1.0",
    openapi_version="3.0.3",
    info=dict(
        description="""
Middleware to connect POSTDATA to a DraCor-like frontend.""",
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
        dict(
            description="Local Flask",
            url="http://localhost:5000"
        ),
        dict(
            description="Production",
            url="https://poecor.org/api"
        ),
        dict(
            description="Staging",
            url="https://staging.poecor.org/api"
        )
    ],
    externalDocs=dict(
        description="Code on Github",
        url="https://github.com/dh-network/postdata-2-dracor-api"
    ),
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)
