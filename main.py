from server import Server
channelName = 'friend-faces-channel'
appKey = 'b13d772cddbd6c3212fe'
appSecret = '97f73f04e6d8fb7a5811'
appId = '485602'
cluster = 'eu'

class Main():
  def __init__(self):
    self.server = Server(appId, appKey, appSecret, channelName, cluster)
    self.assignGPIOs();
    self.bindGPIOs();
  }

  /**
   * Assigns and initializes all gpios inputs and outputs
   */
  assignGPIOs() {
    this.leds = new Gpio(17, 'out');
    this.button1 = new Gpio(4, 'in');
    this.button2 = new Gpio(5, 'in');
    this.button3 = new Gpio(6, 'in');
    this.button4 = new Gpio(7, 'in');
    this.button5 = new Gpio(8, 'in');
  }

  /**
   * Bind all the GPIOS to their own events
   */
  bindGPIOs(){
    const that = this;
    this.button1.watch(function(err, value) {
      that.sayHelloButton();
    });
  }

  sayHelloButton(){
    this.server.broadcastHello(channelName, 'Hello title', 'Hello message');
  }

}

