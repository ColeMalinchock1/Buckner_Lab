from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import requests
import json
from kivy.clock import Clock

class DataApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Data from Flask API:\n")
        self.layout.add_widget(self.label)
        Clock.schedule_interval(self.update_data, 10)  # Refresh data every 10 seconds
        return self.layout

    def update_data(self, *args):
        try:
            response = requests.get('http://127.0.0.1:80/get_data')
            if response.status_code == 200:
                data = response.json()
                self.label.text = "Data from Flask API:\n" + json.dumps(data, indent=4)
            else:
                self.label.text = "Failed to retrieve data"
        except requests.exceptions.RequestException:
            self.label.text = "Failed to connect to the API"

if __name__ == '__main__':
    DataApp().run()