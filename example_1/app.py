from api import API, View, Configurations
from utilities.responses import simple_response, json_response, html_response
from utilities.urls import url, url_group, include_url_group
from utilities.wsgi_http_server import StandaloneApplication


def exception_handler(error):
    response = simple_response("Ops! Something is wrong, please retry later :)")
    return response


app_configs = Configurations(
    debug=True,
    templates_path='example_1/templates',
    # exception_handler=exception_handler
)
app = API(configs=app_configs)


@app.route('/home')
def home(request):
    response = simple_response('Home Page')
    return response


app.add_route('/', home)


@app.route('/status')
def status(request):
    user_agent = request.environ.get('HTTP_USER_AGENT', 'no-agent')
    response = json_response({'user_agent': user_agent})
    return response


@app.route('/echo/{stuff:d}')
def echo(request, stuff):
    response = json_response({'digits': stuff})
    return response


@app.route('/echo/{stuff:D}')
def echo(request, stuff):
    response = json_response({'non-digits': stuff})
    return response


@app.route('/error')
def echo(request):
    value = 1/0
    response = json_response({'error': value})
    return response


@app.route('/template')
def template(request):
    rendered_template = app.render_template('index.html', {'body': 'BODY'})
    return html_response(rendered_template)


class TestView(View):

    def get(self, request):
        return simple_response('Class View Page')

    def post(self, request):
        data = request.json
        return json_response(data)


class TestHTMLView(View):

    def get(self, request):
        rendered_template = self.render_template('index.html', {'body': 'BODY'})
        return html_response(rendered_template)


class TestJsonDigitView(View):

    def get(self, request, stuff):
        return json_response({'class-digit': stuff})


class TestJsonWordView(View):

    def get(self, request, stuff):
        return json_response({'class-word': stuff})


url_test_view = url('/html', TestView)
url_test_view_html = url('/html_rendered', TestHTMLView)
url_test_json_view = url_group(
    url('class/{stuff:d}', TestJsonDigitView),
    url('class/{stuff:D}', TestJsonWordView)
)
route_group = url_group(
    url_test_view,
    url_test_view_html,
    include_url_group('/json', url_test_json_view)
)

app.add_route_group(route_group)


if __name__ == '__main__':
    options = {
        'bind': '127.0.0.1:8000',
        'timeout': 600,
        'workers': 2
    }
    StandaloneApplication(app, options).run()
