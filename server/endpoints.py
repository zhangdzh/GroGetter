"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask, request
from flask_restx import Resource, Api, fields, Namespace

import db.groc_types as gtyp
import db.users as usr
import db.groceries as groc

app = Flask(__name__)
api = Api(app)

# string constants
GROC = 'groc'
USERS = 'users'
LIST = 'list'
DETAILS = 'details'
ADD = 'add'
DICT = 'dict'
TYPES = 'types'
ITEM = 'item'
ITEMS = 'items'
REMOVE = 'remove'
MAIN_PAGE = '/main_page'
MAIN_PAGE_NM = 'Main Page'
GROC_TYPES = f'{GROC}_{TYPES}'
GROC_LIST = f'{GROC}_{LIST}'
USER_DICT_NM = f'{USERS}_{DICT}'
USER_LIST_NM = f'{USERS}_{LIST}'
GROC_TYPE_LIST_NM = f'{GROC_TYPES}_{LIST}'

# name spaces
groc_types = Namespace(GROC_TYPES, 'Grocery Types')
api.add_namespace(groc_types)
groc_lists = Namespace(GROC_LIST, 'Grocery Lists')
api.add_namespace(groc_lists)
users = Namespace(USERS, 'Users')
api.add_namespace(users)
groceries = Namespace(GROC, 'Groceries')
api.add_namespace(groceries)
# note to self/team: focusing just on users namespace rn
# until we figure out the organization for groceries and such


# api namespace endpoints
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


# grocery types namespace endpoints
@groc_types.route(f'/{LIST}')
class GrocTypeList(Resource):
    """
    This will get a list of grocery types.
    """
    def get(self):
        """
        Returns a list of grocery types.
        """
        # leads to "grocery_types_list" key error which is GROC_TYPE_LIST_NM
        return {GROC_TYPE_LIST_NM: gtyp.get_groc_types}


# users namespace endpoints
@users.route(f'/{DICT}')
class UserDict(Resource):
    """
    This will get a dict of currrent users.
    """
    def get(self):
        """
        Returns a list of current users.
        """
        return {'Data': usr.get_users_dict(),
                'Type': 'Data',
                'Title': 'Active Users'}


@users.route(f'/{LIST}')
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


@users.route(f'/{ADD}')
class AddUser(Resource):
    """
    Add a user.
    """
    @users.expect(USER_FIELDS)
    def post(self):
        """
        Add a user.
        """
        name = request.json[usr.USER_NAME]
        del request.json[usr.USER_NAME]
        usr.add_user(name, request.json)


# groceries endpoints
@groceries.route(f'/{ITEMS}')
class GrocItems(Resource):
    """
    Gets items in grocery list.
    """
    @api.response(HTTPStatus.OK, "Success")
    @api.response(HTTPStatus.NOT_FOUND, "Not Found")
    def get(self):
        """
        Returns list of grocery list items.
        """
        return groc.get_items()


GROC_FIELDS = api.model('item', {
    "ITEMNAME": fields.String,
    groc.GROC_TYPE: fields.String,
    groc.QUANTITY: fields.Integer,
    groc.EXPIRATION_DATE: fields.String,
})


@groceries.route(f'/{ADD}')
class AddGrocItem(Resource):
    """
    Get number of items by types
    """
    @api.response(HTTPStatus.OK, "Success")
    @api.response(HTTPStatus.NOT_FOUND, "Not Found")
    def post(self):
        """
        Add grocery item
        """
        item = request.json[ITEM]
        del request.json[ITEM]
        groc.add_item(item, request.json)


@groceries.route(f'/{REMOVE}')
class RemoveGrocItem(Resource):
    """
    Remove grocery item from grocery list
    """
    @api.response(HTTPStatus.OK, "Success")
    @api.response(HTTPStatus.NOT_FOUND, "Not Found")
    def post(self):
        """
        Remove grocery item from grocery list
        """
        item = request.json[ITEM]
        del request.json[ITEM]
        groc.remove_item(item, request.json)
