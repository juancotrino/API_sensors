from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists
from sqlalchemy_utils import create_database


# Creates connection to database
def get_engine(user, password, host, port, db):
    url = f'postgresql://{user}:{password}@{host}:{port}/{db}'

    # Creates database if it does not exist
    if not database_exists(url):
        create_database(url)
        print("Database created successfully........")

    return create_engine(url)


# Creates authentication for connection
def get_engine_from_settings(settings):
    keys = ['pguser', 'pgpass', 'pghost', 'pgport', 'pgdb']

    # Checks that the setting information is complete
    if not all(key in keys for key in settings.keys()):
        raise Exception('Bad settings file. Check local_settings.py')

    return get_engine(settings['pguser'],
                      settings['pgpass'],
                      settings['pghost'],
                      settings['pgport'],
                      settings['pgdb'])


from database import SessionLocal


# Work with the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
