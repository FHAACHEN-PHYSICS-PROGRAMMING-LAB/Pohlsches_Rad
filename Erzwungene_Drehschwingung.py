# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
df=pd.read_csv("ErzwungeneDrehschwingung.csv",sep=';')
df1=df.dropna() #Dataframe without NaN

df1 = df1.replace(',','.', regex=True)
#df.iloc[:,0] = [float(str(i).replace(",", ".")) for i in df.iloc[:,0]]
#df.iloc[:,3] = [float(str(i).replace(",", ".")) for i in df.iloc[:,3]]
Spannung=df1.iloc[:,2].astype('float64').to_numpy()

Amplitude=df1.iloc[:,4].astype('float64').to_numpy()
#Bitte in der nächsten Zeile die Kreisfrequenzen eintragen.
Kreisfrequenz=np.array([1.52,1.52,1.77,2.01,2.24,2.46,2.72,2.95,3.04,3.19,3.30,3.34,3.37,3.40,3.44,3.60,3.60,3.71,3.70,3.90,3.94,4.00,4.21,4.40,4.63,4.88,5.34,6.23])

Amplitude=np.round(Amplitude,3)
plt.plot(Kreisfrequenz,Amplitude,label='Messdaten')
plt.xlabel('Kreisfrequenz in rad/s')
plt.ylabel('Amplitude in rad')
plt.xticks(np.arange(1,6, step=.5))

#Estimating 
delta=0.05
N=12
Kreisfrequenz0=3.4
Off=-0.08

def Testfunktion(Kreisfrequenz,N,Kreisfrequenz0,delta,Off):
    return N/(np.sqrt((Kreisfrequenz0**2-Kreisfrequenz**2)**2 +4*delta**2*Kreisfrequenz**2))+Off
popt,pcov=curve_fit(Testfunktion,Kreisfrequenz,Amplitude,[N,Kreisfrequenz0,delta,Off])

#print(popt)

#Bestimme das R^2=1-(Residual Sum of Squares)/(Total Sum of Squars). Das R^2 gibt an, wie gut der Fit bzw. unsere Funktion zu den Daten passt
residuals=Amplitude -Testfunktion(Kreisfrequenz,*popt) #Bestimme die Residuen, die Abweichung von der Amplitude zur Fitfunktion
Res_square=np.sum(residuals**2)#Quadrat der Residuen
ss_tot=np.sum((Amplitude -np.mean(Amplitude))**2)# Bestimmte die totale Quadratsumme
R2=1-Res_square/ss_tot #Bestimmte das R^2
print('Das Bestimmtheitsmass R^2 ist ={}'.format(round(R2,3)))


#Ausgabe der Parameter mit Fehler in der Konsole
print('Die Fitparameter für das N=Drehmoment/Traegheitsmoment ist N = ({} +- {}) 1/s^2'.format(round(popt[0],2),round(np.sqrt(pcov[0][0]),2)))
print('Die Fitparameter für die Resonanzfrequenz ist w0 = ({} +- {}) rad/s'.format(round(popt[1],3),round(np.sqrt(pcov[1][1]),3)))
print('Die Fitparameter für die Dämpfung ist delta =({} +- {}) 1/s'.format(round(popt[2],4),round(np.sqrt(pcov[2][2]),4)))
print('Die Fitparameter für den Offset der Amplitude ist Offset = ({} +- {}) rad'.format(round(popt[3],2),round(np.sqrt(pcov[3][3]),2)))

print('Das R^2 ist {}'.format(round(R2,3))) #Gebe das R^2 in der Konsole aus.





Kreisfrequenz=np.linspace(1,6,50)
plt.plot(Kreisfrequenz, Testfunktion(Kreisfrequenz,*popt),label='fit: N=%5.3f, w0=%5.3f, delta=%5.3f , Off=%5.3f' % tuple(popt))
plt.legend()

plt.savefig("Erzwungene_Drehschwingung.png",dpi=300)
