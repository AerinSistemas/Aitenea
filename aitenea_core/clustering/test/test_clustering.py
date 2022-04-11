from aitenea.aitenea_core.clustering.kmeans import Kmeans
from aitenea.aitenea_core.pfactory import PFactory
import dask
from numpy.testing import assert_array_equal
from aitenea.exceptions.exceptions  import NotOutputError, NotFitError,ValidationError

meth1 = "k-means||"
meth2 = "k-means++"

def test_createClass():
    """The test try kmeans class constructor. 
       The test is passed if the class is created without errors 
    """
    options = {"num_cluster": 2, "method": meth1,
               "auto_optimal_cluster": False}
    parameters = {"options": options}
    Kmeans(parameters)
    gen_options = {"fitness_functions": "calinski-harabasz"}
    gen_parameters = {"options": gen_options}
    Kmeans(parameters, gen_parameters)

def test_optionsClass():
    """The test try kmeans class constructor. 
       Launches ValidationError if class parameters are no correctly provided
    """
    options = {"num_cluster": 'auto', "method": meth1,}
    parameters = {"options": options}

    try:
      Kmeans(parameters)
    except ValidationError:
      assert True
    else:
      assert False  
    
def test_clasification():
    """The test try kmeans clasification. 
       The test is passed if the class is created without error and make a correct prediction
    """
    X = dask.array.from_array([[0, 0], [0.5, 0], [0.5, 1], [1, 1]])
    options = {"num_cluster": 2, "method": meth1, "auto_optimal_cluster": False}
    parameters = {"options": options}
    test = Kmeans(parameters)
    assert_array_equal(test.fit_predict(X).compute(), [0, 0, 1, 1])

 
def test_auto_cluster():
    """Test that auto_optimal_method finds the correct number of clusters
    """
    X = dask.array.from_array([[0, 0], [0.5, 0], [0.5, 1], [1, 1]])
    options = {"num_cluster": 7, "method": meth2,"auto_optimal_cluster": True}
    parameters = {"options": options}
    test = Kmeans(parameters).fit(X)
    assert test.mind.n_clusters == 3
    assert_array_equal(test.predict(X).compute(), [0, 0, 2, 1])

def test_predictCluster():
    """In this fuction un test that NotFitError is launched if the model is not fitted before makeing prediction.
    """
    X = dask.array.from_array([[0, 0], [0.5, 0], [0.5, 1], [1, 1]])
    options = {"num_cluster": 7, "method": meth2,"auto_optimal_cluster": True}
    parameters = {"options": options}
    test = Kmeans(parameters)
    try:
        test.predict(X)
    except NotFitError as err:
        assert True    
   
def test_pipeCluster():
    """We test that Kmeans class is corectly created inside a pipeline and that 
       transformation of data is correctly performed
    """
    X = dask.array.from_array([[0, 0], [0.5, 0], [0.5, 1], [1, 1]])
    pipefac = PFactory()
    class_group = "aitenea.aitenea_core.clustering.kmeans"
    options = {"num_cluster": 2, "method": meth1, "auto_optimal_cluster": False}
    parameters = {"options": options}
    pipefac.add_pipe("Kmeans", class_group, parameters,class_module=class_group)
    pipe = pipefac.make_pipe()
    pipe.fit(X)
    assert_array_equal(pipe.fit_predict(X).compute(), [0, 0, 1, 1])


def test_pipe_transf_Cluster():
    """We test that Kmeans class is crrectly created inside a pipeline with a
      transformation step and a final ai step
    """
    datax = [[0, 0], [0, 0], [1, 1], [1, 1]]
    X = dask.array.from_array(datax)
    X = dask.dataframe.from_array(X)
    X = X.repartition(partition_size='100MB')
    pipefac = PFactory()
    class_group = "aitenea.aitenea_core.aitenea_transform.scaler"
    options = {"with_mean": True, "with_std": True}
    parameters = {"options": options}
    pipefac.add_pipe("StdScaler", class_group, parameters,class_module=class_group)
    class_group = "aitenea.aitenea_core.clustering.kmeans"
    options = {"num_cluster": 2, "method": meth1, "auto_optimal_cluster": False}
    parameters = {"options": options}
    pipefac.add_pipe("Kmeans", class_group, parameters,class_module=class_group)
    pipe = pipefac.make_pipe()
    pipe.fit(X)
    assert_array_equal(pipe.fit_predict(X).compute(), [1, 1, 0, 0])
    
