import matplotlib.pyplot as plt

# Personal
from dataclass import MyDataClass
from generalfunc import general
from datafetcher import MyDataFetchClass
from Presentation import MyPresentation
from program import MyHeatPainProgramme
from start import setup


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
