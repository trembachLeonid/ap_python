from marshmallow import Schema, fields
from marshmallow.validate import Length, Range


class user_schema(Schema):
    username = fields.String(validate=Length(min=4))
    firstName = fields.String(validate=Length(min=3))
    lastName = fields.String(validate=Length(min=3))
    password = fields.String(validate=Length(min=8))
    email = fields.Email()
    phone = fields.Number()
    currentMoney = fields.Number()

class family_schema(Schema):
    familyName = fields.String(validate=Length(min=5))
    users = fields.List(fields.String,validate=Length(min=2))
    currentMoney = fields.Float()
    
class login_schema(Schema):
    username = fields.String()
    password = fields.String()