import serial
import time
import sys

from generalfunc import general
import config
from stopThreadclass import StoppableThread


gen = general()


class MyDataFetchClass(StoppableThread):

    def __init__(self, dataClass):

        StoppableThread.__init__(self)
        self.ser = serial.Serial()
        self.ser.baudrate = 9600
        self.ser.port = 'COM4'
        self.ser.parity = 'N'
        self.ser.bytesize = 8
        self.ser.stopbits = 1
        self.ser.xonxoff = True
        self.ser.timeout = 5
        self.ser.open()

        for x in range(len(config.thermodeInfo)):
            if config.thermodeInfo[x]['name'] == config.selectedThermode:
                Thermode = config.thermodeInfo[x]

        offset0 = 'G' + gen.num2hex(float(Thermode['OffSetTemp_DA']))
        gain0 = 'H' + gen.num2hex(float(Thermode['ScaleFactorTemp_DA'])*10)
        offset1 = 'O' + gen.num2hex(float(Thermode['OffSetSlope_DA']))
        gain1 = 'N' + gen.num2hex(float(Thermode['ScaleFactorSlope_DA']))
        offsetC = 'K' + gen.num2hex(float(Thermode['OffSetTemp_AD']))
        gainC = 'L' + gen.num2hex(float(Thermode['ScaleFactorTemp_AD'])*10)
        s = self.ser.read(8).decode("utf-8")

        if s == 'INF01.03':
            gen.writeandcheck(self.ser, offset0)
            gen.writeandcheck(self.ser, offset1)
            gen.writeandcheck(self.ser, offsetC)
            gen.writeandcheck(self.ser, gain0)
            gen.writeandcheck(self.ser, gain1)
            gen.writeandcheck(self.ser, gainC)
            self._dataClass = dataClass
            self._period = 1/30
            self._nextCall = time.time()
        else:
            print('Thermode Not Sending Data')
            self.ser.close()
            sys.exit()

        config.startTime = time.time()
        self._dataClass.YData[0] = self.poll_temp()

    def poll_temp(self):
        self.ser.write(str.encode('M000'))
        red = self.ser.read(4).decode("utf-8")
        return int(red[1:], 16)/10

    def run(self):
        while not self.stopped():
            callTime = time.time()
            config.currentTemp = self.poll_temp()
            # add data to data class
            if config.changeProg:
                gen.set_temp(self.ser, config.targetTemp,
                             config.defaultVals['Slope'])
                config.changeProg = False
            self._dataClass.XData.append(time.time()-config.startTime)
            self._dataClass.YData.append(config.currentTemp)
            # sleep until next execution
            sleepTime = self._period-(callTime - time.time())
            time.sleep(sleepTime)
