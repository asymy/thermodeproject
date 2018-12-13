import matplotlib.pyplot as plt

# Personal
from EEGControl import EEGControl
from dataclass import MyDataClass
from generalfunc import general
from datafetcher import MyDataFetchClass
from Presentation import MyPresentation
from program import MyHeatPainProgramme
from start import setup
import vals
import config

config.init()
gen = general()
vals.initialise()
EEGControl = EEGControl()


if __name__ == "__main__":
    setup()
    gen = general()
    data = MyDataClass()
    pres = MyPresentation(data)
    fetcher = MyDataFetchClass(data)
    prog = MyHeatPainProgramme()

    fetcher.start()
    prog.start()
    plt.show()
