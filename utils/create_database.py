from service_metadata import db_credentials, PORTRAITS_DB_NAME, UNIVERSITIES_DB_NAME
from cloudant import Cloudant


def connect(foo):
    def inner(*args, **kwargs):
        client = Cloudant(db_credentials['username'],
                          db_credentials['password'],
                          url=db_credentials['url'])
        client.connect()
        client.session()

        result = foo(client, *args, **kwargs)
        client.session_logout()
        client.disconnect()
        return result
    inner.__name__ = foo.__name__
    inner.__doc__ = foo.__doc__
    return inner


@connect
def create_db(client):
    print(client.all_dbs())
    client.create_database(UNIVERSITIES_DB_NAME)
    client.create_database(PORTRAITS_DB_NAME)


if __name__ == '__main__':
    # create_db()
    pass


