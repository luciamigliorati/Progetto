import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mdl import Stazione
from scipy import constants, fftpack
import seaborn as sns
import scipy.fft

def corrInquinanti(a,b,c,d):
 dict={'NO2': a, 'O3': b, 'SO2': c, 'CO': d}
 df=pd.DataFrame(data=dict)
 corr=df.corr()
 return corr



def medieInquinanti(dataLocaleX, NO2medieX, O3medieX, SO2medieX, COmedieX):
 arraySommeX = np.zeros(len(date))
 NO2sommaX = np.zeros(len(date))
 O3sommaX = np.zeros(len(date))
 SO2sommaX= np.zeros(len(date))
 COsommaX = np.zeros(len(date))
 for i in range(len(date)):
  for j in range(len(dataLocaleX)):
   if(date[i]==dataLocaleX[j]):
    arraySommeX[i] += 1
    NO2sommaX[i] += NO2medieX[j]
    O3sommaX[i] += O3medieX[j]
    SO2sommaX[i] += SO2medieX[j]
    COsommaX[i] += COmedieX[j]
   if(NO2sommaX[i] == 0):
    arraySommeX[i] = 1
 return NO2sommaX/arraySommeX, O3sommaX/arraySommeX, SO2sommaX/arraySommeX, COsommaX/arraySommeX




def subTFstati(X,Y1,Y2,Y3,Y4): # subplot di andamento temporale, spettro in ampiezza, spettro di potenza per gli stati
 plt.figure(figsize=(12,12))
 # Grafico riga 1, colonna 1: Andamento temporale
 plt.subplot(2, 1, 1)
 x=X
 y1=Y1
 y2=Y2
 y3=Y3
 y4=Y4
 plt.plot(x,y1,c='darkturquoise', label="NO2")
 plt.plot(x,y2,c='orchid', label="O3")
 plt.plot(x,y3,c='cornflowerblue', label="SO2")
 plt.plot(x,y4,c='darkorange', label="CO", alpha=0.3)
 plt.plot('Data')
 plt.ylabel('Inquinante')
 if((y1[0:10]==NO2mediaNY[0:10]).all()):
  plt.title('Andamento temporale inquinanti New York')
 elif((y1[0:10]==NO2mediaDC[0:10]).all()):
  plt.title('Andamento temporale inquinanti District of Columbia')
 elif((y1[0:10]==NO2mediaNJ[0:10]).all()):
  plt.title('Andamento temporale inquinanti New Jersey')
 elif((y1[0:10]==NO2mediaMA[0:10]).all()):
  plt.title('Andamento temporale inquinanti Massachusetts')
 else:
  plt.title('Andamento temporale inquinanti Pennsylvanias') 
  
 plt.legend(loc="upper right", title="Legenda", frameon=False)
 #plt.xlim(dataLocaleNY[0:-1]) 
  
 # Grafico riga 2, colonna 1: Spettro di potenza
 plt.subplot(2,1,2)
 plt.plot(y1freq, np.absolute(y1rfft)**2, color='darkturquoise', label="NO2")
 plt.plot(y2freq, np.absolute(y2rfft)**2, color='orchid', label="O3")
 plt.plot(y3freq, np.absolute(y3rfft)**2, color="cornflowerblue", label="SO2")
 plt.plot(y4freq, np.absolute(y4rfft)**2, color='darkorange',   label="CO")
 plt.ylabel('Potenza')
 plt.xlabel('Frequenza')
 plt.yscale("log")
 plt.title('Spettro di potenza')
 plt.legend(loc="upper right", title="Legenda", frameon=False)

 # Grafico riga 2, colonna 2
 plt.show()


 

