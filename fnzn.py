import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from tqdm import tqdm
from mdl import Stazione
from scipy import constants, optimize
import scipy.fft
import plotly.express as px


def trovaIndici(stazioniX, n, a, si, sf): # restituisce un unico array i cui elementi di posizione pari sono indici di inizio dell'array di date considerate per il confronto tra stazioni e i dispari gli indici di fine
 indici = np.zeros(2*n, dtype=int)
 for j in range(n):
  for i in range(stazioniX[a[j]].lunghezzaDate):
   if (stazioniX[a[j]].dateArray[i] == si):
    indici[2*j] = i
   if (stazioniX[a[j]].dateArray[i] == sf):
    indici[(2*j)+1] = i
 return indici

def corrInquinanti(a,b,c,d): #restituisce la matrice di correlazione tra 4 array di inquinanti con stessa lunghezza 
 dict={'NO2': a, 'O3': b, 'SO2': c, 'CO': d}
 df=pd.DataFrame(data=dict)
 corr=df.corr()
 return corr

def convertiDate(dataLocaleX): # converte l'array di date in formato datetime64[ns]
 dictX = {'Data Locale': dataLocaleX}
 dfX = pd.DataFrame(data=dictX)
 return pd.to_datetime(dfX['Data Locale'])

def rumore(f, N, beta): # funzione del rumore nello spettro di potenza
    return (N/f**beta)

def fit(x, y): #funzione per il fit del rumore nello spettro di potenza
    params, params_covariance = optimize.curve_fit(rumore, x, y, p0=[1e3, 0.5])
    return params, params_covariance


def medieInquinanti(dataLocaleX, NO2medieX, O3medieX, SO2medieX, COmedieX, date): #restituisce 4 array di medie degli inquinanti in uno stato per tutta la durata dei 3 anni (mette le medie giornaliere a 0 per i giorni mancanti: ci sono alcuni giorni in cui non viene fatto il campionamento) 
 arraySommeX = np.zeros(len(date))
 NO2sommaX = np.zeros(len(date))
 O3sommaX = np.zeros(len(date))
 SO2sommaX= np.zeros(len(date))
 COsommaX = np.zeros(len(date))
 for i in tqdm(range(len(date))):
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

# funzione più efficiente di quella precedente ma che non sono riuscita a far funzionare
'''def medieInquinantiPro(df, dataLocaleX, s, date):
 conta = 0
 m = df.groupby('Date Local').mean(numeric_only=True) # fa la media per ogni giorno campionato da più di una stazione in uno stato
 m.to_csv(s+'medie.csv')
 m = pd.read_csv(s+'medie.csv')
 dateX = np.unique(dataLocaleX) #elimina doppioni di data
 for i in tqdm(range(len(date)), desc="Controllo date campionate: "):
  for j in range(len(dateX)):
   if(date[i]==dateX[j]):
    conta += 1
  if(conta == 0):
   m.loc[i-0.5] = [date[i], 0, 0, 0, 0, 0] #  aggiungo la data mancante con tutti zeri in fondo con indice giusto
 
 m.sort_index() # ordino per data
 m.to_csv(s+'medie.csv')
 return m['NO2 Mean'], m['O3 Mean'], m['SO2 Mean'], m['CO Mean']
 '''

