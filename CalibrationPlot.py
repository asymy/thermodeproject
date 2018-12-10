def CalibratedPlot_Participant(participantID):

    import numpy as np
    import matplotlib.pyplot as plt
    from pathlib import Path
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import r2_score
    import json

    # Choose Participant and Import data from file
    data_folder = Path('Participant_' + participantID)
    file_to_open = data_folder / \
        ('CalibratedResults_Participant' + participantID + '.json')
    with open(file_to_open, 'r') as filehandle:
        data = json.load(filehandle)

    # Reorganise data array and remove zero pain rating values 
    data = np.array(data)
    alltemps = data[0, :]
    allPainRating = data[1, :]
    i = np.where(allPainRating == 0.0)
    PainRating = np.delete(allPainRating, i[0], 0)
    temps = np.delete(alltemps, i[0], 0)
    temps = np.array(temps).reshape(len(temps), 1)
    PainRating = np.array(PainRating).reshape(len(temps), 1)

    # Make Linear Regression Model
    model = LinearRegression()
    model.fit(PainRating, temps)
    PainRating_plot = [1, 2, 3, 4, 5, 6, 7, 8]
    PainRating_plot = np.array(PainRating_plot).reshape(len(PainRating_plot), 1)
    temps_plot = model.predict(PainRating_plot)

    # Plot and Save 
    fig, ax = plt.subplots()
    plt.scatter(alltemps, allPainRating, color='black', label='Real Data')
    fitlabel = ('Fitted Line ($R^{2}$ = %.2f' %
                r2_score(temps, model.predict(PainRating)) + ')')
    plt.plot(temps_plot, PainRating_plot, color='blue', label=fitlabel)
    ax.axes.set_ylim(-0.2, 10.2)
    ax.axes.set_xlabel('Temperature (°C)', fontsize=14)
    ax.axes.set_ylabel('NRS (0-10)', fontsize=14)
    fig.set_size_inches(10, 7)
    plt.title(('Participant ' + participantID + ' Calibration Graph'), fontsize=20)
    plt.legend(loc='upper left', fontsize=14)

    saveas = data_folder / ('CalibratedPlot_Participant' + participantID + '.png')
    fig.savefig(saveas)