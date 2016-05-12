from service_metadata import db_credentials
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

    return inner

@connect
def create_db(client):
    print(client.all_dbs())
    client.create_database('universities_db')
    client.create_database('portraits_db')

@connect
def select_university_and_features(client):

    universities_db = client['universities_db']
    portraits_db = client['portraits_db']

    universities = []
    for doc in universities_db:
        universities.append(doc['name'], doc['map_id'])


    for doc in portraits_db:





    for u in universities_db:


    print(db)


if __name__ == '__main__':
    # create_db()
    select_university_and_features()

