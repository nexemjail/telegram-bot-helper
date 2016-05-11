import watson_developer_cloud as wdc
import pandas
from StringIO import StringIO
import numpy as np
from service_metadata import pi_credentials as pi


def get_personality_vector(text):
    personality_insights = wdc.PersonalityInsightsV2(
        url=pi['url'],
        username=pi['username'],
        password=pi['password']
    )
    try:
        response = personality_insights.profile(text, accept='text/csv', csv_headers=True)
        text_data = StringIO(response)
        data = pandas.read_csv(text_data)

        required_columns = data.columns[2:np.argwhere(data.columns == 'Sunday')].values
        vectors = data[required_columns].values
        return vectors[0]
    except wdc.WatsonException:
        return None


if __name__ == '__main__':
    text = open('texts/obama_text.txt', 'r').read()
    print get_personality_vector(text)