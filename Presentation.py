
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from psychopy import visual, core, monitors, event
import numpy as np
import webbrowser
import datetime
import threading

import config
from generalfunc import general
from EEGControl import EEGControl

EEGControl = EEGControl()
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
        config.buttonArray['Cancel'] = createButton(
            [a, b, c, d], 'Cancel', self.MyCancel)
        a = a-delta
        config.buttonArray['EEGRand2'] = createButton(
            [a, b, c, d], 'EEG Rand 2', self.MyEEGRand2)
        a = a-delta
        config.buttonArray['EEGRand1'] = createButton(
            [a, b, c, d], 'EEG Rand 1', self.MyEEGRand1)
        a = a-delta
        config.buttonArray['EEGAscend'] = createButton(
            [a, b, c, d], 'EEG Ascending', self.MyEEGAscend)
        a = a-delta
        config.buttonArray['Calibration'] = createButton(
            [a, b, c, d], 'Calibration', self.MyCali)
        a = a-delta
        config.buttonArray['preHeat'] = createButton(
            [a, b, c, d], 'Pre Heat', self.MyPreHeat)
        a = a-delta
        config.buttonArray['PreCap'] = createButton(
            [a, b, c, d], 'Pre Cap', self.MyPreCap)
        a = a-delta
        config.buttonArray['Training'] = createButton(
            [a, b, c, d], 'Training', self.MyTraining)
        a = a-delta
        config.buttonArray['Practice'] = createButton(
            [a, b, c, d], 'Practice', self.MyPractice)
        b = 0.91
        config.buttonArray['About'] = createButton(
            [0.07, b, c, d], 'About', self.AboutMe)
        config.buttonArray['Quit'] = createButton(
            [0.85, b, c, d], 'Quit', self.MyQuit)

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
        config.text = ''
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
        # print(config.text)
        # GRAPH
        self.hLine.set_data(self._dataClass.XData, self._dataClass.YData)
        self.hLine.axes.set_xlim(
            np.max(self._dataClass.XData)-60, np.max(self._dataClass.XData))
        self.ax.legend([str(config.currentTemp)], loc='upper left',
                       fontsize=18)

        # PSYCHOPY
        if config.text == '+':
            self.mes.setText('')
            self.fixation.draw()
        elif config.text == 'rt':
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
                    config.text = '+'
                    EEGControl.EEGTrigger(16)
            elif config.cancelProg:
                self.mes.setText('')
        else:
            self.mes.setText(config.text)
        self.win.flip()

    def MyQuit(self, event):
        config.cancelProg = True
        name = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        fileName = (name + '_Participant' + config.participantID + '.json')
        data = {
            'time': self._dataClass.XData,
            'temp': self._dataClass.YData
        }
        gen.json_write(config.folders['log'], data, fileName)
        for thread in threading.enumerate():
            if thread.name is not 'MainThread':
                print(thread.name)
                thread.stop()
                thread.join()
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
        config.buttonArray['EEGRand1'].color = (
            config.buttonColour['postClick'][0])
        config.buttonArray['EEGRand1'].hovercolor = (
            config.buttonColour['postClick'][1])
        config.buttonState['HPEEGRand1Run'] = True

    def MyEEGRand2(self, event):
        config.buttonArray['EEGRand2'].color = (
            config.buttonColour['postClick'][0])
        config.buttonArray['EEGRand2'].hovercolor = (
            config.buttonColour['postClick'][1])
        config.buttonState['HPEEGRand2Run'] = True

    def MyEEGAscend(self, event):
        config.buttonArray['EEGAscend'].color = (
            config.buttonColour['postClick'][0])
        config.buttonArray['EEGAscend'].hovercolor = (
            config.buttonColour['postClick'][1])
        config.buttonState['HPEEGRun'] = True

    def MyPractice(self, event):
        config.buttonArray['Practice'].color = (
            config.buttonColour['postClick'][0])
        config.buttonArray['Practice'].hovercolor = (
            config.buttonColour['postClick'][1])
        config.buttonState['PracticeRun'] = True

    def MyCali(self, event):
        config.buttonArray['Calibration'].color = (
            config.buttonColour['postClick'][0])
        config.buttonArray['Calibration'].hovercolor = (
            config.buttonColour['postClick'][1])
        config.buttonState['CalibrationRun'] = True

    def MyPreCap(self, event):
        config.buttonArray['PreCap'].color = (
            config.buttonColour['postClick'][0])
        config.buttonArray['PreCap'].hovercolor = (
            config.buttonColour['postClick'][1])
        config.buttonState['PreCapRun'] = True

    def MyPreHeat(self, event):
        config.buttonArray['preHeat'].color = (
            config.buttonColour['postClick'][0])
        config.buttonArray['preHeat'].hovercolor = (
            config.buttonColour['postClick'][1])
        config.buttonState['PreHeatRun'] = True

    def MyTraining(self, event):
        config.buttonArray['Training'].color = (
            config.buttonColour['postClick'][0])
        config.buttonArray['Training'].hovercolor = (
            config.buttonColour['postClick'][1])
        config.buttonState['TrainingRun'] = True

    def AboutMe(self, event):
        webbrowser.open("aboutme.txt")

    def MyCancel(self, event):
        config.cancelProg = True
