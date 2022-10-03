"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask
from flask_restx import Resource, Api
import werkzeug.exceptions as wz

import db.grocery_types as gtyp

app = Flask(__name__)
api = Api(app)

LIST = 'list'
ITEMS = 'items'
MAIN_PAGE = '/main_page'
MAIN_PAGE_NM = 'Main Page'
GROC_TYPE_LIST = f'/groc_types/{LIST}'
GROC_TYPE_LIST_NM = 'groc_types_list'
GROC_TYPE_DETAILS = f'/groc_types/{ITEMS}'
LOGIN = '/login'


# @api.route('/hello')
# class HelloWorld(Resource):
#     """
#     The purpose of the HelloWorld class is to have a simple test to see if the
#     app is working at all.
#     """
#     def get(self):
#         """
#         A trivial endpoint to see if the server is running.
#         It just answers with "hello world."
#         """
#         return {'hello': 'world'}


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
        