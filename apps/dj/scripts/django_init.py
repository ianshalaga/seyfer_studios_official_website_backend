import os
import sys
import django


class DjangoEnvironment():
    _initialized = False

    # def __init__(self):
    #     if not DjangoEnvironment._initialized:
    #         BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
    #         sys.path.append(base_dir)
    #         os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    #         django.setup()
    #         DjangoInitializer._initialized = True

    def __init__(self):
        # Add base folder to the sys.path
        BASE_DIR = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '../../../'))
        sys.path.append(BASE_DIR)
        # Set Django environment
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
        django.setup()  # Initialize Django


django_environment = DjangoEnvironment()
