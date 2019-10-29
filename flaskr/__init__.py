import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            DATABASE = os.path.join(app.instance_path,"flaskr.sqlite"),
            MAX_THREADS = 20,
            # 3 minutes of work time
            WORK_TIME = 180,
            # 10 minutes of wait time
            WAIT_TIME = 600,
            # 1 minute of error time
            ERR_TIME = 60
            )

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
