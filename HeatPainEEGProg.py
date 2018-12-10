import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
import threading, time, serial, msvcrt, json, webbrowser, sys, vals,pickle
import numpy as np
from sklearn.linear_model import LinearRegression
from pathlib import Path
from psychopy import visual, core, monitors, event


class StoppableThread(threading.Thread):

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stopper = threading.Event()

    def stop(self):
        self._stopper.set()

    def stopped(self):
        return self._stopper.is_set()


class MyHeatPainProgramme(StoppableThread):

    def __init__(self):
        StoppableThread.__init__(self)

        startingData = gen.pkl_load('startingdata')
        self.baslineTemp = startingData['baselineTemperature']
        self.Slope = startingData['Slope']
        self.Rest = startingData['RestTime']
        self.Hold = startingData['HoldTime']
        self.tolerance = startingData['tolerance']

        self.cancel = False
        self.change = True
        self.targetTemp = self.baslineTemp
        self.collected = False
        self.EEG = False
        self.allRatings = []

    def run(self):
        while not self.stopped():
            if but.PracticeRun == True:
                self.Practice()
            elif but.TrainingRun == True:
                self.Training()
            elif but.CalibrationRun == True:
                self.Calibration()
            elif but.HPEEGRun == True:
                self.EEGAscend()
            elif but.HPEEGRand1Run == True:
                self.EEGRand(1)
            elif but.HPEEGRand2Run == True:
                self.EEGRand(2)
            elif but.PreCapRun == True:
                self.PreCapHP()
            elif but.PreHeatRun == True:
                self.PreHeat()
            else:
                time.sleep(0.1)

    def HeatPainRun(self, baselineTemp, noxioustemps, holdTimes):
        self.allRatings = np.zeros_like(noxioustemps)
        gen.wait(2)
        pres.text = '+'
        gen.wait(2)
        # Set temperature to baseline temp, check it has reached this, send EEG trigger, hold for rest period
        # set temperature to noxious temp, send EEG trigger, check it as reached temp, send another EEG trigger
        # wait for hold period, send another EEG trigger, set temp back to baseline, check it has reached, send another EEG trigger
        # loop back to begining, and do for all noxious temps
        self.setandcheck(baselineTemp)
        T = time.time()
        gen.EEGTrigger(11)
        gen.wait(5)
        print('\tNext Temperature = ' +
              str(noxioustemps[0]) + '°C, for ' + str(holdTimes[0]) + 's.')
        gen.timer(T, self.Rest)
        gen.EEGTrigger(12)
        for x in range(len(noxioustemps)):
            self.setandcheck(noxioustemps[x])
            T = time.time()
            gen.EEGTrigger(13)
            gen.timer(T, holdTimes[x])
            gen.EEGTrigger(14)
            self.setandcheck(baselineTemp)
            T = time.time()
            gen.EEGTrigger(11)
            gen.wait(5)
            gen.EEGTrigger(15)
            self.collected = False
            pres.text = 'rt'
            while self.collected == False and prog.cancel == False:
                gen.wait(0.05)
            gen.wait(.5)
            print('\tPain Rating to last Temperature = ' + str(currentRating))
            gen.wait(.5)
            if x < len(noxioustemps) - 1:
                print('\tNext Temperature = ' +
                      str(noxioustemps[x+1]) + '°C, for ' + str(holdTimes[x+1]) + 's.')
            gen.timer(T, self.Rest)
            if prog.cancel == False:
                self.allRatings[x] = currentRating
                gen.EEGTrigger(12)
            else:
                break
            if self.EEG == False:
                if currentRating > 8:
                    break
            elif self.EEG == True:
                if currentRating > 9:
                    break

    def Practice(self):
        print('Practice Run')
        messages = ("During the stimulation a fixation cross will appear on the screen.\nPlease relax, and focus on the cross when it is on the screen.\nAn example of the cross is on the next screen.",
                    "After the Heat Stimulus, a rating scale will appear on the screen.\nClick on the line with the mouse, and drag the marker to change your selection.\nClick on the button to confirm your answer.",
                    "You are now experiencing no pain, please use the scale to indicate this.",
                    "You are now experiencing mild pain, please use the scale to indicate this.",
                    "You are now experiencing extreme pain, please use the scale to indicate this.")
        stim = '+', 'rt', 'rt', 'rt', 'rt'
        for x in range(len(messages)):
            if prog.cancel == False:
                pres.text = messages[x]
                gen.wait(2)
                pres.text = stim[x]
                if x == 0:
                    gen.wait(2)
                else:
                    while not self.collected and prog.cancel == False:
                        gen.wait(0.05)
                    self.collected = False
                    print('pain rating: ' + str(currentRating))
                    gen.wait(2)
                
        pres.text = ''
        pres.bPrac.color = (0, 1, 0, 0.9)
        pres.bPrac.hovercolor = (0, 1, 0, 0.6)
        self.SetButtonFalse()

    def Training(self):
        print('\n\nTraining')
        trainingData = gen.pkl_load('trainingdata')
        startingTemperature = trainingData['startingTemperature']
        noxioustemps = trainingData['NoxiousTemps']
        holdTime = trainingData['HoldTime']

        holdTimes = np.ones_like(noxioustemps)*holdTime
        pres.text = "Starting Training Session"
        self.HeatPainRun(startingTemperature, noxioustemps, holdTimes)
        pres.bTraining.color = (0, 1, 0, 0.9)
        pres.bTraining.hovercolor = (0, 1, 0, 0.6)
        self.SetButtonFalse()

    def PreCapHP(self):
        print('\n\nPreCapHP')
        preCapData = gen.pkl_load('precapdata')
        startingTemperature = preCapData['startingTemperature']
        noxioustemps = preCapData['NoxiousTemps']
        holdTimes = np.ones_like(noxioustemps)*preCapData['HoldTime']
        pres.text = "Starting Pre-Treatment Session"
        self.HeatPainRun(startingTemperature, noxioustemps, holdTimes)
        if prog.cancel == False:
            List = np.resize(
                np.append(noxioustemps, self.allRatings), (2, len(noxioustemps)))
            gen.savelist(List, 'PreCapPainRatings')
        pres.bPreCap.color = (0, 1, 0, 0.9)
        pres.bPreCap.hovercolor = (0, 1, 0, 0.6)
        self.SetButtonFalse()

    def PreHeat(self):
        print('\n\nPre-Heat')
        preHeatData = gen.pkl_load('preheatdata')
        noxioustemps = preHeatData['NoxiousTemp']
        startingTemp = preHeatData['startingTemperature']
        holdTimes = preHeatData['HoldTime']
        restTime = preHeatData['RestTime']
        slope = preHeatData['Slope']

        pres.text = "Starting Pre-Heat Session"
        self.setandcheck(startingTemp)
        T = time.time()
        gen.timer(T, 15)
        pres.text = '+'
        gen.wait(5)
        self.setandcheck(noxioustemps)
        T = time.time()
        interval = np.arange(10, holdTimes, 10)
        for x in interval:
            if prog.cancel == 'False':
                gen.timer(T, x)
                print('time elapsed: ' + str(x))
        if prog.cancel == 'False':
            gen.timer(T, holdTimes)
            print('time elapsed: ' + str(holdTimes))
            print('Apply Capsaicin')
            self.setandcheck(startingTemp)
        gen.wait(20)
        pres.bPreHeat.color = (0, 1, 0, 0.9)
        pres.bPreHeat.hovercolor = (0, 1, 0, 0.6)
        self.SetButtonFalse()

    def Calibration(self):
        print('\n\nCalibration')
        caliData = gen.pkl_load('calibrationdata')
        nextTemp = caliData['FirstNoxiousTemp']
        noxioustemps = []
        startingTemp = caliData['startingTemperature']
        holdTimes = caliData['HoldTime']
        restTime = caliData['RestTime']
        slope = caliData['Slope']
        max_samples = caliData['maxSamples']
        sequence = True
        self.allRatings = np.array([])
        pres.text = "Now Begining the Calibration Procedure."
        gen.wait(2)
        pres.text = '+'
        self.setandcheck(startingTemp)
        Tr = time.time()
        for sample in range(max_samples):
            if prog.cancel == False:
                noxioustemps = np.append(noxioustemps, nextTemp)
                print('\tNext Temperature = ' + str(nextTemp) + '°C')
                gen.timer(Tr, self.Rest)
                self.setandcheck(noxioustemps[sample])
                Tn = time.time()
                gen.timer(Tn, self.Hold)
            if prog.cancel == False:
                self.setandcheck(startingTemp)
                Tr = time.time()
                gen.wait(3)
                pres.text = 'rt'
                prog.collected = False
            while prog.collected == False and prog.cancel == False:
                gen.wait(0.5)
            if prog.cancel == False:
                self.allRatings = np.append(self.allRatings, currentRating)
                print('\tPain Rating to last Temperature = ' + str(currentRating))
                if sample > 2:
                    if currentRating < 8. and sequence == True:
                        targetRating = currentRating+0.8
                        if targetRating > 8:
                            targetRating = 8.
                        nextTemp = gen.predict_val(
                            self.allRatings, noxioustemps, targetRating)
                        print('\ttarget rating: ' + str(targetRating))
                    else:
                        nextRating = gen.findmissingvals(self.allRatings)
                        sequence = False
                        if nextRating == 9:
                            break
                        else:
                            nextTemp = gen.predict_val(
                                self.allRatings, noxioustemps, nextRating)
                else:  # not enough samples to perform linear regression
                    if currentRating < 1.:
                        nextTemp = noxioustemps[sample] + 3
                    elif currentRating < 3.:
                        nextTemp = noxioustemps[sample] + 1
                    elif currentRating >= 3. and currentRating < 8.:
                        nextTemp = noxioustemps[sample] + .5
                    elif currentRating >= 8.:
                        nextTemp = noxioustemps[sample] - 2
                nextTemp = np.around(nextTemp, decimals=1)
                gen.wait(1)
                if nextTemp > 50.0:
                    nextTemp = 50.0

        if prog.cancel == False:
            List = np.resize(
                np.append(noxioustemps, self.allRatings), (2, len(noxioustemps)))
            gen.savelist(List, 'CalibratedResults')

            targetRating = np.array([1, 2, 3, 4, 5, 6, 7, 8])
            self.newTemps = np.around(gen.make_model(
                self.allRatings, noxioustemps, targetRating), decimals=1)
            i = np.where(self.newTemps > 50.)
            self.newTemps[i[0]] = 50.
            gen.savelist(newTemps, 'EEGAscendTemps')

            targetRating = np.array(
                [1, 1.7, 2.4, 3.1, 3.8, 4.5, 5.2, 5.9, 6.6, 7.3, 8])
            newTemps = np.around(gen.make_model(
                self.allRatings, noxioustemps, targetRating), decimals=1)
            i = np.where(newTemps > 50.)
            newTemps[i[0]] = 50.
            gen.savelist(newTemps, 'EEGRandTemps')

        gen.timer(Tr, self.Rest)
        pres.bCali.color = (0, 1, 0, 0.9)
        pres.bCali.hovercolor = (0, 1, 0, 0.6)
        self.SetButtonFalse()

    def EEGAscend(self):
        print('\n\nEEGRun')
        try:
            file_to_open = data_folder / \
                ('EEGAscendTemps_Participant' + participantID + '.json')
            with open(file_to_open, 'r') as filehandle:
                noxioustemps = json.load(filehandle)
            baselineTemp = 25
            holdTimes = np.linspace(45, 10, len(noxioustemps))
            pres.text = "Starting EEG Run 1"
            self.EEG = True
            self.HeatPainRun(baselineTemp, noxioustemps, holdTimes)
            List = self.allRatings.tolist()
            file_to_open = data_folder / \
                ('EEGRun1PainRatings_Participant' + participantID + '.json')
            with open(file_to_open, 'w') as filehandle:
                json.dump(List, filehandle)
            self.SetButtonFalse()
        except:
            print('no calibration data')
        pres.bEEGAscend.color = (0, 1, 0, 0.9)
        pres.bEEGAscend.hovercolor = (0, 1, 0, 0.6)
        self.SetButtonFalse()

    def EEGRand(self, num):
        print('\n\nEEGRun2')
        file_to_open = data_folder / \
            ('EEGRandTemps_Participant' + participantID + '.json')
        with open(file_to_open, 'r') as filehandle:
            temps = json.load(filehandle)
        baselineTemp = 25
        Times = np.linspace(60, 10, len(temps))
        if num == 1:
            index = [2, 4, 8, 0, 6]
            pres.text = "Starting EEG Run 2"
        elif num == 2:
            index = [1, 3, 5, 7, 9, 10]
            pres.text = "Starting EEG Run 3"
        noxioustemps = np.zeros_like(index, dtype=float)
        holdTimes = np.zeros_like(index)
        for x in range(len(index)):
            i = index[x]
            noxioustemps[x] = np.around(temps[i], decimals=1)
            holdTimes[x] = Times[i]

        self.EEG = True
        self.HeatPainRun(baselineTemp, noxioustemps, holdTimes)

        List = self.allRatings.tolist()
        file_to_open = data_folder / \
            ('EEGRand1PainRatings_Participant' + participantID + '.json')
        with open(file_to_open, 'w') as filehandle:
            json.dump(List, filehandle)
        if num == 1:
            pres.bEEGRand1.color = (0, 1, 0, 0.9)
            pres.bEEGRand1.hovercolor = (0, 1, 0, 0.6)
        elif num == 2:
            pres.bEEGRand2.color = (0, 1, 0, 0.9)
            pres.bEEGRand2.hovercolor = (0, 1, 0, 0.6)
        self.SetButtonFalse()

    def SetButtonFalse(self):
        pres.text = 'Session Finished'
        gen.wait(2)
        self.targetTemp = self.baslineTemp
        self.change = True
        gen.wait(1)
        pres.text = ''
        but.PracticeRun = False
        but.CalibrationRun = False
        but.HPEEGRun = False
        but.HPEEGRand1Run = False
        but.HPEEGRand2Run = False
        but.PreCapRun = False
        but.TrainingRun = False
        but.PreHeatRun = False
        self.EEG = False
        self.cancel = False
        print('Finished\n\n')

    def setandcheck(self, temp):
        if self.cancel == False:
            self.targetTemp = temp
            self.change = True
            while currentTemp >= self.targetTemp + self.tolerance or currentTemp <= self.targetTemp - self.tolerance:
                gen.wait(0.1)


