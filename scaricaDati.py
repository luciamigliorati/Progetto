import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from tqdm import tqdm
from mdl import Stazione
from scipy import constants, optimize
import scipy.fft


### LEGGO IL CSV DEI DATI
mydata = pd.read_csv('pollution_us_2000_2002.csv')
dataLocale = mydata['Date Local']
print('csv originale letto')

inquinamento = mydata[['Site Num','State','County','City','Date Local','NO2 Mean','O3 Mean','SO2 Mean','CO Mean']]
dataLocale = np.sort( pd.to_datetime(inquinamento['Date Local']))
gruppi = inquinamento.groupby(['State'])

### ESTRAGGO DAI GRUPPI OGNUNO DEI 5 STATI PER L'ANALISI
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

print('csv per ognuno dei 5 stati creati:\n New York, District Of Columbia, New Jersey, Massachusetts, Pennsylvania')
