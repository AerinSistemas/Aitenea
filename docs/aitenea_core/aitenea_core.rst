AITenea: aitenea_core
======================

AItenea_core representa la denominada capa de bajo nivel junto con los elementos de funcionalidad programados. La capa de bajo nivel 
está representada por tres tipologías de clase base que describimos a continuación:

    1. Una clase base específica para los métodos propios de *machine learning*.
    2. Una clase para generar tuberías.
    3. Una clase para gestionar los algoritmos genéticos. 

base_class_ai
--------------

Esta clase base es la encargada de estructurar cualquier método de *machine learning* que se quiera implementar. Está constituida por varios 
elementos: **atributos** de la clase, **métodos de funcionalidad** y **métodos abstractos**. Los atributos de la clase definen por un lado el 
nombre de la clase a implementar y por otro los elementos que forman los parámetros de la clase y los parámetros del usuario, todo 
ello a través de un diccionario definido por el programador. Por otro lado el método denominado *check_parameters* es el método encargado 
de comprobar que los datos introducidos por el usuario coinciden con los impuestos por el programador de la clase. De esta manera el 
programador del algoritmo no tiene que prestar atención a los posibles errores que pudiera cometer el usuario de la clase, cualquier error 
ya es manejado de forma adecuada. Finalmente un conjunto de métodos virtuales obligan al programador a implementarlos en su clase, este requerimiento es necesario para hacer compatible el algoritmo con el entorno de AItenea. Hay que decir que esas son las únicas 
obligaciones o restricciones que tiene la herramienta, el resto de operaciones internas que pueda tener el algoritmo no son relevantes, por 
lo que el programador tiene libertad absoluta a la hora de programar su algoritmo. A través de uno de los métodos integrado en la clase base, 
el usuario puede usar el algoritmo implementado en un algoritmo genético. La finalidad de esta clase es poder usar los algoritmos implementados 
en tuberías *Pline* de *Scikit* a través de los métodos abstractos definidos, usando *Dask*, para una programación distribuida. 

.. autoclass:: aitenea.aitenea_core.base_class_ai.BaseClassAI

**Métodos** 

.. automethod:: aitenea.aitenea_core.base_class_ai.BaseClassAI.check_parameters

.. automethod:: aitenea.aitenea_core.base_class_ai.BaseClassAI.get_info

.. automethod:: aitenea.aitenea_core.base_class_ai.BaseClassAI.fit

.. automethod:: aitenea.aitenea_core.base_class_ai.BaseClassAI.predict

.. automethod:: aitenea.aitenea_core.base_class_ai.BaseClassAI.fit_predict

.. automethod:: aitenea.aitenea_core.base_class_ai.BaseClassAI.score



pipe_factory
--------------

Esta clase base permite al usuario construir una *Pline* de AItenea para realizar 
distintas tareas de *machine learning*. La *Pline* estará conformada por uno o 
más pasos de transformación que deben implementar los métodos *fit* 
y *transform*, y solamente un algoritmo de *machine learning* al final de la 
misma que será el estimador y debe implementar el metodo *fit*. 
La clase contiene los métodos para añadir los pasos a la 
tubería, componer la tubería y finalmente crearla.   

.. autoclass:: aitenea.aitenea_core.pfactory.PFactory

**Métodos**

.. automethod:: aitenea.aitenea_core.pfactory.PFactory.add_pipe

.. automethod:: aitenea.aitenea_core.pfactory.PFactory.add_external_pipe

.. automethod:: aitenea.aitenea_core.pfactory.PFactory.compose_pipe_line

.. automethod:: aitenea.aitenea_core.pfactory.PFactory.make_pipe

BaseClassPreprocessing
-----------------------

Esta clase es la encargada de establecer la estructura que deben implementar
las clases cuya funcionalidad es la de transformar datos. 
La clase incluye todos los métodos necesarios para ser usados en una tubería 
*Pline* cumpliendo su papel de transformación de datos, 
por lo cual se recurre a un conjunto de clases abstractas o virtuales que se 
describen a continuación. 


