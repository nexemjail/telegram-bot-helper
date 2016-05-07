from __future__ import unicode_literals, print_function
import telegram
from telegram.ext import Updater
import logging
import os
import json

from watson_developer_cloud import DialogV1, SpeechToTextV1
from watson_developer_cloud import PersonalityInsightsV2
from service_metadata import audio_content_type,\
    CONTINUE_CONSTANT, pi_credentials,dialog_credentials,\
    dialog_id, bot_token


__all__ = ['start', 'stop']


def _init_conversation(bot):
    bot.watson_info = dict()
    bot.watson_info['dialog_id'] = dialog_id
    bot.personality_insights = PersonalityInsightsV2(
        url=pi_credentials['url'],
        username=pi_credentials['username'],
        password=pi_credentials['password'])

    bot.dialog = DialogV1(url=dialog_credentials['url'],
                          username=dialog_credentials['username'],
                          password=dialog_credentials['password'])

    # bot.speech_to_text = SpeechToTextV1(url=speech_to_text_credentials['url'],
    #                                     username=speech_to_text_credentials['username'],
    #                                     password=speech_to_text_credentials['password'])


def _start(bot, update):
    print('Start called!' + str(bot))
    print('Doing bot initialization')
    _init_conversation(bot)
    print('Init done!')

    print('Starting conversation with Dialog')
    response = bot.dialog.conversation(dialog_id)
    print('Got a response from dialog! Sending it to client')

    bot.watson_info['conversation_id'] = response['conversation_id']
    bot.watson_info['client_id'] = response['client_id']
    for line in response['response']:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=line)
    print('Message sent!')


def _echo(bot, update):
    print('Got a message!')
    if update.message.text:
        print("I't is a text one!")
        response = bot.dialog.conversation(
            bot.watson_info['dialog_id'],
            update.message.text, bot.watson_info['client_id'],
            bot.watson_info['conversation_id'])
        text = response['response']
        print('Got a response from Dialog')

        print('Checking for profile variables')
        variables = bot.dialog.get_profile(
            bot.watson_info['dialog_id'], bot.watson_info['client_id'])
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
            response = bot.personality_insights.profile(obama_text)
            print('Got a response from PI')
            print('Updating profile variables')
            response_profile = bot.dialog.update_profile(bot.watson_info['dialog_id'],
                                                         {'UniversityName': 'Princeton',
                                                          'UniversityWebsite': 'http://www.princeton.edu/main/'},
                                                         bot.watson_info['client_id'])

            print('Sending continue constant to conversation')
            response = bot.dialog.conversation(bot.watson_info['dialog_id'],
                                               CONTINUE_CONSTANT, bot.watson_info['client_id'],
                                               bot.watson_info['conversation_id'])
            text = response['response']

        print('Sening a message')
        for line in text:
            bot.sendMessage(update.message.chat_id, text=line)
    # else:
    #     bot.sendMessage(update.message.chat_id, text="Don't know! Rly, help me and try again!")
        print('Message sent!')


    def init_bot():
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        bot = telegram.Bot(token=bot_token)
        updater = Updater(token=bot_token)
        updater.dispatcher.addTelegramCommandHandler('start', _start)
        updater.dispatcher.addTelegramMessageHandler(_echo)
        return updater


    def start_bot(updater):
        updater.start_polling()


    def stop_bot(updater):
        updater.stop()


    def clear_dispatchers(updater):
        updater.dispatcher.removeHandler(_start)
        updater.dispatcher.removeHandler(_echo)


    def start():
        updater = init_bot()
        start_bot(updater)
        return updater

    def stop(updater):
        clear_dispatchers(updater)
        stop_bot(updater)
