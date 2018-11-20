from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
from time import sleep
import random
import threading

# flask config
app = Flask(__name__)

# websocket object
socket = SocketIO(app)

# test thread function
def generate_random_number():
    while True:
        random_float = round(random.uniform(0, 100), 2)
        socket.emit('new_signal', random_float)
        sleep(2.5)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', page='home')

if __name__ == "__main__":
    socket_test_thread = threading.Thread(target=generate_random_number)
    socket_test_thread.start()

    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=True)