.. autoclass:: aitenea.aitenea_core.base_class_preprocessing.BaseClassPreprocessing

**Métodos**

.. automethod:: aitenea.aitenea_core.base_class_preprocessing.BaseClassPreprocessing.check_parameters

.. automethod:: aitenea.aitenea_core.base_class_preprocessing.BaseClassPreprocessing.get_info

.. automethod:: aitenea.aitenea_core.base_class_preprocessing.BaseClassPreprocessing.init_selector

.. automethod:: aitenea.aitenea_core.base_class_preprocessing.BaseClassPreprocessing.fit

.. automethod:: aitenea.aitenea_core.base_class_preprocessing.BaseClassPreprocessing.transform

.. automethod:: aitenea.aitenea_core.base_class_preprocessing.BaseClassPreprocessing.fit_transform


*Perpetuity*
------------

Esta clase tiene la funcionalidad de gestionar los modelos de AItenea: listado de los modelos 
creados, guardar modelos, o cargar un modelo previamente creado.

.. autoclass:: aitenea.aitenea_core.perpetuity.Perpetuity

**Métodos**    


.. automethod:: aitenea.aitenea_core.perpetuity.Perpetuity.save_model

.. automethod:: aitenea.aitenea_core.perpetuity.Perpetuity.load_model

.. automethod:: aitenea.aitenea_core.perpetuity.Perpetuity.list_models


Decoradores
------------

Los decoradores son muy útiles para reutilizar código que desempeñan tareas comunes y 
ayudan a que nuestro código sea más corto y limpio. En AItenea seguimos 
en esta línea y hemos implementado decoradores. Tanto en las clases de transformación
como en las clases de machine learning los módulos: *fit*, *fit_transform* y *fit_predict* 
deben incluir @fit_decorator. Es una función que asegura la coherencia, entre la 
entrada y salida de los datos en cada tarea del flujo de simulación.

.. code-block:: python
  
    def fit_decorator(func):
        """Decorator to access the transformed input
        Args:
           func (function): fit
        Return (wrapper)
        """
        def fit_wrapper(*args, **kwargs):
            setattr(args[0], 'x_input', args[1])
            if len(args) > 2:
               setattr(args[0], 'y_input', args[2])
            return func(*args, **kwargs)
        return fit_wrapper

Clases implementadas en AItenea
--------------------------------

Como parte del desarrollo de la herramienta, se han implementado 
varios algoritmos que pasamos a describir a continuación.

aitenea_transform
^^^^^^^^^^^^^^^^^^
En este directorio se agrupan aquellos algoritmos que realizan algún 
tipo de transformación de los datos.

*Scaler*
""""""""

Es un algoritmo de transformación de datos. Cuando el conjunto de datos de estudio 
contiene variables que son diferentes en escala, es recomendable transformar los 
mismos de manera que la varianza sea 1 y que la media sea 0.

Esta clase, teniendo la funcionalidad de realizar una transformación de los datos, 
hereda de *BaseClassPreprocessing*.

.. autoclass:: aitenea.aitenea_core.aitenea_transform.scaler.StdScaler

**Métodos**    

.. automethod:: aitenea.aitenea_core.aitenea_transform.scaler.StdScaler.get_info

.. automethod:: aitenea.aitenea_core.aitenea_transform.scaler.StdScaler.init_selector

.. automethod:: aitenea.aitenea_core.aitenea_transform.scaler.StdScaler.fit

.. automethod:: aitenea.aitenea_core.aitenea_transform.scaler.StdScaler.transform

.. automethod:: aitenea.aitenea_core.aitenea_transform.scaler.StdScaler.fit_transform


*Markov Probability*
""""""""""""""""""""

Los modelos de Markov se utilizan a menudo para modelar las probabilidades de los 
diferentes estados del sistema y las tasas de transiciones entre dichos estados. 
El método se utiliza generalmente para modelar sistemas, detectar patrones, hacer 
predicciones y aprender las estadísticas de los datos secuenciales.

