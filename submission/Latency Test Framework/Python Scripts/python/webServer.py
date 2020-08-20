# imports for rest-api for unity


from flask import Flask, request
app = Flask(__name__)





@app.route('/')
def index(): 
    return 'Server Works!'

@app.route('/setTimeStamp', methods=['GET', 'POST', 'PUT'])
def say_hello():
    return "Hello from Server!"


#serialConnector.connect(com_port, frame_rate, timeout)
