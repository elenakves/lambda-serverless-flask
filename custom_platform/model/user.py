from marshmallow import Schema, fields, post_load
# https://auth0.com/blog/developing-restful-apis-with-python-and-flask/#restful-flask

ACCESS = {
    'guest': 0, # no access
    'user': 1,
    'admin': 2
}


class User():

    def __init__(self, user_id, name, password, access=ACCESS['user']):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.access = access

    def __repr__(self):
        d = self.__dict__.copy()
        return "%s(%r)" % (self.__class__, d)

    def get_current_user_role(self):
        return self.access

    def error_response(self):
        message = "User not authorized to perform this action"
        return message

    # def is_admin(self):
    #     return self.access == ACCESS['admin']
    #
    # def is_allowed(self, access_level):
    #     return self.access >= access_level


class UserSchema(Schema):
    user_id = fields.Str()
    name = fields.Str()
    password = fields.Str()
    access = fields.Str()
    @post_load
    def create_user(self, data):
        return User(**data)

