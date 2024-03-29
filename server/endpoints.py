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
DEVELOPER = 'developer'

# name spaces
users = Namespace(USERS, 'Users')
api.add_namespace(users)
groceries = Namespace(GROC, 'Groceries')
api.add_namespace(groceries)
developer = Namespace(DEVELOPER, 'Developer')
api.add_namespace(developer)


# api namespace endpoints
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
                    '1': {'text': 'List Groceries'},
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
                    '1': {'url': '/users/list',
                          'method': 'get', 'text': 'Show Users'},
                    '2': {'url': '/users/login',
                          'method': 'get', 'text': 'User Login'},
                    'X': {'text': 'Exit'},
                }}


# Developer endpoint
@developer.route(f'/n_{RECORDS}')
class Records(Resource):
    """
    Developer endpoint to check number of records
    """

    def get(self):
        """
        Gets number of records in database
        :return: Number of records
        """
        return len(groc.get_all_items())


@developer.route('/purge/<collection>')
class Purge(Resource):
    """
    Purges a collection
    """

    def delete(self, collection):
        """
        Empties collection of all records
        :param collection: Name of collection
        """
        if collection == usr.USER_COLLECT:
            usr.purge()
        elif collection == groc.GROC_COLLECT:
            groc.purge()
        else:
            raise Exception("Invalid collection.")


# users namespace endpoints
@users.route(f'/{LIST}')
class UserList(Resource):
    """
    This will get a list of currrent users.
    """

    def get(self):
        """
        Gets all existing users
        :return: List of usernames
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
        if usr.user_exists(name):
            raise Exception("User already exists.")
        else:
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
        Remove a user from collection.
        """
        name = request.json[usr.USERNAME]
        if usr.user_exists(name):
            usr.del_user(name)
        else:
            raise Exception("User does not exist.")


@users.route(f'/{usr.EMAIL}/<name>')
class UserEmail(Resource):
    """
    Get a user's email.
    """

    def get(self, name):
        """
        Get a user's email.
        :param name: User name
        :return: User email
        """
        if usr.user_exists(name):
            return usr.get_email(name)
        else:
            raise Exception("User does not exist.")


LOGIN_FIELDS = api.model('ExistingUser', {
    usr.USERNAME: fields.String,
    usr.PASSWORD: fields.String,
})


@users.route(f'/{LOGIN}')
class Login(Resource):
    @users.expect(LOGIN_FIELDS)
    def post(self):
        """
        Authenticates a login attempt
        :return: True if successful, False if not
        """
        name = request.json[usr.USERNAME]
        pw = request.json[usr.PASSWORD]
        return usr.authenticate(name, pw)


# groceries endpoints
@groceries.route(f'/{ITEMS}/<user>')
class GrocItems(Resource):
    """
    Gets items in a user's grocery list.
    """
    @api.response(HTTPStatus.OK, "Success")
    @api.response(HTTPStatus.NOT_FOUND, "Not Found")
    def get(self, user):
        """
        Gets list of user's grocery items.
        :param user: User name
        :return: List of grocery items
        """
        items = groc.get_user_list(user)
        if isinstance(items, list):
            # return [str(item[groc.ITEM]) for item in items]
            return items
        else:
            raise wz.NotFound(f'{user} not found.')


@groceries.route(f'/{GROC}_{TYPES}_{LIST}/<user>')
class GrocTypesList(Resource):
    """
    Gets all unique types in a user's list
    """
    @api.response(HTTPStatus.OK, "Success")
    @api.response(HTTPStatus.BAD_REQUEST, "Bad Request")
    def get(self, user):
        """
        Gets the unique grocery types in user's list.
        :param user: User name
        :return: List of grocery types
        """
        if usr.user_exists(user):
            return groc.get_types(user)
        else:
            raise Exception('User does not exist.')


GROC_FIELDS = api.model('item', {
    usr.USERNAME: fields.String,
    groc.ITEM: fields.String,
    groc.GROC_TYPE: fields.String,
    groc.QUANTITY: fields.Integer,
    groc.EXPIRATION_DATE: fields.String,
})


@groceries.route(f'/{ADD}')
class AddGrocItem(Resource):
    """
    Add a grocery item to the collection
    """
    @api.response(HTTPStatus.OK, "Success")
    @api.response(HTTPStatus.BAD_REQUEST, "Bad Request")
    @groceries.expect(GROC_FIELDS)
    def post(self):
        """
        Add grocery item to the collection
        """
        # username included in fields
        groc.add_item(request.json)


REMOVE_FIELDS = api.model('remove',
                          {groc.ITEM: fields.String,
                           usr.USERNAME: fields.String
                           })


@groceries.route(f'/{REMOVE}')
class RemoveGrocItem(Resource):
    """
    Remove grocery item from grocery list
    """
    @api.response(HTTPStatus.OK, "Success")
    @api.response(HTTPStatus.NOT_FOUND, "Not Found")
    @groceries.expect(REMOVE_FIELDS)
    def delete(self):
        """
        Remove grocery item from grocery list
        """
        item = request.json[groc.ITEM]
        user = request.json[usr.USERNAME]
        # if usr.user_exists(user) and groc.exists(item, user):
        #     groc.remove_item(item, user)
        # else:
        #     raise wz.NotFound(f'{item} or {user} not found.')
        # item_remove = groc.get_details(item, user)
        # if item_remove is not None:
        #     print(request.json)
        #     groc.remove_item(item, user)
        # else:
        #     raise wz.NotFound(f'{item} not found.')
        groc.remove_item(item, user)


@groceries.route(f'/{DETAILS}/<user>/<item>')
class GrocTypes(Resource):
    """
    Get details of an item from a user's list
    """
    @api.response(HTTPStatus.OK, "Success")
    @api.response(HTTPStatus.NOT_FOUND, "Not Found")
    def get(self, user, item):
        """
        Get details of an item from a user's list
        :param user: User name
        :param item: Item name
        :return: Details of an item
        """
        if usr.user_exists(user) and groc.exists(item, user):
            return groc.get_details(item, user)
        else:
            raise Exception("User or item invalid.")


UPDATE_FIELDS = api.model('update', {groc.ITEM: fields.String,
                                     usr.USERNAME: fields.String})


@groceries.route(f'/{UPDATE}/<field>/<data>')
class UpdateGrocItem(Resource):
    """
    Update grocery item with new details via optional parameters
    """
    @api.response(HTTPStatus.OK, "Success")
    @api.response(HTTPStatus.NOT_FOUND, "Not Found")
    @groceries.expect(UPDATE_FIELDS)
    def put(self, field, data):
        """
        Update grocery item with relevant new details
        :param field: Field to update
        :param data: Replacement data for field
        """
        item = request.json[groc.ITEM]  # should this be ITEM?
        user = request.json[usr.USERNAME]
        del request.json[groc.ITEM]
        del request.json[usr.USERNAME]

        # Check if user and item are valid
        if not usr.user_exists(user):
            raise Exception('User not found.')
        if not groc.exists(item, user):
            raise Exception('Item not found.')

        # Update relevant fields
        details = groc.get_details(item, user)
        if field.lower() == QUANTITY:
            details[QUANTITY] = int(data)

        elif field.lower() == EXPIRATION:
            details[EXPIRATION] = data

        elif field.lower() == groc.GROC_TYPE:
            details[groc.GROC_TYPE] = data

        groc.update_item(item, user, details)
