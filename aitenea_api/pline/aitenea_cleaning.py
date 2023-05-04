#Useful packages to manipulate data
import dask.dataframe as dd
import dask.array as dda
import pandas as pd
import numpy as np
import re

# Creation of new class
class NaNValues(object): 
    def __init__(self, source, data):
        """Summary:

        This class has been created in order to deal with NaN Values 
        either remove or replace them. It needs two arguments.        

        Args:
            - source (dictionary): It comes from nodered with the parameters 
            that the user chooses from nodered. The source parameter contains 
            two principal keys(type, options). The source argument at the same time contains another important
            arguments that are explained with more detail below:
                - type_nan: it can be delete or replace the NaN values
                - subsets: it only can be choosen with delete type. Here, 
                  the name of one column or columns can be defined.
                - how: it also is only for NaN delete option. It specifies if 
                  the values to delete are in the index or colums.
                - axis: it is valid for replace type. It can be index or column to relace values
                - method: it is valid only for replace type. There are several methods, 
                  thus for a best understanding of all the methods we can check them 
                  in the official [documentation](https://docs.dask.org/en/latest/generated/dask.dataframe.DataFrame.fillna.html)

            - data (list): It contains three elements. The first one is the number 
            of rows that a dask dataframe contains. The second and third element 
            can be the columns that previously were separated in X and Y respectively.
            There may be cases where the third element can not exist because all the 
            columns can be separated only in the X dataframe.
        """        
        self.type = source['options']['type_nan']
        self.subset_arg = source['options']['subset']
        self.how_selected = source['options']['how']
        self.axis = source['options']['axis']
        self.method = source['options']['method']
        self.data = data
        self.df_dict = dict()
      
    def nan_handling(self):
        """Summary:

        This method allows to delete or replace NaN values.
       
        Returns:
            - message: It returns a message if the NaN values have been
            removed or replaced.
        """                
        dc = self.joining()
        initial_shape_rows, initial_shape_cols = dc.shape[0].compute(), dc.shape[1]
        initial_nan = dc.isna().sum().sum().compute()
        if initial_nan > 0:
            if self.type == 'delete':
                if self.subset_arg == 'None' or self.subset_arg == '':
                    subset_arg = None
                    subset_arg = dc.columns
                else:
                    subset_arg = list(self.subset_arg.split(','))
                if self.axis == 'index':
                    if self.how_selected == 'any':
                        dc = dc[~(dc[subset_arg].isna().sum(axis = 1).compute() > 0)]     
                    else:
                        dc = dc[~(dc[subset_arg].isna().sum(axis = 1).compute() == len(subset_arg))]
                    final_shape = dc.shape[0].compute()
                    message_out = f"{initial_shape_rows - final_shape} rows has been deleted. There are {final_shape} rows available."
                else:
                    if self.how_selected == 'any':
                        subset_arg = np.array(subset_arg)[np.array(dc[subset_arg].isna().sum(axis = 0).compute() > 0)]
                        dc = dc.drop(subset_arg, axis = 1)    
                    else:
                        subset_arg = np.array(subset_arg)[np.array(dc[subset_arg].isna().sum(axis = 0).compute() == len(dc))]
                        dc = dc.drop(subset_arg, axis = 1)
                    final_shape = dc.shape[1]
                    message_out = str(initial_shape_cols - final_shape) + ' columns have been deleted'
                dataframe_out = dc                
            else:
                dataframe_out = dc.fillna(method = self.method, axis = self.axis)
                final_shape = dataframe_out.isna().sum().sum().compute()
                message_out = f"{initial_nan - final_shape} rows has been filled"
            self.df_dict['dataframe'] = dataframe_out
            self.df_dict['message'] = 'NaNs treated'
        else:
            message_out = 'There are not NaN values to treat.'
            self.df_dict['message'] = 'NaNs not treated'
        return message_out

    def get(self):
        """Summary:
        
        This method allows to get the output after NaN handling.

        Returns: 
            - dictionary: It contains two keys. The first key contains a dask dataframe.
            The second key contains a message if the NaN values has been treated or not.
        """        
        return self.df_dict

    def joining(self):
        """Summary:

        This method joins two dask dataframes.

        Returns: 
            - dataset: A single dask dataframe.
        """         
        data_d = self.data
        data_X = data_d[1]
        data_Y = data_d[2]
        if (data_X is not None) and (data_Y is not None):
            raw_data = data_X.join(data_Y)
        else:
            raw_data = data_X
        return raw_data 

        
