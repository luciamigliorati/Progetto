import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from tqdm import tqdm
from scipy import constants, optimize
import scipy.fft
import plotly.express as px
from mdl import Stazione
from fnzn import trovaIndici, corrInquinanti, convertiDate, rumore, fit, medieInquinanti, subTFstati, subTFinquinanti, mappa

                        
### LEGGO IL CSV DEI DATI
mydata = pd.read_csv('pollution_us_2000_2002.csv')
dataLocale = mydata['Date Local']

inquinamento = mydata[['Site Num','State','County','City','Date Local','NO2 Mean','O3 Mean','SO2 Mean','CO Mean']]
dataLocale = np.sort( pd.to_datetime(inquinamento['Date Local']))
print('csv originale letto')


### STAZIONI NEW YORK
newYork = pd.read_csv('newYork.csv')
statoNY = newYork['State']
dataLocaleNY = newYork['Date Local']
numeroStazioniNY = newYork['Site Num']
cittàNY = newYork['City']
conteeNY =  newYork['County']
NO2medieNY =  newYork['NO2 Mean'].values
O3medieNY =  newYork['O3 Mean'].values
SO2medieNY =  newYork['SO2 Mean'].values
COmedieNY =  newYork['CO Mean'].values
stazioniNY=np.empty(0)


stazioniNY = np.append(stazioniNY, Stazione())
for i in range(len(numeroStazioniNY)-1):
 stazioniNY[-1].aggiungi_stazione(statoNY[i], dataLocaleNY[i], numeroStazioniNY[i], cittàNY[i], conteeNY[i], NO2medieNY[i], O3medieNY[i], SO2medieNY[i], COmedieNY[i])
 if(numeroStazioniNY[i+1]!= numeroStazioniNY[i] or cittàNY[i+1]!=cittàNY[i]):
  stazioniNY = np.append(stazioniNY,Stazione())  #crea nuovo oggetto solo se c'è switch
 if(i==len(dataLocaleNY)-2): # se sono in fondo al ciclo aggiungo anche l'ultimo campionamento che sennò rimarrebbe fuori
  stazioniNY[-1].aggiungi_stazione(statoNY[i+1], dataLocaleNY[i+1], numeroStazioniNY[i+1], cittàNY[i+1], conteeNY[i+1], NO2medieNY[i+1], O3medieNY[i+1], SO2medieNY[i+1], COmedieNY[i+1])
  


### STAZIONI NY DISTRICT OF COLUMBIA 
districtOfColumbia = pd.read_csv('districtOfColumbia.csv')
statoDC = districtOfColumbia['State']
dataLocaleDC = districtOfColumbia['Date Local']
numeroStazioniDC = districtOfColumbia['Site Num']
cittàDC = districtOfColumbia['City']
conteeDC =  districtOfColumbia['County']
NO2medieDC =  districtOfColumbia['NO2 Mean'].values
O3medieDC =  districtOfColumbia['O3 Mean'].values
SO2medieDC =  districtOfColumbia['SO2 Mean'].values
COmedieDC =  districtOfColumbia['CO Mean'].values
stazioniDC = np.empty(0)


stazioniDC = np.append(stazioniDC, Stazione())
for i in range(len(dataLocaleDC)-1):
 stazioniDC[-1].aggiungi_stazione(statoDC[i], dataLocaleDC[i], numeroStazioniDC[i], cittàDC[i], conteeDC[i], NO2medieDC[i], O3medieDC[i], SO2medieDC[i], COmedieDC[i])
 if(numeroStazioniDC[i+1]!= numeroStazioniDC[i] or cittàDC[i+1]!=cittàDC[i]):
  stazioniDC = np.append(stazioniDC,Stazione())
 if(i==len(dataLocaleDC)-2):
  stazioniDC[-1].aggiungi_stazione(statoDC[i+1], dataLocaleDC[i+1], numeroStazioniDC[i+1], cittàDC[i+1], conteeDC[i+1], NO2medieDC[i+1], O3medieDC[i+1], SO2medieDC[i+1], COmedieDC[i+1])


                              
  
