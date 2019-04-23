from webob import Response


def json_response(data=None, status=200):
    response = Response()
    response.json = data or dict()
    response.content_type = 'application/json'
    response.status_code = status
    return response


def simple_response(data=None, status=200):
    response = Response()
    response.text = data or ''
    response.status_code = status
    return response


def html_response(data=None, status=200):
    response = Response()
    response.body = data or b''
    response.status_code = status
    return response
