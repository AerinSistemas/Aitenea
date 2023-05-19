import dask
import pandas as pd
from aitenea.aitenea_core.aitenea_transform.scaler import StdScaler
from aitenea.aitenea_core.socio.ace import Ace
from aitenea.aitenea_core.pfactory import PFactory
from sklearn.datasets import make_blobs
from pandas._testing import assert_frame_equal
from aitenea.exceptions import exceptions


def test_pipe_ace():
   """We test that Ace class is correctly created inside a pipeline
   """
   #path =  AÑADIR DATA 
   pipefac = PFactory()
   class_group = "aitenea.aitenea_core.socio.ace"
   options = {}
   parameters = {"options": options}
   pipefac.add_pipe("Ace", class_group, parameters,
                     class_module=class_group)
   pipe = pipefac.make_pipe()
   #An example has been added
   datax = [[0, 0], [0, 0], [1, 1], [1, 1]]
   #my_df = dd.read_csv()
   #df_pandas = my_df.compute()
   X = dask.array.from_array(my_df)
   X = dask.dataframe.from_array(X)
   X = X.repartition(partition_size='100MB')
   a = pipe.transform(df_pamdas)
   print('THIS IS THE TYPE DATA OF COMPUTE: ', type(a) )
   
   print('THIS IS THE OUTPUT: ', a)
   print('TEST FINISHED ')
test_pipe_ace()