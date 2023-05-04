------------------------------------------------------------------
       d8888 8888888 88888888888                                  
      d88888   888       888                                      
     d88P888   888       888                                      
    d88P 888   888       888   .d88b.  88888b.   .d88b.   8888b.  
   d88P  888   888       888  d8P  Y8b 888 "88b d8P  Y8b     "88b 
  d88P   888   888       888  88888888 888  888 88888888 .d888888
 d8888888888   888       888  Y8b.     888  888 Y8b.     888  888
d88P     888 8888888     888   "Y8888  888  888  "Y8888  "Y888888

------------------------------------------------------------------


A fun and efficient ML framework

---------------
1. INTRODUCCIóN
---------------

AITENEA es un framework de machine learning (ML) de propósito general cuya principal virtud se encuentra en su capacidad para convertir cualquier algoritmo implementado  en un elemento disponible en una capa de visualización para una programación visual mediante flujos. Con esta filosofía resulta mucho más directo pasar de una implementación teórica o de prueba de concepto a un bloque de funcionalidad preparado para la producción. Desde  un punto de vista formal y siguiendo el estándar CRIPS-DM, AITENEA unifica las fases de preparación y transformación de datos, modelado, evaluación y despliegue, incorporando al mismo tiempo un mecanismo para añadir en esta cadena algoritmos nuevos desde su formulación matemática. De forma más descriptiva el objetivo de AITENEA es poder disponer de un sistema capaz de poner en producción y/o ensayar modelos de ML sin necesidad de hacer codificación alguna, todo ello de forma muy intuitiva. Además el diseño de AITENEA facilita la incorporación rápida de nuevos algoritmos por lo que no deberían existir límites evidentes al crecimiento y ampliación de métodos, por novedosos que estos resulten. Para alcanzar estos objetivos AITENEA se compone de tres capas o niveles y que el presente documento irá describiendo en los sucesivos apartados. A modo de introducción diremos que estos tres niveles son:

1. Capa de bajo nivel o núcleo de la aplicación. Está conformada por una serie de clases y metaclases que permiten transformar los datos y realizar los modelos de ML. 
2. Una capa intermedia, a modo de interfaz, entre la capa de bajo nivel y una capa superior. 
3. Una capa de alto nivel amigable a modo de interfaz gráfica de usuario para poder usar la funcionalidad de la capa de bajo nivel mediante programación de flujos. 



---------------
1. INTRODUCTION
---------------


AITENEA is a general purpose machine learning (ML) framework whose main virtue lies in its ability to convert any implemented algorithm into an available element in the visualization layer for flow-based programming. With this philosophy it is easier to move from a theoretical or proof-of-concept implementation to a block of functionality ready for production. From a formal point of view and following the CRIPS-DM standard, AITENEA unifies the phases of data preparation and transformation, modeling, evaluation and deployment, while incorporating a mechanism to add new algorithms to this chain, from its mathematical formulation. More descriptively, AITENEA's goal is to be able to provide a system capable of putting ML models into production and/or testing without having to do any coding, in a very intuitive way. In addition, the design of AITENEA facilitates easy incorporation of new algorithms so there should be no obvious limits to the growth and expansion of methods, despite how novel they may be. To achieve these objectives AITENEA consists of three layers or levels and this document will describe them in the following sections. that Briefly, these three levels are:

1. Low level layer or application core. It consists of a series of classes and metaclasses that allow data to be transformed and run ML models.
2. An intermediate layer, as an interface, between the low-level layer and a high-level layer.
3. A high-level layer graphical user interface to be able to use the functionality of the low-level layer in flow-based programming.

---------------------------
2. INSTALACIÓN Y DEPENDENCIAS 
---------------------------

A la hora de desplegar el proyecto es necesario verificar si tenemos ciertas dependencias o bien instalarlas en el caso de que nuestro portátil no lo tenga. A continuación se detalla los requisitos necesarios para ejecutar Aitenea los cuales se pueden ejecutar desde la consola:

- GIT

Verificar si existe git a través de:

```sh
   git --version
``` 

Si no existe se procede a su instalación: 

```sh
   sudo apt install git-all
``` 

Para mayor detalle si se necesita se puede acceder a la [documentación]('https://git-scm.com/book/en/v2/Getting-Started-Installing-Git')

- MAKE Package

Verificar si existe a través de:

```sh
   make --version
``` 
 
Para la instalación:

```sh
   sudo apt install make
``` 
O a través de:

```sh
   sudo apt-get install build-essential
```

- BASH

Verificar si existe a través de:

```sh
   bash --version
``` 
 
Para la instalación:

```sh
   sudo apt install bash-completion
``` 
 
 - En local