def subTFstati(x,y1,y2,y3,y4,s): # subplot di andamento temporale, spettro di potenza, filtro per lungo periodo e caratterizzazione rumore per gli stati. Usata anche per l'analisi delle diverse stazioni all'interno di uno stato
 fig, ax = plt.subplots(2 ,1 , figsize=(15, 15))
 fig.suptitle('Andamento medio e analisi di Fourier degli inquinanti di '+s)
 # Grafico riga 1, colonna 1: Andamento temporale
 ax[0].plot(x,y1,c='darkturquoise', label="NO2")
 ax[0].plot(x,y2,c='orchid', label="O3")
 ax[0].plot(x,y3,c='cornflowerblue', label="SO2")
 ax[0].plot(x,y4,c='darkorange', label="CO")
 #ax[0].set_xlabel('Data')
 ax[0].set_ylabel('Inquinante (ppb)')
 
 ax[0].tick_params(axis='x', labelrotation=15)
 ax[0].xaxis.set_major_locator(mdates.DayLocator(interval=60))
 ax[0].set_title('Andamento temporale inquinanti '+ s)
  
 fig.legend(loc="upper right", title="Legenda", frameon=False)
  
 # Grafico riga 2, colonna 1: Spettro di potenza
 y1rfft=scipy.fft.rfft(y1)
 y2rfft=scipy.fft.rfft(y2)
 y3rfft=scipy.fft.rfft(y3)
 y4rfft=scipy.fft.rfft(y4)
 y1freq=0.5*scipy.fft.rfftfreq(len(y1), d=1)
 y2freq=0.5*scipy.fft.rfftfreq(len(y2), d=1) # in realtà 1, 2, 3, 4 sono tutte uguali
 y3freq=0.5*scipy.fft.rfftfreq(len(y3), d=1)
 y4freq=0.5*scipy.fft.rfftfreq(len(y4), d=1)
 ax[1].plot(y1freq, np.absolute(y1rfft)**2, color='darkturquoise', label="NO2")
 ax[1].plot(y2freq, np.absolute(y2rfft)**2, color='orchid', label="O3")
 ax[1].plot(y3freq, np.absolute(y3rfft)**2, color="cornflowerblue", label="SO2")
 ax[1].plot(y4freq, np.absolute(y4rfft)**2, color='darkorange',   label="CO")
 ax[1].set_ylabel('Potenza')
 ax[1].set_xlabel('Frequenza (1/g)')
 ax[1].set_yscale("log")
 ax[1].set_title('Spettro di potenza') 
 plt.savefig(s+'.png')
 plt.show()

 # filtri
 mask = y1freq > 0.005 # pongo a 0 periodi < 6 mesi (filtro lungo periodo)
 y1filtr, y2filtr, y3filtr, y4filtr = y1rfft.copy(), y2rfft.copy(), y3rfft.copy(), y4rfft.copy()
 y1filtr[mask] = 0
 y2filtr[mask] = 0
 y3filtr[mask] = 0
 y4filtr[mask] = 0
 filtred1 = scipy.fft.irfft(y1filtr, n=len(y1))
 filtred2 = scipy.fft.irfft(y2filtr, n=len(y1))
 filtred3 = scipy.fft.irfft(y3filtr, n=len(y1))
 filtred4 = scipy.fft.irfft(y4filtr, n=len(y1))

 #periodi con coefficiente massimo per ogni inquinante dello stato
 tmax = np.zeros(4)
 tmax[0] = 1/(y1freq[(list(y1rfft)).index(max(y1rfft[1:50]))])
 tmax[1] = 1/(y2freq[(list(y2rfft)).index(max(y2rfft[1:50]))])
 tmax[2] = 1/(y3freq[(list(y3rfft)).index(max(y3rfft[1:50]))])
 tmax[3] = 1/(y4freq[(list(y4rfft)).index(max(y4rfft[1:50]))])
 frase = ('Periodi principali di espressi in giorni: ')

 # Grafico
 fig, ax = plt.subplots(2 ,1 , figsize=(15, 15))
 fig.suptitle('Andamento medio degli inquinanti in '+s+' filtrati sul lungo periodo (T > 6mesi) e\n caratterizzazione del rumore')
 
 ax[0].plot(x,filtred1,c='darkturquoise', label="NO2")
 ax[0].plot(x,filtred2,c='orchid', label="O3")
 ax[0].plot(x,filtred3,c='cornflowerblue', label="SO2")
 ax[0].plot(x,filtred4,c='darkorange', label="CO")
 ax[0].set_ylabel('Inquinante filtrato (ppb)')
 
 ax[0].tick_params(axis='x', labelrotation=15)
 ax[0].xaxis.set_major_locator(mdates.DayLocator(interval=60))
 ax[0].set_title('Andamento temporale inquinanti di '+s+' filtrati sul lungo periodo; ' +frase+ f'\n NO2: {round(tmax[0], 0)}   O3: {round(tmax[1],0)}   SO2: {round(tmax[2],0)}   CO: {round(tmax[3],0)}')
  
 fig.legend(loc="upper right", title="Legenda", frameon=False)
 
 ax[1].plot(y1freq, np.absolute(y1rfft-y1filtr)**2, color='darkturquoise', alpha=0.3)
 ax[1].plot(y2freq, np.absolute(y2rfft-y2filtr)**2, color='orchid', alpha=0.3)
 ax[1].plot(y3freq, np.absolute(y3rfft-y3filtr)**2, color="cornflowerblue", alpha=0.3)
 ax[1].plot(y4freq, np.absolute(y4rfft-y4filtr)**2, color='darkorange', alpha=0.3)

 pNO2, pcovNO2 = fit(y1freq[50:], np.absolute(y1rfft[50:]-y1filtr[50:])**2)
 pO3, pcovO3 = fit(y2freq[50:], np.absolute(y2rfft[50:]-y2filtr[50:])**2)
 pSO2, pcovSO2 = fit(y3freq[50:], np.absolute(y3rfft[50:]-y3filtr[50:])**2)
 pCO, pcovCO = fit(y4freq[50:], np.absolute(y4rfft[50:]-y4filtr[50:])**2)

 ax[1].plot(y1freq[1:], rumore(y1freq[1:], pNO2[0], pNO2[1]), color='darkturquoise') # tolgo la prima frequenza per non dividere per 0 nella funzione rumore ed avere Warning in RunTime
 ax[1].plot(y2freq[1:], rumore(y2freq[1:], pO3[0], pO3[1]), color='orchid')
 ax[1].plot(y3freq[1:], rumore(y3freq[1:], pSO2[0], pSO2[1]), color="cornflowerblue")
 ax[1].plot(y4freq[1:], rumore(y4freq[1:], pCO[0], pCO[1]), color='darkorange')

 ax[1].text(0.2, 5e4, rf'$\beta$ NO2 = {round(pNO2[1],2)}', fontsize=10, color='darkturquoise')
 ax[1].text(0.2, 0.5, rf'$\beta$ O3 = {round(pO3[1],2)}', fontsize=10, color='orchid')
 ax[1].text(0.2, 5e3, rf'$\beta$ SO2 = {round(pSO2[1],2)}', fontsize=10, color='cornflowerblue')
 ax[1].text(0.2, 5e2, rf'$\beta$ CO = {round(pCO[1],2)}', fontsize=10, color='darkorange')
 
 ax[1].set_ylabel('Potenza')
 ax[1].set_xlabel('Frequenza (1/g)')
 ax[1].set_yscale("log")
 ax[1].set_title('Spettro di potenza del rumore con T < 6mesi e fit per caratterizzarlo')
 
 plt.savefig(str(s+'Filtred.png')) 
 plt.show()

 


