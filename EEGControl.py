from psychopy import parallel


class EEGControl():

    def EEGTrigger(self, input):
        port = parallel.ParallelPort()
        port.setData(input)
