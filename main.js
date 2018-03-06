'use strict';
import Client from 'client.js';
import Server from 'server.js';
import Gpio from 'onoff';

const channelName = 'friend-faces-channel';
const appKey = 'b13d772cddbd6c3212fe';
const appSecret = '97f73f04e6d8fb7a5811';
const appId = '485602';

class Main{
  constructor(){
    this.client = new Client(appKey, channelName , 'eu');
    this.server = new Server(appId, appKey, appSecret);
    this.assignGPIOs();
    this.bindGPIOs();
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

