from example_2.project.wsp_app import app
from utilities.wsgi_http_server import StandaloneApplication

if __name__ == '__main__':
    options = {
        'bind': '127.0.0.1:8000',
        'timeout': 600,
        'workers': 1
    }
    StandaloneApplication(app, options).run()
