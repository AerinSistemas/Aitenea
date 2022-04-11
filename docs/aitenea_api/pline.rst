***********************
AITenea: aitenea_api
***********************

*Aitenea_api* representa la capa de negocio (o llamada capa intermedia). Esta capa proporciona una *API REST*
totalmente funcional que sirve como interfaz entre una capa de alto nivel y el núcleo o *aitenea_core*. 

La *API REST* ha sido dividida en distintas aplicaciones según la funcionalidad que desempeñan. 

Funcionalidades
^^^^^^^^^^^^^^^^^^^

La API de AItenea debe tener una serie de funcionalidades tales que un usuario pueda, desde ella:

*  Crear *Plines* con los pasos que considere, a elegir entre los ya disponibles en AItenea o los incluidos por él mismo.
*  Entrenar modelos de *machine learning* con tuberías creadas por él.
*  Usar tuberías creadas por cualquier otro usuario (siempre que tenga acceso), para entrenar modelos de *machine learning*.
*  Usar modelos previamente entrenados para hacer predicciones con nuevos datos.
*  Determinar fuentes y destinos de datos, manejando los diferentes conectores disponibles en cada momento.

Elementos
^^^^^^^^^^^^^^

La API está formada por los siguientes elementos:

    1. Modelos.
    2. Serializadores.
    3. URLs.
    4. Vistas.
    5. Tests.

Modelos
==================================

Los modelos son las clases que dan forma a lo que se podría asimilar como las tablas de la base de datos de la aplicación. 
Un modelo va a definir un objeto y en él sus atributos y funciones.

AItenea dispone de modelos para definir:
    - Clases de transformaciones o algoritmos de AItenea: modelo *AiteneaClass*.
    - Tuberías o *Plines*: modelo *Pline*.
    - Pasos de las *Plines*: modelo *Step*.

*AiteneaClass*
----------------------------------

Este modelo sirve para definir las clases tanto de *preprocessing* como de *ai* que están implementadas en *aitenea_core*. 
Los campos que las define son:

* *class_name*: nombre de la clase.
* *type*: tipo de la clase, a elegir entre: *ai* o *transform*.
* *options*: opciones de parametrización de la clase. Los parámetros se deben introducir en formato JSON.

.. autoclass:: pline.models.AiteneaClass

*Step*
----------------------------------

Este modelo sirve para definir cada paso de una tubería. Los campos que define son:

* *pline_id*: *id* de la *Pline* a la que pertenece. Debe existir dado que trabaja como clave secundaria.
* *step_number*: número del paso dentro de la *Pline*. El orden debe ser desde el inicio al final.
* *step_name*: nombre de la clase que ejecuta el paso. Debe ser una clase existente en *AiteneaClass*.
* *step_type*: tipo de la clase que ejecuta el paso. Puede haber varios pasos tipo *transform* y solamente uno de tipo *ai*, que debería ser el último en cuanto a orden.
* *step_options*: opciones de configuración para cada paso. Los parámetros se pasan en formato JSON.

.. autoclass:: pline.models.Step

*Pline*
---------

Compone cada paso de la *Pline*. Hereda de *models.Model* de *Django*. Los campos que define son:

* *name*: Nombre que el usuario da a la *Pline*.
* *description*: breve descripción con el propósito de que sea útil al usuario.
* *path*: ruta donde se guardará el modelo entrenado. Si no se indica se usará la ruta por defecto.
* *fitted*: campo booleano que indica si el modelo ya ha sido entrenado *True* o no *False*.
* *owner*: campo identificador del usuario de *Django* propietario de la *Pline*.
* *creation_timestamp*: fecha de creación de la *Pline* en base de datos. Estos datos se rellenan de forma automática.
* *update_timestamp*: fecha de actualización de la *Pline* en base de datos. Estos datos se rellenan de forma automática.

.. autoclass:: pline.models.Pline

Serializadores
==================================