Esta clase hereda de *BaseClassPreprocessing*.

.. autoclass:: aitenea.aitenea_core.aitenea_transform.markov_matrix_prob.MarkovMatrixProb


**Métodos**:    

.. automethod:: aitenea.aitenea_core.aitenea_transform.markov_matrix_prob.MarkovMatrixProb.get_info

.. automethod:: aitenea.aitenea_core.aitenea_transform.markov_matrix_prob.MarkovMatrixProb.init_selector

.. automethod:: aitenea.aitenea_core.aitenea_transform.markov_matrix_prob.MarkovMatrixProb.fit

.. automethod:: aitenea.aitenea_core.aitenea_transform.markov_matrix_prob.MarkovMatrixProb.transform

.. automethod:: aitenea.aitenea_core.aitenea_transform.markov_matrix_prob.MarkovMatrixProb.fit_transform


*Emissions*
""""""""""""

Esta es una clase de transformación *ad hoc*. Utilizando los datos recogidos de 
distintos sensores internos y externos, durante un ensayo de homologación de vehículos, 
se aplica la algoritmia necesaria para calcular los factores de emisión de los distintos 
gases contaminantes. 

.. autoclass:: aitenea.aitenea_core.emissions.emissions.Emissions


**Métodos**:    

.. automethod:: aitenea.aitenea_core.emissions.emissions.Emissions.get_info

.. automethod:: aitenea.aitenea_core.emissions.emissions.Emissions.init_selector

.. automethod:: aitenea.aitenea_core.emissions.emissions.Emissions.fit

.. automethod:: aitenea.aitenea_core.emissions.emissions.Emissions.transform

.. automethod:: aitenea.aitenea_core.emissions.emissions.Emissions.fit_transform

*MDistance*
""""""""""""

Esta es una clase de transformación *ad hoc*. Calcula la matriz de distancias entre los eventos
de los nodos una entidad. Si se piensa en ello como una tabla con X filas, tantas como eventos, se anexarán 
a dicha tabla tantas columnas como nodos formen parte de la entidad. Con la tabla 
ordenada cronológicamente, se tendrá en cada fila un 0 en la columna que sea igual al nodo del evento 
que se está analizando y en el resto, el tiempo faltante para el evento siguiente de cada uno de los 
nodos, respectivamente.

.. autoclass:: aitenea.aitenea_core.distance.matrix_distance.MDistance


**Métodos**:    

.. automethod:: aitenea.aitenea_core.distance.matrix_distance.MDistance.get_info

.. automethod:: aitenea.aitenea_core.distance.matrix_distance.MDistance.init_selector

.. automethod:: aitenea.aitenea_core.distance.matrix_distance.MDistance.fit

.. automethod:: aitenea.aitenea_core.distance.matrix_distance.MDistance.transform

.. automethod:: aitenea.aitenea_core.distance.matrix_distance.MDistance.fit_transform


*clustering*
^^^^^^^^^^^^
En este directorio se agrupan aquellos algoritmos de clasificación, sea 
supervisados o no supervisados.

K-Means
""""""""
Es un algoritmo de clasificación no supervisada (clusterización) que agrupa las
variables en *k* grupos basándose en la similitud de sus características. 
La agrupación se realiza minimizando la suma de las distancias entre cada variable
y el centroide de su grupo o cluster. Se suele usar la distancia cuadrática. 
El algoritmo, tal como está implementado en AItenea, incluye una mejora, contiene
un método para calcular el número óptimo de clases *k*.

Esta clase, siendo un algoritmo de *machine learning*, hereda de *BaseClassAI*.

.. autoclass:: aitenea.aitenea_core.clustering.kmeans.Kmeans


**Métodos**:    

.. automethod:: aitenea.aitenea_core.clustering.kmeans.Kmeans.get_info

.. automethod:: aitenea.aitenea_core.clustering.kmeans.Kmeans.init_selector

