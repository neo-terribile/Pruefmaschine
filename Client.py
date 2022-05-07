from opcua import Client
import sqlite3
import time
import random
from config import *


class Measurement:
    def __init__(self):
        self.url = 'opc.tcp://192.168.178.34:4080'
        self.name = 'Messung'
        self.client = Client(self.url)
        self.client.connect()

    def get_measurements(self):
        self.temp1 = self.client.get_node('ns=2;i=2')
        self.temperature1 = self.temp1.get_value()

        self.press1 = self.client.get_node('ns=2;i=3')
        self.pressure1 = self.press1.get_value()

        self.time1 = self.client.get_node('ns=2;i=4')
        self.time_value1 = self.time1.get_value()

        self.temp2 = self.client.get_node('ns=2;i=6')
        self.temperature2 = self.temp2.get_value()

        self.press2 = self.client.get_node('ns=2;i=7')
        self.pressure2 = self.press2.get_value()

        self.time2 = self.client.get_node('ns=2;i=8')
        self.time_value2 = self.time2.get_value()

        print('data loaded from server')

    def print_measurements(self):
        if self.temperature1 < bench_temp - random.uniform(-5, 0):
            print(self.temperature1, ' WARNING:Temperature1 critical low!')
        elif self.temperature1 > bench_temp - random.uniform(0, 5):
            print(self.temperature1, ' WARNING:Temperature1 critical high!')
        else:
            print(self.temperature1, 'Temperature1 normal')

        if self.pressure1 < bench_press - random.uniform(-2.5, 0):
            print(self.pressure1, ' WARNING:Pressure1 critical low!')
        elif self.pressure1 > bench_press + random.uniform(0, 2.5):
            print(self.pressure1, ' WARNING:Pressure1 critical high!')
        else:
            print(self.pressure1, ' Pressure1 normal')

        print(self.time_value1)

        if self.temperature2 < bench_temp - random.uniform(-5, 0):
            print(self.temperature2, ' WARNING:Temperature2 critical low!')
        elif self.temperature2 > bench_temp - random.uniform(0, 5):
            print(self.temperature2, ' WARNING:Temperature2 critical high!')
        else:
            print(self.temperature2, ' Temperature2 normal')

        if self.pressure2 < bench_press - random.uniform(-2.5, 0):
            print(self.pressure2, ' WARNING:Pressure2 critical low!')
        elif self.pressure2 > bench_press + random.uniform(0, 2.5):
            print(self.pressure2, ' WARNING:Pressure2 critical high!')
        else:
            print(self.pressure2, ' Pressure2 normal')

        print(self.time_value2)

    def save_measurements(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS temp_press_plot1 ('
                  'Temperature1 DOUBLE, Pressure1 DOUBLE, Time1 DATETIME)')
        conn.commit()
        c.execute('INSERT INTO temp_press_plot1('
                  'Temperature1, Pressure1, Time1) VALUES ('
                  '?, ?, ?)',
                  (self.temperature1, self.pressure1, self.time_value1))
        conn.commit()

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS temp_press_plot2 ('
                  'Temperature2 DOUBLE, Pressure2 DOUBLE, Time2 DATETIME)')
        conn.commit()
        c.execute('INSERT INTO temp_press_plot2('
                  'Temperature2, Pressure2, Time2) VALUES (?, ?, ?)',
                  (self.temperature2, self.pressure2, self.time_value2))
        conn.commit()

        print('data saved to sql')


m = Measurement()

while True:
    m.get_measurements()
    m.print_measurements()
    m.save_measurements()

    time.sleep(2)
