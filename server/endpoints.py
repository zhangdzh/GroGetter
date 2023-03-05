"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask, request
from flask_restx import Resource, Api, fields, Namespace
import werkzeug.exceptions as wz
# import git

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
UPDATE = 'update'
QUANTITY = 'quantity'
MAIN_MENU = '/main_menu'
MAIN_MENU_NM = 'Main Menu'
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

# for webhook
# @app.route('/update_server', methods=['POST'])
# def webhook():
#     if request.method == 'POST':
#         repo = git.Repo('zhangdzh/GroGetter')
#         origin = repo.remotes.origin
#         origin.pull()
#         return 'Updated PythonAnywhere successfully', 200
#     else:
#         return 'Wrong event type', 400

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


@api.route(MAIN_MENU)
class MainMenu(Resource):
    """
    This is the main menu for the app
    """

    def get(self):
        """
        Gets the main menu
        """
        return {'Title': MAIN_MENU_NM,
                'Default': 0,
                'Choices': {
                    '1': {'url': '/groc_types/dict',
                          'method': 'get', 'text': 'List Grocery Types'},
                    '2': {'url': '/groc/dict',
                          'method': 'get', 'text': 'List Groceries'},
                    '3': {'url': '/users/dict',
                          'method': 'get', 'text': 'List Users'},
                    'X': {'text': 'Exit'},
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
        return {GROC_TYPE_LIST_NM: gtyp.get_groc_types()}


@groc_types.route(f'/{DICT}')
class GrocTypeDict(Resource):
    """
    This will get a dict of current grocery types
    """

    def get(self):
        """
        Returns a list of grocery types
        """
        return {'Data': gtyp.get_groc_types_dict(),
                'Type': 'Data',
                'Title': 'Grocery Types'}


# users namespace endpoints
@users.route(f'/{DICT}')
class UserDict(Resource):
    """
    This will get a dict of currrent users.
    """

    def get(self):
        """
        Returns a dict of current users.
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


@users.route(f'/{REMOVE}')
class RemoveUser(Resource):
    """
    Remove a user.
    """
    REMOVE_USER = api.model('RemoveUser', {usr.USER_NAME: fields.String})

    @users.expect(REMOVE_USER)
    def post(self):
        """
        Remove a user using the del_user function.
        """
        name = request.json[usr.USER_NAME]
        usr.del_user(name)


@users.route(f'/{usr.EMAIL}/<name>')
class UserEmail(Resource):
    """
    Get a user's email.
    """

    def get(self, name):
        """
        Get a user's email.
        """
        return {usr.EMAIL: usr.get_email(name)}


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


@groceries.route(f'/{DICT}')
class GrocDict(Resource):
    """
    Gets a dictionary of grocery lists
    """
    @api.response(HTTPStatus.OK, "Success")
    @api.response(HTTPStatus.NOT_FOUND, "Not Found")
    def get(self):
        """
        Returns list of grocery lists
        """
        return {'Data': groc.get_grocery_list(),
                'Type': 'Data',
                'Title': 'Grocery List'}


GROC_FIELDS = api.model('item', {
    ITEM: fields.String,
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
    @api.response(HTTPStatus.BAD_REQUEST, "Bad Request")
    @groceries.expect(GROC_FIELDS)
    def post(self):
        """
        Add grocery item
        """
        item = request.json[ITEM]
        del request.json[ITEM]
        groc.add_item(item, request.json)


REMOVE_FIELDS = api.model('remove', {ITEM: fields.String})


@groceries.route(f'/{REMOVE}/<items>')
class RemoveGrocItem(Resource):
    """
    Remove grocery item from grocery list
    """
    @api.response(HTTPStatus.OK, "Success")
    @api.response(HTTPStatus.NOT_FOUND, "Not Found")
    @groceries.expect(REMOVE_FIELDS)
    def post(self, items):
        """
        Remove grocery item from grocery list
        """
        item_remove = groc.get_details(items)
        if item_remove is not None:
            print(request.json)
            groc.remove_item(request.json[items])
        else:
            raise wz.NotFound(f'{items} not found.')


@groceries.route(f'/{DETAILS}/<item>')
class GrocTypes(Resource):
    """
    Get all groceries with given type
    """
    @api.response(HTTPStatus.OK, "Success")
    @api.response(HTTPStatus.NOT_FOUND, "Not Found")
    def get(self, item):
        """
        Returns number of items by types
        """
        return groc.get_details(item)


@groceries.route(f'/{UPDATE}')
class UpdateGrocItem(Resource):
    """
    Update grocery item
    """
    @api.response(HTTPStatus.OK, "Success")
    @api.response(HTTPStatus.NOT_FOUND, "Not Found")
    @groceries.expect(GROC_FIELDS)
    def post(self):
        """
        Update grocery item
        """
        item = request.json[ITEM]
        del request.json[ITEM]
        groc.update_item(item, request.json)


UPDATE_QUANTITY_FIELDS = api.model('update_quantity',
                                   {QUANTITY: fields.Integer})


@groceries.route(f'/{UPDATE}_{QUANTITY}')
class UpdateGrocItemQuantity(Resource):
    """
    Update grocery item quantity
    """
    @api.response(HTTPStatus.OK, "Success")
    @api.response(HTTPStatus.NOT_FOUND, "Not Found")
    @groceries.expect(GROC_FIELDS)
    def post(self):
        """
        Update grocery item quantity
        """
        item = request.json[ITEM]
        del request.json[ITEM]
        groc.update_item_quantity(item, request.json)
