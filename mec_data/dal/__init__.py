import os
from importlib import import_module


def import_dals():
    models_package = os.path.join(os.getcwd(), 'mec_data', 'dal')
    files = os.listdir(models_package)
    module_names = [
        file[:-3] for file in files if file.endswith('.py') and file != '__init__.py']
    for module_name in module_names:
        import_module('mec_data.dal.{}'.format(module_name))

import_dals()
