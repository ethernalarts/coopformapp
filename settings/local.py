from .base import *
import dj_database_url


DEBUG = env.bool("ANYTHING", default=False)

# postgres://postgresql_coopformapp_user:rHtx7dIKslePiALFGGAmgy4ZQsT7c5mH@dpg-cnc7aota73kc73ekj29g-a.oregon-postgres.render.com/postgresql_coopformapp

DATABASES = {
    'default': dj_database_url.parse(
        env('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    ),
}
