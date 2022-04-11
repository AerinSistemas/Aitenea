from sklearn.datasets import make_blobs
import dask
import pytest


from aitenea.aitenea_core import perpetuity
from aitenea.aitenea_core.pfactory import PFactory


def test_save_model():
    """Create a model inside a pipline and save it 
    """
    pipefac = PFactory()
    class_group = "aitenea.aitenea_core.clustering.kmeans"
    options = {"num_cluster": 10, "method": "k-means++",
               "auto_optimal_cluster": True}
    parameters = {"options": options}
    pipefac.add_pipe("Kmeans",class_group, parameters,class_module=class_group )
    pipe = pipefac.make_pipe()
    X, _ = make_blobs(n_samples=90000,centers=8,cluster_std=0.60,random_state=0)
    X = dask.array.from_array(X)
    pipe.fit_predict(X)
    perp = perpetuity.Perpetuity("admin")
    metadata = {"info_model":{
        "model_name": "Prueba_2", "user": "admin",
        "date": "2021-03-07 20:48:11"}}    
    perp.save_model(metadata, pipe)

def test_list_models():
    """Test list of all models for a user
    """
    perp = perpetuity.Perpetuity("admin")
    models = perp.list_models()
    print('LIST OF MODELS',models)

def test_load():
    """Test loading a model previously saved
    """
    perp = perpetuity.Perpetuity("admin")
    model, metadata = perp.load_model("Prueba_2")
    X_test = [[ 1.24258802 , 4.50399192]]
    predict = model.predict(X_test)
    assert predict.compute() == [3]
