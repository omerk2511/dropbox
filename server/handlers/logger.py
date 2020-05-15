from common import Codes, Message
from ..models import Logs

class Logger(object):
    @staticmethod
    def log_request(message):
        if message.code != Codes.PING:
            logged_message = Message(message.code, message.payload.copy())
            
            if 'content' in logged_message.payload:
                del logged_message.payload['content']

            print '[*]', logged_message
            Logs.create('request', str(logged_message))

    @staticmethod
    def log_error(error):
        print '[-]', error
        Logs.create('error', str(error))