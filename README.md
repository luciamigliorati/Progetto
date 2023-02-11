# Progetto
* Introduzione
* Descrizione script 
*	Istruzioni per l’esecuzione
* Setup
## **Introduzione**
La consegna del progetto è consultabile al file Inquinanti_USA_2000-2002_202208.pdf.
Il progetto concerne l’analisi degli inquinanti biossido di azoto (NO2), ozono (O3), anidride solforosa (SO2) e monossido di carbonio (CO) rilevati nell’arco dei 3 anni 2000-2002 nei vari stati della metropoli atlantica sulla East Coast degli Stati Uniti, in particolare New York (NY), Distretto di Columbia (DC), New Jersey (NJ), Massachusetts (MA) e Pennsylvania (PA).
La prima parte del codice ha lo scopo di estrarre i dati necessari da *pollution_us_2000_2002.csv* e creare un csv per ognuno dei 5 stati in modo da rendere più agevole la manipolazione dei dati. 
La seconda parte consiste nell’analisi vera e propria dei dati, realizzata confrontando:
* le diverse stazioni in uno stato tramite la media giornaliera di ogni inquinante

* i diversi inquinanti mediati giornalmente su tutti gli stati

* i diversi stati tramite i valori dei quattro inquinanti mediati giornalmente sulle diverse stazioni di ciascuno stato

e riportando i relativi:

* andamenti temporali


* spettri di potenza
 
* coefficienti di correlazione

La terza parte riguarda l’andamento sul lungo periodo. Sono state realizzate delle maschere che filtrano le frequenze basse. La differenza tra dati filtrati e non mette in evidenza il rumore che è stato caratterizzato con un fit.
La quarta e ultima parte mostra alcuni dei risultati con delle mappe animate.
## **Descrizione degli script**
* ***scaricaDati.py** legge il csv dei dati e genera un csv per ogni stato riportando stato, contea, città, numero della stazione di monitoraggio, data e un solo valore medio giornaliero di NO2, O3, SO2, CO.
* **mdl.py** è il modulo in cui è definita la classe “Stazione” con i relativi metodi che implementa una stazione di monitoraggio degli inquinanti.
* **fnzn.py** è il modulo con tutte le varie funzioni richiamate in analsiDati.py.
* **analisiDati.py** contiene tutto il codice di analisi, andamento lungo periodo e mappe descritto nell’introduzione. Importa mdl.py e fnzn.py.
## **Istruzioni d’esecuzione**
Per prima cosa, va eseguito scaricaDati.py che salva automaticamente i csv per ogni stato; una volta salvati i file, non sarà più necessario. Successivamente, eseguendo AnalisiDati.py si potrà accede a tutti i contenuti del progetto. Lo script di analisi salva i grafici in formato png, stampa a terminale le matrici di correlazione e fa visualizzare le mappe. Il codice di analisiDaty.py è diviso in tre “sezioni” da if true/if false: la prima riguarda l’analisi delle stazioni, la seconda quella di inquinanti e stati, la terza le mappe. Cambiando la condizione booleana si può eseguire la prima o la seconda separatamente e anche la terza (a patto di aver eseguito almeno una volta la seconda). Infatti, mentre le prime due sezioni sono indipendenti tra loro, la terza prende i dati dalla seconda per creare le mappe; essendo quest’ultima un’operazione piuttosto lenta, durante la prima esecuzione, i dati necessari sono salvati in csv per non doverlo più rifare, qualora il programma fosse eseguito di nuovo.
## **Setup**
Gli script importano i seguenti pacchetti: Pandas, Numpy, Matplotlib, Scipy, Tqdm, Plotly.
