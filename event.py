class Event(object):
    def __init__(self, type, channelID, user, message):
        self.type = type
        self.channelID = channelID
        self.user = user
        self.text = message

    def getType(self):
        return type

    def getChannelID(self):
        return self.channelID

    def getUser(self):
        return self.user

    def getText(self):
        return self.text

    def setText(self, str):
        self.text = str
