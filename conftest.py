from pytest import fixture
from server_configs.setup import running_loop
from pytest_postgresql import factories
from server_configs.setup import DB_PORT, DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DATABASE_URI
from yoyo import read_migrations
from yoyo import get_backend


postgresql_executor = factories.postgresql_noproc(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD)
postgresql_conn = factories.postgresql('postgresql_executor', db_name=DB_NAME)


@fixture(scope='session', autouse=True)
def event_loop():
    return running_loop


@fixture(autouse=True)
def postgresql_instance(postgresql_conn):
    backend = get_backend(DATABASE_URI)
    migrations = read_migrations('./migrations')
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))


