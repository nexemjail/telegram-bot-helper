from service_metadata import db_credentials, PORTRAITS_DB_NAME, UNIVERSITIES_DB_NAME
import cloudant
from cloudant.client import Cloudant
import numpy as np
from create_database import connect


def _fetch_data_from_db(client, db_name):
    db = client[db_name]
    data = [i for i in db]
    return data


@connect
def get_universities(client=None):
    """Function to get universities from db
    :return:dict with keys - map_id's and values - dicts with name and url of university
    """
    data = _fetch_data_from_db(client, UNIVERSITIES_DB_NAME)
    universities = {}
    for university in data:
        universities[university['map_id']] = {'name': university['name'],
                                              'url': university['url']}
    return universities


@connect
def get_portraits(client=None):
    data = _fetch_data_from_db(client, PORTRAITS_DB_NAME)
    portraits = []
    universities = []
    for portrait in data:
        portraits.append(np.array(portrait['features']))
        universities.append(portrait['university_map_id'])
    return portraits, np.array(universities)


if __name__ == '__main__':
    print(get_portraits())


