from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
from time import sleep
import random
import threading
import json
import plotly

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

        graphs = [
                dict(
                        data=[
                        dict(
                                x=[60, 70, 65],
                                y=[60, 120, 180],
                                type='scatter'
                        ),
                        ],
                        layout=dict(
                        title='Sample Temperature Graph'
                        )
                ),

                dict(
                        data=[
                        dict(
                                x=[0.1, 0.3, 0.5],
                                y=[60, 120, 180],
                                type='bar'
                        ),
                        ],
                        layout=dict(
                        title='Sample Height Graph graph'
                        )
                )
        ]

        # Add "ids" to each of the graphs to pass up to the client
        # for templating
        ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

        # Convert the figures to JSON
        # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
        # objects to their JSON equivalents
        graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('home.html', page='home', cls=plotly.utils.PlotlyJSONEncoder, ids=ids, graphJSON=graphJSON)

if __name__ == "__main__":
    socket_test_thread = threading.Thread(target=generate_random_number)
    socket_test_thread.start()

    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=True)