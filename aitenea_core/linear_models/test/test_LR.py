# -*- coding:utf-8 -*-
"""
Testing for create class

"""
import numpy as np
from aitenea.aitenea_core.linear_models.linear_regression import LRegression
from aitenea.exceptions.exceptions  import NotOutputError, NotFitError
import dask.dataframe as df
from dask.distributed import Client
from numpy.testing import assert_array_equal
from sklearn.datasets import make_blobs
from dask_glm.datasets import make_regression
import pandas as pd
from aitenea.aitenea_core.pfactory import PFactory
from aitenea.exceptions.exceptions  import NotOutputError, NotFitError,ValidationError

def test_classLR():
    X, y = make_regression(n_samples=10, n_features=5)
    options = {"penalty":"l2", "tol": 0.0001,"solver": "admm"}   
    parameters = {"options": options}
    lr = LRegression(parameters)


def test_optionsClass():
    """Test that validationError is launched if class parameters are no correctly provided.
    """
    X, y = make_regression(n_samples=10, n_features=5)
    options = {"penalty":"l2", "tol": 0.0001}     
    parameters = {"options": options}
    try:
      LRegression(parameters)
    except ValidationError:
      assert True
    else:
      assert False

def test_NotOutputRegr():
    """The test try linear regression algorithm. Launch a NotOutputError if target values is not given when fit the model     
    """
    X, y = make_regression(n_samples=10, n_features=5)
    options = {"penalty":"l2", "tol": 0.0001,"solver": "admm"}     
    parameters = {"options": options}
    lr = LRegression(parameters)
    try: 
       lr.fit(X,y=None)
    except NotOutputError: 
       assert True
 
def test_predictRegr():
    """Test that NotFitError is launched if try to predict without prevous fit
    """
    X, y = make_regression(n_samples=10, n_features=5)
    X = df.from_array(X)
    y = df.from_array(y)
    options = {"penalty":"l2", "tol": 0.0001,"solver": "admm"}     
    parameters = {"options": options}
    lr = LRegression(parameters)
    try:
        lr.predict(X)
    except NotFitError as err:
        assert True    
    else:
        assert False   

def test_pipeRegr():
    X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
    y = np.dot(X, np.array([1, 2])) + 3
    X = df.from_array(X)
    y = df.from_array(y)
    expected_result = [0.30503452,0.76470639,0.86686245,0.85166531,0.57981735,0.29452749,0.31169408,0.80314646,0.60452741,0.75977622]
    options = {"penalty":"l2", "tol": 0.0001,"solver": "admm"}     
    parameters = {"options": options}
    pipefac = PFactory()
    class_group = "aitenea.aitenea_core.linear_models.linear_regression"
    pipefac.add_pipe("LRegression", class_group, parameters,class_module=class_group)
    pipe = pipefac.make_pipe()
    pipe.fit(X,y)
    assert_array_equal(pipe.predict(df.from_array(np.array([[3,5]]))).compute().tolist(),[14.300100367031217])


def test_pipe_transf_LR():
    """We test that Linear Regression class is crrectly created inside a pipeline with a
      transformation step and a final ai step
    """
    X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
    y = np.dot(X, np.array([1, 2])) + 3
    X = df.from_array(X)
    y = df.from_array(y)
    expected_result = [5.22867025, 6.92956377, 8.06349179, 9.76438531]
    pipefac = PFactory()
    ### first step
    class_group = "aitenea.aitenea_core.aitenea_transform.scaler"
    options = {"with_mean": True, "with_std": True}
    parameters = {"options": options}
    pipefac.add_pipe("StdScaler", class_group, parameters,class_module=class_group)
    ### second step
    options = {"penalty":"l2", "tol": 0.0001,"solver": "admm"}     
    parameters = {"options": options}
    class_group = "aitenea.aitenea_core.linear_models.linear_regression"
    pipefac.add_pipe("LRegression", class_group, parameters,class_module=class_group)
    pipe = pipefac.make_pipe()
    assert_array_equal(np.around(pipe.fit_predict(X,y).compute().tolist(),6), np.around(expected_result,6))