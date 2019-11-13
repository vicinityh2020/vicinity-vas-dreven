"""
Example Application

Usage:
    falcon-example [options]

Options:
    -h --help                   Show this screen.
"""
import aumbry
import argparse
from gunicorn.app.base import BaseApplication
from gunicorn.workers.sync import SyncWorker

from evcharger.app import DefaultService
from evcharger.config import AppConfig




class CustomWorker(SyncWorker):
    def handle_quit(self, sig, frame):
        self.app.application.stop(sig)
        super(CustomWorker, self).handle_quit(sig, frame)

    def run(self):
        self.app.application.start()
        super(CustomWorker, self).run()


class GunicornApp(BaseApplication):
    """ Custom Gunicorn application

    This allows for us to load gunicorn settings from an external source
    """

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(GunicornApp, self).__init__()

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key.lower(), value)

        self.cfg.set('worker_class', 'evcharger.__main__.CustomWorker')

    def load(self):
        return self.application


def main():
    """
    optional arguments:
        -h, --help  show this help message and exit
        -dev        Use development confifuration with in-memory db (DEFAULT)
        -qa         Use remote db with postgres configuration
    """

    conf_file = ''

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-dev',
        help='Use development confifuration with in-memory db (DEFAULT)',
        action='store_true')
    group.add_argument('-qa',
        help='Use remote db with postgres configuration',
        action='store_true')
    args = parser.parse_args()

    if args.qa:
        conf_file = './etc/evcharger/QA.yml'
    else:
        conf_file = './etc/evcharger/dev.yml'

    cfg = aumbry.load(
        aumbry.FILE,
        AppConfig,
        {
            'CONFIG_FILE_PATH': conf_file
        }
    )

    api_app = DefaultService(cfg)
    gunicorn_app = GunicornApp(api_app, cfg.gunicorn)
    gunicorn_app.run()

if __name__ == "__main__":
    main()