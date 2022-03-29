from marshmallow.validate import Length
from auth_api.extensions import ma


class TOTPRequestSchema(ma.Schema):
    totp_code = ma.String(required=True, validate=Length(min=6, max=6), example='411526')
    totp_status = ma.Boolean(required=True)
