"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask, request
from flask_restx import Resource, Api, fields, Namespace
import werkzeug.exceptions as wz

import db.groc_types as gtyp
import db.groc_lists as glst
import db.users as usr

app = Flask(__name__)
api = Api(app)

GROC_TYPES_NS = 'grocery_types'
GROC_LISTS_NS = 'grocery_lists'
USERS_NS = 'users'

groc_types = Namespace(GROC_TYPES_NS, 'Grocery Types')
api.add_namespace(groc_types)
groc_lists = Namespace(GROC_LISTS_NS, 'Grocery Lists')
api.add_namespace(groc_lists)
users = Namespace(USERS_NS, 'Users')


LIST = 'list'
DETAILS = 'details'
ADD = 'add'
DICT = 'dict'
MAIN_PAGE = '/main_page'
MAIN_PAGE_NM = 'Main Page'
GROC_TYPES = 'groc_types'
GROC_TYPE_LIST = f'/{GROC_TYPES}/{LIST}'
# GROC_TYPE_LIST_NM = f'{GROC_TYPES}_{LIST}'
GROC_TYPE_DETAILS = f'/{GROC_TYPES}/{DETAILS}'
GROC_LIST_ADD = f'/groc_list/{ADD}'
LOGIN = '/login'
USERS = 'users'
USER_ADD = f'/{USERS}/{ADD}'
USER_DICT = f'/{DICT}'
USER_DICT_NM = f'{USERS_NS}_dict'
USER_LIST = f'/{LIST}'
USER_LIST_NM = f'{USERS_NS}_list'

# for namespaces
GROC_TYPE_LIST_W_NS = f'{GROC_TYPES_NS}/{LIST}'
GROC_TYPE_LIST_NM = f'{GROC_TYPES_NS}_list'
GROC_TYPE_DETAILS = f'/{DETAILS}'
GROC_TYPE_DETAILS_W_NS = f'{GROC_TYPES_NS}/{DETAILS}'
USER_LIST_W_NS = f'{USERS_NS}/{LIST}'
USER_DICT_W_NS = f'{USERS_NS}/{DICT}'
USER_ADD_W_NS = f'{USERS_NS}/{ADD}'


@api.route('/endpoints')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = ''
        # sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


@api.route(MAIN_PAGE)
class MainPage(Resource):
    """
    This will deliver our main app page
    """
    def get(self):
        """
        Gets the main homepage
        """
        return {'Title': MAIN_PAGE_NM,
                'Default': 0,
                'Choices': {
                    '1': {'text': 'List Grocery Types'},
                    }}

# causing issues 10/29 --- fix later if necessary
# @groc_types.route(GROC_TYPE_LIST)
# class GrocTypeList(Resource):
#     """
#     This will get a list of grocery types.
#     """
#     def get(self):
#         """
#         Returns a list of grocery types.
#         """
#         return {GROC_TYPE_LIST_NM: gtyp.get_groc_types()}


@groc_types.route(f'{GROC_TYPE_DETAILS}/<groc_type>')
class GroceryTypeDetails(Resource):
    """
    This will get the items by the type..
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, groc_type):
        gt = gtyp.get_groc_items_by_type(groc_type)
        if gt is not None:
            return {groc_type: gt}
        else:
            raise wz.NotFound(f'{groc_type} not found.')


@api.route(LOGIN)
class Login(Resource):
    """
    I'm not too sure how this login route will work.
    """
    def login(self):
        pass


user_fields = api.model('NewUser', {
    usr.USER_NAME: fields.String,
    usr.EMAIL: fields.String,
})


@api.route(USER_DICT)
class UserDict(Resource):
    """
    This will get a list of currrent users.
    """
    def get(self):
        """
        Returns a list of current users.
        """
        return {'Data': usr.get_users_dict(),
                'Type': 'Data',
                'Title': 'Active Users'}


@api.route(USER_LIST)
class UserList(Resource):
    """
    This will get a list of currrent users.
    """
    def get(self):
        """
        Returns a list of current users.
        """
        return {USER_LIST_NM: usr.get_usernames()}


USER_FIELDS = api.model('NewUser', {
    usr.USER_NAME: fields.String,
    usr.EMAIL: fields.String,
    usr.PASSWORD: fields.String,
})


@api.route(USER_ADD)
class AddUser(Resource):
    """
    Add a user.
    """
    @api.expect(user_fields)
    def post(self):
        """
        Add a user.
        """
        print(f'{request.json=}')
        name = request.json[usr.USER_NAME]
        del request.json[usr.USER_NAME]
        usr.add_user(name, request.json)


class GrocListType(fields.Raw):
    """
    This is a custom data type for the grocery list to be used
    for checking the input type.
    """
    def output(self, key, obj, **kwargs):
        try:
            dct = getattr(obj, self.attribute)
        except AttributeError:
            return {}
        return dct or {}


GROC_FIELDS = api.model('GROC_LIST_ADD', {
    glst.USER_NAME: fields.String,
    glst.LIST_NAME: fields.String,
    glst.NUM_ITEMS: fields.Integer,
    glst.GROC_LIST: GrocListType,
})


@groc_lists.route(GROC_LIST_ADD)
class AddGroceryList(Resource):
    """
    This will add a new grocery list to the database.
    """
    @api.expect(GROC_FIELDS)
    def post(self):
        """
        Add list to groc_list database.
        """
        print(f'{request.json=}')
        name = request.json[glst.USER_NAME]
        del request.json[glst.USER_NAME]
        glst.add_groc(name, request.json)
