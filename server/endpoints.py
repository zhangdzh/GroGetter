"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask, request
from flask_restx import Resource, Api, fields
import werkzeug.exceptions as wz

import db.groc_types as gtyp
import db.groc_lists as glst
import db.users as usr

app = Flask(__name__)
api = Api(app)

LIST = 'list'
ITEMS = 'items'
ADD = 'add'
MAIN_PAGE = '/main_page'
MAIN_PAGE_NM = 'Main Page'
GROC_TYPES = 'groc_types'
GROC_TYPE_LIST = f'/{GROC_TYPES}/{LIST}'
GROC_TYPE_LIST_NM = f'{GROC_TYPES}_{LIST}'
GROC_TYPE_DETAILS = f'/{GROC_TYPES}/{ITEMS}'
GROC_LIST_ADD = f'/groc_list/{ADD}'
LOGIN = '/login'


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
        return {MAIN_PAGE_NM: {'the': 'grocery'}}


@api.route(GROC_TYPE_LIST)
class GrocList(Resource):
    """
    This will get a list of grocery types.
    """
    def get(self):
        """
        Returns a list of grocery types.
        """
        return {GROC_TYPE_LIST_NM: gtyp.get_groc_types()}


@api.route(f'{GROC_TYPE_DETAILS}/<groc_type>')
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
    usr.USERNAME: fields.String,
    usr.EMAIL: fields.String,
    usr.FULL_NAME: fields.String,
})


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


@api.route(GROC_LIST_ADD)
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
