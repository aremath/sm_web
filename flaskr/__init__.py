import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = "dev"
    app.config.from_mapping(
            DATABASE = os.path.join(app.instance_path,"flaskr.sqlite"),
            # Path to door rando
            RANDO_PATH = "../../sm_rando/",
            # Path from door rando to instance
            REL_PATH = "../sm_flask/instance/",
            # Number of possible active generation threads
            MAX_THREADS = 10,
            # Number of possible folders (sleeping threads)
            MAX_FOLDERS = 40,
            # 3 minutes of work time
            WORK_TIME = 180,
            # 10 minutes of wait time
            WAIT_TIME = 600,
            # 1 minute of error time
            ERR_TIME = 60
            )
    # If this file exists, use it to override secret_key
    app.config.from_pyfile("app_config.py", silent=True)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    from . import views
    app.register_blueprint(views.main_bp)

    from . import database
    database.init_app(app)

    return app