class MyBut(object):

    def __init__(self):
        self.PracticeRun = False
        self.CalibrationRun = False
        self.HPEEGRun = False
        self.HPEEGRand1Run = False
        self.HPEEGRand2Run = False
        self.PreCapRun = False
        self.TrainingRun = False
        self.PreHeatRun = False

    def MyQuit(self, event):
        self.MyExit()

    def MyExit(self):
        prog.cancel = True
        prog.stop()
        prog.join()
        fetcher.ser.close()
        fetcher.stop()
        fetcher.join()
        core.quit()
        print('Quit Button Pressed')
        time.sleep(2)

    def MyEEGRand1(self, event):
        pres.bEEGRand1.color = (1, 0, 0, 0.9)
        pres.bEEGRand1.hovercolor = (1, 0, 0, 0.6)
        self.HPEEGRand1Run = True

    def MyEEGRand2(self, event):
        pres.bEEGRand2.color = (1, 0, 0, 0.9)
        pres.bEEGRand2.hovercolor = (1, 0, 0, 0.6)
        self.HPEEGRand2Run = True

    def MyEEGAscend(self, event):
        pres.bEEGAscend.color = (1, 0, 0, 0.9)
        pres.bEEGAscend.hovercolor = (1, 0, 0, 0.6)
        self.HPEEGRun = True

    def MyPractice(self, event):
        pres.bPrac.color = (1, 0, 0, 0.9)
        pres.bPrac.hovercolor = (1, 0, 0, 0.6)
        self.PracticeRun = True

    def MyCali(self, event):
        pres.bCali.color = (1, 0, 0, 0.9)
        pres.bCali.hovercolor = (1, 0, 0, 0.6)
        self.CalibrationRun = True

    def MyPreCap(self, event):
        pres.bPreCap.color = (1, 0, 0, 0.9)
        pres.bPreCap.hovercolor = (1, 0, 0, 0.6)
        self.PreCapRun = True

    def MyPreHeat(self, event):
        pres.bPreHeat.color = (1, 0, 0, 0.9)
        pres.bPreHeat.hovercolor = (1, 0, 0, 0.6)
        self.PreHeatRun = True

    def MyTraining(self, event):
        pres.bTraining.color = (1, 0, 0, 0.9)
        pres.bTraining.hovercolor = (1, 0, 0, 0.6)
        self.TrainingRun = True

    def AboutMe(self, event):
        webbrowser.open("readme.txt")

    def MyCancel(self, event):
        prog.cancel = True
        CTimer = threading.Timer(5, self.CancelCancel)

    def CancelCancel(self):
        prog.cancel = False


