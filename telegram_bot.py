from __future__ import print_function
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from watson_developer_cloud import DialogV1, SpeechToTextV1
from watson_developer_cloud import PersonalityInsightsV2
from service_metadata import audio_content_type,\
    CONTINUE_CONSTANT, pi_credentials,dialog_credentials,\
    dialog_id, bot_token
from personality_extractor import get_personality_vector
from parse_twitter import get_all_tweets
from classifier import classify
__all__ = ['start', 'stop']


def _init_conversation(bot):
    print('begin it! Conversation not initialized')
    bot.watson_info = dict()
    bot.dialog = DialogV1(url=dialog_credentials['url'],
                          username=dialog_credentials['username'],
                          password=dialog_credentials['password'])
    bot.dialog_id = dialog_id

    print('Conversation initialized')

    # bot.speech_to_text = SpeechToTextV1(url=speech_to_text_credentials['url'],
    #                                     username=speech_to_text_credentials['username'],
    #                                     password=speech_to_text_credentials['password'])


def _start(bot, update):
    print('Start called!' + str(bot))
    print('Doing bot initialization')
    _init_conversation(bot)
    print('Init done!')

    print('Starting conversation with Dialog')
    response = bot.dialog.conversation(bot.dialog_id)
    print('Got a response from dialog! Sending it to client')

    bot.conversation_id = response['conversation_id']
    bot.client_id = response['client_id']
    for message in response['response']:
        bot.sendMessage(chat_id=update.message.chat_id,
                    text=message)
    print('Message sent!')


def _echo(bot, update):
    print('Got a message!')
    print("I't is a text one!")
    response = bot.dialog.conversation(
        bot.dialog_id,
        update.message.text, bot.client_id,
        bot.conversation_id)
    print(response)
    text = response['response']
    print('Got a response from Dialog')

    print('Checking for profile variables')
    variables = bot.dialog.get_profile(
        bot.dialog_id, bot.client_id)
    print('Profile variables ' + str(variables))

    got_twitter = variables and variables['name_values'] \
            and variables['name_values'][0] \
            and variables['name_values'][0]['name'] \
            and variables['name_values'][0]['name'] == 'TwitterAccount' \
            and variables['name_values'][0]['value'] \
            and variables['name_values'][0]['value'].startswith('@')

    if got_twitter:
        for message in text:
            bot.sendMessage(update.message.chat_id, text=str(message))

        print('It\'s twitter!')

        tweets = get_all_tweets(update.message.text[1:])
        if not tweets:
            text = ['Parsing error occured!']
        else:
            print(tweets[:2])
            joined_text = ''.join(tweets)
            print(joined_text)
            feature_vector = get_personality_vector(joined_text)
            print(feature_vector)
            if feature_vector is not None:
                print(type(feature_vector))
                print(feature_vector.shape)
                recommendation = classify(feature_vector)
                print(recommendation)

                if recommendation:
                    print(recommendation)
                    print('Updating profile variables')
                    response_profile = bot.dialog.update_profile(bot.dialog_id,
                                                                 {'UniversityName': recommendation['name'],
                                                                  'UniversityWebsite': recommendation['url']},
                                                                 bot.client_id)
                    print('Sending continue constant to conversation')
                    response = bot.dialog.conversation(bot.dialog_id,
                                                       CONTINUE_CONSTANT, bot.client_id,
                                                       bot.conversation_id)
                    text = response['response']
            else:
                text = ["Twitter don't pass minimum requirement of 100 words. Specify another account"]
    print('Sending a message')
    print(str(text))
    for message in text:
        bot.sendMessage(update.message.chat_id, text=str(message))

# else:
#     bot.sendMessage(update.message.chat_id, text="Don't know! Rly, help me and try again!")
    print('Message sent!')
    # else:
    #     bot.sendMessage(update.message.chat_id, text="Don't know you, m8!")


def init_bot():
    # logger = logging.getLogger()
    # logger.setLevel(logging.INFO)
    bot = telegram.Bot(token=bot_token)
    updater = Updater(token=bot_token)
    start_handler = CommandHandler('start', _start)
    updater.dispatcher.addHandler(start_handler)
    message_handler = MessageHandler([Filters.text], _echo)
    updater.dispatcher.addHandler(message_handler)

    print(updater.dispatcher.handlers)
    return updater, bot


def start_bot(updater):
    updater.start_polling()


def stop_bot(updater):
    updater.stop()


def clear_dispatchers(updater):
    pass


def start():
    print('Initing bot')
    updater, bot = init_bot()
    print('Bot inited')
    start_bot(updater)
    print('Bot started')
    return updater


def stop(updater):
    clear_dispatchers(updater)
    stop_bot(updater)
