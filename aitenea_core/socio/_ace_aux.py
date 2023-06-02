import numpy as np
import pandas as pd
from sklearn.utils import resample
import scipy
#import matplotlib.pyplot as plt

# por el uso de la función append en vez de concat es necesario suprimir ciertos mensajes molestos
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

class _AceAux(object):
    def __init__(self):
        pass

    def calculate(self, data):
        print('PASSING THROUGH CALCULATE *****')
        return data*8
    
    def ace(self, data):
        """

        Esta función recibe un conjunto de datos en formato csv o como un data frame depurado y devuelven los resultados de un análisis coste - efctividad

        Entrada
        ----------
        datos: [path del fichero csv o pandas DataFrame]
        los datos correspondientes al grupo experiemtal y control (identificados por una variable dicotómica) en cuanto a costes y 
        resultados en la variable de efectividad

        la estructura del fichero (ya se un df o un csv) debe ser la siguiente: (estos serán los nombres de las variables)
        - grupo cotrol: variable que identificará si el sujeto pertenece al grupo control o al experimental (0 exp, 1 control)
        - costes: variable que determina los costes en los que se incurre con cada sujeto 
        - efectividad: variable que dará el valor de la efectividad en cada caso para cada sujeto

        Returns
        -------
        data frame 1
            en él se tendrá información de la distribución del RCEI tras una simulación bootstrap que podrá ser utilizada para la construcción
            de gráficos
        data frame 2
            en él se tendrá información sobre el IC al 95% para el RCEI, la media de los costes y la media de la variable de efectividad para cada grupo
        data frame 3 
            en él se tendrá información de la media y la desviación típica del RCEI, el coste medio y la efectividad media para cada grupo
        
        """

        # se comprueba si el objeto de entrada es un df y si no lo es se lee el csv que se ha dado en su lugar
        if type(data) != pd.core.frame.DataFrame:
            print('YES. IT IS DIFFERENT')
            #datos = datos = pd.read_csv(datos)
        else:
            print('No***')
        #UPLOAD DATA FROM CSV WITH DASK
        #result = dd.read_csv(csv_path, blocksize=100e6,
        #                     sep=dialect.delimiter, assume_missing=True)
        


        """
        # separación del grupo control y el experimental
        exp = datos.loc[datos['grupo control'] == 0]
        control = datos.loc[datos['grupo control'] == 1]

        # data frame en el que se guardarán los resultados del remuestreo bootstrap
        remuestreo = pd.DataFrame(columns = ['rcei', 'coste_medio_exp', 'coste_medio_control', 'efectividad_media_exp', 'efectividad_media_control'])

        # remuetreo bootstrap en el que se van guardando los resultados de interés de este 
        for i in range(0,1000):

            bootstrap_exp = resample(exp)
            bootstrap_control = resample(control)

            costemedioexp = bootstrap_exp['costes'].mean()
            costemediocontrol = bootstrap_control['costes'].mean()
            efectividadmediaexp = bootstrap_exp['efectividad'].mean()
            efectividadmediacontrol = bootstrap_control['efectividad'].mean()
            rcei = (costemedioexp - costemediocontrol)/(efectividadmediaexp - efectividadmediacontrol)

            remuestreo = remuestreo.append({'rcei': rcei, 'coste_medio_exp': costemedioexp, 'coste_medio_control': costemediocontrol, 'efectividad_media_exp': efectividadmediaexp, 'efectividad_media_control': efectividadmediacontrol}, ignore_index = True)    

        # data frame con los descriptivos de interés de cada elemento del data frame remuestreo
        stats = remuestreo.describe()
        stats = stats.iloc[[1, 2]]


        # creación del data frame que contiene la información de los intervalos de confianza para la media de cada elemento del data frame remuestreo
        intervalos = pd.DataFrame(columns = ['var', 'ic'])

        for i in remuestreo.columns:
            ic = scipy.stats.t.interval(0.95, 999, loc=remuestreo[i].mean(), scale=scipy.stats.sem(remuestreo[i]))
            print(i, ic)
            intervalos = intervalos.append({'var': i, 'ic': ic}, ignore_index = True)

        # creación del data frame para la representación de la distribución del willingnes to pay x incremento de efectividad
        remuestreo['mC'] = remuestreo['coste_medio_exp'] - remuestreo['coste_medio_control']
        remuestreo['mE'] = remuestreo['efectividad_media_exp'] - remuestreo['efectividad_media_control']

        ceac = pd.DataFrame(columns = ['wtp', 'propPos'])

        for wtp in np.arange(0, 1001, 5):
            propPos = np.mean((wtp * remuestreo.mE - remuestreo.mC) > 0)

            ceac = ceac.append({'wtp': wtp, 'propPos': propPos}, ignore_index=True) 

        return stats, intervalos, ceac
        """
    
