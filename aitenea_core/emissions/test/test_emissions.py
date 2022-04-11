# -*- coding:utf-8 -*-
"""
Testing for create class

"""
import numpy as np
import random
import dask
import pandas as pd
from dask import dataframe
from numpy.testing import assert_array_equal
from aitenea.aitenea_core.emissions.emissions import Emissions
from aitenea.aitenea_core.pfactory import PFactory
from pandas._testing import assert_frame_equal, assert_series_equal



def test_emissionsClass():
    data_init = pd.read_excel("/home/ramona/Desktop/Aerin/emisiones_init2.xlsx")
    data_init = dataframe.from_pandas(data_init, npartitions=1) 
    data_init.repartition(partition_size='100MB')
    options = {'carbono': 1.0,'hidrogeno':1.89,'oxigeno':0.005}
    parameters = {"options": options}
    emisiones = Emissions(parameters)
    emisiones.fit()
    emisiones.transform(data_init)
    


def test_pipeEmissions():
    """Test class Emisions inside a pipeline
    """
    data_init = pd.read_excel("/home/ramona/Desktop/Aerin/emisiones_init2.xlsx")
    
    expected_result = [0.001807,0.001836,0.001828,0.001788,0.001764]
    data_init = dataframe.from_pandas(data_init, npartitions=1) 
    data_init.repartition(partition_size='100MB')
    pipefac = PFactory()
    class_group = "aitenea.aitenea_core.emissions.emissions"
    options = {'carbono': 1.0,'hidrogeno':1.89,'oxigeno':0.005}
    parameters = {"options": options}
    pipefac.add_pipe("Emissions", class_group, parameters,class_module=class_group) 
    pipe = pipefac.make_pipe()
    pipe.fit_transform(data_init, y=None)
    assert_array_equal(np.around(pipe.fit_transform(data_init, y=None)['Work'].head(5).tolist(),5),np.around(expected_result,5))