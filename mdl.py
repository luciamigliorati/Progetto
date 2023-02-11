import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from tqdm import tqdm
from scipy import constants, optimize
import scipy.fft


class Stazione():
    """
    Classe per rappresentare le stazioni di monitoraggio degli inquinanti
    
    Parametri
    -------------------------------------------
    numero stazione   : numero del sito
    stato             : stato di monitoraggio in U.S.A
    contea            : contea di monitoraggio 
    città             : città di monitoraggio 
    date  array       : date di campionamento
    lunghezza date    : lunghezza array date
    prima data        : data di inzio monitoraggio
    ultima data       : data di fine monitoraggio
    medie NO2         : valor medio del diossido di azoto rilevato dalla stazione di monitoraggio nelle date di campionamento
    medie O3          : valor medio dell'ozono rilevato dalla stazione di monitoraggio nelle date di campionamento
    medie SO2         : valor medio dell'anidride solforosa rilevata dalla stazione di monitoraggio nelle date di campionamento
    medie CO          : valor medio del monossido di azoto rilevato dalla stazione di monitoraggio nelle date di campionamento
    
    
    
 
    """
    
    def __init__(self):
        self.numeroStazione = 0
        self.stato     = ''
        self.contea    = ''
        self.città     = ''
        self.dateArray = np.empty(0)
        self.lunghezzaDate = 0
        self.primaData = 0
        self.ultimaData= 0
        self.medieNO2  = np.empty(0)
        self.medieO3   = np.empty(0)
        self.medieSO2  = np.empty(0)
        self.medieCO   = np.empty(0)

    def aggiungi_stazione(self, stato, dataLocale, numeroStazioni, città, contea, NO2medie, O3medie, SO2medie, COmedie):
        self.numeroStazione = numeroStazioni
        self.stato = stato     
        self.contea = contea
        self.città = città
        self.dateArray = np.append(self.dateArray, dataLocale)
        self.lunghezzaDate = len(self.dateArray)
        self.primaData = np.sort(self.dateArray)[0]
        self.ultimaData = np.sort(self.dateArray)[-1]
        self.medieNO2 = np.append(self.medieNO2, NO2medie)
        self.medieO3 = np.append(self.medieO3, O3medie)
        self.medieSO2 = np.append(self.medieSO2, SO2medie)
        self.medieCO = np.append(self.medieCO, COmedie)
