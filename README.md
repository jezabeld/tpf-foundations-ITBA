# Trabajo Práctico Final Foundations
### ITBA - Cloud Data Engineering

Bienvenido al TP Final de la sección Foundations del Módulo 1 de la Diplomatura en Cloud Data Engineering del ITBA.

En este trabajo práctico vas a poner en práctica los conocimientos adquiridos en: 

1. Bases de Datos Relacionales (PostgreSQL específicamente).
2. BASH y Linux Commandline.
3. Python 3.7+.
4. Docker.

Para realizar este TP vamos a utlizar la plataforma Github Classrooms donde cada alumno tendrá acceso a un repositorio de Git privado hosteado en la plataforma Github.

En cada repositorio, en la sección de [Issues](https://guides.github.com/features/issues/) (tab a la derecha de Code en las tabs de navegación en la parte superior de la pantalla) podrás ver que hay creado un issue por cada ejercicio. 
El objetivo es resolver ejercicio/issue creando un branch y un pull request asociado. 

Debido a que cada ejercico utiliza el avance realizado en el issue anterior, cada nuevo branch debe partir del branch del ejercicio anterior.

Para poder realizar llevar a cabo esto puede realizarlo desde la web de Github pero recomendamos hacerlo con la aplicación de línea de comando de git o con la aplicación de [Github Desktop](https://desktop.github.com/) (interfaz visual) o [Github CLI](https://cli.github.com/) (interfaz de línea de comando).

La idea de utilizar Github es replicar el ambiente de un proyecto real donde las tareas se deberían definir como issues y cada nuevo feature se debería crear con un Pull Request correspondiente que lo resuelve. 
https://guides.github.com/introduction/flow/
https://docs.github.com/en/github/getting-started-with-github/quickstart/github-flow

**MUY IMPORTANTE: parte importante del Trabajo Práctico es aprender a buscar en Google para poder resolver de manera exitosa el trabajo práctico**

## Ejercicios

### Ejercicio 1: Elección de dataset y preguntas

Elegir un dataset de la [wiki de PostgreSQL ](https://wiki.postgresql.org/wiki/Sample_Databases) u otra fuente que sea de interés para el alumno.

Crear un Pull Request con un archivo en [formato markdown](https://guides.github.com/features/mastering-markdown/) expliando el dataset elegido y  una breve descripción de al menos 4 preguntas de negocio que se podrían responder teniendo esos datos en una base de datos relacional de manera que sean consultables con lenguaje SQL.


Otras fuentes de datos abiertos sugeridas:
https://catalog.data.gov/dataset
https://datasetsearch.research.google.com/
https://www.kaggle.com/datasets

## Ejercicio 2: Crear container de la DB

Crear un archivo de [docker-compose](https://docs.docker.com/compose/gettingstarted/) que cree un container de [Docker](https://docs.docker.com/get-started/) con una base de datos PostgreSQL con la versión 12.7.
Recomendamos usar la [imagen oficial de PostgreSQL](https://hub.docker.com/_/postgres) disponible en Docker Hub.
 
Se debe exponer el puerto estándar de esa base de datos para que pueda recibir conexiones desde la máquina donde se levante el container.


## Ejercicio 3: Script para creación de tablas

Crear un script de bash que ejecute uno o varios scripts SQL que creen las tablas de la base de datos en la base PostgreSQL creada en el container del ejercicio anterior.

Se deben solamente crear las tablas, primary keys, foreign keys y otras operaciones de [DDL](https://en.wikipedia.org/wiki/Data_definition_language) sin crear o insertar los datos. 

## Ejercicio 4: Popular la base de datos

Crear un script de Python que una vez que el container se encuentre funcionando y se hayan ejecutado todas las operaciones de DDL necesarias, popule la base de datos con el dataset elegido.

La base de datos debe quedar lista para recibir consultas. Durante la carga de información puede momentareamente remover cualquier constraint que no le permita insertar la información pero luego debe volverla a crear.

Este script debe ejecutarse dentro de un nuevo container de Docker mediante el comando `docker run`.

El container de Docker generado para no debe contener los datos crudos que se utilizarían para cargar la base.
Para pasar los archivos con los datos, se puede montar un volumen (argumento `-v` de `docker run`) o bien bajarlos directamente desde Internet usando alguna librería de Python (como `requests`).


## Ejercicio 5: Consultas a la base de datos

Escribir un script de Python que realice al menos 5 consultas SQL que puedan agregar valor al negocio y muestre por pantalla un reporte con los resultados.

Este script de reporting debe correrse mediante una imagen de Docker con `docker run` del mismo modo que el script del ejercicio 4.

## Ejercicio 6: Documentación y ejecución end2end

Agregue una sección al README.md comentando como resolvió los ejercicios, linkeando al archivo con la descripción del dataset y explicando como ejecutar un script de BASH para ejecutar todo el proceso end2end desde la creación del container, operaciones de DDL, carga de datos y consultas. Para esto crear el archivo de BASH correspondiente. 

***

# Explicación de los ejercicios

## Ejercicio 1
Para el ejercicio 1 simplemente se seleccionó una base de datos de interés y se creó un [archivo markdown](Dataset.md) explicando brevemente la info contenida en la fuente seleccionada y algunas posibles preguntas de interés sobre dicha información.


## Ejercicio 2
Para el ejercicio 2, se creó un archivo de docker-compose que instancia un container con la base de datos postgres version 12.7 como fue solicitado, exponiendo el puerto por defecto (5432) y creando las variables de entorno de user, password y db, mapeando también un volumen externo para poder persistir la información de la base de datos fuera del container.

## Ejercicio 3
Para el ejercicio 3, se generó un script de creación de las tablas iniciales en la base de datos.

Dado que el script debe correr una vez se instancie el container para poder conectarse a la base de datos, fue necesario implementar un método que permita el normal inicio de la imagen de postgres en el container, pero que también permita correr el script de creación de las tablas. 

Para esto, se investigó cuál es el comando "entrypoint" utilizado en la imagen oficial de postegres (disponible en https://github.com/docker-library/postgres/blob/master/Dockerfile-alpine.template) y se creó un script de bash (wrapper.sh) encargado de correr el comando original para inicializar normalmente la imagen de postgres pero dejandolo en backgroud, y así poder correr en primer plano el script de creacion de tablas, teniendo en cuenta que al finalizar éste último, se devuelva el proceso original al primer plano para evitar que el container se detenga.

Otro cambio para este ejercicio fue la necesidad de crear un archivo Dockerfile que permite el copiado de los sctipts creados a la imagen que se instancia a partir del archivo de docker-compose.

## Ejercicio 4
Para el ejercicio 4, se creó un servicio que se levante junto con la base de datos en el archivo de docker-compose cuya funcionalidad es ingestar la data necesaria para los análisis. Este servicio descarga la información de los archivos indicados mediante el yml de docker-compose conectandose a través de internet para transformarla e insertarla en la base de datos. Dado que la información de los archivos se actualiza diariamente, el servicio está diseñado para comparar la información de los archivos descargados contra los datos existentes en la base de datos e insertar únicamente la información nueva aún no cargada.

Dicho servicio se levanta a partir de una imagen estándar de Python 3 a la cual se le instalan las librerias necesarias mediante un archivo de requierimientos al momento de la creación de la imagen final, luego al instanciarse se mapea la carpeta en la que se encuentra el código fuente que realiza el trabajo.

Para resolver este ejercicio fue necesario resolver algunos inconveniente típicos de la arquitectura de microservicios como reintetar las conecciones en caso de fallar, o contemplar que el servicio al que se quiere alcanzar puede que aún no se encuentre operativo, además de tener en cuenta cuestiones como la creación de una única conexion abierta hacia la base de datos y cerrar los cursores una vez utilizados.

## Ejercicio 5
Para el ejercicio 5, se creó un nuevo servicio que expone las API's creadas a partir de consultas sql que responden a las preguntas planteadas. Este servicio se levanta en el mismo docker-compose que los creados anteriormente y expone los endpoints mediante Flask en el puerto 5000 de localhost.

Para exponer los diferentes endpoints en Flask, fue necesario crear las plantillas (o blueprints) para los diferentes endpoints, definir cada una de las rutas de cada endpoint y los métodos a utilizar, en este caso solo se utiliza en método GET ya que no se requiere cargar ni modificar data desde dichos endpoints, solo siendo necesaria la consulta de información a través de las rutas definidas.

Luego se definieron las queries que responden a cada una de las consultas, creando también algunos errores específicos con mensajes acordes para capturar los casos de reportes vacíos.

Adicionalmente en este paso se corrigieron algunos bugs del servicio de carga de datos generados en el ejercicio anterior para capturar correctamente la información y agregar algunos mensajes personalizados en la consola para poder determinar el avance de dicho proceso.

## Ejercicio 6
Para el último ejercicio se creó el archivo [run_reports.sh](run_reports.sh) que se encarga de levantar todos los servicios, imprimir los reportes y bajar los servicios nuevamente. En este paso se encontraron algunas complicaciones en relación a las deependencias de los servicios teniendo en cuenta las siguientes cuestiones:
1. Si bien en docker-compose se definió la dependencia de servicios, cada uno de los containers solo espera a que el anterior haya levantado, pero no necesariamente a que el servicio esté disponible. Ya se había visto esta cuestión al resolver el ejercicio 4, por lo que se agregaron algunos chequeos similares a los utilizados para detectar el estado de la base de datos en el servicio de APIs también.
2. Si bien los servicios pueden estar disponibles, no se podrían (o deberían) realizar las consultas a la API hasta que el servicio que carga la data no haya finalizado dicha tarea.

Este ultimo punto fue más complejo de resolver, porque habría que poder identificar cuándo el servicio de carga de la info finaliza con status 0 (ok) para poder realizar las consultas a los endpoints. Este problema se resolvió levantando mediante docker-compose run la base de datos y el servicio de carga de datos primero, y al finalizar este último utilizar docker-compose up para levantar el resto de stack faltante (en este caso, levanta la app pero no levanta la base de datos porque ya se encuentra levantada por el comando anterior). La única desventaja es que el segundo comando levanta nuevamente el servicio load_data porque como el anterior ya finalizó, no lo detecta corriendo, y este servicio vuelve a descargar la data de internet aunque no la vuelve a cargar porque la BD se encuentra actualizada.

Para lidiar con este tipo de problemas de forma correcta, se podría utilizar algún tipo de mensajería entre servicios, pero ya que este tema escapaba un poco del scope del TP, se deja pendiente para plantear en una arquitectura cloud en el próximo TP. 