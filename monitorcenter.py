from psychopy import visual, monitors


# Main Dell 4k monitor

my_monitor = monitors.Monitor(name='my_monitor_name')
my_monitor.setSizePix((1280, 800))
my_monitor.setWidth(20)
my_monitor.setDistance(100)
my_monitor.saveMon()

mon = monitors.Monitor(name='Dell')
mon.setWidth(52.5)
mon.setDistance(50)
mon.setSizePix((3840,2160))
mon.saveMon()

# Secondary Dell Monitor

mon2 = monitors.Monitor(name='Dell2')
mon2.setWidth(47.8)
mon2.setDistance(50)
mon2.setSizePix((1680,1050))
mon2.saveMon()

# Lenovo Monitor

mon3 = monitors.Monitor(name='Lonovo')
mon3.setWidth(52)
mon3.setDistance(50)
mon3.setSizePix((1920, 1200))
mon3.saveMon()

