# Standar Modules
import os
import sys
# Django
import django

this_file_path: str = __file__
this_file_folder: str = os.path.dirname(this_file_path)
move_up_folder: str = "../"
up_folder: str = os.path.join(this_file_folder, move_up_folder)
# Base Directory Absolute Path / Repository Folder
BASE_DIR: str = os.path.abspath(up_folder)

if BASE_DIR not in sys.path:  # Avoid repeating the path
    sys.path.append(BASE_DIR)  # or sys.path.insert(0, BASE_DIR)


class DjangoInitializer:
    '''
    Singleton class to initialize Django environment
    '''
    _instance: object | None = None  # Class attribute

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DjangoInitializer, cls).__new__(cls)
            cls._instance._setup_django()
        return cls._instance

    def _setup_django(self):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
        django.setup()
        print("✅ Django environment initialized.")


DjangoInitializer()  # Django environment initialization
