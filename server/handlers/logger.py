from common import Codes, Message
from ..models import Logs

class Logger(object):
    @staticmethod
    def log_activity(message):
        """
        Logs an activity message
        args: message
        ret: none
        """

        if type(message) == Message:
            if message.code == Codes.PING:
                return

            logged_message = Message(message.code, message.payload.copy())
            
            if 'content' in logged_message.payload:
                del logged_message.payload['content']
        else:
            logged_message = message

        print '[*]', logged_message
        Logs.create('activity', str(logged_message))

    @staticmethod
    def log_error(error):
        """
        Logs an error message
        args: message
        ret: none
        """

        print '[-]', error
        Logs.create('error', str(error))