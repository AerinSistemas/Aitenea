import dask
from aitenea.aitenea_core.clustering.kmeans import Kmeans
from aitenea.aitenea_core.pfactory import PFactory
from sklearn.datasets import make_blobs
from pandas._testing import assert_frame_equal

def test_pipe():
    """Compose a complete pipeline and run it. No transformation
       Pass: Not error
    """
    pipefac = PFactory()
    class_group = "aitenea.aitenea_core.clustering.kmeans"
    options = {"num_cluster": 20, "method": "k-means++",
               "auto_optimal_cluster": False}
    parameters = {"options": options}
    pipefac.add_pipe("Kmeans", class_group, parameters,
                     class_module=class_group)
    pipe = pipefac.make_pipe()
    X, _ = make_blobs(n_samples=90000,centers=8,cluster_std=0.60,
                      random_state=0)
    X = dask.dataframe.from_array(X)
    pipe.fit_predict(X=X)
    pipe.predict(X)
    assert type(pipefac.get_input()[0]) == type(X)
    assert_frame_equal(pipefac.get_input()[0].compute(), X.compute())

def test_factory_scaler():
    pipefac = PFactory()
    class_group = "aitenea.aitenea_core.aitenea_transform.scaler"
    options = {"with_mean": True, "with_std": False}
    parameters = {"options": options}
    pipefac.add_pipe("StdScaler", class_group, parameters,class_module=class_group)
    pipe = pipefac.make_pipe()
    datax = [[0, 0], [0, 0], [1, 1], [1, 1]]
    datay = [[3], [2], [1], [3]]
    expected_result = [[-0.5,-0.5],[-0.5,-0.5],[0.5,0.5],[0.5,0.5]]
    expected_result = dask.array.from_array(expected_result)
    expected_result = dask.dataframe.from_array(expected_result)
    expected_result = expected_result.repartition(partition_size='100MB')
    X = dask.array.from_array(datax)
    X = dask.dataframe.from_array(X)
    X = X.repartition(partition_size='100MB')
    y = dask.array.from_array(datay)
    y = dask.dataframe.from_array(y)
    y = y.repartition(partition_size='100MB')
    assert_frame_equal(pipe.fit_transform(X=X).compute(), expected_result.compute())


                                      
