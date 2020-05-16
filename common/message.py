import json

class Message(object):
    def __init__(self, code, payload):
        """
        Creates a Message object
        args: self, code, payload
        ret: none
        """

        self.code = code
        self.payload = payload

    def serialize(self):
        """
        Serializes a message
        args: self
        ret: serialized
        """

        return json.dumps({
            'code': self.code,
            'payload': self.payload
        })

    @classmethod
    def deserialize(cls, data):
        """
        Deserializes a message and creates a Message object
        args: cls, data
        ret: message
        """

        message = json.loads(data)

        if 'code' not in message or 'payload' not in message:
            raise Exception('Invalid message')

        return cls(message['code'], message['payload'])

    def __str__(self):
        """
        Returns a string representation of a message
        args: self
        ret: str_message
        """

        return 'code = ' + str(self.code) + ', payload = ' + json.dumps(self.payload)