from psychopy import visual, core, monitors
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
        self.fixation = visual.ShapeStim(self.win,
                                         units='cm',
                                         vertices=((0, -.25),
                                                   (0, .25),
                                                   (0, 0),
                                                   (-.25, 0),
                                                   (.25, 0)),
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
            EEGTrigger(start)
            self.fixation.draw()
            self.win.flip()
            core.wait(int(time))


def EEGTrigger(input):
    print(input)


pres = MyPresentation()
start = 5

time = input('Time to record for (in seconds): ')
input('Press Enter to begin.')

pres.run()
core.quit()
