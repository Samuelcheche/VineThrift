"""
WSGI config for Vinethrift project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Vinethrift.settings')


def _env_true(name, default=False):
	value = os.getenv(name)
	if value is None:
		return default
	return value.strip().lower() in {"1", "true", "yes", "on"}


def _run_startup_migrations():
	# Render sets the RENDER environment variable for deployed services.
	auto_migrate = _env_true("AUTO_MIGRATE", bool(os.getenv("RENDER")))
	if not auto_migrate:
		return

	call_command("migrate", interactive=False, run_syncdb=True, verbosity=0)


_run_startup_migrations()

application = get_wsgi_application()
