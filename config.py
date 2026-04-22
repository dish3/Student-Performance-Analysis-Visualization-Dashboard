"""
Application configuration.

Local development keeps using the same defaults as before, but production
deployments can override them with environment variables.
"""

import os


def _get_env(*names, default=None):
    """Return the first non-empty environment variable from names."""
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return default


DB_CONFIG = {
    "host": _get_env("DB_HOST", "MYSQL_HOST", default="localhost"),
    "port": int(_get_env("DB_PORT", "MYSQL_PORT", default="3306")),
    "user": _get_env("DB_USER", "MYSQL_USER", default="root"),
    "password": _get_env("DB_PASSWORD", "MYSQL_PASSWORD", default="root"),
    "database": _get_env(
        "DB_NAME",
        "MYSQL_DATABASE",
        "MYSQL_DB",
        default="student_assessment_system",
    ),
}


APP_SECRET_KEY = _get_env(
    "SECRET_KEY",
    "FLASK_SECRET_KEY",
    default="your-secret-key-change-this-in-production",
)
