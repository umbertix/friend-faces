from pusher import Pusher


class Server():
    """Server side logic."""

    def __init__(self, app_id, key, secret, channel_name, cluster=None, encrypted=None):
        """Initializes the server object."""
        if cluster is None:
            cluster = 'eu'
        if encrypted is None:
            encrypted = True

        self.pusher = Pusher(app_id, key, secret, cluster, encrypted)

        self.app_id = app_id
        self.key = key
        self.secret = secret
        self.channel_name = channel_name
        self.cluster = cluster
        self.encrypted = encrypted
        self.socket_id = None
        self.auth = self.join_channel()

    def join_channel(self):
        """ Authenticates for the channel and return auth"""
        return self.pusher.authenticate(
            self.channel_name,
            self.socket_id
        )

    def send_message(self, title, message, channel=None):
        """Send a message to the channel"""
        if channel is None:
            channel = self.channel_name
        self.pusher.trigger(channel, title, {message})
