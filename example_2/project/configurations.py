from api import Configurations
from example_2.application.middleware import ExampleMiddleware
from utilities.constants import Constants

configurations_params = {
    'debug': False,
    'error_404': Constants.BASE_ERROR_404,
    'error_500': Constants.BASE_ERROR_500,
    'templates_path': "example_2/templates",
    'static_path': "example_2/static",
    'serve_static': True,
    'exception_handler': None
}

CONFIGURATIONS = Configurations(**configurations_params)

MIDDLEWARE_LIST = [
    ExampleMiddleware
]
