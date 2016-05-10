from __future__ import unicode_literals, print_function
from watson_developer_cloud import DialogV1, PersonalityInsightsV2
from service_metadata import dialog_credentials, dialog_id,\
    pi_credentials, CONTINUE_CONSTANT

dialog = None
personality_insights = None


def init_dialog():
    global dialog, personality_insights
    dialog = DialogV1(url=dialog_credentials['url'],
                      username=dialog_credentials['username'],
                      password=dialog_credentials['password'])

    personality_insights = PersonalityInsightsV2(
        url=pi_credentials['url'],
        username=pi_credentials['username'],
        password=pi_credentials['password'])

    print('Starting conversation with Dialog')
    response = dialog.conversation(dialog_id)
    print('Got a response from dialog! Sending it to client')
    return response


def send_message(client_id, conversation_id, message, dialog_id=dialog_id):
    if dialog and personality_insights:
        response = dialog.conversation(
            dialog_id,
            message, client_id,
            conversation_id)

        text = response['response']

        print('Checking for profile variables')
        variables = dialog.get_profile(
           dialog_id, client_id)
        print('Profile variables ' + str(variables))

        got_twitter = variables and variables['name_values'] \
                      and variables['name_values'][0] \
                      and variables['name_values'][0]['name'] \
                      and variables['name_values'][0]['name'] == 'TwitterAccount' \
                      and variables['name_values'][0]['value'] \
                      and variables['name_values'][0]['value'].startswith('@')

        if got_twitter:
            print('It\'s twitter!')
            obama_text = ''
            with open('texts/obama_text.txt', 'r') as f:
                obama_text = f.read()
            response = personality_insights.profile(obama_text)
            print('Got a response from PI')
            print('Updating profile variables')
            response_profile = dialog.update_profile(dialog_id,
                                                         {'UniversityName': 'Princeton',
                                                          'UniversityWebsite': 'http://www.princeton.edu/main/'},
                                                         'client_id')

            print('Sending continue constant to conversation')
            response = dialog.conversation(dialog_id,
                                               CONTINUE_CONSTANT, client_id,
                                               conversation_id)
            text = response['response']
        return text
    return {'error': 'dialog not initializes'}