def subTFinquinanti(x, y, inq): # subplot di andamento temporale, spettro di potenza, filtro per lungo periodo e caratterizzazione rumore per gli inquinanti mediati giornalmente tra tutti gli stati*
 fig, ax = plt.subplots(2 ,1 , figsize=(15, 15))
 fig.suptitle('Andamento medio e analisi di Fourier di un inquinante')
 yrfft=scipy.fft.rfft(y)
 yfreq=0.5*scipy.fft.rfftfreq(len(y), d=1)
 
 if(inq=='NO2'):
  ax[0].plot(x,y,c='darkturquoise', label=inq)
  fig.legend(loc="upper right", title="Legenda", frameon=False) 
  ax[1].plot(yfreq, np.absolute(yrfft)**2, color='darkturquoise', label=inq)
 elif(inq=='O3'):
  ax[0].plot(x,y,c='orchid', label=inq)
  fig.legend(loc="upper right", title="Legenda", frameon=False) 
  ax[1].plot(yfreq, np.absolute(yrfft)**2, color='orchid', label=inq) 
 elif(inq=='SO2'):
  ax[0].plot(x,y,c='forestgreen', label=inq)
  fig.legend(loc="upper right", title="Legenda", frameon=False) 
  ax[1].plot(yfreq, np.absolute(yrfft)**2, color='forestgreen', label=inq) 
 else:
  ax[0].plot(x,y,c='darkorange', label=inq)
  fig.legend(loc="upper right", title="Legenda", frameon=False) 
  ax[1].plot(yfreq, np.absolute(yrfft)**2, color='darkorange', label=inq) 
  
 ax[0].set_title('Andamento temporale '+ inq + ' nei 5 stati')  
 #ax[0].set_xlabel('Data')
 ax[0].set_ylabel('Inquinante (ppb)')
 ax[0].tick_params(axis='x', labelrotation=15)
 ax[0].xaxis.set_major_locator(mdates.DayLocator(interval=60))
 
 ax[1].set_yscale("log")
 ax[1].set_ylabel('Potenza')
 ax[1].set_xlabel('Frequenza (1/g)')
 ax[1].set_title('Spettro di potenza')
 plt.savefig(str(inq+'.png'))
 plt.show()

 # filtri
 mask = yfreq > 0.005 # pongo a 0 periodi < 6 mesi (filtro lungo periodo)
 yfiltr = yrfft.copy()
 yfiltr[mask] = 0
 filtred = scipy.fft.irfft(yfiltr, n=len(y))

 # fit rumore
 par, pcov = fit(yfreq[1:], np.absolute(yrfft[1:]-yfiltr[1:])**2)

 #periodi con coefficiente massimo per ogni inquinante
 tmax = 0
 tmax = 1/(yfreq[(list(yrfft)).index(max(yrfft[1:50]))])
 frase = ('Periodo principale dell\'andamento di '+inq+' mediato espresso in giorni: ')

 # Grafico
 fig, ax = plt.subplots(2 ,1 , figsize=(15, 15))
 fig.suptitle('Andamento medio dell\' inquinante '+inq+' filtrato sul lungo periodo (T > 6mesi) e\n caratterizzazione del rumore')

 if(inq=='NO2'):
  ax[0].plot(x,filtred,c='darkturquoise', label=inq)
  ax[0].text(pd.to_datetime('2000-01-01'), 16, frase + f'{round(tmax, 0)}', fontsize=10, color='darkturquoise')
  fig.legend(loc="upper right", title="Legenda", frameon=False) 
  ax[1].plot(yfreq, np.absolute(yrfft-yfiltr)**2, color='darkturquoise', alpha = 0.3)
  ax[1].plot(yfreq[1:], rumore(yfreq[1:], par[0], par[1]), color='darkturquoise')
  ax[1].text(0.2, 1e3, rf'$\beta$ NO2 = {round(par[1],2)}', fontsize=10, color='darkturquoise')
 elif(inq=='O3'):
  ax[0].plot(x,filtred,c='orchid', label=inq)
  ax[0].text(pd.to_datetime('2000-01-01'), 0.021, frase + f'{round(tmax, 0)}', fontsize=10, color='orchid')
  fig.legend(loc="upper right", title="Legenda", frameon=False) 
  ax[1].plot(yfreq, np.absolute(yrfft-yfiltr)**2, color='orchid', alpha = 0.3)
  ax[1].plot(yfreq[1:], rumore(yfreq[1:], par[0], par[1]), color='orchid')
  ax[1].text(0.2, 0.1, rf'$\beta$ O3 = {round(par[1],2)}', fontsize=10, color='orchid')
 elif(inq=='SO2'):
  ax[0].plot(x,filtred,c='forestgreen', label=inq)
  ax[0].text(pd.to_datetime('2001-04-26'), 6, frase + f'{round(tmax, 0)}', fontsize=10, color='forestgreen')
  fig.legend(loc="upper right", title="Legenda", frameon=False) 
  ax[1].plot(yfreq, np.absolute(yrfft-yfiltr)**2, color='forestgreen', alpha = 0.3)
  ax[1].plot(yfreq[1:], rumore(yfreq[1:], par[0], par[1]), color="forestgreen")
  ax[1].text(0.2, 1e4, rf'$\beta$ SO2 = {round(par[1],2)}', fontsize=10, color='forestgreen')
 else:
  ax[0].plot(x,filtred,c='darkorange', label=inq)
  ax[0].text(pd.to_datetime('2000-01-01'), 0.25, frase + f'{round(tmax, 0)}', fontsize=10, color='darkorange')
  fig.legend(loc="upper right", title="Legenda", frameon=False) 
  ax[1].plot(yfreq, np.absolute(yrfft-yfiltr)**2, color='darkorange', alpha = 0.3)
  ax[1].plot(yfreq[1:], rumore(yfreq[1:], par[0], par[1]), color='darkorange')
  ax[1].text(0.2, 1e2, rf'$\beta$ CO = {round(par[1],2)}', fontsize=10, color='darkorange')

 ax[0].set_ylabel('Inquinante filtrato (ppb)')
 ax[0].tick_params(axis='x', labelrotation=15)
 ax[0].xaxis.set_major_locator(mdates.DayLocator(interval=60))
 ax[0].set_title('Andamento temporale '+inq+' filtrato sul lungo periodo')

 ax[1].set_ylabel('Potenza')
 ax[1].set_xlabel('Frequenza (1/g)')
 ax[1].set_yscale("log")
 ax[1].set_title('Spettro di potenza del rumore con T < 6mesi e fit per caratterizzarlo')
 
 plt.savefig(inq+'Filtred.png')
 plt.show()




def mappa(dataframe, maxx, inq): #funzione per visualizzare mappa andamento inquinanti giornaliero seguendo una scala di colori
    fig = px.choropleth(dataframe,
                        locations='states', 
                        locationmode="USA-states", 
                        scope="usa",
                        color=inq, # inq è il nome dell'inquinante da visualizzare
                        color_continuous_scale="Agsunset_r",
                        range_color = (0, 100),
                        animation_frame = 'date'
                        )
    fig.update_layout(coloraxis_colorbar=dict(
        title= inq + '% rispetto al massimo = ' + str(maxx) ,
        ticks="outside", 
        dtick=50))
    fig.show()
