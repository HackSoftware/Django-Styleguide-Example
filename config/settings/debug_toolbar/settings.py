from config.env import env

DEBUG_TOOLBAR_ENABLED = env.bool("DEBUG_TOOLBAR_ENABLED", default=True)
DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": "config.settings.debug_toolbar.setup.show_toolbar"}

# You can place additional settings below
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html