Los serializadores son unos de los componentes más poderosos que aporta *Django Rest Framework*. Estos permiten 
que estructuras complejas y modelos del proyecto en *Django* sean convertidos a estructuras nativas de Python y 
puedan ser convertidas fácilmente en JSON o XML, JSON en nuestro caso.

Se crea un serializador por cada modelo.

*AiteneaClassSerializer*
----------------------------------

Serializa el modelo *AiteneaClass* sin modificaciones.

.. autoclass:: pline.api.serializers.AiteneaClassSerializer

*StepSerializer*
----------------------------------

Serializa el modelo *Step* sin modificaciones.

.. autoclass:: pline.api.serializers.StepSerializer


*PlineSerializer*
----------------------------------

Serializa el modelo *Pline* sin modificaciones.

.. autoclass:: pline.api.serializers.PlineSerializer


*PlineSerializerFull*
----------------------------------

Serializa el modelo *Pline* reescribiendo el método *create* para que relacione los pasos incluidos dentro del campo 
*steps* con los modelos *Step* creados en base de datos.

.. autoclass:: pline.api.serializers.PlineSerializerFull

URLs
==================================

Incluye las rutas URLs a las vistas creadas en nuestra API, y que describimos a continuación. 


Vistas
==================================

Las vistas son extensiones de las *class-view* de *Django* mejoradas para simplificar la conexión con las URLs, los modelos y los serializadores. En lugar de renderizar un HTML como respuesta se puede devolver de forma sencilla un JSON, XML u otra estructura de datos que nos interese que devuelva nuestra API.

La API de AItenea consta de unas vistas dedicadas a la gestión de los modelos por parte del usuario, en las que podrá listar los elementos e incluso crear nuevos o modificarlos. Además, hay unas vistas enfocadas solamente en entrenar modelos o hacer predicciones con alguno ya existente. A estas últimas no se podrá acceder como una vista HTML al uso si no que devolverá un resultado de una ejecución de una de estas operaciones en formato JSON.

Las vistas existentes actualmente son:

*PlineViewSet*
----------------------------------

Se muestra una lista de todas las *Pline* creadas por el usuario. Se puede crear una nueva *Pline* haciendo uso del formulario de la parte inferior de la vista.

La URL de acceso a esta vista será: /api/pline/

.. autoclass:: pline.api.api.PlineViewSet


**fit**

Contiene un método *post* que es al que se debe llamar para hacer un entrenamiento de una *Pline*. El JSON que se envía a esta vista debe tener las claves *pline* y *origin*.

.. automethod:: pline.api.api.PlineViewSet.fit

**predict**

Contiene un método *post* que es al que se debe llamar para hacer una predicción usando una *Pline*. El JSON que se envía a esta vista debe tener las claves *pline*, *origin* y *target*.

.. automethod:: pline.api.api.PlineViewSet.predict

**fit_predict**

Contiene un método *post* que es al que se debe llamar para hacer un entrenamiento de una *Pline* y una predicción con la generada. El JSON que se envía a esta vista debe tener las claves *pline*, *origin* y *target*.

.. automethod:: pline.api.api.PlineViewSet.fit_predict

**fit_transform**


Contiene un método *post* que es al que se debe llamar para hacer un entrenamiento de una *Pline* y realizar una transformación sobre esta. El JSON que se envía a esta vista debe tener las claves *pline* y *origin*.

.. automethod:: pline.api.api.PlineViewSet.fit_transform

**fit_transform**

Contiene un método *post* que es al que se debe llamar para hacer entrenamientos con varias *Plines* y realizar predicciones de manera genética. El JSON que se envía a esta vista debe tener las claves *pline* y *origin*.

.. automethod:: pline.api.api.PlineViewSet.genetic

**delete_bulk**

Contiene un método *post* que es al que se debe llamar para eliminar varias *Plines* a la vez. Esta función debe recibir un *Array* con los *IDs* de las *Plines* a borrar.

.. automethod:: pline.api.api.PlineViewSet.delete_bulk

*StepViewSet*
----------------------------------

Se listan todos los pasos creados por el usuario. Permite filtrar por *pline_id*, para ver todos los pasos parte de una *Pline*.