### STAZIONI NEW JERSEY
newJersey = pd.read_csv('newJersey.csv')
statoNJ = newJersey['State']
dataLocaleNJ = newJersey['Date Local']
numeroStazioniNJ = newJersey['Site Num']
cittàNJ = newJersey['City']
conteeNJ =  newJersey['County']
NO2medieNJ =  newJersey['NO2 Mean'].values
O3medieNJ =  newJersey['O3 Mean'].values
SO2medieNJ =  newJersey['SO2 Mean'].values
COmedieNJ =  newJersey['CO Mean'].values
stazioniNJ = np.empty(0)


stazioniNJ = np.append(stazioniNJ, Stazione())
for i in range(len(dataLocaleNJ)-1):
 stazioniNJ[-1].aggiungi_stazione(statoNJ[i], dataLocaleNJ[i], numeroStazioniNJ[i], cittàNJ[i], conteeNJ[i], NO2medieNJ[i], O3medieNJ[i], SO2medieNJ[i], COmedieNJ[i])
 if(numeroStazioniNJ[i+1]!= numeroStazioniNJ[i] or cittàNJ[i+1]!=cittàNJ[i]):
  stazioniNJ = np.append(stazioniNJ,Stazione())
 if(i==len(dataLocaleNJ)-2):
  stazioniNJ[-1].aggiungi_stazione(statoNJ[i+1], dataLocaleNJ[i+1], numeroStazioniNJ[i+1], cittàNJ[i+1], conteeNJ[i+1], NO2medieNJ[i+1], O3medieNJ[i+1], SO2medieNJ[i+1], COmedieNJ[i+1])

                              
### STAZIONI MASSACHUSETTS
massachusetts = pd.read_csv('massachusetts.csv')
statoMA = massachusetts['State']
dataLocaleMA = massachusetts['Date Local']
numeroStazioniMA = massachusetts['Site Num']
cittàMA = massachusetts['City']
conteeMA =  massachusetts['County']
NO2medieMA =  massachusetts['NO2 Mean'].values
O3medieMA =  massachusetts['O3 Mean'].values
SO2medieMA =  massachusetts['SO2 Mean'].values
COmedieMA =  massachusetts['CO Mean'].values
stazioniMA = np.empty(0)

stazioniMA = np.append(stazioniMA, Stazione())
for i in range(len(dataLocaleMA)-1):
 stazioniMA[-1].aggiungi_stazione(statoMA[i], dataLocaleMA[i], numeroStazioniMA[i], cittàMA[i], conteeMA[i], NO2medieMA[i], O3medieMA[i], SO2medieMA[i], COmedieMA[i])
 if(numeroStazioniMA[i+1]!= numeroStazioniMA[i] or cittàMA[i+1]!=cittàMA[i]):
  stazioniMA = np.append(stazioniMA,Stazione())
 if(i==len(dataLocaleMA)-2):
  stazioniMA[-1].aggiungi_stazione(statoMA[i+1], dataLocaleMA[i+1], numeroStazioniMA[i+1], cittàMA[i+1], conteeMA[i+1], NO2medieMA[i+1], O3medieMA[i+1], SO2medieMA[i+1], COmedieMA[i+1])
 




### STAZIONI PENNSYLVANIA
pennsylvania = pd.read_csv('pennsylvania.csv')
statoPA = pennsylvania['State']
dataLocalePA = pennsylvania['Date Local']
numeroStazioniPA = pennsylvania['Site Num']
cittàPA = pennsylvania['City']
conteePA =  pennsylvania['County']
NO2mediePA =  pennsylvania['NO2 Mean'].values
O3mediePA =  pennsylvania['O3 Mean'].values
SO2mediePA =  pennsylvania['SO2 Mean'].values
COmediePA =  pennsylvania['CO Mean'].values
stazioniPA=np.empty(0)


