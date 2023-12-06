
# import os
# os.environ["KIVY_NO_CONSOLELOG"] = "1"

import kivy

from kivy.network.urlrequest import UrlRequest
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner

import json
import requests

Builder.load_file('plotter.kv')

global url
global patient1
global patient2

patient1 = "Cole Malinchock"
patient2 = "John Bullock"


url = "https://github.com/ColeMalinchock1/HGT-JSON-Server/blob/main/HGT_Data.json"

class GetURL:
    def get_url(self):
        response = requests.get(url)
        data = json.loads(response.text)
        json_data = json.loads(data['payload']['blob']['rawLines'][0])['data'][0][patient1]
        return json_data
    
class DataStorage():
    def put(self , data):
        self.time_list = data
        print(f"From storage: {self.time_list}")
    
    def take(self):
        if self.time_list == None:
           self.time_list = []
        else:
            pass
        return self.time_list

class GraphCurrent(Screen , GetURL):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.graph = self.ids.graph
        self.plot = MeshLinePlot(color=[1 , 0 , 0 , 1])
        self.graph.add_plot(self.plot)
        self.tensions = []
        self.times = []
        self.start_time = self.get_url()[1]['patient data'][0]["time"]
        Clock.schedule_interval(self.retrieve_data , 60)

    def retrieve_data(self , ran):
        json_data = self.get_url()[1]['patient data']
        #start_time = int(json_data[0]['time'])
        for i in range(len(json_data)):
            x_value = int(json_data[i]['time'])
            y_value = int(json_data[i]['tension'])
            x_value = x_value - self.start_time
            if x_value in self.times:
                pass
            else:
                self.times.append(x_value)
                self.plot.points.append((x_value , y_value))
        self.ids.display.text = ("Measured Tension: %.2f" % abs(y_value))

class SelectTime(Screen , GetURL , DataStorage):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.read_dropdown , 2)

    def read_dropdown(self , ran):
        month = self.ids.month.text
        day = self.ids.day.text
        start_hour = self.ids.start_hour.text
        end_hour = self.ids.end_hour.text

        self.time_list = [month , day , start_hour , end_hour]
        App.get_running_app().shared_variable = self.time_list


class GraphRange(Screen , GetURL , DataStorage):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)

        self.graph = self.ids.graph
        self.plot = MeshLinePlot(color=[1 , 0 , 0 , 1])
        self.graph.add_plot(self.plot)
        self.tensions = []
        self.times = []
        Clock.schedule_interval(self.retrieve_data , 5)

    def retrieve_data(self , ran):
        time_list = App.get_running_app().shared_variable
        print(time_list)
        json_data = self.get_url()[1]['patient data']
        for i in range(len(json_data)):
            x_value = int(json_data[i]['time'])
            y_value = int(json_data[i]['tension'])
            if x_value in self.times:
                pass
            else:
                self.times.append(x_value)
                self.plot.points.append((x_value , y_value))

class Info(Screen , GetURL):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        json_data = self.get_url()[0]["info"][0]
        patient_name = json_data['name']
        age = json_data['age']
        guardian = json_data['guardian']
        number = json_data['phone number']
        self.ids.name.text = ("Name: %s    " % patient_name)
        self.ids.age.text = ("Age: %s    " % age)
        self.ids.guardian.text = ("Parent/Guardian(s):\n%s    " % guardian)
        self.ids.phone_number.text = ("Phone Number: %s    " % number)

class PatientSelect(Screen):

    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        response = requests.get(url)
        data = json.loads(response.text)
        json_data = json.loads(data['payload']['blob']['rawLines'][0])['data']

        name1 = json_data[0][patient1][0]['info'][0]['name']
        self.ids.patient1.text = name1
        name2 = json_data[1][patient2][0]['info'][0]['name']
        self.ids.patient2.text = name2

        

class MenuScreen(Screen):
    pass
    def __init__(self , **kwargs):
        super().__init__(**kwargs)

class GraphApp(App):
    def build(self):
        Window.clearcolor = (230/255 , 230/255 , 230/255 , 1)
        sm = ScreenManager()
        sm.add_widget(PatientSelect(name='patient_select'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GraphCurrent(name='graph_current'))
        sm.add_widget(SelectTime(name='select_time'))
        sm.add_widget(GraphRange(name='graph_range'))
        sm.add_widget(Info(name='info'))
        return sm

if __name__ == '__main__':
    GraphApp().run()