from os import getcwd, listdir
from os.path import join
from importlib import import_module
import shutil
from unittest import TestLoader, TextTestRunner

from coverage import Coverage
from pylint import epylint as lint

from mec_data.manage.app import create_app

from flask_migrate import Migrate, init as _init, migrate as _migrate, upgrade

from mec_data.model.databases import data_warehouse as db


def import_models():
    models_package = join(getcwd(), "mec_data", "model")
    files = listdir(models_package)
    module_names = [
        file[:-3] for file in files if file.endswith(".py") and file != "__init__.py"
    ]
    for module_name in module_names:
        import_module("mec_data.model.{}".format(module_name))


def init():
    application = create_app()
    Migrate(application, db)
    with application.app_context():
        try:
            _init()
            # Move files to ignore spatial_ref_sys from alembic
            alembic_static_path = join(getcwd(), "alembic_static")
            migrations_path = join(getcwd(), "migrations")

            ini_source = join(alembic_static_path, "alembic.ini")
            ini_destination = join(migrations_path, "alembic.ini")
            shutil.copyfile(ini_source, ini_destination)

            env_source = join(alembic_static_path, "env.py")
            env_destination = join(migrations_path, "env.py")
            shutil.copyfile(env_source, env_destination)
        except:
            """
            If db exists, than this will raise an error
            """


def migrate():
    application = create_app()
    import_models()
    Migrate(application, db)
    with application.app_context():
        _migrate()


def serve():
    """
    Launch web server with flask application
    """
    application = create_app()
    migrate = Migrate(application, db)
    # import all models for migration
    import_models()
    # apply migrations to db
    with application.app_context():
        upgrade()
    # run app
    application.run(
        host=application.config["MEC_DATA_NETWORK_HOST"],
        port=application.config["MEC_DATA_NETWORK_PORT"],
        debug=True,
        use_reloader=False,
    )


def lint_all():
    """
    Lint all app packages using Pylint
    """
    lint.py_run(join(getcwd(), "mec_data"))
    lint.py_run(join(getcwd(), "tests"))


def unittest():
    """
    Runs all unit tests using test discovery.
    """
    loader = TestLoader()
    suite = loader.discover(join(getcwd(), "tests"), pattern="*.py")

    runner = TextTestRunner(verbosity=2)
    runner.run(suite)


def test_all():
    """
    Runs all tests.
    """
    unittest()


def generate_coverage_report():
    """
    Runs all tests in a Code Coverage context and generates a report.
    """
    cov = Coverage()
    cov.start()

    from unittest import TestLoader, TextTestRunner

    test_all()

    cov.stop()
    cov.save()

    cov.html_report(directory="htmlcov")
