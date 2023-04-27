"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask, request
from flask_cors import CORS
from flask_restx import Resource, Api, fields, Namespace
import werkzeug.exceptions as wz
import db.users as usr
import db.groceries as groc

app = Flask(__name__)
api = Api(app)
CORS(app)

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
EXPIRATION = 'expiration'
RECORDS = 'records'
LOGIN = 'login'

# name spaces
groc_lists = Namespace(GROC_LIST, 'Grocery Lists')
api.add_namespace(groc_lists)
users = Namespace(USERS, 'Users')
api.add_namespace(users)
groceries = Namespace(GROC, 'Groceries')
api.add_namespace(groceries)


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
                    '1': {'url': '/groc/items',
                          'method': 'get', 'text': 'Show Grocery Items'},
                    '2': {'url': '/groc/dict',
                          'method': 'get', 'text': 'Show Grocery Lists'},
                    '3': {'url': '/users/dict',
                          'method': 'get', 'text': 'Show Users'},
                    'X': {'text': 'Exit'},
                }}


# Developer endpoint
@api.route(f'/N_{RECORDS}')
class Records(Resource):
    """
    Developer endpoint to check number of records
    """

    def get(self):
        """
        Returns number of records in database
        """
        return len(groc.get_items())


# users namespace endpoints
@users.route(f'/{LIST}')
class UserList(Resource):
    """
    This will get a list of currrent users.
    """

    def get(self):
        """
        Returns a list of current users.
        """
        return usr.get_usernames()


