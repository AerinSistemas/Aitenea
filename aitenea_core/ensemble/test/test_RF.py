# -*- coding:utf-8 -*-
"""
Testing for create class

"""
#from elastictools.aerastic.elastic_index import ElasticIndex, InsertData
#from elastictools.aerastic.elastic_query import ElasticQuery
#from elastictools.aerastic.elastic_index import ElasticIndex
from aitenea.aitenea_core.ensemble.random_forest import RandomForestRegress
import numpy as np
import dask
from dask.distributed import Client
from numpy.testing import assert_array_equal
from sklearn.datasets import make_blobs
from dask_glm.datasets import make_regression
import pandas as pd
from sklearn.model_selection import train_test_split,cross_val_score
import pickle
from aitenea.exceptions.exceptions  import NotOutputError
import matplotlib.pylab as plt
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import GridSearchCV
from aitenea.aitenea_core.pfactory import PFactory
import dask.dataframe as df
from aitenea.exceptions.exceptions  import NotOutputError, NotFitError,ValidationError


def test_optionsRF():
    """Test that ValidaionError is launched if class parameters are not correctly given
    """
    X, y = make_regression(n_samples=10, n_features=4, n_informative=2, chunksize=1)
    options = {"n_estimators":1000, "max_depth": None, 'max_features':'auto','min_samples_leaf':1,} 
    parameters = {"options": options}
    try:
      RandomForestRegress(parameters)
    except ValidationError:
      assert True
    else:
      assert False

def test_classRandForest():
    """Test class creation without error 
    """ 
    X, y = make_regression(n_samples=10, n_features=4, n_informative=2, chunksize=1)
    options = {"n_estimators":1000, "max_depth": None, 'max_features':'auto','min_samples_leaf':1,'min_samples_split':2} 
    parameters = {"options": options}
    forest = RandomForestRegress(parameters)
    
def test_NotOutput():
    """Test NotOutputError, must give value to 'y', otherwise launces error message.
    """
    X, y = make_regression(n_samples=10, n_features=4, n_informative=2, chunksize=1)
    options = {"n_estimators":1000, "max_depth": None, 'max_features':'auto','min_samples_leaf':1,'min_samples_split':2} 
    parameters = {"options": options}
    forest = RandomForestRegress(parameters)
    try: 
       forest.fit(X,y=None)
       assert False
    except NotOutputError: 
       assert True

def test_predictRF():
    """In this fuction we test that NotFitError is launched if the model is not fitted before makeing prediction.
    """
    X, y = make_regression(n_samples=10, n_features=4, n_informative=2, chunksize=1)
    options = {"n_estimators":1000, "max_depth": None, 'max_features':'auto','min_samples_leaf':1,'min_samples_split':2} 
    parameters = {"options": options}
    forest = RandomForestRegress(parameters)
    try:
        forest.predict(X)
    except NotFitError as err:
        assert True    


def test_pipeRandForest():
    """Test that Random Forest algorithm work corectly inside a pipeline
    """
    X, y = make_regression(n_samples=10, n_features=4, n_informative=2,chunksize=1)
   
    options = {"n_estimators":1000, "max_depth": None, 'max_features':'auto','min_samples_leaf':1,'min_samples_split':2} 
    parameters = {"options": options}
    pipefac = PFactory()
    class_group = "aitenea.aitenea_core.ensemble.random_forest"
    pipefac.add_pipe("RandomForestRegress", class_group, parameters,class_module=class_group)
    pipe = pipefac.make_pipe()
    pipe.fit(X,y)
    assert pipe.predict(df.from_array(np.array([[0,0,0,0]]))).compute().size == 1
   

def test_pipe_transf_Randfor():
    """We test that Random Forest class is crrectly created inside a pipeline with a
      transformation step and a final ai step
    """
    X, y = make_regression(n_samples=10, n_features=4, n_informative=2,chunksize=1)
    pipefac = PFactory()
    ### first step
    class_group = "aitenea.aitenea_core.aitenea_transform.scaler"
    options = {"with_mean": True, "with_std": True}
    parameters = {"options": options}
    pipefac.add_pipe("StdScaler", class_group, parameters,class_module=class_group)
    ### second step
    class_group = "aitenea.aitenea_core.ensemble.random_forest"
    options = {"n_estimators":1000, "max_depth": None, 'max_features':'auto','min_samples_leaf':1,'min_samples_split':2} 
    parameters = {"options": options}
    pipefac.add_pipe("RandomForestRegress", class_group, parameters,class_module=class_group)
    pipe = pipefac.make_pipe()
    assert pipe.fit_predict(X,y).compute().size == 10
     
    