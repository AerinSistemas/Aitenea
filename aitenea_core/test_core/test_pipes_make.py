"""
Testing for create pipes

"""
import dask
from dask.distributed import Client
from sklearn.datasets import make_blobs
import pytest
from dask_ml.preprocessing import StandardScaler, MinMaxScaler
import os
from dotenv import load_dotenv
from pathlib import Path

from aitenea.aitenea_core.pfactory import PFactory
from aitenea.exceptions import exceptions
#from elastictools.aerastic.elastic_query import ElasticQuery


dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)

HOST = os.getenv("ELASTIC_HOST")
PORT = os.getenv("ELASTIC_PORT")
USER = os.getenv("ELASTIC_USER")
PASS = os.getenv("ELASTIC_PASS")


def test_factory():
    """Compose a complete pipeline and run it. No transformation
       Pass: Not error 
    """
    pipefac = PFactory()
    class_group = "aitenea.aitenea_core.clustering.kmeans"
    options = {"num_cluster": 2, "method":"k-means||", "auto_optimal_cluster": False}
    parameters = {"options": options}
    pipefac.add_pipe("Kmeans", class_group, parameters,class_module=class_group)
    pipe = pipefac.make_pipe()
    X, _ = make_blobs(n_samples=90000,centers=8, cluster_std=0.60, random_state=0)
    X = dask.array.from_array(X)
    pipe.fit_predict(X)


def test_error_class_factory():
    """Test a raise NotClassError 
       Pass: Raise a NotClassError. Try to create pipe with class 'cluster' but as it does not exist launches NotClassError
    """
    pipefac = PFactory()
    class_group = "aitenea.aitenea_core.clustering.cluster"
    options = {"num_cluster": 2, "method":"k-means||", "auto_optimal_cluster": False}
    parameters = {"options": options} 
    try:
        pipefac.add_pipe("Kmeans", class_group, parameters,class_module=class_group)
        assert False
    except exceptions.NotClassError:
        assert True
    

def test_error_options_factory():
    """Test that rises a ValidationError if class parameters are not correctly provided
    """
    pipefac = PFactory()
    class_group = "aitenea.aitenea_core.clustering.kmeans"
    options = {"num_cluster": 2, "method":"k-means||", }
    parameters = {"options": options} 
    try:
        pipefac.add_pipe("Kmeans", class_group, parameters,class_module=class_group)
        assert False
    except exceptions.ValidationError:
        assert True


def test_pipe_external_arg():
    """Test Pipeline whith external transformation. To compare use the same trasnformation
       ouyside of AItenea
    """
    scaler = MinMaxScaler(feature_range=(-1, 1))
    pipefac = PFactory()
    job_list = (
        {"type": "external_transform", "name": "MinMaxScaler",
         "options": {"feature_range": (-1, 1)}},)
    pipefac.compose_pipe_line(job_list)
    pipe = pipefac.make_pipe()
    X, _ = make_blobs(n_samples=10,
                      centers=8,
                      cluster_std=0.60,
                      random_state=0)
    assert (pipe.fit_transform(X) == scaler.fit_transform(X)).all()


def test_pipe_external_arg2():
    """Test Pipeline whith external transformation and aitea algoritm.
    """
    scaler = MinMaxScaler(feature_range=(-1, 1))
    pipefac = PFactory()
    job_list = [
        {"type": "external_transform", "name": "MinMaxScaler",
         "options": {"feature_range": (-1, 1)}}, ]
    parameters = {"options": { "num_cluster": 10, "method": "k-means++", "auto_optimal_cluster": True}}
    job_list.append({"type": "clustering.kmeans", "name": "Kmeans", "options": parameters})
    pipefac.compose_pipe_line(job_list)
    query = ElasticQuery(
        host=HOST, port=PORT, user=USER,
        password=PASS, dask=True)
    q = {"query": {"match_all": {}}, "_source": ["alcalinity_of_ash", "alcohol", "ash", "color_intensity"]}
    count, result = query.raw_query(
        "wine_dataset", q)
    test, train = result.random_split([0.2, 0.8])
    pipe = pipefac.make_pipe()
    pipe.fit(train)
    test = pipe.predict(test)
