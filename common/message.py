import json

class Message(object):
    def __init__(self, code, payload):
        self.code = code
        self.payload = payload

    @classmethod
    def deserialize(cls, data):
        message = json.loads(data)

        if 'code' no in message or 'payload' not in message:
            throw Exception('Invalid message')

        return cls(message['code'], message['payload'])

    def serialize(self):
        return json.dumps({
            'code': self.code,
            'payload': self.payload
        })