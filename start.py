import config
from pathlib import Path
import vals
import tkinter as tk
from tkinter import messagebox


def setup():
    vals.initialise()
    config.init()

    def accept():
        config.participantID = e.get()
        question = 'Would you like to run the programme with these settings?'
        ok = messagebox.askokcancel('Confirm Set Up', question)
        if ok:
            config.folders['data'] = Path(
                'ParticipantFiles/Participant_' + config.participantID)
            config.folders['calibration'] = Path(
                './CalibrationFiles')
            config.folders['log'] = Path('logs')
            config.folders['data'].mkdir(parents=True, exist_ok=True)
            root.destroy()

    def on_selected_thermode(port):
        config.availaleCOMportsThermode = dict.fromkeys(
            config.availaleCOMportsThermode, False)
        config.availaleCOMportsThermode[port] = True

    def COMDialog():

        def draw_thermode():

            topContainerW = tk.Frame(
                selectorContainer, borderwidth=1, bg=lightColour)
            topContainerW.pack(side=tk.RIGHT, expand=True)
            thermodeLabel = tk.Label(topContainerW,
                                     text='Thermode:',
                                     bg=lightColour,
                                     width=defaultWidth,
                                     pady=5, padx=5)
            thermodeLabel.pack(side=tk.LEFT, anchor=tk.N)
            ThermButtonContainer = tk.Frame(topContainerW, bg=lightColour)
            ThermButtonContainer.pack(side=tk.RIGHT)

            vT = tk.StringVar()
            inital = 'none'
            vT.set(inital)
            on_selected_thermode(inital)

            for portT in config.availaleCOMportsThermode:
                rbTherm = tk.Radiobutton(ThermButtonContainer,
                                         text=portT,
                                         value=portT,
                                         variable=vT,
                                         bg=lightColour,
                                         command=lambda portT=portT:
                                         on_selected_thermode(portT))
                rbTherm.pack(anchor=tk.W)

        window = tk.Toplevel(root)
        window.geometry('475x350')
        window.configure(background=defaultBGColour)
        window.title('COM Settings')
        window.focus_force()

        spacer = tk.Frame(window, borderwidth=1, bg=defaultBGColour)
        spacer.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        instrucContainer = tk.Frame(window, borderwidth=1, bg=defaultBGColour)
        instrucContainer.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        instruc = 'Select COM ports for each:'
        tk.Label(instrucContainer,
                 text=instruc,
                 bg=defaultBGColour,
                 font='Helvetica, 16'
                 ).pack()

        selectorContainer = tk.Frame(window, bg=defaultBGColour)
        selectorContainer.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        draw_thermode()

        bottomContainerW = tk.Frame(window, borderwidth=1, bg=defaultBGColour)
        bottomContainerW.pack(side=tk.BOTTOM, expand=True)
        saveButton = tk.Button(bottomContainerW,
                               bg=strongButtonColour,
                               fg='white',
                               font='helvetica 12 bold',
                               text="Save",
                               width=defaultWidth,
                               command=window.destroy)
        saveButton.pack(side=tk.RIGHT, padx=5, pady=5)

    def selectThermode(selected):
        thermMenuDisplay.set(selected)
        config.selectedThermode = selected

    def selectMonitor(selected):
        monitorInfoDisplay.set(selected)
        config.monitor = selected

    root = tk.Tk()

    root.geometry('500x400')
    lightColour = 'SkyBlue1'
    defaultBGColour = 'LightSkyBlue1'
    strongButtonColour = 'RoyalBlue4'
    lightButtonColour = 'RoyalBlue1'
    textColor = 'midnight blue'
    defaultWidth = 13
    root.configure(background=defaultBGColour)
    root.option_add("*Font", "Helvetica, 12")
    # root.wm_iconbitmap('PainScaleicon.ico')
    root.title('Set Up')

    # top label
    topContainer = tk.Frame(root, borderwidth=1, bg=defaultBGColour)
    topContainer.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    instruc = 'Please Enter the Following Details:'
    labelInstruc = tk.Label(topContainer,
                            fg=textColor,
                            text=instruc,
                            bg=defaultBGColour,
                            font='Helvetica, 16')
    labelInstruc.pack(side=tk.BOTTOM, pady=20)

    title = 'Heat Pain EEG Programme'
    labelTitle = tk.Label(topContainer,
                          fg=textColor,
                          text=title,
                          bg=defaultBGColour,
                          font='Helvetica 18 bold')
    labelTitle.pack(side=tk.BOTTOM)

    # Patrticipant ID Info

    participantContainer = tk.Frame(root, bg=defaultBGColour)
    participantContainer.pack(side=tk.TOP, expand=True)

    labelParticipantID = tk.Label(participantContainer,
                                  justify=tk.RIGHT,
                                  fg=textColor,
                                  text='Participant ID:',
                                  bg=defaultBGColour,
                                  width=defaultWidth)
    labelParticipantID.pack(side=tk.LEFT)
    e = tk.Entry(participantContainer, width=defaultWidth)
    e.pack(side=tk.RIGHT)
    e.focus_set()

    # Thermode Info

    thermodeContainer = tk.Frame(root, bg=defaultBGColour)
    thermodeContainer.pack(side=tk.TOP, expand=True)

    thermLabel = tk.Label(thermodeContainer,
                          fg=textColor,
                          justify=tk.RIGHT,
                          text='Thermode:',
                          bg=defaultBGColour,
                          width=defaultWidth)
    thermLabel.pack(side=tk.LEFT)

    thermMenuDisplay = tk.StringVar()
    thermMenuDisplay.set('select')
    thermMenu = tk.Menubutton(thermodeContainer,
                              textvariable=thermMenuDisplay,
                              width=defaultWidth)

    picks = tk.Menu(thermMenu)
    thermMenu.config(menu=picks)

    for x in range(len(config.thermodeInfo)):
        name = config.thermodeInfo[x]['name']
        picks.add_command(label=name,
                          command=lambda name=name: selectThermode(name))

    thermMenu.config(bg=strongButtonColour,
                     fg='white',
                     font='helvetica 12 bold',
                     bd=4,
                     relief=tk.RAISED)
    thermMenu.pack(side=tk.RIGHT, expand=True)

    # Monitor info

    monitorContainer = tk.Frame(root, bg=defaultBGColour)
    monitorContainer.pack(side=tk.TOP)

    monitorLable = tk.Label(monitorContainer,
                            fg=textColor,
                            justify=tk.RIGHT,
                            text='Monitor:',
                            bg=defaultBGColour,
                            width=defaultWidth)
    monitorLable.pack(side=tk.LEFT)

    monitorInfoDisplay = tk.StringVar()
    monitorInfoDisplay.set('select')
    monitorMenu = tk.Menubutton(monitorContainer,
                                textvariable=monitorInfoDisplay,
                                width=defaultWidth)

    monPicks = tk.Menu(monitorMenu)
    monitorMenu.config(menu=monPicks)

    for x in range(len(config.monitorInfo)):
        name = config.monitorInfo[x]
        monPicks.add_command(label=name,
                             command=lambda name=name: selectMonitor(name))

    monitorMenu.config(bg=strongButtonColour,
                       fg='white',
                       font='helvetica 12 bold',
                       bd=4,
                       relief=tk.RAISED)
    monitorMenu.pack(side=tk.RIGHT)

    # Bottom buttons

    bottomContainer = tk.Frame(root, bg=defaultBGColour)
    bottomContainer.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # Accept Button

    acceptButton = tk.Button(bottomContainer,
                             text="Accept",
                             bg=strongButtonColour,
                             fg='white',
                             font='helvetica 12 bold',
                             width=defaultWidth,
                             command=accept)
    acceptButton.pack(side=tk.RIGHT, padx=20, pady=5)

    # COM port button

    bCOM = tk.Button(bottomContainer,
                     text='COM Settings',
                     bg=strongButtonColour,
                     fg='white',
                     font='helvetica 12 bold',
                     width=defaultWidth,
                     command=COMDialog)
    bCOM.pack(side=tk.LEFT, padx=20, pady=5)

    selectMonitor('ViewPix')
    selectThermode('thermode_v5')

    tk.mainloop()
