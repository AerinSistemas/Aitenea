from dask import array 
from dask.dataframe import from_array, from_pandas
from pandas import DataFrame
from dask_ml import model_selection
from dask_ml.preprocessing import StandardScaler
import pytest
import os
from dotenv import load_dotenv
from pathlib import Path

from aitenea.aitenea_core.pfactory import PFactory
from aitenea.aitenea_core.clustering.kmeans import Kmeans
from aitenea.exceptions import exceptions
from elastictools.aerastic.elastic_query import ElasticQuery
from elastictools.aerastic.elastic_index import ElasticIndex, InsertData
from aitenea.aitenea_core.perpetuity import Perpetuity

dotenv_path = Path('../')
load_dotenv(dotenv_path=dotenv_path)

HOST = os.getenv("ELASTIC_HOST")
PORT = os.getenv("ELASTIC_PORT")
USER = os.getenv("ELASTIC_USER")
PASS = os.getenv("ELASTIC_PASS")

def test_elastic():
    """This test check the integration of the aitenea and the elastictools tool
    A data series is read from elasticsearch, then a classification is performed, and the
    result is added to elastic.
    """
    query = ElasticQuery(
        host=HOST, port=PORT, user=USER,
        password=PASS, dask=True)
    q = {"query": {"match_all": {}}, "_source": ["alcalinity_of_ash", "alcohol", "ash", "color_intensity"]}
    count, result = query.raw_query(
        "wine_dataset", q)
    test, train = result.random_split([0.2, 0.8])
    options = {"num_cluster": 10 , "method": "k-means++",
               "auto_optimal_cluster": True}
    parameters = {"options": options}
    testk = Kmeans(parameters)
    testk.fit(train.to_dask_array(lengths=True))
    predict = testk.predict(test.to_dask_array(lengths=True))
    pandas_predict = DataFrame(predict.compute(), columns = ["predictions"])
    predict = from_pandas(pandas_predict, npartitions = test.npartitions)
    test = test.reset_index()
    to_elastic = test.join(predict)
    to_elastic = to_elastic.drop('index', axis=1)
    elas = ElasticIndex(HOST, PORT, USER, PASS)
    pandas_head = to_elastic.head()
    elas.set_index_from_pandas("wine_class", pandas_head)
    multi_ingest = InsertData(HOST, PORT, USER, PASS)
    multi_ingest.insert_dask(to_elastic, "wine_class", "dask", index_id=True)





    
    







