import logging

from api import Middleware

logger = logging.getLogger("middleware")


class ExampleMiddleware(Middleware):
    def process_request(self, request):
        logger.error("Processing request {}".format(request.url))

    def process_response(self, request, response):
        logger.error("Processing response {}".format(request.url))
