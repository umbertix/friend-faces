import Pusher from 'pusher-js';

/**
 *
 */
class Client {
  /**
   *
   * @param appKey
   * @param channelName
   * @param cluster
   */
  constructor(appKey, channelName, cluster = 'eu') {
    this.pusher = new Pusher(appKey, {
      cluster
    });
    this.channel = pusher.subscribe(channelName);

    this.channel.bind(channelName, this.channelEvent);
  }

  channelEvent(data){
    console.log('Message received:', data.message);
  }
}

export default Client;