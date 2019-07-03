
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


def write_to_axes(ax, txt, pos):
    return ax.text(pos[0], pos[1], txt,
                   horizontalalignment='left',
                   verticalalignment='center',
                   transform=ax.transAxes,
                   fontsize=18)


def create_info_box(ax, pos):
    boxInfo = dict(
        facecolor='snow',
        edgecolor='black',
        boxstyle='round,pad=0.3')
    return ax.text(pos[0], pos[1], '',
                   horizontalalignment='center',
                   verticalalignment='bottom',
                   transform=ax.transAxes,
                   fontsize=18,
                   bbox=boxInfo)


class MyPresentation():

    def __init__(self, dataClass):
        # GRAPH
        self._dataClass = dataClass
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(left=0.2, bottom=0.23)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.title('Temperature of Thermode', fontsize=20)
        self.fig.patch.set_facecolor('snow')
        self.fig.set_size_inches(20, 10)
        self.fig.canvas.set_window_title('Thermode Heat Pain EEG')
        self.hLine, = plt.plot(0, 0, 'g')
        self.hLine.set_color('b')
        self.ani = FuncAnimation(self.fig, self.run, interval=10, repeat=True)
        self.ax.axes.set_ylim(19, 51)
        self.ax.axes.set_ylabel('Temperature (°C)', fontsize=16)
        self.ax.axes.set_xlabel('Time (s)', fontsize=16)
        self.ax.axes.grid()

        # Buttons
        def createButton(pos, text, function):
            axB = plt.axes(pos)
            button = Button(axB, text)
            button.label.set_fontsize(14)
            button.on_clicked(function)
            button.color = config.buttonColour['preClick'][0]
            button.hovercolor = config.buttonColour['preClick'][1]
            return button

        delta = 0.08
        a, b, c, d = 0.02, 0.1, 0.1, 0.06
        config.buttonArray['Cancel'] = createButton(
            [a, b, c, d], 'Cancel', self.MyCancel)
        config.buttonArray['Cancel'].color = 'orangered'
        config.buttonArray['Cancel'].hovercolor = 'lightsalmon'
        b = b+delta+0.07
        config.buttonArray['EEGRand2'] = createButton(
            [a, b, c, d], 'EEG Rand 2', self.MyEEGRand2)
        b = b+delta
        config.buttonArray['EEGRand1'] = createButton(
            [a, b, c, d], 'EEG Rand 1', self.MyEEGRand1)
        b = b+delta
        config.buttonArray['EEGAscend'] = createButton(
            [a, b, c, d], 'EEG Ascending', self.MyEEGAscend)
        b = b+delta
        config.buttonArray['Calibration'] = createButton(
            [a, b, c, d], 'Calibration', self.MyCali)
        b = b+delta
        config.buttonArray['preHeat'] = createButton(
            [a, b, c, d], 'Pre Heat', self.MyPreHeat)
        b = b+delta
        config.buttonArray['PreCap'] = createButton(
            [a, b, c, d], 'Pre Cap', self.MyPreCap)
        b = b+delta
        config.buttonArray['Training'] = createButton(
            [a, b, c, d], 'Training', self.MyTraining)
        b = b+delta
        config.buttonArray['Practice'] = createButton(
            [a, b, c, d], 'Practice', self.MyPractice)
        a, b, c = 0.93, 0.91, 0.05
        config.buttonArray['Quit'] = createButton(
            [a, b, c, d], 'Quit', self.MyQuit)
        config.buttonArray['Quit'].color = 'orangered'
        config.buttonArray['Quit'].hovercolor = 'lightsalmon'
        a = a-0.06
        config.buttonArray['About'] = createButton(
            [a, b, c, d], 'About', self.AboutMe)
        config.buttonArray['About'].color = 'mediumturquoise'
        config.buttonArray['About'].hovercolor = 'paleturquoise'

        tax = plt.axes([0.2, 0.02, 0.7, 0.13], facecolor='floralwhite')
        tax.get_xaxis().set_visible(False)
        tax.get_yaxis().set_visible(False)

        x1, x2, x3 = 0.02, 0.43, 0.75
        y1, y2 = 0.73, 0.35
        txt = 'Programme Running:'
        write_to_axes(tax, txt, [x1, y1])

        txt = 'Current Temperature:'
        write_to_axes(tax, txt, [x1, y2])

        txt = 'Previous Temp:'
        write_to_axes(tax, txt, [x2, y1])

        txt = 'Pain Rating:'
        write_to_axes(tax, txt, [x2, y2])

        txt = 'Next Temp:'
        write_to_axes(tax, txt, [x3, y1])

        txt = 'Time to Next:'
        write_to_axes(tax, txt, [x3, y2])

        x1, x2, x3 = 0.31, 0.63, 0.93
        y1, y2 = 0.65, 0.25
        self.infoCurrentProgramme = create_info_box(tax, [x1, y1])
        self.infoCurrentProgramme.set_text('None')
        self.infoCurrentTemp = create_info_box(tax, [x1, y2])
        self.infoPreviousTemp = create_info_box(tax, [x2, y1])
        self.infoPainRating = create_info_box(tax, [x2, y2])
        self.infoNextTemp = create_info_box(tax, [x3, y1])
        self.infoTimeToNext = create_info_box(tax, [x3, y2])

        # PSYCHOPY
        self.mon = monitors.Monitor(name=config.monitor)
        self.win = visual.Window(fullscr=True,
                                 size=self.mon.getSizePix(),
                                 screen=1,
                                 monitor=self.mon)
        self.mes = visual.TextStim(self.win, text='')