class MyDataClass():

    def __init__(self):

        self.XData = [0]
        self.YData = [0]


class MyPresentation():

    def __init__(self, dataClass):
        # GRAPH
        self._dataClass = dataClass
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.2)
        self.hLine, = plt.plot(0, 0, 'g')
        self.ax.axes.grid()
        self.fig.set_size_inches(17, 10)
        self.ani = FuncAnimation(self.fig, self.run, interval=10, repeat=True)
        self.ax.axes.set_ylim(19, 51)
        self.ax.axes.set_ylabel('Temperature (°C)', fontsize=14)
        self.ax.axes.set_xlabel('Time (s)', fontsize=14)
        self.hLine.set_color('b')

        def createButton(pos, text, function):
            axB = plt.axes(pos)
            button = Button(axB, text)
            button.label.set_fontsize(14)
            button.on_clicked(function)
            return button

        delta = 0.10
        a, b, c, d = 0.86, 0.05, 0.09, 0.06
        self.bCancel = createButton([a, b, c, d], 'Cancel', but.MyCancel)
        a = a-delta
        self.bEEGRand2 = createButton(
            [a, b, c, d], 'EEG Rand 2', but.MyEEGRand2)
        a = a-delta
        self.bEEGRand1 = createButton(
            [a, b, c, d], 'EEG Rand 1', but.MyEEGRand1)
        a = a-delta
        self.bEEGAscend = createButton(
            [a, b, c, d], 'EEG Ascending', but.MyEEGAscend)
        a = a-delta
        self.bCali = createButton([a, b, c, d], 'Calibration', but.MyCali)
        a = a-delta
        self.bPreHeat = createButton([a, b, c, d], 'Pre Heat', but.MyPreHeat)
        a = a-delta
        self.bPreCap = createButton([a, b, c, d], 'Pre Cap', but.MyPreCap)
        a = a-delta
        self.bTraining = createButton([a, b, c, d], 'Training', but.MyTraining)
        a = a-delta
        self.bPrac = createButton([a, b, c, d], 'Practice', but.MyPractice)
        b = 0.91
        self.bHelp = createButton([0.07, b, c, d], 'About', but.AboutMe)
        self.bQuit = createButton([0.85, b, c, d], 'Quit', but.MyQuit)

        # PSYCHOPY
        self.mon = monitors.Monitor(name='Lonovo')
        self.win = visual.Window(fullscr=True, screen=1, monitor=self.mon)
        self.mes = visual.TextStim(self.win, text='')
        self.mes.height = .05
        self.mes.setAutoDraw(True)  # automatically draw every frame
        self.win.flip()
        self.text = ''
        self.fixation = visual.ShapeStim(self.win,
                                         units='cm',
                                         vertices=((0, -.25), (0, .25),
                                                   (0, 0), (-.25, 0), (.25, 0)),
                                         lineWidth=2,
                                         closeShape=False,
                                         lineColor="white")
        self.myRatingScale = visual.RatingScale(self.win, low=0, high=20,
                                                marker='triangle', stretch=1.5, 
                                                tickHeight=1.2, precision=1,
                                                tickMarks=(0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20),
                                                labels=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
                                                scale='0 = No Pain, 10 = Worst Pain Imaginable',
                                                acceptText= 'Accept',
                                                maxTime=20, showValue=False)
        self.Question = visual.TextStim(self.win, units='norm', pos=[0, 0.4],
                                        text='What was the maximum pain intensity during the last period?')
        PRpicture = 'PainScale2.png'
        self.ScalePic = visual.ImageStim(self.win, image=PRpicture, 
                                         units='cm', pos=[0, 0])

    def run(self, i):
        global currentRating

        # GRAPH
        self.hLine.set_data(self._dataClass.XData, self._dataClass.YData)
        self.hLine.axes.set_xlim(
            np.max(self._dataClass.XData)-60, np.max(self._dataClass.XData))
        self.ax.legend([str(currentTemp)], loc='upper left',
                       fontsize='xx-large')

        # PSYCHOPY
        if self.text == '+':
            self.mes.setText('')
            self.fixation.draw()
        elif self.text == 'rt':
            if prog.cancel == False:
                self.mes.setText('')
                self.Question.draw()
                self.ScalePic.draw()
                if self.myRatingScale.noResponse:
                    self.myRatingScale.draw()
                else:
                    prog.collected = True
                    currentRating = (self.myRatingScale.getRating())/2.
                    event.clearEvents()
                    self.myRatingScale.reset()
                    self.text = '+'
                    gen.EEGTrigger(16)
            elif prog.cancel == True:
                self.mes.setText('')
        else:
            self.mes.setText(self.text)
        self.win.flip()


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

        Thermode = calibration_folder / (SelectedThermode)
        fileObject = open(Thermode, 'rb')
        Thermode = pickle.load(fileObject)
        fileObject.close()
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
            core.quit()
            sys.exit()

    def poll_temp(self):
        self.ser.write(str.encode('M000'))
        red = self.ser.read(4).decode("utf-8")
        return int(red[1:], 16)/10

    def run(self):
        while not self.stopped():
            global currentTemp
            callTime = time.time()
            currentTemp = self.poll_temp()
            # add data to data class
            if prog.change == True:
                gen.set_temp(prog.targetTemp, prog.Slope)
                prog.change = False
            self._dataClass.XData.append(time.time()-startTime)
            self._dataClass.YData.append(currentTemp)
            # sleep until next execution
            sleepTime = self._period-(callTime - time.time())
            time.sleep(sleepTime)