La URL de acceso a esta vista será: /api/steps/

.. autoclass:: pline.api.api.StepViewSet


*AiteneaClassViewSet*
----------------------------------


Se listan todas las clases, *transform* o *ai*, disponibles en AItenea.

.. autoclass:: pline.api.api.AiteneaClassViewSet


*CSVViewSet*
----------------------------------


Se listan todos los *CSVs* disponibles, los presenta en una lista sin extensión. 
Elimina cualquier *path* que pueda haber en nombre del fichero y genera la ruta destino, guarda archivo 
después de previamente verificar su integridad.


.. autoclass:: pline.api.api.CSVViewset


*Tests*
==================================

*Utils*
==================================

Se proveen unas funciones en *utils* para facilitar ciertas operaciones.

Componer una pipeline
----------------------------------

El proceso de *fit* requiere, antes de crear el modelo, haberlo compuesto en la base de datos. Para ello se define este método, que además de hacer la propia composición ayudándose de *create_pline*, hace las comprobaciones pertinentes y devuelve tanto el modelo como el objeto de *Django* al método *fit*.

.. automethod:: pline.utils.compose_pline

La función *create_pline* se usará para facilitar el manejo del objeto de Django y su creación haciendo uso del serializador correspondiente.

.. automethod:: pline.utils.create_pline

Ejemplo fit
-----------------------------------

Se adjunta un ejemplo de un JSON para componer una *Pline* y entrenarla con unos datos que residen en un índice de *Elasticsearch*. En este caso, no se hace ninguna transformación, por lo que la *Pline* solo contiene un paso y es del tipo *ai*.

.. code-block:: JSON
    :linenos:

    {
        "origin": {
            "type": "elastic",
            "options": {
                "connection": {
                    "host": "host",
                    "port": "port",
                    "user": "user",
                    "password": "password"
                },
                "index": "wine_quality",
                "q": {
                    "_source": ["alcohol", "ash", "alcalinity_of_ash", "color_intensity"],
                    "query": {
                        "bool": {
                        "must": [],
                        "filter": [
                            {
                            "match_all": {}
                            }
                        ],
                        "should": [],
                        "must_not": []
                        }
                    }
                }
            }
        },
        "pline":{
            "name": "Wine quality classification",
            "description": "Classification to predict quality of wines depending on some characteristics",
            "path": "resources/Pline/",
            "owner": 1,
            "steps": [
                {
                    "step_number": 1,
                    "step_name": "Kmeans",
                    "step_type": "clustering.kmeans",
                    "step_options": "{\"num_cluster\": 3, \"method\": \"k-means++\", \"auto_optimal_cluster\": False}"
                }
            ]
        }
    }

Ejemplo predict
-----------------------------------


.. code-block:: JSON
    :linenos:

    {
        "pline":{
            "id": 1
            },
        "origin": {
            "type": "elastic",
            "options": {
                "connection": {
                    "host": "host",
                    "port": "port",
                    "user": "user",
                    "password": "password"
                },
                "index": "wine_quality_test",
                "q": {
                    "_source": ["alcohol", "ash", "alcalinity_of_ash", "color_intensity"],
                    "query": {
                        "bool": {
                        "must": [],
                        "filter": [
                            {
                            "match_all": {}
                            }
                        ],
                        "should": [],
                        "must_not": []
                        }
                    }
                }
            }
        },
        "target": {
            "type": "elastic",
            "options": {
                "connection": {
                    "host": "host",
                    "port": "port",
                    "user": "user",
                    "password": "password"
                },
                "index": "wine_quality_test_predict",
                "update_index": "False"
            }
        }
    }

Conector *API -- BBDD*
----------------------------------

En la API de AItenea también se define una clase para manejar las conexiones con las diferentes bases de datos que se quieran gestionar. Actualmente solo se usa *Elasticsearch*, pero se da la posibilidad de ampliar a cualquier gestor deseado.

.. autoclass:: pline.data_utils.HandlerData