import os
import sys
import time
import numpy as np
import pandas as pd
from dask import dataframe as dd
from datetime import timedelta
from aitenea.aitenea_core.base_class_preprocessing import BaseClassPreprocessing
from aitenea.logsconf.log_conf import logging_config


class MDistance(BaseClassPreprocessing):
    """[summary]

    Args:
        BaseClassPreprocessing ([type]): [description]
    """
    options = {
        'entity':
        {"type": "str", "range": None, "default": "", "gen": False},
        'nodes':
        {"type": "str", "range": None, "default": "", "gen": False},
        "distance_field":
        {"type": "str", "range": None, "default": "", "gen": False},
        "window_size":
        {"type": "int", "range": [60, 1, 60], "default": 60, "gen": False},
        "percentage_threshold":
        {"type": "int", "range": [0, 10, 100], "default": 50, "gen": False},
    }

    def __init__(self, user_parameters, user_genetic_parameters=None):
        class_options = {
            'entity': {
                'type': 'str', 'default': 'anagrama'
            },
            'nodes': {
                'type': 'str', 'default': 'nodehints_dnsname'
            },
            'distance_field': {
                'type': 'str', 'default': 'fec_crea'
            },
            'window_size': {
                'type': 'int', 'default': 60
            },
            'percentage_threshold': {
                'type': 'int', 'default': 50
            }
        }
        attributes_types = {}
        self.class_parameters = {'options': class_options, 'attributes_types': attributes_types}
        super(MDistance, self).__init__(
            self.__class__.__name__, self.class_parameters, user_parameters
        )

    def get_info(self):
        description = """
        Transformación de AITenea que calcula las distancias temporales entre los eventos de distintos nodos de una misma entidad.
        Para cada evento, calcula la distancia con el evento inmediatamente siguiente de cada uno del resto de nodos de la entidad.
        Se debe indicar qué columna representa a los nodos ('nodes') y qué columna establece el momento en el que ocurre el evento 
        ('distance_field'), que será la utilizada para el cálculo de la distancia."""
        return description

    def init_selector(self):
        pass

    def fit(self, X, y=None):
        """[summary]

        Args:
            X ([dask dataframe]): conjunto de datos para el análisis
        """
        df = X.compute() # Comprobar que es dask, si no, no hacer compute
        options = self.parameters_values['options']
        # Se ordena cronológicamente de manera inversa, para hacer más óptimos los cálculos de distancia
        df = df.sort_values(by=[options['distance_field'], 'state'], ascending=False)
        # Se eliminan ids (eventos) duplicados
        df = df.drop_duplicates(subset=['id', options['distance_field']], keep='last') # Con el orden anterior de 'state' se mantiene la que sea CLOSED
        df = df.reset_index()
        # Se establecen los nodos/hosts que existen y se crean sus columnas pobladas de NaNs
        hosts = df[options['nodes']].unique()
        for host in hosts:
            df[host] = np.nan
        prev_index = 0
        # Se itera fila por fila
        for i in df.iterrows():
            index = i[0]
            prev_row = df.iloc[prev_index]
            # Se calcula la diferencia con la fila anterior
            difference = prev_row[options['distance_field']] - i[1][options['distance_field']]
            for host in hosts:
                if i[1][options['nodes']] == host:
                    # Si el nodo es el actual, se pone a 0
                    value = timedelta(0)
                else:
                    # Si el nodo es diferente del actual, se le añade la diferencia previamente calculada
                    value = difference + prev_row[host]
                # Se asigna el valor calculado
                df.at[index, host] = value
            prev_index = index
        # Se reordena a cronológico natural
        df = df.sort_values(by=options['distance_field'], ascending=True)
        df = df.reset_index(drop=True) # Revisar si es necesario
        self.mind = df
        return self

    def fit_transform(self, X, y=None): #DE MOMENTO NO USAR
        """[summary]

        Args:
            X ([dask dataframe]): conjunto de datos para el análisis
        """

        self.fit(X, y)
        return self.transform()

    def transform(self, X=None):
        options = self.parameters_values['options']
        df = self.mind.copy()
        # Se prescinde de los nans para poder hacer la matriz de cuentas. Se puede valorar eliminar los registros donde empiezan,
        # pero se perderían algunos valiosos.
        df = df.fillna(timedelta(0))
        hosts = df[options['nodes']].unique()
        # Se pasan los valores de las diferencias de timedeltas a segundos
        for host in hosts:
            df[host] = df[host].dt.total_seconds()
        results = dict()
        aux = pd.DataFrame()
        for host in hosts:
            results[host] = dict()
            dff = df[df[options['nodes']] == host]
            for host2 in hosts:
                value = dff[(dff[host2]<options['window_size']) & (dff[host2] > 0)].copy()
                if len(value) >0:
                    # Se añade a cada evento origen y destino para facilitar el análisis de posprocesado
                    value.loc[:, ('ori')] = host
                    value.loc[:, ('dest')] = host2
                    aux = aux.append(value)
                d = {host2: len(value)}
                results[host].update(d)
        results = pd.DataFrame(results)
        # Se anexa la cuenta de eventos por nodo y se nombra adecuadamente
        results = results.join(df.groupby(options['nodes'])['index'].count())
        results = results.rename(columns={'index': 'events_per_node'})
        # print(results)
        # Se pasa la matriz a porcentaje
        for host in hosts:
            results.loc[:, host] = 100 * results.loc[:, host] / results.loc[:, 'events_per_node']
        aux['time_next'] = 0
        aux['perc'] = 0
        # Se procesa para que cada evento refleje la diferencia entre los nodos origen y destino y desaparezcan las columnas de nodos
        for i in aux.iterrows():
            index = i[0]
            node = i[1]['dest']
            aux.at[index, 'time_next'] = aux.at[index,node]
            aux.at[index, 'perc'] = results.at[i[1]['ori'], i[1]['dest']]
        aux = aux.drop(hosts, axis=1)
        # Se guarda la matriz cuadrada en un csv. Esto habrá que personalizarlo y/o mejorarlo
        PATH = os.getenv("PATH_MODELS")
        results.to_csv(PATH + '/aitenea_results_' + str(options['entity']) + '.csv')
        aux = aux[aux['perc'] >= options['percentage_threshold']]
        aux['anagrama'] = options['entity']
        aux = aux.reset_index(drop=True)
        return dd.from_pandas(aux, npartitions=1)