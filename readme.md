# Thermode Project #

GNU General Public License v3.0

Copyright (c) 2018 Alison Symon

## Summary ##

This program will commnuicate with the MSA Thermal Stimulator, using the normal thermode. It will present EEG stimulus to the participant via psychopy, and show the experimenter what the thermode is doing via a matplotlib graph.
There are various buttons on the graph which will start various programs.

## To Do List ##

- [ ] Refactor
  - [ ] change to multiple more manageable files
  - [ ] flags to set button to false
  - [ ] Make sure nothing is hardcoded that should be from input variables
- [ ] add slope and rest time editing in each program, but default to inital values if not supplied
- [ ] move 'practice' to seperate programme?

### Done List ###

- [x] Install flake8 and make sure formatting is good
- [x] Change to consistant file output - JSON or PICKLE
- [x] Baseline recording script - independent?


