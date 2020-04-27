import json

class Message(object):
    def __init__(self, code, payload):
        self.code = code
        self.payload = payload

    def serialize(self):
        return json.dumps({
            'code': self.code,
            'payload': self.payload
        })

    @classmethod
    def deserialize(cls, data):
        message = json.loads(data)

        if 'code' not in message or 'payload' not in message:
            raise Exception('Invalid message')

        return cls(message['code'], message['payload'])

    def __str__(self):
        return 'code = ' + str(self.code) + ', payload = ' + str(self.payload)