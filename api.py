import inspect
import logging
import os
import traceback

from jinja2 import Environment, FileSystemLoader
from parse import parse
from webob import Request
from whitenoise import WhiteNoise

from utilities.constants import Constants
from utilities.exceptions import PathAlreadyExists, UnimplementedMethod
from utilities.responses import simple_response
from utilities.urls import check_url

api_log = logging.getLogger("web_sync_framework")


class API(object):
    def __init__(self, configs=None):
        self.routes = dict()
        self.configs = configs
        if not isinstance(self.configs, Configurations):
            self.configs = Configurations()

        self.static_content_provider = self._process_call
        if self.configs.serve_static:
            self.static_content_provider = WhiteNoise(
                self._process_call, self.configs.static_path
            )

    def render_template(self, filename, context=None):
        rendering_context = context
        if rendering_context is None:
            rendering_context = dict()
        return self.configs.get_template(filename).render(
            **rendering_context
        ).encode()

    def add_route(self, path, handler):
        if path in self.routes:
            raise PathAlreadyExists("{}".format(path))
        check_url(path)
        self.routes[path] = handler

    def add_route_group(self, path_group):
        for url_tuple in path_group:
            self.add_route(url_tuple[0], url_tuple[1])

    def route(self, path):
        def wrapper(handler):
            self.add_route(path, handler)
            return handler
        return wrapper

    def _missing_request_404(self):
        response = simple_response(self.configs.error_404, 404)
        return response

    def _error_request_500(self, error):
        api_log.error(str(error), exc_info=True)
        if self.configs.exception_handler is not None:
            return self.configs.exception_handler(error)

        text = self.configs.error_500
        if self.configs.debug:
            text = "<pre>{}</pre>".format(
                traceback.format_exc()
            ).replace("\n", "<br />")
        response = simple_response(text, 500)
        return response

    def _find_handler(self, requested_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, requested_path)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None

    def _handle_request(self, request):
        handler, kwargs = self._find_handler(request.path)
        if inspect.isclass(handler):
            handler = handler(self)

        if handler is not None:
            return handler(request, **kwargs)

        return self._missing_request_404()

    def _process_call(self, environ, start_response):
        request = Request(environ)
        try:
            response = self._handle_request(request)
        except Exception as error:
            response = self._error_request_500(error)

        return response(environ, start_response)

    def __call__(self, environ, start_response):
        path_info = environ.get("PATH_INFO", "")

        if path_info.startswith("/static"):
            environ["PATH_INFO"] = path_info[len("/static"):]
            return self.static_content_provider(environ, start_response)

        return self._process_call(environ, start_response)


class View(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, request, **kwargs):
        method_name = request.method.lower()
        method = getattr(self, method_name, None)
        if method is None:
            raise UnimplementedMethod(method_name)
        return method(request, **kwargs)

    def render_template(self, filename, context=None):
        return self.app.render_template(filename, context)


class Configurations(object):
    def __init__(
            self, debug=False,
            error_404=Constants.BASE_ERROR_404,
            error_500=Constants.BASE_ERROR_500,
            templates_path=Constants.TEMPLATES_PATH,
            static_path=Constants.STATIC_PATH,
            serve_static=True,
            exception_handler=None
    ):
        self.debug = debug
        self.error_404 = error_404
        self.error_500 = error_500
        self.templates_env = Environment(
            loader=FileSystemLoader(os.path.abspath(templates_path))
        )
        self.static_path = static_path
        self.serve_static = serve_static
        self.exception_handler = exception_handler

    def get_template(self, template):
        return self.templates_env.get_template(template)
