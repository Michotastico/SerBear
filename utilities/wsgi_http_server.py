import multiprocessing

from gunicorn.app.base import Application


class StandaloneApplication(Application):

    def init(self, parser, opts, args):
        pass

    def __init__(self, application, options=None):
        self.options = options or {}
        self.application = application
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

    @classmethod
    def default_number_of_workers(cls):
        cores = multiprocessing.cpu_count()
        return (cores * 2) + 1
