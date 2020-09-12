"""
  GoogleCloudStorage extension classes for MEDIA and STATIC uploads
"""
import logging
import os
from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import setting
from urllib.parse import urljoin
from django_heroku import HerokuDiscoverRunner
import dj_database_url

logger = logging.getLogger(__name__)

MAX_CONN_AGE = 600


class GoogleCloudMediaFileStorage(GoogleCloudStorage):
    """
    Google file storage class which gives a media file
    path from MEDIA_URL not google generated one.
    """

    bucket_name = setting("GS_MEDIA_BUCKET_NAME")

    def url(self, name):
        """
        Gives correct MEDIA_URL and not google generated url.
        """
        return urljoin(settings.MEDIA_URL, name)


class GoogleCloudStaticFileStorage(GoogleCloudStorage):
    """
    Google file storage class which gives a media file
    path from MEDIA_URL not google generated one.
    """

    bucket_name = setting("GS_STATIC_BUCKET_NAME")

    def url(self, name):
        """
        Gives correct STATIC_URL and not google generated url.
        """
        return urljoin(settings.STATIC_URL, name)


class Heroku_googlecloud(HerokuDiscoverRunner):
    """
    passing the staticfiles steps of django_heroku for ggcloud
    """

    def settings(
        config,
        *,
        db_colors=False,
        databases=True,
        test_runner=True,
        staticfiles=True,
        allowed_hosts=True,
        logging=True,
        secret_key=True
    ):

        # Database configuration.
        # TODO: support other database (e.g. TEAL, AMBER, etc, automatically.)
        if databases:
            # Integrity check.
            if "DATABASES" not in config:
                config["DATABASES"] = {"default": None}

            if db_colors:
                # Support all Heroku databases.
                # TODO: This appears to break TestRunner.
                for (env, url) in os.environ.items():
                    if env.startswith("HEROKU_POSTGRESQL"):
                        db_color = env[len("HEROKU_POSTGRESQL_") :].split("_")[
                            0
                        ]
                        logger.info(
                            "Adding ${} to DATABASES Django setting ({}).".format(
                                env, db_color
                            )
                        )
                        config["DATABASES"][db_color] = dj_database_url.parse(
                            url, conn_max_age=MAX_CONN_AGE, ssl_require=True
                        )

            if "DATABASE_URL" in os.environ:
                logger.info(
                    "Adding $DATABASE_URL to default DATABASE Django setting."
                )

                # Configure Django for DATABASE_URL environment variable.
                config["DATABASES"]["default"] = dj_database_url.config(
                    conn_max_age=MAX_CONN_AGE, ssl_require=True
                )

                logger.info(
                    "Adding $DATABASE_URL to TEST default DATABASE Django setting."
                )

                # Enable test database if found in CI environment.
                if "CI" in os.environ:
                    config["DATABASES"]["default"]["TEST"] = config[
                        "DATABASES"
                    ]["default"]

            else:
                logger.info(
                    "$DATABASE_URL not found, falling back to previous settings!"
                )

        if test_runner:
            # Enable test runner if found in CI environment.
            if "CI" in os.environ:
                config["TEST_RUNNER"] = "django_heroku.HerokuDiscoverRunner"

        # Staticfiles configuration.
        if staticfiles:
            # Insert Whitenoise Middleware.
            try:
                config["MIDDLEWARE_CLASSES"] = tuple(
                    ["whitenoise.middleware.WhiteNoiseMiddleware"]
                    + list(config["MIDDLEWARE_CLASSES"])
                )
            except KeyError:
                config["MIDDLEWARE"] = tuple(
                    ["whitenoise.middleware.WhiteNoiseMiddleware"]
                    + list(config["MIDDLEWARE"])
                )

        if allowed_hosts:
            logger.info(
                "Applying Heroku ALLOWED_HOSTS configuration to Django settings."
            )
            config["ALLOWED_HOSTS"] = ["*"]

        if logging:
            logger.info(
                "Applying Heroku logging configuration to Django settings."
            )

            config["LOGGING"] = {
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "verbose": {
                        "format": (
                            "%(asctime)s [%(process)d] [%(levelname)s] "
                            + "pathname=%(pathname)s lineno=%(lineno)s "
                            + "funcname=%(funcName)s %(message)s"
                        ),
                        "datefmt": "%Y-%m-%d %H:%M:%S",
                    },
                    "simple": {"format": "%(levelname)s %(message)s"},
                },
                "handlers": {
                    "null": {
                        "level": "DEBUG",
                        "class": "logging.NullHandler",
                    },
                    "console": {
                        "level": "DEBUG",
                        "class": "logging.StreamHandler",
                        "formatter": "verbose",
                    },
                },
                "loggers": {
                    "testlogger": {
                        "handlers": ["console"],
                        "level": "INFO",
                    }
                },
            }

        # SECRET_KEY configuration.
        if secret_key:
            if "SECRET_KEY" in os.environ:
                logger.info("Adding $SECRET_KEY to SECRET_KEY Django setting.")
                # Set the Django setting from the environment variable.
                config["SECRET_KEY"] = os.environ["SECRET_KEY"]