stazioniPA = np.append(stazioniPA, Stazione())
for i in range(len(numeroStazioniPA)-1):
 stazioniPA[-1].aggiungi_stazione(statoPA[i], dataLocalePA[i], numeroStazioniPA[i], cittàPA[i], conteePA[i], NO2mediePA[i], O3mediePA[i], SO2mediePA[i], COmediePA[i])
 if(numeroStazioniPA[i+1]!= numeroStazioniPA[i] or cittàPA[i+1]!=cittàPA[i]):
  stazioniPA = np.append(stazioniPA,Stazione())
 if(i==len(dataLocalePA)-2):
  stazioniPA[-1].aggiungi_stazione(statoPA[i+1], dataLocalePA[i+1], numeroStazioniPA[i+1], cittàPA[i+1], conteePA[i+1], NO2mediePA[i+1], O3mediePA[i+1], SO2mediePA[i+1], COmediePA[i+1])

print('csv dei 5 stati letti e oggetti stazione creati')



######################## DIVERSE STAZIONI
if True:
 indNY = trovaIndici(stazioniNY, 3, np.array([0, 1, 3]), '2000-05-05', '2001-12-27')
 indNJ = trovaIndici(stazioniNJ, 2, np.array([0, 1]), '2001-08-16', '2002-12-31')
 indPA = trovaIndici(stazioniPA, 4, np.array([0, 1, 2, 3]), '2000-03-31', '2002-10-31')
 
 #stazioni 0 1 2 di New York
 subTFstati(stazioniNY[0].dateArray[indNY[0]:indNY[1]+1], stazioniNY[0].medieNO2[indNY[0]:indNY[1]+1], stazioniNY[0].medieO3[indNY[0]:indNY[1]+1], stazioniNY[0].medieSO2[indNY[0]:indNY[1]+1], stazioniNY[0].medieCO[indNY[0]:indNY[1]+1], 'NYstazione0')
 
 subTFstati(stazioniNY[1].dateArray[indNY[2]:indNY[3]+1], stazioniNY[1].medieNO2[indNY[2]:indNY[3]+1], stazioniNY[1].medieO3[indNY[2]:indNY[3]+1], stazioniNY[1].medieSO2[indNY[2]:indNY[3]+1], stazioniNY[1].medieCO[indNY[2]:indNY[3]+1], 'NYstazione1')

 subTFstati(stazioniNY[3].dateArray[indNY[4]:indNY[5]+1], stazioniNY[3].medieNO2[indNY[4]:indNY[5]+1], stazioniNY[3].medieO3[indNY[4]:indNY[5]+1], stazioniNY[3].medieSO2[indNY[4]:indNY[5]+1], stazioniNY[3].medieCO[indNY[4]:indNY[5]+1], 'NYstazione3')
 
 # stazioni 0 1 di New Jersey
 subTFstati(stazioniNJ[0].dateArray[indNJ[0]:indNJ[1]+1], stazioniNJ[0].medieNO2[indNJ[0]:indNJ[1]+1], stazioniNJ[0].medieO3[indNJ[0]:indNJ[1]+1], stazioniNJ[0].medieSO2[indNJ[0]:indNJ[1]+1], stazioniNJ[0].medieCO[indNJ[0]:indNJ[1]+1], 'NJstazione0')
 
 subTFstati(stazioniNJ[1].dateArray[indNJ[2]:indNJ[3]+1], stazioniNJ[1].medieNO2[indNJ[2]:indNJ[3]+1], stazioniNJ[1].medieO3[indNJ[2]:indNJ[3]+1], stazioniNJ[1].medieSO2[indNJ[2]:indNJ[3]+1], stazioniNJ[1].medieCO[indNJ[2]:indNJ[3]+1], 'NJstazione1')
 
 # stazioni 0 1 2 3 di Pennsylvania
 subTFstati(stazioniPA[0].dateArray[indPA[0]:indPA[1]+1], stazioniPA[0].medieNO2[indPA[0]:indPA[1]+1], stazioniPA[0].medieO3[indPA[0]:indPA[1]+1], stazioniPA[0].medieSO2[indPA[0]:indPA[1]+1], stazioniPA[0].medieCO[indPA[0]:indPA[1]+1], 'PAstazione0')
 
 subTFstati(stazioniPA[1].dateArray[indPA[2]:indPA[3]+1], stazioniPA[1].medieNO2[indPA[2]:indPA[3]+1], stazioniPA[1].medieO3[indPA[2]:indPA[3]+1], stazioniPA[1].medieSO2[indPA[2]:indPA[3]+1], stazioniPA[1].medieCO[indPA[2]:indPA[3]+1], 'PAstazione1')

 subTFstati(stazioniPA[2].dateArray[indPA[4]:indPA[5]+1], stazioniPA[2].medieNO2[indPA[4]:indPA[5]+1], stazioniPA[2].medieO3[indPA[4]:indPA[5]+1], stazioniPA[2].medieSO2[indPA[4]:indPA[5]+1], stazioniPA[2].medieCO[indPA[4]:indPA[5]+1], 'PAstazione2')

 subTFstati(stazioniPA[3].dateArray[indPA[6]:indPA[7]+1], stazioniPA[3].medieNO2[indPA[6]:indPA[7]+1], stazioniPA[3].medieO3[indPA[6]:indPA[7]+1], stazioniPA[3].medieSO2[indPA[6]:indPA[7]+1], stazioniPA[3].medieCO[indPA[6]:indPA[7]+1], 'PAstazione3') 


 ### Matrici di correlazione tra stesso inquinante di diverse stazioni di uno stato

 # non tutti della stessa lunghezza perchè mancano alcuni giorni: taglio alla lughezza minima per fare le correlazioni
 indMinNY = min(len(stazioniNY[0].dateArray[indNY[0]:indNY[1]+1]), len(stazioniNY[1].dateArray[indNY[2]:indNY[3]+1]), len(stazioniNY[3].dateArray[indNY[4]:indNY[5]+1]) )
 indMinNJ = min(len(stazioniNJ[0].dateArray[indNJ[0]:indNJ[1]+1]), len(stazioniNJ[1].dateArray[indNJ[2]:indNJ[3]+1]) )
 indMinPA = min(len(stazioniPA[0].dateArray[indPA[0]:indPA[1]+1]), len(stazioniPA[1].dateArray[indPA[2]:indPA[3]+1]), len(stazioniPA[2].dateArray[indPA[4]:indPA[5]+1]), len(stazioniPA[3].dateArray[indPA[6]:indPA[7]+1]) )

 # NY
 NYdictNO2={'staz 0': stazioniNY[0].medieNO2[indNY[0]:indNY[0]+indMinNY], 'staz 1': stazioniNY[1].medieNO2[indNY[2]:indNY[2]+indMinNY], 'staz 3': stazioniNY[3].medieNO2[indNY[4]:indNY[4]+indMinNY]}
 NYdfNO2=pd.DataFrame(data=NYdictNO2)
 NYcorrNO2=NYdfNO2.corr()
 print('\n correlazione NO2 tra stazioni di NY\n', NYcorrNO2)

 NYdictO3={'staz 0': stazioniNY[0].medieO3[indNY[0]:indNY[0]+indMinNY], 'staz 1': stazioniNY[1].medieO3[indNY[2]:indNY[2]+indMinNY], 'staz 3': stazioniNY[3].medieO3[indNY[4]:indNY[4]+indMinNY]}
 NYdfO3=pd.DataFrame(data=NYdictO3)
 NYcorrO3=NYdfO3.corr()
 print('\n correlazione O3 tra stazioni di NY\n', NYcorrO3)

 NYdictSO2={'staz 0': stazioniNY[0].medieSO2[indNY[0]:indNY[0]+indMinNY], 'staz 1': stazioniNY[1].medieSO2[indNY[2]:indNY[2]+indMinNY], 'staz 3': stazioniNY[3].medieSO2[indNY[4]:indNY[4]+indMinNY]}
 NYdfSO2=pd.DataFrame(data=NYdictSO2)
 NYcorrSO2=NYdfSO2.corr()
 print('\n correlazione SO2 tra stazioni di NY\n', NYcorrSO2)

 NYdictCO={'staz 0': stazioniNY[0].medieCO[indNY[0]:indNY[0]+indMinNY], 'staz 1': stazioniNY[1].medieCO[indNY[2]:indNY[2]+indMinNY], 'staz 3': stazioniNY[3].medieCO[indNY[4]:indNY[4]+indMinNY]}
 NYdfCO=pd.DataFrame(data=NYdictCO)
 NYcorrCO=NYdfCO.corr()
 print('\n correlazione CO tra stazioni di NY\n', NYcorrCO)
 

 # NJ 
 NJdictNO2={'staz 0': stazioniNJ[0].medieNO2[indNJ[0]:indNJ[0]+indMinNJ], 'staz 1': stazioniNJ[1].medieNO2[indNJ[2]:indNJ[2]+indMinNJ]}
 NJdfNO2=pd.DataFrame(data=NJdictNO2)
 NJcorrNO2=NJdfNO2.corr()
 print('\n correlazione NO2 tra stazioni di NJ\n', NJcorrNO2)

 NJdictO3={'staz 0': stazioniNJ[0].medieO3[indNJ[0]:indNJ[0]+indMinNJ], 'staz 1': stazioniNJ[1].medieO3[indNJ[2]:indNJ[2]+indMinNJ]}
 NJdfO3=pd.DataFrame(data=NJdictO3)
 NJcorrO3=NJdfO3.corr()
 print('\n correlazione O3 tra stazioni di NJ\n', NJcorrO3)

 NJdictSO2={'staz 0': stazioniNJ[0].medieSO2[indNJ[0]:indNJ[0]+indMinNJ], 'staz 1': stazioniNJ[1].medieSO2[indNJ[2]:indNJ[2]+indMinNJ]}
 NJdfSO2=pd.DataFrame(data=NJdictSO2)
 NJcorrSO2=NJdfSO2.corr()
 print('\n correlazione SO2 tra stazioni di NJ\n', NJcorrSO2)

 NJdictCO={'staz 0': stazioniNJ[0].medieCO[indNJ[0]:indNJ[0]+indMinNJ], 'staz 1': stazioniNJ[1].medieCO[indNJ[2]:indNJ[2]+indMinNJ]}
 NJdfCO=pd.DataFrame(data=NJdictCO)
 NJcorrCO=NJdfCO.corr()
 print('\n correlazione CO tra stazioni di NJ\n', NJcorrCO)
 
 # PA
 PAdictNO2={'staz 0': stazioniPA[0].medieNO2[indPA[0]:indPA[0]+indMinPA], 'staz 1': stazioniPA[1].medieNO2[indPA[2]:indPA[2]+indMinPA], 'staz 2': stazioniPA[2].medieNO2[indPA[4]:indPA[4]+indMinPA], 'staz 3': stazioniPA[3].medieNO2[indPA[6]:indPA[6]+indMinPA]}
 PAdfNO2=pd.DataFrame(data=PAdictNO2)
 PAcorrNO2=PAdfNO2.corr()
 print('\n correlazione NO2 tra stazioni di PA\n', PAcorrNO2)

 PAdictO3={'staz 0': stazioniPA[0].medieO3[indPA[0]:indPA[0]+indMinPA], 'staz 1': stazioniPA[1].medieO3[indPA[2]:indPA[2]+indMinPA], 'staz 2': stazioniPA[2].medieO3[indPA[4]:indPA[4]+indMinPA], 'staz 3': stazioniPA[3].medieO3[indPA[6]:indPA[6]+indMinPA]}
 PAdfO3=pd.DataFrame(data=PAdictO3)
 PAcorrO3=PAdfO3.corr()
 print('\n correlazione O3 tra stazioni di PA\n', PAcorrO3)

 PAdictSO2={'staz 0': stazioniPA[0].medieSO2[indPA[0]:indPA[0]+indMinPA], 'staz 1': stazioniPA[1].medieSO2[indPA[2]:indPA[2]+indMinPA], 'staz 2': stazioniPA[2].medieSO2[indPA[4]:indPA[4]+indMinPA], 'staz 3': stazioniPA[3].medieSO2[indPA[6]:indPA[6]+indMinPA]}
 PAdfSO2=pd.DataFrame(data=PAdictSO2)
 PAcorrSO2=PAdfSO2.corr()
 print('\n correlazione SO2 tra stazioni di PA\n', PAcorrSO2)

 PAdictCO={'staz 0': stazioniPA[0].medieCO[indPA[0]:indPA[0]+indMinPA], 'staz 1': stazioniPA[1].medieCO[indPA[2]:indPA[2]+indMinPA], 'staz 2': stazioniPA[2].medieCO[indPA[4]:indPA[4]+indMinPA], 'staz 3': stazioniPA[3].medieCO[indPA[6]:indPA[6]+indMinPA]}
 PAdfCO=pd.DataFrame(data=PAdictCO)
 PAcorrCO=PAdfCO.corr()
 print('\n correlazione CO tra stazioni di PA\n', PAcorrCO, '\n')


 