USER_FIELDS = api.model('NewUser', {
    usr.USERNAME: fields.String,
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
        name = request.json[usr.USERNAME]
        del request.json[usr.USERNAME]
        usr.add_user(name, request.json)


@users.route(f'/{REMOVE}')
class RemoveUser(Resource):
    """
    Remove a user.
    """
    REMOVE_USER = api.model('RemoveUser', {usr.USERNAME: fields.String})

    @users.expect(REMOVE_USER)
    def post(self):
        """
        Remove a user using the del_user function.
        """
        name = request.json[usr.USERNAME]
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


LOGIN_FIELDS = api.model('ExistingUser', {
    usr.USERNAME: fields.String,
    usr.PASSWORD: fields.String,
})


@users.route(f'/{LOGIN}')  # no test yet
class Login(Resource):
    @users.expect(LOGIN_FIELDS)
    def get(self):
        """
        Authenticate a login attempt
        True if successful, False otherwise
        """
        name = request.json[usr.USERNAME]
        pw = request.json[usr.PASSWORD]
        del request.json[usr.USERNAME]
        del request.json[usr.PASSWORD]

        if not usr.user_exists(name):
            return False
        if usr.get_user_password(name) == pw:
            return True
        else:
            return False


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
        item = groc.get_items()
        if item is not None:
            return item
        else:
            raise wz.NotFound(f'{item} not found.')


@groceries.route(f'/{GROC}_{TYPES}_{LIST}')
class GrocTypesList(Resource):
    """
    Gets list of grocery types
    """
    @api.response(HTTPStatus.OK, "Success")
    @api.response(HTTPStatus.BAD_REQUEST, "Bad Request")
    def get(self):
        """
        Returns a list of grocery types.
        """
        types = groc.get_groc_types()
        return types


@groceries.route(f'/{DICT}')
class GrocDict(Resource):
    """
    Gets a dictionary of grocery list info
    """
    @api.response(HTTPStatus.OK, "Success")
    @api.response(HTTPStatus.NOT_FOUND, "Not Found")
    def get(self):
        """
        Returns list of grocery lists
        """
        list = groc.get_grocery_list()
        if list is not None:
            return {'Data': list,
                    'Type': 'Data',
                    'Title': 'Grocery List'}
        else:
            raise wz.NotFound(f'{list} not found.')


GROC_FIELDS = api.model('item', {
    ITEM: fields.String,
    usr.USERNAME: fields.String,
    groc.GROC_TYPE: fields.String,
    groc.QUANTITY: fields.Integer,
    groc.EXPIRATION_DATE: fields.String,
})


@groceries.route(f'/{ADD}')
class AddGrocItem(Resource):
    """
    Add a grocery item 
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


@groceries.route(f'/{REMOVE}/<item>/<user>')
class RemoveGrocItem(Resource):
    """
    Remove grocery item from grocery list
    """
    @api.response(HTTPStatus.OK, "Success")
    @api.response(HTTPStatus.NOT_FOUND, "Not Found")
    @groceries.expect(REMOVE_FIELDS)
    def delete(self, item, user):
        """
        Remove grocery item from grocery list
        """
        item_remove = groc.get_details(item)
        if item_remove is not None:
            print(request.json)
            groc.remove_item(item, user)
        else:
            raise wz.NotFound(f'{item} not found.')


@groceries.route(f'/{DETAILS}/<item>')
class GrocTypes(Resource):
    """
    Get details of an item
    """
    @api.response(HTTPStatus.OK, "Success")
    @api.response(HTTPStatus.NOT_FOUND, "Not Found")
    def get(self, item):
        """
        Returns number of items by types
        """
        return groc.get_details(item)


UPDATE_FIELDS = api.model('update', {ITEM: fields.String})


@groceries.route(f'/{UPDATE}/{QUANTITY}/<num>')
@groceries.route(f'/{UPDATE}/{EXPIRATION}/<date>')
@groceries.route(f'/{UPDATE}/{groc.GROC_TYPE}/<type>')
class UpdateGrocItem(Resource):
    """
    Update grocery item with new details via optional parameters
    """
    @api.response(HTTPStatus.OK, "Success")
    @api.response(HTTPStatus.NOT_FOUND, "Not Found")
    @groceries.expect(UPDATE_FIELDS)
    def put(self, num=None, date=None, type=None):
        """
        Update grocery item with relevant new details
        """
        item = request.json[ITEM]  # should this be ITEM?
        del request.json[ITEM]

        # need to update each of the fields if not None
        if num is not None:
            groc.update_quantity(item, num)

        if date is not None:
            groc.update_expiration(item, date)

        if type is not None:
            groc.update_groc_type(item, type)


# Deprecated --separate update endpoints
# @groceries.route(f'/{UPDATE}')
# class UpdateGrocItem(Resource):
#     """
#     Update grocery item with new details
#     """
#     @api.response(HTTPStatus.OK, "Success")
#     @api.response(HTTPStatus.NOT_FOUND, "Not Found")
#     @groceries.expect(GROC_FIELDS)
#     def put(self):
#         """
#         Update grocery item with new details
#         """
#         item = request.json[ITEM]
#         del request.json[ITEM]
#         groc.update_item(item, request.json)


# UPDATE_QUANTITY_FIELDS = api.model('update_quantity',
#                                    {QUANTITY: fields.Integer})


# @groceries.route(f'/{UPDATE}_{GROC_TYPES}')
# class UpdateGrocItemType(Resource):
#     """
#     Update grocery item type
#     """
#     @api.response(HTTPStatus.OK, "Success")
#     @api.response(HTTPStatus.NOT_FOUND, "Not Found")
#     @groceries.expect(GROC_FIELDS)
#     def put(self):
#         """
#         Update grocery item type
#         """
#         item = request.json[ITEM]
#         del request.json[ITEM]
#         groc.update_groc_type(item, request.json)


# @groceries.route(f'/{UPDATE}_{QUANTITY}')
# class UpdateGrocItemQuantity(Resource):
#     """
#     Update grocery item quantity
#     """
#     @api.response(HTTPStatus.OK, "Success")
#     @api.response(HTTPStatus.NOT_FOUND, "Not Found")
#     @groceries.expect(GROC_FIELDS)
#     # ^Is this supposed to expect all the fields or just the quantity?
#     def put(self):
#         """
#         Update grocery item quantity
#         """
#         item = request.json[ITEM]
#         del request.json[ITEM]
#         groc.update_quantity(item, request.json)

# # Note: this should exist if update_quantity exists


# @groceries.route(f'/{UPDATE}_{EXPIRATION}')
# class UpdateGrocItemExpiration(Resource):
#     """
#     Update grocery item expiration date
#     """
#     @api.response(HTTPStatus.OK, "Success")
#     @api.response(HTTPStatus.NOT_FOUND, "Not Found")
#     @groceries.expect('string')  # Syntax?
#     def put(self):
#         """
#         Update grocery item expiration date
#         """
#         item = request.json[ITEM]
#         del request.json[ITEM]
#         groc.update_expiration(item, request.json)