def subTFinquinanti(X, Y): # subplot di andamento temporale, spettro in ampiezza e spettro di potenza per gli inquinanti
 plt.figure(figsize=(12,12))
 # Grafico riga 1, colonna 1: Andamento temporale
 plt.subplot(2, 2, 1)
 x=X
 y=Y
 if((y[0:10]==NO2media[0:10]).all()):
  plt.plot(x,y,c='darkturquoise', label="NO2")
  plt.title('Andamento temporale NO2 nei 5 stati')
 elif((y[0:10]==O3media[0:10]).all()):
  plt.plot(x,y,c='orchid', label="O3")
  plt.title('Andamento temporale O3 nei 5 stati')
 elif((y[0:10]==SO2media[0:10]).all()):
  plt.plot(x,y,c='forestgreen', label="SO2")
  plt.title('Andamento temporale SO2 nei 5 stati')
 else:
  plt.plot(x,y,c='darkorange', label="CO")
  plt.title('Andamento temporale CO nei 5 stati')  
 plt.plot('Data')
 plt.ylabel('Inquinante')
 plt.title('Andamento temporale inquinanti New York')
 plt.legend(loc="upper right", title="Legenda", frameon=False) 
 #plt.xlim(dataLocaleNY[0:-1]) 
 # Grafico riga 1, colonna 2: Spettro in ampiezza
 plt.subplot(2, 2, 2)
 yrfft=scipy.fft.rfft(y)
 yfreq=0.5*scipy.fft.rfftfreq(len(y), d=1)
 if(y[0]==NO2media[0]):
   plt.plot(yfreq, np.absolute(yrfft), color='darkturquoise', label="NO2") 
 elif(y[0]==O3media[0]):
   plt.plot(yfreq, np.absolute(yrfft), color='orchid', label="O3") 
 elif(y[0]==SO2media[0]):
   plt.plot(yfreq, np.absolute(yrfft), color="forestgreen", label="SO2") 
 else:
   plt.plot(yfreq, np.absolute(yrfft), color='darkorange',   label="CO")
 plt.yscale("log")
 plt.ylabel('Ampiezza')
 plt.xlabel('Frequenza')
 plt.title('Spettro in ampiezza')
 plt.legend(loc="upper right", title="Legenda", frameon=False) 
 # Grafico riga 2, colonna 1: Spettro di potenza
 plt.subplot(2,2,3)                              
 if(y[0]==NO2media[0]):
   plt.plot(yfreq, np.absolute(yrfft)**2, color='darkturquoise', label="NO2") 
 elif(y[0]==O3media[0]):
   plt.plot(yfreq, np.absolute(yrfft)**2, color='orchid', label="O3") 
 elif(y[0]==SO2media[0]):
   plt.plot(yfreq, np.absolute(yrfft)**2, color="forestgreen", label="SO2") 
 else:
   plt.plot(yfreq, np.absolute(yrfft)**2, color='darkorange',   label="CO") 
 plt.ylabel('Potenza')
 plt.xlabel('Frequenza')
 plt.yscale("log")
 plt.title('Spettro di potenza')
 plt.legend(loc="upper right", title="Legenda", frameon=False)
 plt.show()



                              

