import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mdl 
from mdl import Stazione
from scipy import constants, fftpack
import seaborn as sns
import scipy.fft

def stampa_array(stazioniX):#stampa l'array di date di una stazione
        for i in range(len(stazioniX)):
         print(len(stazioniX[i].lunghezzaDate))

mydata = pd.read_csv('pollution_us_2000_2002.csv')
dataLocale = mydata['Date Local']
date = np.empty(0)
indici=np.zeros(len(dataLocale))
for i in range(len(dataLocale)):
 indici = i
 
vuoto=np.zeros(len(dataLocale))
dictGiorni={'Indici':indici,'Data Locale': dataLocale, 'Giorni': vuoto  }
dfGiorni=pd.DataFrame(data=dictGiorni)
dfGiorni['Giorni']=pd.to_datetime(dfGiorni['Data Locale'], format = '%Y-%m-%d')
dfGiorni.sort_values(by='Giorni', inplace=True)
giorniOrdinati=dfGiorni['Giorni']
#date = pd.to_datetime(date)
for i in range(len(giorniOrdinati)-1):
 if(giorniOrdinati[i]!= giorniOrdinati[i+1] and i!=(len(giorniOrdinati)-1)):
  date=np.append(date, giorniOrdinati[i])
date=np.append(date, giorniOrdinati[len(giorniOrdinati)-1])

indiciDate=np.zeros(len(date))
for i in range(len(date)):
 indiciDate = i

dictDate={'Indici Date':indiciDate,'Data': date}
dfDate=pd.DataFrame(data=dictDate)
dfDate['Data'] = pd.to_datetime(dfDate['Data'], format = '%Y-%m-%d')

date=dfDate['Data']


newYork = pd.read_csv('newYork.csv')
statoNY = newYork['State']
dataLocaleNY = newYork['Date Local']
numeroStazioniNY = newYork['Site Num']
cittàNY = newYork['City']
conteeNY =  newYork['County']
NO2medieNY =  newYork['NO2 Mean']
O3medieNY =  newYork['O3 Mean']
SO2medieNY =  newYork['SO2 Mean']
COmedieNY =  newYork['CO Mean']
stazioniNY=np.empty(0)
   
for i in range(len(dataLocaleNY)-1):
  stazioniNY = np.append(stazioniNY, Stazione())
  if(numeroStazioniNY[i+1]!= numeroStazioniNY[i] or cittàNY[i+1]!=cittàNY[i]):
    stazioniNY = np.append(stazioniNY,Stazione())
  stazioniNY[-1].aggiungi_stazione(statoNY[i], dataLocaleNY[i], numeroStazioniNY[i], cittàNY[i], conteeNY[i], NO2medieNY[i], O3medieNY[i], SO2medieNY[i], COmedieNY[i]) #crea nuovo oggetto solo se c'è switch

stampa_array(stazioniNY)
