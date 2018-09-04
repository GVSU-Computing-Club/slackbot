from slackclient import SlackClient
from time import sleep
from pprint import pprint
import traceback
from sys import exit

from commands import demo
from event import Event

'''
2018 Computing Club Slack Bot

This is the base for the slack bot. Commands should be in the commands sub
folder and each command in the commands.txtdictionary file should point
to its correct file.

Tabs were used for indentation

@author: Eric Darr, Matthew Shan

'''


class Bot(object):


    #contructor, called when an instance is created
    def __init__(self):
        self.username = None
        self.userid = None
        self.teamid = None
        self.token = None
        self.slackclient = None


    #Gets a auth token form a given file name
    def getToken(self, filename):
        try:
            tokenFile = open('tokens/' + filename, 'r')
            token = tokenFile.read().rstrip()
            tokenFile.close()
        except IOError:
            print('Failed to retrieve token from ' + filename)
            exit(1)
        return token


    #Prints a given message to a channel
    def printMessage(self, text, channel):
        self.slackclient.api_call(
        'chat.postMessage',
        channel=channel,
        text=text
        )


    #Processes a give command by first opening the commands.txt file
    #and then attempting to execute the command fomr the file name
    def processCommand(self, command, data):
        with open('commands/commands.txt', 'r') as inf:
            commands = eval(inf.read())
        if command in commands:
            file = commands.get(command)
            method_command = getattr(file, command)
            try:
                self.printMessage(method_command(data), data.getChannelID())
            except:
                self.printMessage("There was an error running the command",
                                  data.getChannelID())
                traceback.print_stack()
        else:
            self.printMessage("Command not found...", data.getChannelID())


    #Creates a connection with Slack
    def connect(self):
        self.token = self.getToken('token.txt')
        self.slackclient = SlackClient(self.token)
        print('Attempting to connect...')
        if(self.slackclient.rtm_connect()):
            print('Connection successful!')
            return True
        else:
            print('Failed to connect')
            return False


    #Bot execution starts here
    def run(self):
        print("Preparing to connect....")
        if(self.connect()):
            #Retrieve ID
            print('Retrieving self ID...')
            data = self.slackclient.api_call('auth.test')
            self.userid = data['user_id']

            print('Bot running...')

            while True:
                event = self.slackclient.rtm_read()
                if(len(event) != 0):
                    pprint(event)
                    if(len(event) != 0):
                        try:
                            if event[0]['type'] == 'message':
                                data = Event(event[0]['type'],
                                          event[0]['channel'],
                                          event[0]['user'],
                                          event[0]['text'])
                                if data.text.startswith('!'):
                                    #Gets the command given
                                    command = data.text.split(' ')[0][1:]
                                    data.setText(data.getText()
                                                 .split(' ', 1)[1])
                                    self.processCommand(command, data)
                        except Exception:
                            print(traceback.format_exc())
                sleep(1)