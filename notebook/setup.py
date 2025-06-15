import os
import pathlib
import sys

NOTEBOOK_DIR_PATH = pathlib.Path(__file__).parent
REPO_DIR= NOTEBOOK_DIR_PATH.parent
DJANGO_PROJECT_ROOT = REPO_DIR / "src"
DJANGO_SETTINGS_MODULE  = "main.settings"

def init(verbose=False):
    try:
        import nest_asyncio 

        nest_asyncio.apply()
        if verbose:
            print("Applied nest_asyncio path to Jupyter compatibility")
    except ImportError:
        if verbose:
            print("nest_asyncio not available, Skipping patch")
    
    os.chdir(DJANGO_PROJECT_ROOT)
    sys.path.insert(0, str(DJANGO_PROJECT_ROOT))
    if verbose:
        print(f"Changed working directory to: {DJANGO_PROJECT_ROOT}")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    import django

    django.setup()
