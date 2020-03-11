import os
from importlib import import_module


def import_service():
    models_package = os.path.join(os.getcwd(), 'mec_data', 'service')
    files = os.listdir(models_package)
    module_names = [
        file[:-3] for file in files if file.endswith('.py') and file != '__init__.py']
    for module_name in module_names:
        import_module('mec_data.service.{}'.format(module_name))


import_service()