<<<<<<< HEAD
        # self.mes.setSize(12)
=======
	# self.mes.setSize(12)
>>>>>>> 825cad075484cb5a40c9a368a4f7f0d25f245b1a
        self.mes.height = .05
        self.mes.setAutoDraw(True)  # automatically draw every frame
        self.win.flip()
        config.text = ''
        self.fixation = visual.ShapeStim(self.win,
<<<<<<< HEAD
                                         units='cm',
                                         vertices=((0, -.75),
                                                   (0,  .75),
                                                   (0,    0),
                                                   (-.75,    0),
                                                   (.75,    0)),
                                         lineWidth=4,
                                         closeShape=False,
                                         lineColor="white")
=======
                            units='cm',
                            vertices=((0, -.75),
                                    (0,  .75),
                                    (0,    0),
                                    (-.75,    0),
                                    (.75,    0)),
                            lineWidth=4,
                            closeShape=False,
                            lineColor="white")
>>>>>>> 825cad075484cb5a40c9a368a4f7f0d25f245b1a
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
        self.infoCurrentTemp.set_text(
            str(config.currentTemp) + '°C')
        changeDisp = False
        for x in config.buttonState:
            if config.buttonState[x]:
                changeDisp = True
        if changeDisp:
            self.infoCurrentProgramme.set_text(config.progStatus['name'])
            self.infoPreviousTemp.set_text(
                (str(config.progStatus['prevTemp']) + '°C'))
            self.infoPainRating.set_text(
                (str(config.currentRating) + ' /10'))
            self.infoNextTemp.set_text(
                (str(config.progStatus['nextTemp']) + '°C'))
            self.infoTimeToNext.set_text(
                (str(config.progStatus['timeLeft']) + 's'))

        else:
            self.infoCurrentProgramme.set_text('None')
            self.infoPreviousTemp.set_text('')
            self.infoPainRating.set_text('')
            self.infoNextTemp.set_text((''))
            self.infoTimeToNext.set_text((''))

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
<<<<<<< HEAD
        fileName = (name + '_Participant' + config.participantID)
=======
        fileName = (name + '_Participant' + config.participantID + '.json')
>>>>>>> 825cad075484cb5a40c9a368a4f7f0d25f245b1a
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
