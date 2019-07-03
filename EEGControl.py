from psychopy import parallel
<<<<<<< HEAD
from time import sleep
=======
>>>>>>> 825cad075484cb5a40c9a368a4f7f0d25f245b1a


class EEGControl():

    def EEGTrigger(self, input):
        port = parallel.ParallelPort()
        port.setData(input)
<<<<<<< HEAD
        sleep(0.01)
        port.setData(0)
=======
>>>>>>> 825cad075484cb5a40c9a368a4f7f0d25f245b1a
