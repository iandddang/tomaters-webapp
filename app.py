from flask import Flask, request, jsonify, render_template, session
from flask_socketio import SocketIO
from PlotManager import PlotManager
from PlantManager import PlantManager
from time import sleep
import random
import threading
import json
import plotly
from datetime import datetime
from pytz import timezone

# flask config
app = Flask(__name__)
app.secret_key = "top secret key"

# websocket object
socket = SocketIO(app)

# memory management options
plot_manager = PlotManager(socket)
plant_manager = PlantManager()


# endpoint for home, only allows access when session is authenticated
@app.route('/', methods=['GET'])
def home():
        if session.get('logged_in'):
                graphs = plot_manager.graphs

                # Add "ids" to each of the graphs to pass up to the client
                # for templating
                ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

                # Convert the figures to JSON
                # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
                # objects to their JSON equivalents
                graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

                return render_template('home.html', page='home', cls=plotly.utils.PlotlyJSONEncoder, ids=ids, graphJSON=graphJSON, plant_manager=plant_manager)
        else:
                return render_template('login.html')


# endpoint for login, also has login page
@app.route('/login', methods=['POST'])
def login():
        try:
                status = "Login failed, incorrect authentication!"
                if request.json['password'] == 'EECS159A' and request.json['username'] == 'Tomater':
                        session['logged_in'] = True
                        status = "Login success!"
        except Exception as e:
                status = 'Error caught: ' + str(e)
        
        return status


# endpoint for light detection
@app.route('/lightdetected', methods=['POST'])
def light_detected():
        try:
                if request.json['password'] == 'EECS159A' and request.json['username'] == 'Tomater':
                        status = request.json['status'].upper()
                        time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        data = {
                                'status': status,
                                'timestamp': time_now        
                        }

                        plant_manager.light_status = status
                        plant_manager.light_status_timestamp = time_now

                        socket.emit('light_detected_signal', data)
                        ret_status = 'Success.'
                else:
                        ret_status = 'Credentials were invalid.'
        except Exception as e:
                ret_status = 'Error caught: ' + str(e)

        return ret_status


# endpoint to toggle light
@app.route('/lighttoggle', methods=['GET', 'POST'])
def toggle_light():
        if plant_manager.light_toggle:
                plant_manager.light_toggle = False
        else:
                plant_manager.light_toggle = True

        return 'a'


# endpoint to add data point to temperature plot
@app.route('/plot/temperature', methods=['GET', 'POST'])
def plot_temperature():
        try:
                if request.json['password'] == 'EECS159A' and request.json['username'] == 'Tomater':
                        temperature = request.json['temp']
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        now_pacific = timestamp.astimezone(timezone('US/Pacific')).strftime('%Y-%m-%d %H:%M:%S')
                        
                        plot_manager.append_temperature(temperature, now_pacific)
                        
                        socket.emit('new_temperature_signal', {
                                'charData': plot_manager.graphs[0]['data'],
                                'layout': plot_manager.graphs[0]['layout']
                        })

                        ret_status = 'Success. Temperature plotted.'
                else:
                        ret_status = 'Credentials were invalid.'
        except Exception as e:
                ret_status = 'Error caught: ' + str(e)

        return ret_status


if __name__ == "__main__":
        app.run(host='0.0.0.0', port=80, debug=True, use_reloader=True)