### LEGGO IL CSV DEI DATI
mydata = pd.read_csv('pollution_us_2000_2002.csv')
dataLocale = mydata['Date Local']
'''
inquinamento = mydata[['Site Num','State','County','City','Date Local','NO2 Mean','O3 Mean','SO2 Mean','CO Mean']]
dataLocale =np.sort( pd.to_datetime(inquinamento['Date Local']))
gruppi = inquinamento.groupby(['State'])

### DIVIDO I DATI DI OGNUNO DEI 5 STATI
inquinamentoNY=gruppi.get_group('New York')
inquinamentoDC=gruppi.get_group('District Of Columbia')
inquinamentoNJ=gruppi.get_group('New Jersey')
inquinamentoMA=gruppi.get_group('Massachusetts')
inquinamentoPA=gruppi.get_group('Pennsylvania')

### CSV PER OGNUNO DEI 5 STATI, ORDINATI SECONDO SITE NUM E DATE LOCAL, CON UN VALOR MEDIO PER GIORNO
NY = inquinamentoNY.sort_values(by=['Site Num', 'Date Local'])
NY = NY.groupby(['State','County','City','Site Num','Date Local']).mean()
(NY).to_csv('newYork.csv')

DC = inquinamentoDC.sort_values(by=['Site Num', 'Date Local'])
DC = DC.groupby(['State','County','City','Site Num','Date Local']).mean()
(DC).to_csv('districtOfColumbia.csv')

NJ = inquinamentoNJ.sort_values(by=['Site Num', 'Date Local'])
NJ = NJ.groupby(['State','County','City','Site Num','Date Local']).mean()
(NJ).to_csv('newJersey.csv')

MA = inquinamentoMA.sort_values(by=['Site Num', 'Date Local'])
MA = MA.groupby(['State','County','City','Site Num','Date Local']).mean()
(MA).to_csv('massachusetts.csv')

PA = inquinamentoPA.sort_values(by=['Site Num', 'Date Local'])
PA = PA.groupby(['State','County','City','Site Num','Date Local']).mean()
(PA).to_csv('pennsylvania.csv')
'''

### STAZIONI NEW YORK
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


### STAZIONI NY DISTRICT OF COLUMBIA 
districtOfColumbia = pd.read_csv('districtOfColumbia.csv')
statoDC = districtOfColumbia['State']
dataLocaleDC = districtOfColumbia['Date Local']
numeroStazioniDC = districtOfColumbia['Site Num']
cittàDC = districtOfColumbia['City']
conteeDC =  districtOfColumbia['County']
NO2medieDC =  districtOfColumbia['NO2 Mean']
O3medieDC =  districtOfColumbia['O3 Mean']
SO2medieDC =  districtOfColumbia['SO2 Mean']
COmedieDC =  districtOfColumbia['CO Mean']
stazioniDC = np.empty(0)

for i in range(len(dataLocaleDC)-1):
 stazioniDC = np.append(stazioniDC, Stazione())
 if(numeroStazioniDC[i+1]!= numeroStazioniDC[i] or cittàDC[i+1]!=cittàDC[i]):
    stazioniDC = np.append(stazioniDC,Stazione())
 stazioniDC[-1].aggiungi_stazione(statoDC[i], dataLocaleDC[i], numeroStazioniDC[i], cittàDC[i], conteeDC[i], NO2medieDC[i], O3medieDC[i], SO2medieDC[i], COmedieDC[i])
                              
  
### STAZIONI NEW JERSEY
newJersey = pd.read_csv('newJersey.csv')
statoNJ = newJersey['State']
dataLocaleNJ = newJersey['Date Local']
numeroStazioniNJ = newJersey['Site Num']
cittàNJ = newJersey['City']
conteeNJ =  newJersey['County']
NO2medieNJ =  newJersey['NO2 Mean']
O3medieNJ =  newJersey['O3 Mean']
SO2medieNJ =  newJersey['SO2 Mean']
COmedieNJ =  newJersey['CO Mean']
stazioniNJ = np.empty(0)

for i in range(len(dataLocaleNJ)-1):
 stazioniNJ = np.append(stazioniNJ, Stazione())
 if(numeroStazioniNJ[i+1]!= numeroStazioniNJ[i] or cittàNJ[i+1]!=cittàNJ[i]):
    stazioniNJ = np.append(stazioniNJ,Stazione())
 stazioniNJ[-1].aggiungi_stazione(statoNJ[i], dataLocaleNJ[i], numeroStazioniNJ[i], cittàNJ[i], conteeNJ[i], NO2medieNJ[i], O3medieNJ[i], SO2medieNJ[i], COmedieNJ[i])

                              
