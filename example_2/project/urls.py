from example_2.application.views import HomeView
from utilities.urls import url_group, url

ROUTES = url_group(
    url('/', HomeView)
)
