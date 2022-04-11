**************************************
AITenea: reports
**************************************

Esta aplicación ofrece las siguientes funcionalidades:

* Presenta toda la información relevante que resume la ejecución de la *Pline*.
* Muestra el *score* y nombre del algoritmo de *Machine Learning* relacionado con el reporte de la *Pline*.
* Muestra el estado actual de la *Pline* relacionada.
  
La API está formada por los siguientes elementos:


Modelos
========

Los modelos son las clases que dan forma a lo que se podrían asimilar como las tablas de la base de datos de la aplicación. 
Un modelo va a definir un objeto y en él sus atributos y funciones.

*PlineReport*
----------------------------------

.. autoclass:: reports.models.PlineReport

*PlineReportMetric*
----------------------------------

.. autoclass:: reports.models.PlineReportMetric

*PlineStatus*
-----------------

.. autoclass:: reports.models.PlineStatus


Serializadores
==================================

Los serializadores son unos de los componentes más poderosos que aporta *Django Rest Framework*. Estos permiten 
que estructuras complejas y modelos del proyecto en *Django* sean convertidos a estructuras nativas de Python y 
puedan ser convertidas fácilmente en JSON o XML, JSON en nuestro caso.

Se crea un serializador por cada modelo.

*PlineReportSerializer*
----------------------------------

Serializa el modelo *PlineReportSerializer* sin modificaciones.

.. autoclass:: reports.api.serializers.PlineReportSerializer


*PlineReportMetricSerializer*
----------------------------------

Serializa el modelo *PlineReportMetricSerializer* sin modificaciones.

.. autoclass:: reports.api.serializers.PlineReportMetricSerializer


*PlineStatusSerializer*
----------------------------------

Serializa el modelo *PlineStatusSerializer* sin modificaciones.

.. autoclass:: reports.api.serializers.PlineStatusSerializer


URLs
==================================

Incluye las rutas URLs a las vistas creadas en nuestra API, y que describimos a continuación. 


Vistas
==================================

Las vistas son extensiones de las *class-view* de Django mejoradas para simplificar la conexión con las URLs, los modelos y los serializadores. 
En lugar de renderizar un HTML como respuesta se puede devolver de forma sencilla un JSON, XML u otra estructura de datos que nos interese que 
devuelva nuestra API.

La API de AItenea consta de unas vistas dedicadas a la gestión de los modelos por parte del usuario, en las que podrá listar los elementos e incluso 
crear nuevos o modificarlos.

Las vistas existentes actualmente son:

*PlineReportViewSet*
----------------------------------

Se listan todas los reportes de las *Plines* creadas por el usuario.

La URL de acceso a esta vista será: /api/pline_report/

.. autoclass:: reports.api.api.PlineReportViewSet

**delete_bulk**

Contiene un método *post* que es al que se debe llamar para eliminar varios *Reports* a la vez. Esta función debe recibir un *Array* con los 
*IDs* de los *Reports* a borrar.

.. automethod:: reports.api.api.PlineReportViewSet.delete_bulk


*PlineReportMetricViewSet*
----------------------------------

Se listan todas las métricas de los *Reports* creadas por el usuario.

La URL de acceso a esta vista será: /api/pline_report_metric/

.. autoclass:: reports.api.api.PlineReportMetricViewSet


*PlineStatusViewSet*
----------------------------------

Se muestra una lista con todas las métricas de los estados de las *Plines* creadas por el usuario.

La URL de acceso a esta vista será: /api/pline_report_status/

.. autoclass:: reports.api.api.PlineStatusViewSet