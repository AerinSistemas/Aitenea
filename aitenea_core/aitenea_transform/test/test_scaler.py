
import dask
import pandas as pd
from aitenea.aitenea_core.aitenea_transform.scaler import StdScaler
from aitenea.aitenea_core.pfactory import PFactory
from sklearn.datasets import make_blobs
from pandas._testing import assert_frame_equal
from aitenea.exceptions import exceptions


def test_classScaler():
   """we test that class is created without error, it transforms data and compare with expected result
   """
   datax = [[0, 0], [0, 0], [1, 1], [1, 1]]
   X = dask.array.from_array(datax)
   X = dask.dataframe.from_array(X)
   X = X.repartition(partition_size='100MB')
   expected_result = [[-1.0,-1.0],[-1.0,-1.0],[1.0,1.0],[1.0,1.0]]
   expected_result = pd.DataFrame(expected_result)
   class_group = "aitenea.aitenea_core.aitenea_transform.scaler"
   options = {"with_mean": True, "with_std": True}
   parameters = {"options": options}
   std = StdScaler(parameters)
   assert_frame_equal(std.fit_transform(X).compute(),expected_result)

def test_optionsScaler():
   """we test that ValidationError is launched if class options are not correctly provided
   """
   datax = [[0, 0], [0, 0], [1, 1], [1, 1]]
   X = dask.array.from_array(datax)
   X = dask.dataframe.from_array(X)
   X = X.repartition(partition_size='100MB')
   expected_result = [[-1.0,-1.0],[-1.0,-1.0],[1.0,1.0],[1.0,1.0]]
   expected_result = pd.DataFrame(expected_result)
   class_group = "aitenea.aitenea_core.aitenea_transform.scaler"
   options = {"with_mean": True,}
   parameters = {"options": options}
   try:
      StdScaler(parameters)
   except exceptions.ValidationError:
      assert True
   else:
      assert False     
   

def test_pipeScaler():
   """We test that StdScaler class is crrectly created inside a pipeline and that 
       transformation of data is correctly performed
   """
   pipefac = PFactory()
   class_group = "aitenea.aitenea_core.aitenea_transform.scaler"
   options = {"with_mean": True, "with_std": True}
   parameters = {"options": options}
   pipefac.add_pipe("StdScaler", class_group, parameters,
                     class_module=class_group)
   pipe = pipefac.make_pipe()
    
   datax = [[0, 0], [0, 0], [1, 1], [1, 1]]
   datay = [[3], [2], [1], [3]]
   expected_result = [[-1.0,-1.0],[-1.0,-1.0],[1.0,1.0],[1.0,1.0]]
   expected_result = pd.DataFrame(expected_result)  
   X = dask.array.from_array(datax)
   X = dask.dataframe.from_array(X)
   X = X.repartition(partition_size='100MB')
   y = dask.array.from_array(datay)
   y = dask.dataframe.from_array(y)
   y = y.repartition(partition_size='100MB')
   assert_frame_equal(pipe.fit_transform(X, y).compute(),expected_result)

    
    