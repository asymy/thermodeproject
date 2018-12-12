import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
import time
import json
import sys

# Personal
from EEGControl import EEGControl
from dataclass import MyDataClass
from generalfunc import general
from datafetcher import MyDataFetchClass
from CalibrationPlot import CalibratedPlot_Participant
from Presentation import MyPresentation
from stopThreadclass import StoppableThread
import vals
import config


config.init()
gen = general()
vals.initialise()
EEGControl = EEGControl()


class MyHeatPainProgramme(StoppableThread):

    def __init__(self):
        StoppableThread.__init__(self)

        print(config.folders['calibration'])

        # config.defualtVals =
        startingVals = gen.json_read(
            config.folders['calibration'], 'startingdata')

        config.defaultVals = startingVals

        config.targetTemp = config.defaultVals['baselineTemperature']
        config.changeProg = True

        self.allRatings = []
        self.EEG = False

    def run(self):
        while not self.stopped():
            if config.buttonState['PracticeRun']:
                self.Practice()
            elif config.buttonState['TrainingRun']:
                self.Training()
            elif config.buttonState['CalibrationRun']:
                self.Calibration()
            elif config.buttonState['HPEEGRun']:
                self.EEGAscend()
            elif config.buttonState['HPEEGRand1Run']:
                self.EEGRand(1)
            elif config.buttonState['HPEEGRand2Run']:
                self.EEGRand(2)
            elif config.buttonState['PreCapRun']:
                self.PreCapHP()
            elif config.buttonState['PreHeatRun']:
                self.PreHeat()
            else:
                time.sleep(0.1)

    def HeatPainRun(self, baselineTemp, noxioustemps, holdTimes):
        self.allRatings = np.zeros_like(noxioustemps)
        gen.wait(2)
        pres.text = '+'
        gen.wait(2)
        # Set temperature to baseline temp, check it has reached this, send
        # EEG trigger, hold for rest period.
        # set temperature to noxious temp, send EEG trigger, check it as
        # reached temp, send another EEG trigger
        # wait for hold period, send another EEG trigger, set temp back to
        # baseline, check it has reached, send another EEG trigger
        # loop back to begining, and do for all noxious temps
        self.setandcheck(baselineTemp)
        T = time.time()
        EEGControl.EEGTrigger(11)
        gen.wait(5)
        print('\tNext Temperature = ' +
              str(noxioustemps[0]) + '°C, for ' + str(holdTimes[0]) + 's.')
        gen.timer(T, config.defaultVals['RestTime'])
        EEGControl.EEGTrigger(12)
        for x in range(len(noxioustemps)):
            self.setandcheck(noxioustemps[x])
            T = time.time()
            EEGControl.EEGTrigger(13)
            gen.timer(T, holdTimes[x])
            EEGControl.EEGTrigger(14)
            self.setandcheck(baselineTemp)
            T = time.time()
            EEGControl.EEGTrigger(11)
            gen.wait(5)
            EEGControl.EEGTrigger(15)
            config.ratingCollected = False
            pres.text = 'rt'
            while (config.ratingCollected is False and
                   config.cancelProg is False):
                gen.wait(0.05)
            gen.wait(.5)
            print('\tPain Rating to last Temperature = ' +
                  str(config.currentRating))
            gen.wait(.5)
            if x < len(noxioustemps) - 1:
                print('\tNext Temperature = ' +
                      str(noxioustemps[x+1]) + '°C, for ' +
                      str(holdTimes[x+1]) + 's.')
            gen.timer(T, config.defaultVals['RestTime'])
            if not config.cancelProg:
                self.allRatings[x] = config.currentRating
                EEGControl.EEGTrigger(12)
            else:
                break
            if not self.EEG:
                if config.currentRating > 8:
                    break
            elif self.EEG:
                if config.currentRating > 9:
                    break

    def Practice(self):
        print('Practice Run')
        messages = (('During the stimulation a fixation cross will appear on '
                     'the screen.\nPlease relax, and focus on the cross when '
                     'it is on the screen.\nAn example of the cross is on the '
                     'next screen.'),
                    ('After the Heat Stimulus, a rating scale will appear on '
                     'the screen.\nClick on the line with the mouse, and drag '
                     'the marker to change your selection.\nClick on the '
                     'button to confirm your answer.'),
                    ('You are now experiencing no pain, '
                     'please use the scale to indicate this.'),
                    ('You are now experiencing mild pain, '
                     'please use the scale to indicate this.'),
                    ('You are now experiencing extreme pain, '
                     'please use the scale to indicate this.'))
        stim = ('+', 'rt', 'rt', 'rt', 'rt')
        for x in range(len(messages)):
            if not config.cancelProg:
                pres.text = messages[x]
                gen.wait(2)
                pres.text = stim[x]
                if x == 0:
                    gen.wait(2)
                else:
                    while (config.ratingCollected is False and
                           config.cancelProg is False):
                        gen.wait(0.05)
                    config.ratingCollected = False
                    print('pain rating: ' + str(config.currentRating))
                    gen.wait(2)

        pres.text = ''
        pres.bPrac.color = (0, 1, 0, 0.9)
        pres.bPrac.hovercolor = (0, 1, 0, 0.6)
        self.SetButtonFalse()

    def Training(self):
        print('\n\nTraining')

        trainingData = gen.json_read(
            config.folders['calibration'], 'trainingdata')
        startingTemperature = trainingData['startingTemperature']
        noxioustemps = trainingData['NoxiousTemps']

        holdTimes = np.ones_like(noxioustemps)*trainingData['HoldTime']
        pres.text = "Starting Training Session"
        self.HeatPainRun(startingTemperature, noxioustemps, holdTimes)
        pres.bTraining.color = (0, 1, 0, 0.9)
        pres.bTraining.hovercolor = (0, 1, 0, 0.6)
        self.SetButtonFalse()

    def PreCapHP(self):
        print('\n\nPreCapHP')
        preCapData = gen.json_read(config.folders['calibration'], 'precapdata')
        startingTemperature = preCapData['startingTemperature']
        noxioustemps = preCapData['NoxiousTemps']
        holdTimes = np.ones_like(noxioustemps)*preCapData['HoldTime']
        pres.text = "Starting Pre-Treatment Session"
        self.HeatPainRun(startingTemperature, noxioustemps, holdTimes)
        data = {
            'noxioustemps': noxioustemps,
            'painRatings': self.allRatings
        }
        fileName = ('PreCapPainRatings' + '_Participant' +
                    config.participantID + '.json')
        gen.json_write(config.folders['data'], data, fileName)
        pres.bPreCap.color = (0, 1, 0, 0.9)
        pres.bPreCap.hovercolor = (0, 1, 0, 0.6)
        self.SetButtonFalse()

    def PreHeat(self):
        print('\n\nPre-Heat')
        preHeatData = gen.json_read(
            config.folders['calibration'], 'preheatdata')
        noxioustemps = preHeatData['NoxiousTemp']
        startingTemp = preHeatData['startingTemperature']
        holdTimes = preHeatData['HoldTime']
        restTime = preHeatData['RestTime']
        slope = preHeatData['Slope']
        sample = 60
        self.allRatings = np.zeros((int(holdTimes/60)+1, 1))

        pres.text = "Starting Pre-Heat Session"
        self.setandcheck(startingTemp)
        T = time.time()
        gen.timer(T, 10)
        pres.text = '+'
        gen.wait(10)
        self.setandcheck(noxioustemps)
        T = time.time()
        endTime = T + holdTimes

        time_in_s = holdTimes+2
        currentTime = time.time()
        startTime = currentTime
        endTime = startTime + time_in_s
        self.timeLeft = endTime - currentTime
        i = 0
        while currentTime < endTime and config.cancelProg is False:
            if np.around(self.timeLeft-1, decimals=0) % sample == 0:
                config.ratingCollected = False
                pres.text = 'rt'
                while (config.ratingCollected is False and
                       config.cancelProg is False):
                    gen.wait(0.05)
                    currentTime = time.time()
                    self.timeLeft = endTime - currentTime
                gen.wait(.5)
                print('\n\tPain Rating to last Temperature = ' +
                      str(config.currentRating))
                self.allRatings[i] = config.currentRating
                i = i+1

            else:
                gen.wait(0.05)
                currentTime = time.time()
                self.timeLeft = endTime - currentTime
                if np.around(self.timeLeft, decimals=1) % 1 == 0:
                    txt = ('time left: ' +
                           str(int(np.around(self.timeLeft, decimals=0))) +
                           's ')
                    sys.stdout.write('\r' + txt)
                    sys.stdout.flush()

        print('Apply Capsaicin')
        self.setandcheck(startingTemp)

        data = {
            'painRating': self.allRatings
        }
        fileName = ('PreHeatRatings_Participant' +
                    config.participantID + '.json')
        gen.json_write(config.folders['data'], data, fileName)
        gen.wait(20)
        pres.bPreHeat.color = (0, 1, 0, 0.9)
        pres.bPreHeat.hovercolor = (0, 1, 0, 0.6)
        self.SetButtonFalse()

    def Calibration(self):
        print('\n\nCalibration')
        caliData = gen.json_read(
            config.folders['calibration'], 'calibrationdata')
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
            if not config.cancelProg:
                noxioustemps = np.append(noxioustemps, nextTemp)
                print('\tNext Temperature = ' + str(nextTemp) + '°C')
                gen.timer(Tr, config.defaultVals['RestTime'])
                self.setandcheck(noxioustemps[sample])
                Tn = time.time()
                gen.timer(Tn, config.defaultVals['HoldTime'])
            if not config.cancelProg:
                self.setandcheck(startingTemp)
                Tr = time.time()
                gen.wait(3)
                pres.text = 'rt'
                config.ratingCollected = False
            while (config.ratingCollected is False and
                   config.cancelProg is False):
                gen.wait(0.5)
            if not config.cancelProg:
                self.allRatings = np.append(
                    self.allRatings, config.currentRating)
                print('\tPain Rating to last Temperature = ' +
                      str(config.currentRating))
                if sample > 2:
                    if config.currentRating < 8. and sequence:
                        targetRating = config.currentRating+0.8
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
                    if config.currentRating < 1.:
                        nextTemp = noxioustemps[sample] + 3
                    elif config.currentRating < 3.:
                        nextTemp = noxioustemps[sample] + 1
                    elif (config.currentRating >= 3. and
                          config.currentRating < 8.):
                        nextTemp = noxioustemps[sample] + .5
                    elif config.currentRating >= 8.:
                        nextTemp = noxioustemps[sample] - 2
                nextTemp = np.around(nextTemp, decimals=1)
                gen.wait(1)
                if nextTemp > 50.0:
                    nextTemp = 50.0

        data = {
            'noxioustemps': noxioustemps,
            'painRatings': self.allRatings
        }
        fileName = ('CalibratedResults_Participant' +
                    config.participantID + '.json')

        gen.json_write(config.folders['data'], data, fileName)

        targetRating = np.array([1, 2, 3, 4, 5, 6, 7, 8])
        newTempsAscend = np.around(gen.make_model(
            self.allRatings, noxioustemps, targetRating), decimals=1)
        i = np.where(newTempsAscend > 50.)
        newTempsAscend[i[0]] = 50.

        targetRating = np.array(
            [1, 1.7, 2.4, 3.1, 3.8, 4.5, 5.2, 5.9, 6.6, 7.3, 8])
        newTempsRand = np.around(gen.make_model(
            self.allRatings, noxioustemps, targetRating), decimals=1)
        i = np.where(newTempsRand > 50.)
        newTempsRand[i[0]] = 50.

        data = {
            'EEGAscendTemps': newTempsAscend,
            'EEGRandTemps': newTempsRand
        }
        fileName = ('EEGTemps_Participant' + config.participantID + '.json')
        gen.json_write(config.folders['data'], data, fileName)

        gen.timer(Tr, config.defaultVals['RestTime'])
        pres.bCali.color = (0, 1, 0, 0.9)
        pres.bCali.hovercolor = (0, 1, 0, 0.6)
        CalibratedPlot_Participant(config.participantID)
        self.SetButtonFalse()

    def EEGAscend(self):
        print('\n\nEEGRun')
        try:
            file_to_open = config.folders['data'] / \
                ('EEGAscendTemps_Participant' + config.participantID + '.json')
            with open(file_to_open, 'r') as filehandle:
                noxioustemps = json.load(filehandle)
            baselineTemp = 25
            holdTimes = np.linspace(45, 10, len(noxioustemps))
            pres.text = "Starting EEG Run 1"
            self.EEG = True
            self.HeatPainRun(baselineTemp, noxioustemps, holdTimes)
            List = self.allRatings.tolist()
            fileName = ('EEGRun1PainRatings_Participant' +
                        config.participantID + '.json')
            file_to_open = config.folders['data'] / fileName

            with open(file_to_open, 'w') as filehandle:
                json.dump(List, filehandle)
            self.SetButtonFalse()
        except FileNotFoundError as fnf_error:
            print(fnf_error)
        pres.bEEGAscend.color = (0, 1, 0, 0.9)
        pres.bEEGAscend.hovercolor = (0, 1, 0, 0.6)
        self.SetButtonFalse()

    def EEGRand(self, num):
        print('\n\nEEGRun2')
        file_to_open = config.folders['data'] / \
            ('EEGRandTemps_Participant' + config.participantID + '.json')
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
        fileName = ('EEGRand1PainRatings_Participant' +
                    config.participantID + '.json')
        file_to_open = config.folders['data'] / fileName

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
        config.targetTemp = config.defaultVals['baselineTemperature']
        config.changeProg = True
        gen.wait(1)
        pres.text = ''
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
        config.cancelProg = False
        print('Finished\n\n')

    def setandcheck(self, temp):
        if not config.cancelProg:
            config.targetTemp = temp
            config.changeProg = True
            while (config.currentTemp >=
                   (config.targetTemp + config.defaultVals['Tolerance'])
                   or config.currentTemp <=
                   (config.targetTemp - config.defaultVals['Tolerance'])):
                gen.wait(0.1)


