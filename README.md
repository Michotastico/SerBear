# Ser-Bear

Ser-bear is a Python synchronous web server framework built to learn how frameworks like Flask work, and how it can grow to become something like Django.

It uses WSGI to work (the `requirements.pip` comes with `Gunicorn` to be able to run).

## How to use it

Basically, it works like Flask (see `example_1`) in the following way.

```python
from serbear import Serbear
from serbear.utilities import simple_response, json_response, html_response

app = Serbear()

@app.route("/")
def home(request):
    response = simple_response("Home Page")
    return response

@app.route('/echo/{stuff:d}')
def echo(request, stuff):
    response = json_response({'digits': stuff})
    return response

@app.route('/template')
def template(request):
    rendered_template = app.render_template('index.html', {'body': 'BODY'})
    return html_response(rendered_template)
```

To start the server, you can always run it from the terminal 
```
gunicorn server:app
```

But, if you wish, you can use gunicorn in the programmatic way included

```python
from server import app
from serbear.utilities.wsgi_http_server import StandaloneApplication
if __name__ == '__main__':
    options = {
        'bind': '127.0.0.1:8000',
        'timeout': 600,
        'workers': 1
    }
    StandaloneApplication(app, options).run()
```

And run it with 
```
python main.py
```

### Features
 * WSGI compatible
 * Basic, parametric and grouped url routing.
 * Function/Class bases handlers
 * Support of static content and template rending.
 * Middlewares and Exception handlers
 * Bears

### TO-DO
 * Add missing things and build the pypi package.
 * Improve this readme adding content like `example_2`, a Django-like project structure.
 * Add method type handling in the `@app.route` decorator.
 * Add testing.
 * Add documentation.
 * Add github-integration stuff.
 * Add more bear puns with my bearly hands :).
 * Design and add the second part of the project which includes an async bear.


### Prerequisites
[2020 is almost here](https://pythonclock.org/), so this project is made using Python, A.K.A. Python 3. In a personal way I use Python 3.6.x and 3.7.x.


## Version

0.1.0

## Authors

* **Michel Llorens** - [Michotastico](https://github.com/Michotastico)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details
