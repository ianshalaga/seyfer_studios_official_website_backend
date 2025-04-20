import os
import sys
import django
# from pathlib import Path


# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../'))

if BASE_DIR not in sys.path:
    # sys.path.insert(0, BASE_DIR)
    sys.path.append(BASE_DIR)


class DjangoInitializer:
    _instance = None  # Atributo de clase

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DjangoInitializer, cls).__new__(cls)
            cls._instance._setup_django()
        return cls._instance

    def _setup_django(self):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
        django.setup()
        print("✅ Entorno de Django inicializado.")


DjangoInitializer()