Crear las carpetas "data" y "csv" en local. Para ello hay que estar dentro de la carpeta donde ha sido clonado aitenea y ejecutar el siguiente comando desde un terminal:

```sh
   mkdir data && mkdir data/csv
``` 

- Elastic Tools repositorio


Se debe incluir el repositorio Elastic Tools dentro de la carpeta raíz de AITenea ejecutando el siguiente comando:

```sh
   git clone https://github.com/AerinSistemas/elastictools.git
```
- Docker Engine

Verificar si existe a través de:

```sh
   docker --version
```
 
Para la instalación:

```sh
   sudo apt install bash-completion
```
 
- Docker Compose

Verificar si existe a través de:

```sh
   docker-compose --version
```

En el caso que no esté instalado lo podemos realizar tomando los pasos de la página oficial de Docker:

- Docker Engine: https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository

- Docker Compose: https://docs.docker.com/compose/install/

Una vez que hemos realizado todos estos pasos, estamos listos para desplegar AItenea.

---------------------------
3. DESPLIEGUES
---------------------------

AITenea cuenta con 2 opciones de despliegue:

1. Desarrollo: Despliegue usando Docker y recarga de nodos automática al modificar su código.
2. Producción: Despliegue sin Docker
3. Producción en diferentes equipos: Despliegue sin docker, separando Node-RED y Django/Redis en 2 equipos diferentes.

En el caso de que ejecutemos el despliegue de producción, tenemos la opción de definir puertos externos para Node-RED, Django y Redis, al ejecutar el script de despliegue, este
nos preguntará por nuestro valores personalizados, si no queremos modificarlo, al pulsar
"Enter" se asignarán los valores por defecto.

---------------------------
3. 1 Despliegue para desarrollo (con Docker):
---------------------------

```sh
# Generar entorno
make devel

# Iniciar entorno
make run
```

---------------------------
3. 2 Despliegue para producción (sin Docker):
---------------------------

```sh
# Generar entorno
make production

# Iniciar Django y Redis
make run-production-backend
# Iniciar Node-RED
make run-production-frontend
```

---------------------------
3. 3 Despliegue para producción en diferentes equipos:
---------------------------

En cada equipo cuando el script lo pida, deberemos introducir la IP pública del equipo
en donde estará desplegado la otra parte de AITenea:

- Si desplegamos el entorno de Node-RED deberemos introducir la IP de Django/Redis.
- Si desplegamos el entorno de Django/Redis deberemos introducir la IP de Node-RED.

Cuando el script lo pida, deberemos definir los puertos externos que queramos usar, 
si no introducimos puertos se asignarán los valores por defecto:

- Django: 7000
- Redis: 6379
- Node-RED: 1880

Despliegue en: Equipo 1
```sh
# Generar entorno para Django y Redis
make production-backend

# Introducimos IP y puertos...

# Iniciar Django y Redis
make run-production-backend
```

Despliegue en: Equipo 2
```sh
# Generar entorno para Node-RED
make production-frontend

# Introducimos IP y puertos...

# Iniciar Node-RED
make run-production-frontend
```

---------------------------
4. ACCESO
---------------------------

Si los valores están por defecto, se utilizarán estos enlaces para poder entrar:

1. Node-Red: http://0.0.0.0:1880/
2. Backend: http://0.0.0.0:7000/

*En el caso de que se hayan modificado las variables, se utilizaría la IP y el puerto cambiado.*

Se crea un usuario por defecto:

- Username: admin
- Password: admin

Para generar un superusuario manualmente:

- DOCKER

  Debes acceder a la shell de docker y ejecutar `python3 manage.py createsuperuser`

- PRODUCTION
  
  Situandote en la ruta `/opt/aitenea/aitenea_api/` se ejecuta el mismo comando. `python3 manage.py createsuperuser`

---------------------------
5. DOCUMENTACIÓN DESARROLLO
---------------------------

A la hora de programar una nueva funcionalidad para AITenea se debe construir el siguiente árbol de directorios

```
nueva_funcionalidad/
    -__init__.py
    |
    -class_name.py
    |
    -_auxiliar_files.py
    |
    --test/
```

Si ya existe una carpeta que contenga algoritmos cuya tipología fuera similar podemos incluir allí nuestra clase (denominada aquí como class_name.py). De la misma manera podemos incluir los archivos .py con contenido auxiliar, esto totalmente optativo y los test, siendo esto último preceptivo.

Una vez decidida la unicación se debe decidir si el algoritmo es una transformación (en el sentido de un algoritmo que transforma los datos sin generar un modelo) o un modelo. Si se trata de una trasformación debemos heredar de la clase BaseClassPreprocessing, en otro caso debemos heredar de BaseClassAI.
