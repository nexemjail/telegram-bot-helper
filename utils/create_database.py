from service_metadata import db_credentials
from cloudant import Cloudant


def connect(foo):
    def inner(*args, **kwargs):
        client = Cloudant(db_credentials['username'],
                          db_credentials['password'],
                          url=db_credentials['url'])
        client.connect()
        client.session()
        kwargs['client'] = client

        result = foo(*args, **kwargs)
        client.session_logout()
        client.disconnect()
        return result

    return inner

@connect
def create_db(client = None):
    print(client.all_dbs())
    client.create_database('universities_db')
    client.create_database('portraits_db')

@connect
def select_university_and_features(client = None):


    universities_db = client['universities_db']
    portraits_db = client['portraits_db']

    universities = {}
    for u in universities_db:
        universities['name'] = u['name']
        universities['url'] = u['url']
        universities['map_id'] = u['map_id']


    portraits = []
    map_ids = []
    for doc in portraits_db:
        portraits.append(doc['features'])
        map_ids.append(doc['university_map_id'])

    return portraits, map_ids, universities

if __name__ == '__main__':
    # create_db()
    select_university_and_features()

