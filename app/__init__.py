"""
TODO:
- deploy

Reminders:
    export FLASK_APP=app
    export FLASK_ENV=development
    flask run
"""
import os
import secrets

from threading import Thread
from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap

from .utils.file_removal import file_cleaning


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # Built-in
        SECRET_KEY=secrets.token_urlsafe(16),
        MAX_CONTENT_PATH=2000000,
        # Not built-in
        UPLOAD_FOLDER='/home/tom/Desktop/Github/PDF_Website/loads/uploads',
        DOWNLOAD_FOLDER='/home/tom/Desktop/Github/PDF_Website/loads/downloads',
        ALLOWED_EXTENSIONS={'pdf'},
        CLEANING_CYCLE_TIME=60,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Takes care of css
    bootstrap = Bootstrap(app)

    # Blueprint stuff
    from . import merging
    app.register_blueprint(merging.bp)

    @app.route('/')
    @app.route('/home')
    def home():
        app.logger.info('User accessing home page')
        return render_template('home.jinja2')

    # Start thread to remove files from loads periodically
    file_cleaning_thread = Thread(
        target=file_cleaning,
        args=(app.config['CLEANING_CYCLE_TIME'],
              app.config['UPLOAD_FOLDER'],
              app.config['DOWNLOAD_FOLDER']),
        daemon=True).start()

    return app
