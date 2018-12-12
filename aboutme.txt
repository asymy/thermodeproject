About Thermode Project

GNU General Public License v3.0

Copyright (c) 2018 Alison Symon

#################################################################################
################################## Description ##################################
#################################################################################

This program will commnuicate with the MSA Thermal Stimulator, using the normal thermode. It will present EEG stimulus to the participant via psychopy, and show the experimenter what the thermode is doing via a matplotlib graph.
There are various buttons on the graph which will start various programs.

- Practice
This will show the participant what stimulation they can expect on screen during the experiment.

- Training
This will show the participant what the thermode might feel like, at 3 different temperatures and to start using the pain rating scale with a painful stimulus.

- Pre-Capsaicin
This will give the participant the full range of painful temperatures from 43 to 50°C. It will cancel higher temperatures if the participant rates above an 8. It will save the pain rating data into a json file.

- Calibration
This is for post capsaicin, in order to learn how the capsaicin has affected the participant. It will try to collect enough data to do a linear regression to predict what temperatures the participant will rate from 1 to 8. It will save the temperatures to a json file.

- EEG Ascending
This is for a straight run of EEG, starting with a low intensity and longer time, slowly increasing intensity and decreasing time.

- EEG Rand 1 & 2
**** Incomplete ****

#################################################################################
################################## EEG Triggers #################################
#################################################################################

11 = starting temperature reached
12 = temperature chaning from starting
13 = temperature reached its target
14 = temperature chaning from target
11 = starting temperature reached again

15 = starting rating
16 = stop rating

#################################################################################
################################ Making Changes #################################
#################################################################################

There are a few easy changes to make this program run the way you want.

- Changing Ports
The port may be different on different machines, go to 'MyDataFetchClass' class and change the variable self.ser.port to the correct port.

- Changing thermodes
The thermode is selected and calibrated in the 'MyDataFetchClass' class. Go to this class and change the name of the thermode.
If a new thermode is aquired, go to ThermodeCenter.py and add the new one in a similar fashion.

- Changing temperatures
The temperatures are all loaded from .json files, the first number in the list will be the starting/returning temperature, and the rest of the numbers will be the noxious temperatures. Changing these numbers before the program runs will change the temperatures.

- Changing stimulus
Find the string of text you want to change and change it.

#################################################################################
############################## Detailed Description #############################
#################################################################################