config.participantID = input('Enter the Participant ID: ')
config.folders['data'] = Path(
    'ParticipantFiles/Participant_' + config.participantID)
config.folders['calibration'] = Path('E:/ThermodeProject/CalibrationFiles')
config.folders['log'] = Path('logs')
config.folders['data'].mkdir(parents=True, exist_ok=True)

Thermode = input(
    '\nChoose the thermode: 0 = RegularThermode_v5, 1 = fMRI Thermode: ')
if Thermode == '0':
    config.selectedThermode = 'RegularThermode_v5'
elif Thermode == '1':
    config.selectedThermode = 'fMRIThermode'
else:
    config.selectedThermode = 'RegularThermode_v5'
print('Thermode Selected: ' + config.selectedThermode)

Monitor = input(
    '\nChoose the Monitor: 0 = Lonovo, 1 = Dell: ')
if Monitor == '0':
    monitorName = 'Lonovo'
elif Monitor == '1':
    monitorName = 'Dell'
else:
    monitorName = 'Lonovo'
print('Monitor Selected: ' + monitorName + '\n')


gen = general()
data = MyDataClass()
pres = MyPresentation(data)
fetcher = MyDataFetchClass(data)

prog = MyHeatPainProgramme()

fetcher.start()
prog.start()
plt.show()
