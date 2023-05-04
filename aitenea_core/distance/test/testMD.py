from aitenea.aitenea_core.distance.matrix_distance import MDistance
from aitenea.aitenea_core.pfactory import PFactory
from elastictools.aerastic.elastic_query import ElasticQuery

def test_init():
    """Se instancia un objeto de la clase con unas opciones."""
    md = MDistance(
        user_parameters={
            "options": {
                "entity": "anagrama",
                "nodes": "nodehints_dnsname",
                "distance_field": "fec_crea",
                "window_size": 60,
            },
            "attributes_types": {},
        }
    )
    assert True

def make_query(host, port, user, password, anagrama):
    """Consulta para tener datos de entrada"""
    query = ElasticQuery(host=host, port=port, user=user, password=password, dask=True)
    q = {"query": {
            "bool": {
                "must": [],
                "filter": [
                    {
                        "bool": {
                            "should": [
                                {
                                    "match_phrase": {
                                        "CI": "\"*" + anagrama + "*\""
                                    }
                                }
                            ],
                            "minimum_should_match": 1
                        }
                    },
                    {
                        "range": {
                            "fec_crea": {
                                "gte": "2019-05-19T04:54:09.422Z",
                                "lte": "2019-07-24T09:12:23.792Z",
                                "format": "strict_date_optional_time"
                            }
                        }
                    }
                ],
                "should": [],
                "must_not": []
            }}}
    count, result = query.raw_query("tsol_ci_test", q)
    return result

def test_MDistance():
    """Se testea que a la clase se le puede pasar una entrada y hacer fit y transform.
    """
    result = make_query()
    md = MDistance(user_parameters = {'options': {'entity': 'anagrama', 'nodes': 'nodehints_dnsname', 'distance_field': 'fec_crea', 'window_size': 600}, 'attributes_types': {}})
    md = md.fit(result)
    md.transform()
    assert True

def test_pipeMDistance():
    """Se intenta meter la clase en una pipeline de AITenea.
    """
    X = make_query()
    pipefac = PFactory()
    class_group = "distance.matrix_distance"
    options = {'entity': 'anagrama', 'nodes': 'nodehints_dnsname', 'distance_field': 'fec_crea', 'window_size': 60}
    parameters = {"options": options}
    pipefac.add_pipe("MDistance", class_group, parameters)
    pipe = pipefac.make_pipe()
    print(X)
    pipe.fit(X, y=None)
    pipe.transform(None)
    # pipe.fit_transform(X, y=None)
    assert True

if __name__ == '__main__':
    test_pipeMDistance()