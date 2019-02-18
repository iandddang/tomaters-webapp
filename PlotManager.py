import random
import threading
from time import sleep

class PlotManager:
    def __init__(self, socket):
        self.graphs = [
            dict(
                    data=[
                        dict(
                                x=[1, 2, 3],
                                y=[3, 1, 2],
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
                            x=[1, 2, 3],
                            y=[5, 4, 2],
                            type='bar'
                    ),
                ],
                layout=dict(
                    title='Sample Height Graph graph'
                )
            )
        ]

        self.randomlyFillGraph_thread = threading.Thread(target=self.randomlyFillGraph)
        self.socket = socket


    def randomlyFillGraph(self):
        counter = 0
        while True:

            # randomly adding stuff
            for graph in self.graphs:
                
                x_array = graph['data'][0]['x']
                y_array = graph['data'][0]['y']


                x_array.append(x_array[-1] + 1)
                y_array.append(random.randint(1, 10))

                graph['data'][0]['x'] = x_array
                graph['data'][0]['y'] = y_array
                
                self.socket.emit('new_graph_signal', self.graphs)
            
            # limit to 3 data entries 
            if counter == 5:
                print('reset')
                counter = 0
                for graph in self.graphs:
                    graph['data'][0]['x'] = graph['data'][0]['x'][0:2]
                    graph['data'][0]['x'] = graph['data'][0]['x'][0:2]

            counter += 1
            sleep(15)