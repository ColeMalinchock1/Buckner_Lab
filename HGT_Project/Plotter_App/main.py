import kivy
import socket

from kivy.app import App
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.clock import Clock 

Builder.load_file('plotter.kv')

class MyLayout(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Define the IP address and port to listen on (same as defined in the sender)
        receiver_ip = '192.168.117.95'  # Listen on all available interfaces
        receiver_port = 80

        # Create a socket object
        receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the specified address and port
        receiver_socket.bind((receiver_ip, receiver_port))

        # Listen for incoming connections (1 connection at a time)
        receiver_socket.listen(1)
        print("Receiver: Listening for connections...")

        # Accept incoming connections
        self.connection, sender_address = receiver_socket.accept()
        print(f"Receiver: Connection established with {sender_address}")
        self.graph = self.ids.graph
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])
        self.graph.add_plot(self.plot)
        Clock.schedule_interval(self.update_label, 1)

    def update(self):
        return

    def update_label(self , ran):
        data_bytes = self.connection.recv(1024)
        if not data_bytes:
            return

        # Convert received bytes to integer
        received_data = int(data_bytes.decode('utf-8'))

        # Do something with the received integer (e.g., print it)
        print(f"Received: {received_data}")
        x_value = len(self.plot.points) + 1
        y_value = received_data
        self.plot.points.append((x_value , y_value))
        # x_value = len(self.plot.points) + 1
        # y_value = 0.5 * (1 + (x_value / 100.0) ** 2)
        # self.plot.points.append((x_value, y_value))

class GraphApp(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    GraphApp().run()
