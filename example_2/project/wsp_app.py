from api import API
from example_2.project.configurations import CONFIGURATIONS, MIDDLEWARE_LIST
from example_2.project.urls import ROUTES

configurations = CONFIGURATIONS
middleware_list = MIDDLEWARE_LIST
routes = ROUTES

app = API(configs=configurations)
app.add_multiple_middleware(middleware_list)
app.add_route_group(routes)