class general(threading.Thread):

    def __init__(self):
        # self.serE = serial.Serial()
        # self.serE.baudrate = 115200
        # self.serE.port = 'COM4'
        # self.serE.parity = 'N'
        # self.serE.bytesize = 8
        # self.serE.stopbits = 1
        # self.serE.xonxoff = False
        # self.serE.open()
        pass

    def wait(self, time_in_s):
        start = time.time()
        endTime = start + time_in_s
        currentTime = time.time()
        while currentTime < endTime and prog.cancel == False:
            time.sleep(0.1)
            currentTime = time.time()

    def num2hex(self, num):
        num = int(num)
        if num < 0:
            num = sum([4095, num])
        return f'{num:03x}'

    def writeandcheck(self, ser, towrite):
        ser.write(str.encode(towrite))
        red = ser.read(4).decode("utf-8")
        if red == towrite:
            pass
        else:
            exit('Error: Value to write = ' + str(towrite) +
                 ', Value read = ' + str(red))

    def set_temp(self, floattemp, floatslope):
        st = self.num2hex(int(floattemp*10))
        slope = self.num2hex(int(floatslope*10))
        self.writeandcheck(fetcher.ser, 'B' + st)
        self.writeandcheck(fetcher.ser, 'R' + slope)
        self.writeandcheck(fetcher.ser, 'C000')

    def timer(self, startTime, time_in_s):
        endTime = startTime + time_in_s
        currentTime = time.time()
        while currentTime < endTime and prog.cancel == False:
            time.sleep(0.1)
            currentTime = time.time()

    def predict_val(self, x, y, next_x):
        i = np.where(x == 0.0)
        x = np.delete(x, i[0], 0)
        y = np.delete(y, i[0], 0)
        x = np.array(x).reshape(len(x), 1)
        model = LinearRegression()
        model.fit(x, y)
        x_predict = np.array(next_x).reshape(1, -1)
        y_predict = model.predict(x_predict)
        return y_predict

    def findmissingvals(self, painRatings):
        for r in reversed(range(9)):
            i = np.where((painRatings >= r-0.5) & (painRatings < r+0.5))
            a = list(i[0])
            if not a:
                print('\ttarget rating: ' + str(r))
                return r
        return 9

    def make_model(self, x, y, x_predictors):
        x = np.array(x).reshape(len(x), 1)
        model = LinearRegression()
        model.fit(x, y)
        x_predict = np.array(x_predictors).reshape(len(x_predictors), 1)
        y_predict = model.predict(x_predict)
        return y_predict

    def savelist(self, nums, namelist):
        if prog.cancel == False:
            List = nums.tolist()
            file_to_open = data_folder / \
                (namelist + '_Participant' + participantID + '.json')
            with open(file_to_open, 'w') as filehandle:
                json.dump(List, filehandle)

    def pkl_load(self, text):
        DataFile = calibration_folder / (text)
        fileObject = open(DataFile, 'rb')
        Data = pickle.load(fileObject)
        fileObject.close()
        return Data

    def EEGTrigger(self, num):
        if prog.EEG == True:
            print('EEG Trigger ' + str(num))
            # self.serE


vals.initialise_vals()
vals.initialise_thermodes()
participantID = input('Enter the Participant ID: ')
data_folder = Path('Participant_' + participantID)
calibration_folder = Path('E:/ThermodeProject/CalibrationFiles')
data_folder.mkdir(parents=True, exist_ok=True)

Thermode = input('\nChoose the thermode: 0 = RegularThermode_v5, 1 = fMRI Thermode: ')
if Thermode == '0':
    SelectedThermode = 'RegularThermode_v5'
elif Thermode == '1':
    SelectedThermode = 'fMRIThermode'
else:
    SelectedThermode = 'RegularThermode_v5'
print('Thermode Selected: ' + SelectedThermode + '\n')

currentRating = []
startTime = time.time()
gen = general()
data = MyDataClass()
but = MyBut()
prog = MyHeatPainProgramme()
pres = MyPresentation(data)
fetcher = MyDataFetchClass(data)

fetcher.start()
prog.start()
plt.show()
