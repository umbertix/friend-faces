from flask import Flask, request
import json

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def receive():
    data = json.loads(request.data)
    print "New commit by: {}".format(data)
    return "OK"


if __name__ == '__main__':
    app.run()