######################## DIVERSI INQUINANTI
if True:
 dataLocaleNY =np.sort(newYork['Date Local']) #sortati mi servono per le medie
 dataLocaleDC = np.sort(districtOfColumbia['Date Local'])
 dataLocaleNJ = np.sort(newJersey['Date Local'])
 dataLocaleMA = np.sort(massachusetts['Date Local'])
 dataLocalePA = np.sort(pennsylvania['Date Local'])

 vuoto = np.zeros(len(dataLocale))
 dictGiorni={'Data Locale': dataLocale, 'Giorni': vuoto}
 dfGiorni=pd.DataFrame(data=dictGiorni)
 dfGiorni['Giorni']=pd.to_datetime(dfGiorni['Data Locale'], format = '%Y-%m-%d')
 dfGiorni.sort_values(by='Giorni', inplace=True)
 giorniOrdinati=dfGiorni['Giorni']
 
 date = np.empty(0)
 for i in range(len(giorniOrdinati)-1):
  if(giorniOrdinati[i]!= giorniOrdinati[i+1] and i!=(len(giorniOrdinati)-1)):
   date=np.append(date, giorniOrdinati[i])
 date=np.append(date, giorniOrdinati[len(giorniOrdinati)-1])
 
 dictDate={'Data': date}
 dfDate=pd.DataFrame(data=dictDate)
 date = pd.to_datetime(dfDate['Data'], format = '%Y-%m-%d')
 dataLocaleNY = convertiDate(dataLocaleNY)
 dataLocaleDC = convertiDate(dataLocaleDC)
 dataLocaleNJ = convertiDate(dataLocaleNJ)
 dataLocaleMA = convertiDate(dataLocaleMA)
 dataLocalePA = convertiDate(dataLocalePA)
 print('date sistemate')

 #come avrei potuto chiamare la funzione medieInquinanti più efficace ma che non sono riuscita a far funzionare
 '''
 NO2mediaNY, O3mediaNY, SO2mediaNY, COmediaNY = medieInquinantiPro(newYork, dataLocaleNY, 'newYork', date)
 NO2mediaDC, O3mediaDC, SO2mediaDC, COmediaDC = medieInquinantiPro(districtOfColumbia, dataLocaleDC, 'columbia', date)
 NO2mediaNJ, O3mediaNJ, SO2mediaNJ, COmediaNJ = medieInquinantiPro(newJersey, dataLocaleNJ, 'newJersey', date)
 NO2mediaMA, O3mediaMA, SO2mediaMA, COmediaMA = medieInquinantiPro(massachusetts, dataLocaleMA, 'massachusetts', date)
 NO2mediaPA, O3mediaPA, SO2mediaPA, COmediaPA = medieInquinantiPro(pennsylvania, dataLocalePA, 'pennsylvania', date)
 '''
 # faccio le medie con la funzione meno efficace  
 NO2mediaNY, O3mediaNY, SO2mediaNY, COmediaNY = medieInquinanti(dataLocaleNY, NO2medieNY, O3medieNY, SO2medieNY, COmedieNY, date)
 NO2mediaDC, O3mediaDC, SO2mediaDC, COmediaDC = medieInquinanti(dataLocaleDC, NO2medieDC, O3medieDC, SO2medieDC, COmedieDC, date)
 NO2mediaNJ, O3mediaNJ, SO2mediaNJ, COmediaNJ = medieInquinanti(dataLocaleNJ, NO2medieNJ, O3medieNJ, SO2medieNJ, COmedieNJ, date)
 NO2mediaMA, O3mediaMA, SO2mediaMA, COmediaMA = medieInquinanti(dataLocaleMA, NO2medieMA, O3medieMA, SO2medieMA, COmedieMA, date)
 NO2mediaPA, O3mediaPA, SO2mediaPA, COmediaPA = medieInquinanti(dataLocalePA, NO2mediePA, O3mediePA, SO2mediePA, COmediePA, date)
   
 NO2somma = np.zeros(len(date))
 O3somma = np.zeros(len(date))
 SO2somma = np.zeros(len(date))
 COsomma = np.zeros(len(date))
 NO2media = np.zeros(len(date))
 O3media = np.zeros(len(date))
 SO2media = np.zeros(len(date))
 COmedia = np.zeros(len(date))
 
 # faccio la media non considerando il Massachusetts perchè ha soltanto una stazione con periodo che monitora soltanto per l'ultimo anno e mezzo
 NO2somma= NO2mediaNY + NO2mediaDC + NO2mediaNJ + NO2mediaPA
 O3somma = O3mediaNY + O3mediaDC + O3mediaNJ +  O3mediaPA
 SO2somma= SO2mediaNY + SO2mediaDC + SO2mediaNJ + SO2mediaPA
 COsomma = COmediaNY + COmediaDC + COmediaNJ + COmediaPA
 
 NO2media = NO2somma/4 # divido per 4= il numero di stati considerati (no Massachusetts)
 O3media = O3somma/4
 SO2media = SO2somma/4
 COmedia = COsomma/4
 print('medie fatte')
 
 
 # Andamento temporale, spettro in ampiezza e spettro di potenza dei diversi inquinanti
 subTFinquinanti(date, NO2media, 'NO2')
 subTFinquinanti(date, O3media, 'O3')
 subTFinquinanti(date, SO2media, 'SO2')
 subTFinquinanti(date, COmedia, 'CO')                            
 
 # Correlazione tra i diversi inquinanti rilevati nei 5 stati
 corr4inquinanti=corrInquinanti(NO2media, O3media, SO2media, COmedia)
 print('\n Correlazione tra medie inquinanti sui 4 stati\n', corr4inquinanti)


 ################################## DIVERSI STATI
 # NEW YORK
 # Andamento temporale, spettro in ampiezza e spettro di potenza dei diversi inquinanti 
 subTFstati(date, NO2mediaNY, O3mediaNY, SO2mediaNY, COmediaNY, 'New York')
 # Correlazione tra i diversi inquinanti
 corrNY=corrInquinanti(NO2mediaNY, O3mediaNY, SO2mediaNY, COmediaNY)
 print('\n Correlazione New York\n', corrNY)
 
 # DISTRICT OF COLUMBIA
 # Andamento temporale, spettro in ampiezza e spettro di potenza dei diversi inquinanti 
 subTFstati(date, NO2mediaDC, O3mediaDC, SO2mediaDC, COmediaDC, 'District of Columbia')
 # Correlazione tra i diversi inquinanti 
 corrDC=corrInquinanti(NO2mediaDC, O3mediaDC, SO2mediaDC, COmediaDC)
 print('\n Correlazione District of Columbia\n', corrDC)
 
 # NEW JERSEY
 # Andamento temporale, spettro in ampiezza e spettro di potenza dei diversi inquinanti
 subTFstati(date, NO2mediaNJ, O3mediaNJ, SO2mediaNJ, COmediaNJ, 'New Jersey')
 # Correlazione tra i diversi inquinanti rilevati nel New Jersey
 corrNJ=corrInquinanti(NO2mediaNJ, O3mediaNJ, SO2mediaNJ, COmediaNJ)
 print('\n Correlazione New Jersey\n', corrNJ)
 
 # MASSACHUSETTS
 # Andamento temporale, spettro in ampiezza e spettro di potenza dei diversi inquinanti
 subTFstati(date, NO2mediaMA, O3mediaMA, SO2mediaMA, COmediaMA, 'Massachussets')
 # Correlazione tra i diversi inquinanti rilevati nel Massachusetts
 corrMA=corrInquinanti(NO2mediaMA, O3mediaMA, SO2mediaMA, COmediaMA)
 print('\n Correlazione Massachussets\n', corrMA)
 
 # PENNSYLVANIA
 # Andamento temporale, spettro in ampiezza e spettro di potenza dei diversi inquinanti
 subTFstati(date, NO2mediaPA, O3mediaPA, SO2mediaPA, COmediaPA, 'Pennsylvania')
 # Correlazione tra i diversi inquinanti rilevati in Pennsylvania
 corrPA=corrInquinanti(NO2mediaPA, O3mediaPA, SO2mediaPA, COmediaPA)
 print('\n Correlazione Pennsylvania\n', corrPA)




 ################################# MAPPA
 newyork = np.full(len(date), 'NY')
 columbia = np.full(len(date), 'DC')
 newjersey = np.full(len(date), 'NJ')
 massachusetts = np.full(len(date), 'MA')
 pennsylvania = np.full(len(date), 'PA')
 
 dates = np.concatenate((date, date, date, date, date))
 states = np.concatenate((newyork, columbia, newjersey, massachusetts, pennsylvania))
 no2 = np.concatenate((NO2mediaNY, NO2mediaDC, NO2mediaNJ, NO2mediaMA, NO2mediaPA))
 o3 = np.concatenate((O3mediaNY, O3mediaDC, O3mediaNJ, O3mediaMA, O3mediaPA))
 so2 = np.concatenate((SO2mediaNY, SO2mediaDC, SO2mediaNJ, SO2mediaMA, SO2mediaPA))
 co = np.concatenate((COmediaNY, COmediaDC, COmediaNJ, COmediaMA, COmediaPA))
 
 maxno2 = max(no2)
 maxo3 = max(o3)
 maxso2 = max(so2)
 maxco = max(co)
 
 dataframe = pd.DataFrame()
 dataframe['date'] = dates
 dataframe['states'] = states
 dataframe['no2'] = no2*100/maxno2
 dataframe['o3'] = o3*100/maxo3
 dataframe['so2'] = so2*100/maxso2
 dataframe['co'] = co*100/maxco
 dataframe['date'] = pd.to_datetime(dataframe['date']).dt.date.astype(str)
 dataframe = dataframe.sort_values('date')
 
 dataframe.to_csv('datiMappa.csv') #salva il dataframe in un csv
 
 maxdf = pd.DataFrame()
 maxdf['max'] = np.array([maxno2, maxo3, maxso2, maxco])
 maxdf.to_csv('maxMappa.csv') #salva max in csv
 
if True: # legge il csv e rende possibile visualizzare la mappa anche senza rianalizzare i dati, basta porre False l'if nella sezione precedente
 dataframe = pd.read_csv('datiMappa.csv')
 maxx = (pd.read_csv('maxMappa.csv'))['max'].values
 # visualizzo con 4 mappe l'andamento degli inquinanti
 mappa(dataframe, round(maxx[0],2), 'no2')
 mappa(dataframe, round(maxx[1],2), 'o3')
 mappa(dataframe, round(maxx[2],2), 'so2')
 mappa(dataframe, round(maxx[3],2), 'co')
 print('mappe create')
