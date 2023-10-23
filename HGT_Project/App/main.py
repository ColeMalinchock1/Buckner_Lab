import kivy

from kivy.app import App
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.clock import Clock 
from kivy.logger import Logger

import psycopg2
import os

Logger.info("Starting YourApp")

Builder.load_file('plotter.kv')

class MyLayout(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.graph = self.ids.graph
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])
        self.graph.add_plot(self.plot)
        Clock.schedule_interval(self.update_label, 1)

    def update(self):
        return

    def update_label(self , ran):
        conn = psycopg2.connect(
            host = "ec2-52-45-200-167.compute-1.amazonaws.com",
            database = "db21rgicqdggjt",
            user = "vipvuskuzhbrsx",
            password = "cadc830239a433cc331b0665422d99b755647c8510cfcb5d6b3c9e07883e1f66",
            port = "5432",
            sslmode = "require",
        )

        c = conn.cursor()

        c.execute("SELECT * FROM tensions")
        self.records = c.fetchall()


        y_value = max(self.records , key=lambda item: item[1])[0]

        x_value = len(self.plot.points) + 1

        self.plot.points.append((x_value , y_value))
        self.ids.display.text = ("Measured Tension: %.2f lb." % abs(y_value))

        conn.commit()

        conn.close()

class GraphApp(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    GraphApp().run()