.. automethod:: aitenea.aitenea_core.clustering.kmeans.Kmeans.fit

.. automethod:: aitenea.aitenea_core.clustering.kmeans.Kmeans.transform

.. automethod:: aitenea.aitenea_core.clustering.kmeans.Kmeans.predict

.. automethod:: aitenea.aitenea_core.clustering.kmeans.Kmeans.fit_transform

.. automethod:: aitenea.aitenea_core.clustering.kmeans.Kmeans.fit_predict

.. automethod:: aitenea.aitenea_core.clustering.kmeans.Kmeans.score

.. automethod:: aitenea.aitenea_core.clustering.kmeans.Kmeans.calculate_optima_nclasses



*Ensemble* (conjunto)
^^^^^^^^^^^^^^^^^^^^^

El objetivo de los métodos de conjunto es combinar las predicciones de varios 
estimadores base construidos con un algoritmo de aprendizaje dado para mejorar 
la robustez y la generalización del algoritmo. 

Esta clase, siendo un algoritmo de *machine learning*, hereda de *BaseClassAI*.

*Random Forest Regressor*
""""""""""""""""""""""""""

Un bosque aleatorio es un estimador que se ajusta a una serie de árboles
de decisión de regresión en varios subconjuntos del conjunto de datos y
utiliza el promedio para mejorar la precisión predictiva y controlar el 
sobreajuste. 


.. autoclass:: aitenea.aitenea_core.ensemble.random_forest.RandomForestRegress


**Métodos**:    

.. automethod:: aitenea.aitenea_core.ensemble.random_forest.RandomForestRegress.get_info

.. automethod:: aitenea.aitenea_core.ensemble.random_forest.RandomForestRegress.init_selector

.. automethod:: aitenea.aitenea_core.ensemble.random_forest.RandomForestRegress.fit

.. automethod:: aitenea.aitenea_core.ensemble.random_forest.RandomForestRegress.transform

.. automethod:: aitenea.aitenea_core.ensemble.random_forest.RandomForestRegress.predict    

.. automethod:: aitenea.aitenea_core.ensemble.random_forest.RandomForestRegress.fit_transform

.. automethod:: aitenea.aitenea_core.ensemble.random_forest.RandomForestRegress.fit_predict

.. automethod:: aitenea.aitenea_core.ensemble.random_forest.RandomForestRegress.score

modelos lineales
^^^^^^^^^^^^^^^^
Este directorio agrupa algoritmos que describen relaciones de tipo lineal 
entre las variables del sistema de estudio.

*Linear Regression*
"""""""""""""""""""

El objetivo de un modelo de regresión lineal es tratar de explicar la 
relación que existe entre una variable dependiente (variable respuesta *Y*)
un conjunto de variables independientes (variables explicativas *X*).
El algoritmo se ajusta a un modelo lineal para minimizar la suma de 
los cuadrados de las diferencias entre los valores reales observados
y los valores estimados por el modelo.

Esta clase, siendo un algoritmo de machine learning, hereda de *BaseClassAI*.

.. autoclass:: aitenea.aitenea_core.linear_models.linear_regression.LRegression


**Métodos**:    

.. automethod:: aitenea.aitenea_core.linear_models.linear_regression.LRegression.get_info

.. automethod:: aitenea.aitenea_core.linear_models.linear_regression.LRegression.init_selector

.. automethod:: aitenea.aitenea_core.linear_models.linear_regression.LRegression.fit

.. automethod:: aitenea.aitenea_core.linear_models.linear_regression.LRegression.transform

.. automethod:: aitenea.aitenea_core.linear_models.linear_regression.LRegression.predict    

.. automethod:: aitenea.aitenea_core.linear_models.linear_regression.LRegression.fit_transform

.. automethod:: aitenea.aitenea_core.linear_models.linear_regression.LRegression.fit_predict

.. automethod:: aitenea.aitenea_core.linear_models.linear_regression.LRegression.score