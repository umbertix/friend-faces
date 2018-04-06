import pusherclient


class Receiver:
    """Pusher receiver, channel subscription, side logic"""

    def __init__(self, key, secret, channel_name, event_name, event_callback_function):
        self.channel_name = channel_name
        self.event_name = event_name
        self.event_callback_function = event_callback_function
        self.pusher = pusherclient.Pusher(key, secret)
        self.pusher.connection.bind('pusher:connection_established', self.connect_handler)
        self.pusher.connect()

    # We can't subscribe until we've connected, so we use a callback handler
    # to subscribe when able
    def connect_handler(self, data):
        channel = self.pusher.subscribe(self.channel_name)
        channel.bind(self.event_name, self.event_callback_function)
