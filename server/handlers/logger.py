from common import Codes, Message

class Logger(object):
    @staticmethod
    def log(message):
        if message.code != Codes.PING:
            logged_message = Message(message.code, message.payload.copy())
            
            if 'content' in logged_message.payload:
                del logged_message.payload['content']

            print '[*]', logged_message