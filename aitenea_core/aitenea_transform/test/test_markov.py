# -*- coding:utf-8 -*-
"""
Testing for create class

"""
from dask import dataframe
import random
import dask
import pandas as pd

from aitenea.aitenea_core.aitenea_transform.markov_matrix_prob import MarkovMatrixProb


def test_create():
     """Create MarkovMatrixProb, and check with a dummy matrix
     """
     user_parameters = {"options": {
         "window_size": 3, "datetime_field": "date", "main_attribute": "nodehints_dnsname", "future_window": 3 }}
     datetime = pd.date_range(start="2018-01-01 00:00:01",
                              end="2018-01-01 00:00:6", periods=10)
     values = ["A","B","A","C","C","A","A","B","C","B"]
     pandas = pd.DataFrame(({"date": datetime, "nodehints_dnsname": values}))
     pandas["date"] = pandas["date"].astype('datetime64[s]')
     X = dask.dataframe.from_pandas(pandas, npartitions=2)
     result_pandas = pd.DataFrame({"A": [6,3,3], "B": [5, 2, 4], "C": [6, 3, 3]})
     result_pandas.index = ["A", "B", "C"]
     result_pandas = result_pandas/result_pandas.to_numpy().sum()
     print('result',result_pandas)
     print('X',X.compute())
     prob = MarkovMatrixProb(user_parameters)
     test = prob.fit_transform(X).compute()
     print('test',test)
     #assert test.equals(result_pandas)
'''
def test_freq():
    tk = 4700
    user_parameters = {"options": {
        "window_size": 4, "datetime_field": "fec_crea", "main_attribute": "nodehints_dnsname", "future_window": 3 }}
    samples_dns = list("QWER")
    dns = [random.choices(samples_dns, k = tk)[0] for i in range (0, tk)]
    dti = pd.date_range(start = "2018-01-01 00:00:00", end = "2018-01-01 09:00:00", periods=tk)
    pandas_dataframe = pd.DataFrame({"fec_crea": dti, "nodehints_dnsname": dns})
    pandas_dataframe["fec_crea"] = pandas_dataframe["fec_crea"].astype('datetime64[s]')
    dask_dataframe = dataframe.from_pandas(pandas_dataframe, npartitions=2)
    prob = MarkovMatrixProb(user_parameters)
    test = prob.fit_transform(dask_dataframe)
    print(test)
'''