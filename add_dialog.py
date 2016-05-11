from watson_developer_cloud import DialogV1
from service_metadata import dialog_credentials

if __name__ == '__main__':
    dialog = DialogV1(url=dialog_credentials['url'],
                      username=dialog_credentials['username'],
                      password=dialog_credentials['password'])
    dialog.delete_dialog('ba12d884-0f78-4b8a-a987-96aa419273ec')
    dialogs = dialog.get_dialogs()['dialogs']
    for d in dialogs:
        print(d, '\n')
    response = dialog.create_dialog(open('dialogs/dialogV2.xml', 'r'), 'dialogV2')
    print(response)
