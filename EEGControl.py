from psychopy import parallel
from time import sleep


class EEGControl():

    def EEGTrigger(self, input):
        port = parallel.ParallelPort()
        port.setData(input)
        sleep(0.01)
        port.setData(0)