### STAZIONI MASSACHUSETTS
massachusetts = pd.read_csv('massachusetts.csv')
statoMA = massachusetts['State']
dataLocaleMA = massachusetts['Date Local']
numeroStazioniMA = massachusetts['Site Num']
cittàMA = massachusetts['City']
conteeMA =  massachusetts['County']
NO2medieMA =  massachusetts['NO2 Mean']
O3medieMA =  massachusetts['O3 Mean']
SO2medieMA =  massachusetts['SO2 Mean']
COmedieMA =  massachusetts['CO Mean']
stazioniMA = np.empty(0)

for i in range(len(dataLocaleMA)-1):
 stazioniMA = np.append(stazioniMA, Stazione())
 if(numeroStazioniMA[i+1]!= numeroStazioniMA[i] or cittàMA[i+1]!=cittàMA[i]):
    stazioniMA = np.append(stazioniMA,Stazione())
 stazioniMA[-1].aggiungi_stazione(statoMA[i], dataLocaleMA[i], numeroStazioniMA[i], cittàMA[i], conteeMA[i], NO2medieMA[i], O3medieMA[i], SO2medieMA[i], COmedieMA[i])
                              
        
### STAZIONI PENNSYLVANIA
pennsylvania = pd.read_csv('pennsylvania.csv')
statoPA = pennsylvania['State']
dataLocalePA = pennsylvania['Date Local']
numeroStazioniPA = pennsylvania['Site Num']
cittàPA = pennsylvania['City']
conteePA =  pennsylvania['County']
NO2mediePA =  pennsylvania['NO2 Mean']
O3mediePA =  pennsylvania['O3 Mean']
SO2mediePA =  pennsylvania['SO2 Mean']
COmediePA =  pennsylvania['CO Mean']
stazioniPA=np.empty(0)

for i in range(len(dataLocalePA)-1):
 stazioniPA = np.append(stazioniPA, Stazione())
 if(numeroStazioniPA[i+1]!= numeroStazioniPA[i] or cittàPA[i+1]!=cittàPA[i]):
  stazioniPA = np.append(stazioniPA,Stazione())
 stazioniPA[-1].aggiungi_stazione(statoPA[i], dataLocalePA[i], numeroStazioniPA[i], cittàPA[i], conteePA[i], NO2mediePA[i], O3mediePA[i], SO2mediePA[i], COmediePA[i])


### DIVERSI INQUINANTI

indici=np.zeros(len(dataLocale))
for i in range(len(dataLocale)):
 indici = i
 
vuoto=np.zeros(len(dataLocale))
dictGiorni={'Indici':indici,'Data Locale': dataLocale, 'Giorni': vuoto  }
dfGiorni=pd.DataFrame(data=dictGiorni)
dfGiorni['Giorni']=pd.to_datetime(dfGiorni['Data Locale'], format = '%Y-%m-%d')
dfGiorni.sort_values(by='Giorni', inplace=True)
giorniOrdinati=dfGiorni['Giorni']
'''
date = np.empty(0)
date = pd.to_datetime(date)
dataLocale =np.sort( pd.to_datetime(((pd.read_csv('pollution_us_2000_2002.csv'))['Date Local']), format = '%Y-%m-%d') )
'''
date = np.empty(0)
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
#print(date)



NO2mediaNY, O3mediaNY, SO2mediaNY, COmediaNY = medieInquinanti(dataLocaleNY, NO2medieNY, O3medieNY, SO2medieNY, COmedieNY)
NO2mediaDC, O3mediaDC, SO2mediaDC, COmediaDC = medieInquinanti(dataLocaleDC, NO2medieDC, O3medieDC, SO2medieDC, COmedieDC)
NO2mediaNJ, O3mediaNJ, SO2mediaNJ, COmediaNJ = medieInquinanti(dataLocaleNJ, NO2medieNJ, O3medieNJ, SO2medieNJ, COmedieNJ)
NO2mediaMA, O3mediaMA, SO2mediaMA, COmediaMA = medieInquinanti(dataLocaleMA, NO2medieMA, O3medieMA, SO2medieMA, COmedieMA)
NO2mediaPA, O3mediaPA, SO2mediaPA, COmediaPA = medieInquinanti(dataLocalePA, NO2mediePA, O3mediePA, SO2mediePA, COmediePA)

