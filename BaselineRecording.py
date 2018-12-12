from psychopy import visual, core, monitors
from EEGControl import EEGControl
# import serial


class MyPresentation():

    def __init__(self):

        self.mon = monitors.Monitor(name='Lonovo')
        self.win = visual.Window(fullscr=True,
                                 size=self.mon.getSizePix(),
                                 screen=1,
                                 monitor=self.mon)
        self.mes = visual.TextStim(self.win, text='')
        self.prompt = visual.TextStim(
            self.win,
            units='norm',
            pos=[0, 0],
            text='')
        self.mes.height = .05
        self.mes.setAutoDraw(True)  # automatically draw every frame
        self.win.flip()
        v = .25
        vx = ((0, -v), (0, v), (0, 0), (-v, 0), (v, 0))
        self.fixation = visual.ShapeStim(self.win,
                                         units='cm',
                                         vertices=vx,
                                         lineWidth=2,
                                         closeShape=False,
                                         lineColor="white")

        self.win.flip()

    def run(self):
        prompts = ['Begining Baseline Recording.\n'
                   'Please relax and focus on fixation cross.',
                   'Please now close your eyes.']
        for prompt in prompts:
            self.prompt.setText(prompt)
            self.prompt.draw()
            self.win.flip()
            core.wait(10)
            EEGControl.EEGTrigger(start)
            self.fixation.draw()
            self.win.flip()
            core.wait(int(time))
            EEGControl.EEGTrigger(stop)
        print('Finished Baseline Recording')


pres = MyPresentation()
EEGControl = EEGControl()
start = 5
stop = 6

defaultTime = 30

inputTime = input('[Default = ' + str(defaultTime) +
                  's] Time to record for (in seconds): ')
if inputTime:
    time = inputTime
else:
    time = defaultTime

input('Press Enter to begin.')

pres.run()
core.quit()
