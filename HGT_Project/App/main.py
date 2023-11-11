import kivy
from kivy.network.urlrequest import UrlRequest
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.widget import Widget

import json
import requests

Builder.load_file('plotter.kv')

class MyLayout(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.graph = self.ids.graph
        self.plot = MeshLinePlot(color=[1 , 0 , 0 , 1])
        self.graph.add_plot(self.plot)
        self.tensions = []
        self.times = []
        Clock.schedule_interval(self.retrieve_data , 1)

    def retrieve_data(self , ran):
        url = "https://github.com/ColeMalinchock1/HGT-JSON-Server/blob/main/HGT_Data.json"
        self.response = requests.get(url)
        data = json.loads(self.response.text)
        json_data = json.loads(data['payload']['blob']['rawLines'][0])['data']
        for i in range(len(json_data)):
            x_value = int(json_data[i]['time'])
            y_value = int(json_data[i]['tension'])
            self.plot.points.append((x_value , y_value))
        self.ids.display.text = ("Measured Tension: %.2f" % abs(y_value))

class GraphApp(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    GraphApp().run()