NO2somma = np.zeros(len(date))
O3somma = np.zeros(len(date))
SO2somma = np.zeros(len(date))
COsomma = np.zeros(len(date))
NO2media = np.zeros(len(date))
O3media = np.zeros(len(date))
SO2media = np.zeros(len(date))
COmedia = np.zeros(len(date))

for i in range(len(date)):
 NO2somma[i]= NO2mediaNY[i]+NO2mediaDC[i]+NO2mediaNJ[i]+NO2mediaMA[i]+NO2mediaPA[i]
 O3somma[i] = O3mediaNY[i]+O3mediaDC[i]+O3mediaNJ[i]+O3mediaMA[i]+O3mediaPA[i]
 SO2somma[i]= SO2mediaNY[i]+SO2mediaDC[i]+SO2mediaNJ[i]+SO2mediaMA[i]+SO2mediaPA[i]
 COsomma[i] = COmediaNY[i]+COmediaDC[i]+COmediaNJ[i]+COmediaMA[i]+COmediaPA[i]

NO2media = NO2somma/len(date)
O3media = O3somma/len(date)
SO2media = SO2somma/len(date)
COmedia = COsomma/len(date)

# Andamento temporale, spettro in ampiezza e spettro di potenza dei diversi inquinanti
subTFinquinanti(date, NO2media)
'''
subTFinquinanti(date, O3media)
subTFinquinanti(date, SO2media)
subTFinquinanti(date, COmedia)                            

# Correlazione tra i diversi inquinanti rilevati nei 5 stati
corr4inquinanti=corrInquinanti(NO2media, O3media, SO2media, COmedia)
### DIVERSI STATI
                            
# NEW YORK
# Andamento temporale, spettro in ampiezza e spettro di potenza dei diversi inquinanti 
subTFstati(date, NO2mediaNY, O3mediaNY, SO2mediaNY, COmediaNY)
# Correlazione tra i diversi inquinanti
corrNY=corrInquinanti(NO2mediaNY, O3mediaNY, SO2mediaNY, COmediaNY)

# DISTRICT OF COLUMBIA
# Andamento temporale, spettro in ampiezza e spettro di potenza dei diversi inquinanti 
subTFstati(date, NO2mediaDC, O3mediaDC, SO2mediaDC, COmediaDC)
# Correlazione tra i diversi inquinanti 
corrDC=corrInquinanti(NO2mediaDC, O3mediaDC, SO2mediaDC, COmediaDC)
                              
# NEW JERSEY
# Andamento temporale, spettro in ampiezza e spettro di potenza dei diversi inquinanti
subTFstati(date, NO2mediaNJ, O3mediaNJ, SO2mediaNJ, COmediaNJ)
# Correlazione tra i diversi inquinanti rilevati nel New Jersey
corrNJ=corrInquinanti(NO2mediaNJ, O3mediaNJ, SO2mediaNJ, COmediaNJ)
              
# MASSACHUSSETS
# Andamento temporale, spettro in ampiezza e spettro di potenza dei diversi inquinanti
subTFstati(date, NO2mediaMA, O3mediaMA, SO2mediaMA, COmediaMA)
# Correlazione tra i diversi inquinanti rilevati nel Massachusetts
corrMA=corrInquinanti(NO2mediaMA, O3mediaMA, SO2mediaMA, COmediaMA)

# PENNSYLVANIA
# Andamento temporale, spettro in ampiezza e spettro di potenza dei diversi inquinanti
subTFstati(date, NO2mediaPA, O3mediaPA, SO2mediaPA, COmediaPA)
# Correlazione tra i diversi inquinanti rilevati in Pennsylvania
corrPA=corrInquinanti(NO2mediaPA, O3mediaPA, SO2mediaPA, COmediaPA)
'''
   
      










