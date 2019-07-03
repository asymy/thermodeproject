# Thermode Project #

GNU General Public License v3.0

Copyright (c) 2018 Alison Symon

## Summary ##

This program will commnuicate with the MSA Thermal Stimulator, using the normal thermode. It will present EEG stimulus to the participant via psychopy, and show the experimenter what the thermode is doing via a matplotlib graph.
There are various buttons on the graph which will start various programs.

## To Do List ##

- [ ] Refactor
  - [x] change to multiple more manageable files
  - [x] flags to set button to false
  - [ ] Make sure nothing is hardcoded that should be from input variables
    - [ ] wait times for rating scale to appear
- [ ] add slope and rest time editing in each program, but default to inital values if not supplied
    - general funct -> writeandcheck
    - datafetcher -> uses set temp with default val
    - prog sets target temp, also set target slope
- [x] Redraw matplotlib with info boxes
  - [x] move current temp to below window
  - [x] get name of current program
  - [x] get next temp
  - [x] get previous temp
  - [ ] get timing info?
- [ ] write aboutme more 

- [ ] get theme sorted better


### Done List ###

- [x] change button colours better
- [x] Install flake8 and make sure formatting is good
- [x] Change to consistant file output - JSON or PICKLE
- [x] Baseline recording script - independent?

#### Tkinter starup box ####

- [x] input box participant id
- [x] thermode drop down menu
- [x] monitor drop down menu
- [x] com port settings button
  - [x] pop up window
  - [x] com port thermode drop down menu - radio buttons
  - [x] com port eeg drop down menu - radio buttons
- [x] Accept Setting


