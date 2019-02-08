from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
from PlotManager import PlotManager
from PlantManager import PlantManager
from time import sleep
import random
import threading
import json
import plotly

# flask config
app = Flask(__name__)

# websocket object
socket = SocketIO(app)

# plot object
plot_manager = PlotManager(socket)
plant_manager = PlantManager()

# test thread function
def generate_random_number():
    while True:
        random_float = round(random.uniform(0, 100), 2)
        socket.emit('new_signal', random_float)
        sleep(2.5)

@app.route('/', methods=['GET'])
def home():

        graphs = plot_manager.graphs

        # Add "ids" to each of the graphs to pass up to the client
        # for templating
        ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

        # Convert the figures to JSON
        # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
        # objects to their JSON equivalents
        graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('home.html', page='home', cls=plotly.utils.PlotlyJSONEncoder, ids=ids, graphJSON=graphJSON, plant_manager=plant_manager)


@app.route('/lighttoggle', methods=['GET', 'POST'])
def toggle_light():
        if plant_manager.light_toggle:
                plant_manager.light_toggle = False
        else:
                plant_manager.light_toggle = True

        return 'a'


if __name__ == "__main__":
        socket_test_thread = threading.Thread(target=generate_random_number)
        socket_test_thread.start()
        plot_manager.randomlyFillGraph_thread.start()

        app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=True)