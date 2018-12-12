from threading import Thread, Event


class StoppableThread(Thread):

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stopper = Event()

    def stop(self):
        self._stopper.set()

    def stopped(self):
        return self._stopper.is_set()
