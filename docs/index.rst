========================================
Proyecto AITenea
========================================
by Aerin Sistemas

AITenea es un *framework* cuya finalidad es la experimentación de algoritmos avanzados de *machine learning* (ML), realización de modelos y despliegue de los mismos. 
AITenea pretende ser una herramienta útil para que los usuarios interesados en desarrollar algoritmos puedan hacerlo de tal manera que su trabajo persista para ser usado
por el mismo o por terceros, desde un entorno gráfico y de forma intuitiva, incluso sin tener conocimientos de *machine learning*. Por otro lado la existencia de un entorno
gráfico especialmente concebido para el IoT industrial (*Internet Of Things*) convierte AITenea en una herramienta especialmente dotada para aplicar soluciones de 
*machine learning* en el sector industrial.

AITenea cuenta con tres capas: 

*  **una capa de bajo nivel**: que permite incorporar algoritmos, usando arrays básicos y librerías típicas de Python para operar con ellos (NumPy, SciPy, ...)
   intercalándolos si se desea con librerías más específicas de ML como *Scikit* o de *deep learning* como *Pytorch* (por citar algunas). Esta capa incluye las 
   clases base que van a estructurar cualquier algoritmo de ML que se quiera implementar.
*  **una capa intermedia**: que sirve de interfaz entre la capa de bajo nivel y la de alto nivel (capa gráfica). Basada en *Node-RED* tiene la capacidad de
   generar bloques gráficos para la capa de visualización y conectar con las bases de datos.
*  **una capa de alto nivel**: hace a veces de interfaz grafica del usuario, de tal forma que cualquier algoritmo implementado en la capa de bajo nivel 
   queda disponible de forma automática en esta capa como un elemento grafico de la misma. Esto último permite que el dasarrollador del algoritmo se 
   abstraiga completamente de la creación de elementos gráficos centrandose exclusivamente en el dasarrollo de los mismos. La capa de alto nivel se construye 
   según las especificaciones de *API REST*, lo que facilita su empleo como un servicio. Esta capacidad permite ser "embebida", 
   en una herramienta de programacion visual como *Node-RED*, por lo que AITenea para un usuario final no es mäs que un 
   conjunto de funcionalidades gráficas preparadas para ser usadas en un entorno de programación de flujos. El desarrollo de la *API REST* ofrece la libertad 
   por un lado de no depender de una capa vizual concreta y por otro lado permite que nuestro *framework* pueda conectarse con diferentes entornos.

Esta herramienta permitirá de forma muy sencilla realizar:

1. Búsqueda de hiperparámetros usando técnicas de algoritmia genética mediante diferentes criterios, como función de fitness (incluso valorando los tiempos de cómputo).

2. Correr los algoritmos, tanto el entrenamiento como la predicción de forma distribuida (incluidos cluster de GPUs).

3. Poner rápidamente en producción o en preproducción la solución implementada. 

4. Programar pruebas simultáneas con varios algoritmos en paralelo ofreciendo un informe final comparativo.


.. toctree::
   :numbered:
   :maxdepth: 4
   
   user_manual/user_manual
   aitenea_core/aitenea_core
   aitenea_api/pline
   aitenea_api/reports
   aitenea_nodes/aitenea_nodes