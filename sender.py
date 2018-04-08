from pusher import Pusher


class Sender:
    """Pusher send side logic."""

    def __init__(self, app_id, key, secret, channel_name, cluster=None, encrypted=None):
        """Initializes the server object."""
        if cluster is None:
            cluster = 'mt1'

        if encrypted is None:
            encrypted = True

        self.pusher = Pusher(app_id, key, secret, cluster=cluster, ssl=encrypted)

        self.app_id = app_id
        self.key = key
        self.secret = secret
        self.channel_name = channel_name
        self.cluster = cluster
        self.encrypted = encrypted
        self.socket_id = u"1234.12"
        self.auth = self.join_channel()

    def join_channel(self):
        """ Authenticates for the channel and return auth"""
        return self.pusher.authenticate(
            self.channel_name,
            self.socket_id
        )

    def send_message(self, event, message, channel=None):
        """Send an event to the channel"""
        if channel is None:
            channel = self.channel_name
        self.pusher.trigger(channel, event, message)
