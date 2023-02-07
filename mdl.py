import numpy as np
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
    medie NO2         : valor medio del diossido di azoto rilevato dalla stazione di monitoraggio nelle date di campionamento
    medie O3          : valor medio dell'ozono rilevato dalla stazione di monitoraggio nelle date di campionamento
    medie SO2         : valor medio dell'anidride solforosa rilevata dalla stazione di monitoraggio nelle date di campionamento
    medie CO          : valor medio del monossido di azoto rilevato dalla stazione di monitoraggio nelle date di campionamento
    
    
    
 
    """
    
    def __init__(self):
        self.numeroStazione = 0
        self.stato    = ''
        self.contea   = ''
        self.città    = ''
        self.dateArray= np.empty(0)
        self.medieNO2 = np.empty(0)
        self.medieO3  = np.empty(0)
        self.medieSO2 = np.empty(0)
        self.medieCO  = np.empty(0)
        self.lunghezzaDate= len(self.dateArray)

    def aggiungi_stazione(self, stato, dataLocale, numeroStazioni, città, contea, NO2medie, O3medie, SO2medie, COmedie):
        self.numeroStazione = numeroStazioni
        self.stato = stato     
        self.contea = contea
        self.città = città
        self.dateArray = dataLocale
        self.medieNO2 = NO2medie
        self.medieO3 = O3medie
        self.medieSO2 = SO2medie
        self.medieCO = COmedie

'''
    
    def stampa_stazione(numeroStazione):
        print('Numero stazione /n', self.numeroStazione)
        print('New York /n', self.stato)
        print('Contea /n', self.contea)
        print('Città /n', self.città)
        print('Medie giornaliere NO2 /n', self.dateArray, '  ', self.medieNO2)
        print('Medie giornaliere O3 /n', self.dateArray, '  ', self.medieO3)
        print('Medie giornaliere SO2 /n', self.dateArray, '  ', self.medieSO2)
        print('Medie giornaliere CO /n', self.dateArray, '  ' ,self.medieCO)
        
    def __eq__(self, other):
        return  self.ruote == other.ruote and self.potenza == other.potenza


    def __lt__(self, other):
        return self.potenza < other.potenza

    def __gt__(self, other):
        return self.potenza > other.potenza
    
    def minore(self, other):
        return self.potenza < other.potenza  
'''
