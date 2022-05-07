from opcua import Server
import random
import datetime
import time
from config import *


class Miniplant:
    def __init__(self, bench_temp, bench_press):
        self.url = 'opc.tcp://192.168.178.34:4080'
        self.name = 'Miniplant'
        self.myserver = Server()
        self.myserver.set_endpoint(self.url)
        self.addspace = self.myserver.register_namespace(self.name)

        self.bench_temp = bench_temp
        self.bench_press = bench_press

        self.node = self.myserver.get_objects_node()
        self.param1 = self.node.add_object(self.addspace, 'Parameters1')
        self.temp1 = self.param1.add_variable(self.addspace, 'Temperature1', 0.0)
        self.press1 = self.param1.add_variable(self.addspace, 'Pressure1', 0.0)
        self.time1 = self.param1.add_variable(self.addspace, 'Time1', 0)

        self.param2 = self.node.add_object(self.addspace, 'Parameters2')
        self.temp2 = self.param2.add_variable(self.addspace, 'Temperature2', 0.0)
        self.press2 = self.param2.add_variable(self.addspace, 'Pressure2', 0.0)
        self.time2 = self.param2.add_variable(self.addspace, 'Time2', 0)

        self.temp1.set_writable()
        self.press1.set_writable()
        self.time1.set_writable()
        self.temp2.set_writable()
        self.press2.set_writable()
        self.time2.set_writable()

        print('Miniplantsimulation gestartet')

        self.myserver.start()

        while True:

            self.temperature1 = self.bench_temp + random.uniform(-10, 10)
            self.pressure1 = self.bench_press + random.uniform(-5, 5)
            self.time_stamp1 = datetime.datetime.now()

            self.temp1.set_value(self.temperature1)
            self.press1.set_value(self.pressure1)
            self.time1.set_value(self.time_stamp1)

            print(self.temperature1, self.pressure1, self.time_stamp1)

            self.temperature2 = self.bench_temp + random.uniform(-10, 10)
            self.pressure2 = self.bench_press + random.uniform(-5, 5)
            self.time_stamp2 = datetime.datetime.now()

            self.temp2.set_value(self.temperature2)
            self.press2.set_value(self.pressure2)
            self.time2.set_value(self.time_stamp2)

            print(self.temperature2, self.pressure2, self.time_stamp2)

            time.sleep(1)


Miniplant(bench_temp, bench_press)

