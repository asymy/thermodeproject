
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from psychopy import visual, core, monitors, event
import numpy as np
import webbrowser
import datetime

import config
from generalfunc import general
from EEGControl import EEGControl


gen = general()


class MyPresentation():

    def __init__(self, dataClass):
        # GRAPH
        self._dataClass = dataClass
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.set_window_title('Thermode Heat Pain EEG')
        plt.subplots_adjust(bottom=0.2)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        self.hLine, = plt.plot(0, 0, 'g')
        self.ax.axes.grid()
        self.fig.set_size_inches(17, 10)
        self.ani = FuncAnimation(self.fig, self.run, interval=10, repeat=True)
        self.ax.axes.set_ylim(19, 51)
        self.ax.axes.set_ylabel('Temperature (°C)', fontsize=16)
        self.ax.axes.set_xlabel('Time (s)', fontsize=16)
        self.hLine.set_color('b')

        # Buttons

        def createButton(pos, text, function):
            axB = plt.axes(pos)
            button = Button(axB, text)
            button.label.set_fontsize(14)
            button.on_clicked(function)
            return button

        delta = 0.10
        a, b, c, d = 0.86, 0.05, 0.09, 0.06
        self.bCancel = createButton([a, b, c, d], 'Cancel', self.MyCancel)
        a = a-delta
        self.bEEGRand2 = createButton(
            [a, b, c, d], 'EEG Rand 2', self.MyEEGRand2)
        a = a-delta
        self.bEEGRand1 = createButton(
            [a, b, c, d], 'EEG Rand 1', self.MyEEGRand1)
        a = a-delta
        self.bEEGAscend = createButton(
            [a, b, c, d], 'EEG Ascending', self.MyEEGAscend)
        a = a-delta
        self.bCali = createButton([a, b, c, d], 'Calibration', self.MyCali)
        a = a-delta
        self.bPreHeat = createButton([a, b, c, d], 'Pre Heat', self.MyPreHeat)
        a = a-delta
        self.bPreCap = createButton([a, b, c, d], 'Pre Cap', self.MyPreCap)
        a = a-delta
        self.bTraining = createButton(
            [a, b, c, d], 'Training', self.MyTraining)
        a = a-delta
        self.bPrac = createButton([a, b, c, d], 'Practice', self.MyPractice)
        b = 0.91
        self.bHelp = createButton([0.07, b, c, d], 'About', self.AboutMe)
        self.bQuit = createButton([0.85, b, c, d], 'Quit', self.MyQuit)

        # PSYCHOPY
        self.mon = monitors.Monitor(name='Lonovo')
        self.win = visual.Window(fullscr=True,
                                 size=self.mon.getSizePix(),
                                 screen=1,
                                 monitor=self.mon)
        self.mes = visual.TextStim(self.win, text='')
        self.mes.height = .05
        self.mes.setAutoDraw(True)  # automatically draw every frame
        self.win.flip()
        self.text = ''
        self.fixation = visual.ShapeStim(self.win,
                                         units='cm',
                                         vertices=((0, -.25),
                                                   (0,  .25),
                                                   (0,    0),
                                                   (-.25,    0),
                                                   (.25,    0)),
                                         lineWidth=2,
                                         closeShape=False,
                                         lineColor="white")
        self.myRatingScale = visual.RatingScale(
            self.win, low=0, high=20,
            marker='triangle', stretch=1.5,
            tickHeight=1.2, precision=1,
            tickMarks=(0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20),
            labels=['0', '1', '2', '3', '4',
                    '5', '6', '7', '8', '9', '10'],
            scale=('0 = No Pain, 10 = Worst Pain Imaginable'),
            acceptText='Accept',
            maxTime=20, showValue=False)
        self.Question = visual.TextStim(
            self.win,
            units='norm',
            pos=[0, 0.4],
            text=('What was the maximum pain '
                  'intensity during the last period?'))
        PRpicture = 'PainScale2.png'
        self.ScalePic = visual.ImageStim(self.win, image=PRpicture,
                                         units='cm', pos=[0, 0])

    def run(self, i):
        # GRAPH
        self.hLine.set_data(self._dataClass.XData, self._dataClass.YData)
        self.hLine.axes.set_xlim(
            np.max(self._dataClass.XData)-60, np.max(self._dataClass.XData))
        self.ax.legend([str(config.currentTemp)], loc='upper left',
                       fontsize=18)

        # PSYCHOPY
        if self.text == '+':
            self.mes.setText('')
            self.fixation.draw()
        elif self.text == 'rt':
            if not config.cancelProg:
                self.mes.setText('')
                self.Question.draw()
                self.ScalePic.draw()
                if self.myRatingScale.noResponse:
                    self.myRatingScale.draw()
                else:
                    config.ratingCollected = True
                    config.currentRating = (self.myRatingScale.getRating())/2.
                    event.clearEvents()
                    self.myRatingScale.reset()
                    self.text = '+'
                    EEGControl.EEGTrigger(16)
            elif config.cancelProg:
                self.mes.setText('')
        else:
            self.mes.setText(self.text)
        self.win.flip()

    def MyQuit(self, event):
        config.cancelProg = True
        self.MyExit()

    def MyExit(self):
        name = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        fileName = (name + '_Participant' + config.participantID + '.json')
        data = {
            'time': self._dataClass.XData,
            'temp': self._dataClass.YData
        }
        gen.json_write(config.folders['log'], data, fileName)
        prog.stop()
        prog.join()
        fetcher.ser.close()
        fetcher.stop()
        fetcher.join()
        print('Quit Button Pressed')

        core.quit()

        config.buttonState = {
            'PracticeRun': False,
            'CalibrationRun': False,
            'HPEEGRun': False,
            'HPEEGRand1Run': False,
            'HPEEGRand2Run': False,
            'PreCapRun': False,
            'TrainingRun': False,
            'PreHeatRun': False

        }

    def MyEEGRand1(self, event):
        self.bEEGRand1.color = (1, 0, 0, 0.9)
        self.bEEGRand1.hovercolor = (1, 0, 0, 0.6)
        config.buttonState['HPEEGRand1Run'] = True

    def MyEEGRand2(self, event):
        self.bEEGRand2.color = (1, 0, 0, 0.9)
        self.bEEGRand2.hovercolor = (1, 0, 0, 0.6)
        config.buttonState['HPEEGRand2Run'] = True

    def MyEEGAscend(self, event):
        self.bEEGAscend.color = (1, 0, 0, 0.9)
        self.bEEGAscend.hovercolor = (1, 0, 0, 0.6)
        config.buttonState['HPEEGRun'] = True

    def MyPractice(self, event):
        self.bPrac.color = (1, 0, 0, 0.9)
        self.bPrac.hovercolor = (1, 0, 0, 0.6)
        config.buttonState['PracticeRun'] = True

    def MyCali(self, event):
        self.bCali.color = (1, 0, 0, 0.9)
        self.bCali.hovercolor = (1, 0, 0, 0.6)
        config.buttonState['CalibrationRun'] = True

    def MyPreCap(self, event):
        self.bPreCap.color = (1, 0, 0, 0.9)
        self.bPreCap.hovercolor = (1, 0, 0, 0.6)
        config.buttonState['PreCapRun'] = True

    def MyPreHeat(self, event):
        self.bPreHeat.color = (1, 0, 0, 0.9)
        self.bPreHeat.hovercolor = (1, 0, 0, 0.6)
        config.buttonState['PreHeatRun'] = True

    def MyTraining(self, event):
        self.bTraining.color = (1, 0, 0, 0.9)
        self.bTraining.hovercolor = (1, 0, 0, 0.6)
        config.buttonState['TrainingRun'] = True

    def AboutMe(self, event):
        webbrowser.open("aboutme.txt")

    def MyCancel(self, event):
        config.cancelProg = True
