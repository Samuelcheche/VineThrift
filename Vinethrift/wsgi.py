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
	# Fallback safety net: run migrations at boot when enabled.
	if not _env_true("AUTO_MIGRATE", True):
		return

	try:
		call_command("migrate", interactive=False, run_syncdb=True, verbosity=0)
	except Exception as exc:
		print(f"Startup migration skipped due to error: {exc}")


_run_startup_migrations()

application = get_wsgi_application()
