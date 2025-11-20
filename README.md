# Guía para el proyecto de drones   
 
## 1. Introducción   

El proceso que se describe en este guía tiene por objetivo el desarrollo de una aplicación de control de un dron (o varios) que pueda demostrarse en el DroneLab del Campus del Baix Llobregat. Esta aplicación se desarrollará en equipos de 3 o 4 personas.
El proceso permite el aprendizaje de una variedad de conceptos, tecnologías y herramientas. En particular, se aprende (entre otras cosas):   

*	Cómo es un dron cuatrimotor y qué componentes tiene
*	Cómo se controla el dron desde un programa de ordenador (un portátil) o desde un teléfono móvil
*	Cómo se desarrolla una interfaz gráfica para controlar el dron, en Python o en C#, que incluya mapas geolocalizados para visualizar la posición del dron
*	Cómo se articula la comunicación entre los diferentes dispositivos que intervienen en la aplicación
*	Cómo se transmite/recibe el stream de vídeo capturado por la cámara del dron
*	Cómo se reconocen objetos en el stream de vídeo

La aplicación tiene 4 versiones. La versión 1 está muy guiada. Se desarrolla paso a paso siguiendo las instrucciones de esta guía. En cada paso se introduce algún concepto/herramienta/tecnología nueva. Este repositorio proporciona los códigos implicados en cada paso de manera que basta comprobar que el código funciona correctamente. La guía también propone sencillos ejercicios que requieren la modificación del código proporcionado para corregir algún mal funcionamiento o para introducir alguna nueva funcionalidad. Es muy conveniente que cada miembro del equipo desarrolle de forma individual esta primera versión, aunque naturalmente compartiendo dudas y progresos con los compañeros de equipo y con los profesores.    
 
La versión 2 tiene unos requisitos prefijados, pero está mucho menos guiada que la versión 1. También se proporcionarán algunos códigos útiles pero la tarea fundamental consistirá en la investigación y experimentación necesarias para implementar las nuevas funcionalidades. El trabajo de la versión 2 se beneficiará mucho de un buen reparto de tareas entre los miembros del equipo.    
 
Acabada la versión 2 cada equipo deberá decidir las funcionalidades que tendrá la versión final de su aplicación. En esta guía se proporcionarán algunas ideas que pueden resultar de inspiración. Cada equipo deberá decidir también que subconjunto de las funcionalidades estará ya disponible en la versión 3, que será una versión intermedia pero que deberá poder ser demostrada en el DroneLab.     
 
La versión 4 será la versión final con todas las funcionalidades previstas. Además de demostrar el correcto funcionamiento en el DroneLab, cada equipo deberá entregar el resultado en forma de repositorio en GitHub, que incluya los códigos desarrollados, explicaciones detalladas sobre cómo instalar y poner en marcha la aplicación y vídeos que muestren el funcionamiento y describan cómo está organizado el código desarrollado.    

## 2. Criterios de evaluación    


## 3. Recursos    
### 3.1 Git y GitHub   
Git y GitHub son herramientas que facilitan la gestión de versiones, el mantenimiento de código en la nube y el trabajo cooperativo en el desarrollo de código o documentos.   

En este vídeo se explica lo esencial para instalarse las herramientas y entender los principios de funcionamiento:   

[![](https://markdown-videos-api.jorgenkh.no/url?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DI_fQlby426k)](https://www.youtube.com/playlist?list=PLj_C4NVXL2Sgq1N5G1MGbSjsXUIVGZ4S3)    

Git puede instalarse desde esta página:   
https://git-scm.com/downloads

### 3.2 Mission Planner y SITL    
Mission planner es una aplicación de escritorio que permite interactuar con el dron. Por ejemplo, permite configurar muchos parámetros del dron y darle ordenes típicas (armar, despegar, volar a un punto dado, etc.). Mission Planner permite también poner en marcha un simulador del dron, que llamaremos SITL (Software In The Loop). Tanto Mission Planner como las aplicaciones que se desarrollan en esta guía interactúan con el simulador, exactamente igual que como lo harían con el dron real. Esto es ideal para desarrollar y verificar el correcto funcionamiento de los códigos antes de usarlos para controlar el dron real.    

Mission Planner puede descargarse desde aquí:   
https://ardupilot.org/planner/docs/mission-planner-installation.html

### 3.3 Python y PyCharm     
Una buena parte del código se desarrollará en Python, por lo que se necesita un intérprete, que puede descargarse de aquí:
https://www.python.org/downloads/

PyCharm es el IDE más popular para el desarrollo de código en Python. Puede descargarse desde aqui:   
https://www.jetbrains.com/pycharm/

### 3.4 Visual C# y Visual Studio    
También será necesario programar en Visual C#. La herramienta recomendada para esto es Visual Studio, que puede descargarse desde aqui:
https://visualstudio.microsoft.com/es/downloads/


### 3.5 Repo taller teleco-renta, que incluye una breve descripción de cómo es el dron    
En este repositorio puede encontrarse una guía que permite iniciarse en el uso de Mission Planner. También contiene una descripción de los aspectos más básicos del dron en el que se basa el proyecto a desarrollar.  
 
### 3.6 Librería DronLink    
Esta librería facilita la programación en Python de las operaciones necesarias para controlar el dron. Todos los detalles pueden encontrarse en este repositorio. Es importante leer en detalle el apartado en el que se describe el modelo de programación. También pueden ser de utilidad los diferentes programas de test que ilustran la manera de usar las diferentes funciones de la librería.    

### 3.7 Librería csDronLink    
Esta es una implementación de DronLink para C#. Toda la información (incluyendo ejemplos de uso) puede encontrarse en este repositorio. Es importante tener en cuenta que esta librería está menos desarrollada que DronLink y tiene menos funcionalidades.    
[![DroneEngineeringEcosystem Badge](https://img.shields.io/badge/DEE-Flying_Indoor-blue.svg)](https://github.com/dronsEETAC/DashIndoor.git) 

## 4. Versión 1    

### 4.1 Escenario local    

En un escenario local la estación de tierra que controla el dron está directamente conectada a éste, a través de la radio de telemetría. Por tanto, es el código de la estación de tierra el que genera las órdenes para el dron usando las funciones de la librería DronLink.    
  
Veamos dos casos de estación de tierra, una implementada en Python y otra en C#.    

#### 4.1.1 Estación de tierra en Python para el escenario local
La estación de tierra en Python tiene una interfaz de usuario como la que se muestra en la imagen.    
 
<img width="272" height="511" alt="image" src="https://github.com/user-attachments/assets/6ef6efb5-aca7-46d2-9e91-6910a030900c" />   
 
Se trata de un conjunto de botones para ordenar algunas operaciones muy básicas. La interfaz está hecha en Tkinter. Conviene pensar en esa interfaz como una matriz de 9 filas y 2 columnas. Los diferentes widgets (botones, etiquetas, etc.) se disponen en esa matriz. Por ejemplo, el botón para conectarse con el dron se coloca en la fila 0 y se extiende a lo largo de las 2 columnas. Sin embargo, el botón de aterrizar se coloca en la fila 4 y ocupa la primera columna. El bloque de Navegación va a la fila 5, ocupa las dos columnas, pero tiene asociado un espacio lateral a la izquierda, que hace que se desplace un poco hacia el centro. Aunque el código que genera esa interfaz gráfica puede atemorizar un poco inicialmente, en realidad es sencillo si se tiene presente la matriz en la que se disponen los widgets.   
 
Cuando se pulsa alguno de los botones de la interfaz, el programa usa la función adecuada de la librería DronLink para enviar la orden al dron. El botón de conexión usa la función de la librería para establecer una conexión con el simulador SITL, que naturalmente debe estar en marcha.   
   
Es importante observar lo que ocurre al pulsar el botón de despegar. Se hace una llamada no bloqueante a la función correspondiente de la librería y se indica también una función de callback que la librería ejecutará cuando el dron haya alcanzado la altura de despegue. Puesto que la llamada es no bloqueante, la interfaz gráfica sigue operativa durante el despegue y, por tanto, pueden verse los datos de telemetría (por ejemplo, la altura del dron), si se piden esos datos clicando el botón correspondiente. La función de callback se limita a poner en color verde el botón para indicar visualmente que el dron ya ha alcanzado la altura esperada.    
 
En cambio, los botones de aterrizaje y RTL no tienen ese comportamiento. Al pulsar el botón de aterrizaje el dron efectivamente inicia el aterrizaje, pero al haber usado una llamada bloqueante, la interfaz gráfica queda congelada hasta que el dron está en tierra. Eso impide, por ejemplo, observan cómo cambia la altura del dron durante el aterrizaje.    
 
Los 9 botones de navegación permiten hacer que el dron navegue en cualquiera de las direcciones indicadas (Norte, Sur, etc). El dron navegará en la dirección elegida hasta que se pulse el botón correspondiente a otra dirección o el botón de Stop (o aterrizaje o RTL).    
  
Se proponen lo siguientes ejercicios:    

1.	Modificar el código para que las operaciones de aterrizaje y RTL tengan un comportamiento similar a la operación de despegue (llamada no bloqueante)
2.	Incorporar al bloque de datos de telemetría algún dato más (por ejemplo, el estado del dron o la velocidad). Conviene mirar la documentación de DronLink para ver qué información viene en el paquete de datos de telemetría.
3.	Añadir algún botón más para realizar una nueva función. De nuevo, mirar la documentación de DronLink en busca de inspiración.
   
#### 4.1.2 Estación de tierra en C# para el escenario local    
 
Esta versión está hecha en C# usando Windows Forms. La interfaz gráfica se muestra en la figura. Funcionalmente es prácticamente igual que la estación de tierra en Python. En este caso, el usuario puede especificar la altura de despegue, la operación de despegue realiza el armado del dron antes del despegue y entre los datos de telemetría se incluye la posición del dron (latitud y longitud).   
  
<img width="436" height="334" alt="image" src="https://github.com/user-attachments/assets/4f2c31cb-ef7f-4e41-b947-60bdbebb7f60" />

Esta estación de tierra utiliza la librería csDronLink, que es una versión de DronLink para C#, con el mismo modelo de programación (llamadas no bloqueantes, funciones de callback, etc.).   
 
El botón para conectar establece una conexión con el simulador SITL. Aunque técnicamente sería posible conectar al simulador simultáneamente la estación de tierra en Python y la estación en C#, en la realidad solo una de las dos podrá usar la radio de telemetría para enviar órdenes al dron. Por ese motivo, el botón de conexión se conecta al SITL solo si no está conectada ya la estación en Python.    
 
Trabajar en Visual C# con Windows Forms tiene la ventaja de que es más fácil (para muchos) diseñar la interfaz gráfica. Además, al ser C# un lenguaje compilado el código se ejecuta más rápido que el código de Python (que es un lenguaje interpretado). Esta es una ventaja relativa porque una interfaz de usuario trabaja en la mayoría de los casos a la velocidad del usuario humano, que no es mucha comparada con la velocidad del ordenador. La desventaja de C# frente a Python es que para implementar una cierta función se requieren normalmente más líneas de código.     
 
Se proponen los ejercicios siguientes:    
 
1.	Hacer que el usuario pueda establecer la altura de despegue con una barra de desplazamiento, igual que el heading o la velocidad
2.	Añadir algún dato más a los datos de telemetría (consultar la documentación de csDronLink)
3.	Incorporar un botón para realizar alguna nueva función (a elegir)
   
### 4.2 Escenario global    
 
En el escenario global, el programa que controla el dron (que llamaremos AutopilotService), además de estar conectado directamente al dron (por ejemplo, a través de la radio de telemetría) está conectado a Internet, de manera que puede recibir peticiones desde otros dispositivos también conectados a Internet, que pueden estar, por tanto, físicamente lejos. La figura ilustra el escenario global.   

 <img width="833" height="412" alt="image" src="https://github.com/user-attachments/assets/c130fd14-b5d5-4d04-86d4-2125560a2a15" />

El escenario global puede ser interesante en varios casos. En el caso de que el dron tenga un computador abordo (por ejemplo, una Raspberry Pi) conectado por cable al autopiloto, el AutopilotService se ejecutaría en ese computador abordo y podría recibir órdenes por internet. Esto permitiría al dron reaccionar de manera rápida en caso de que se produzcan determinadas situaciones. Por ejemplo, el AutopilotService podría recibir los datos de telemetría del autopiloto, detectar que el dron está peligrosamente cerca de una cierta posición y aterrizar inmediatamente en ese caso. Esta operación también podría implementarse en el escenario local descrito antes, porque los datos de telemetría también pueden llegar a la estación de tierra a través de la radio de telemetría, ser procesados en esa estación de tierra desde la que se enviaría la orden de aterrizaje. Pero ese proceso introduciría un retardo en la operación que podría ser inaceptable.    
 
Un segundo caso de interés del escenario global sería una aplicación en la que queremos que sean varios dispositivos conectados a internet los que puedan controlar el dron. Eso permitiría, por ejemplo, enviar la orden de despegar desde un dispositivo y la orden de aterrizar desde otro. O podría implementarse un divertido juego en el que el espacio de vuelo se divide en secciones de manera que cada jugador, con su portátil, controla el dron solo cuando éste está dentro de la zona que tiene asignada.    
 
Como es lógico, la implementación de un escenario global requiere de algún mecanismo de comunicación a través de Internet, entre el AutopilotService y los dispositivos que deben poder controlar el dron. Para este propósito vamos a utilizar la tecnología MQTT. Se trata de un protocolo de comunicación que utiliza el mecanismo de suscripción/publicación. Los dispositivos conectados pueden publicar mensajes y pueden suscribirse a ciertos tipos de mensajes. Por ejemplo, el AutopilotService puede suscribirse a los mensajes de tipo “despegar” (decimos que el mensaje tiene el topic “despegar”). Cualquiera de los dispositivos conectados puede publicar un mensaje de tipo “despegar” de manera que ese mensaje llegará al AutopilotService que dará la orden al autopiloto. De manera análoga, todos los dispositivos pueden suscribirse a mensajes del tipo “TelemetryInfo” de manera que cuando el AutopilotService tiene un nuevo paquete de datos de telemetría publica un mensaje de ese tipo con los datos y ese mensaje llegará a todos los suscriptores.   
 
La comunicación usando MQTT requiere de la intervención de un agente software que se denomina bróker y que se encarga de administrar las publicaciones y las suscripciones y encaminar los mensajes que se publican. Naturalmente, el bróker también tiene que estar conectado a Internet. Existen brokers públicos y gratuitos, como, por ejemplo, el bróker de Hivemq, que puede usarse en la aplicación a desarrollar.    
 
#### 4.2.1 Un autopilotService    
 
El código autopilotService.py implemente un posible servicio de autopiloto. Este código usa la librería DronLink para realizar una variedad de operaciones con el dron, a petición de los clientes que se conecten. El programa se conecta al bróker Hivemq y se suscribe a todas las publicaciones que tengan un topic con el formato:   
```
 '+/autopilotServiceDemo/#'
```
Esto indica que el topic puede empezar con cualquier palabra (que indica de dónde viene la publicación) y que puede acabar con cualquier texto (que contendrá la especificación de la operación que debe realizar el servicio.    
 
Cuando el bróker recibe una publicación cuyo topic tiene el formato especificado reenvía la publicación al servicio y éste ejecuta la función on_message. En esa función se extrae del topic el origen de la publicación, la operación solicitada (command) y se usa la librería DronLink para realizar la operación.    
 
En algunos casos, al completar la operación solicitada, el servicio publica un mensaje para avisar al cliente de tal circunstancia. Por ejemplo, al completar la operación de despegue, publica el mensaje:   
```
'autopilotServiceDemo/ORIGEN/flying'
```
siendo ORIGEN el identificador del cliente que ha solicitado los datos de telemetría, que se obtuvo del topic del mensaje en el que se solicitaba la operación de despegue.
En el caso de que se soliciten datos de telemetría, el autopilotService publicará esos datos cada vez que tenga un nuevo paquete. Para ello usará el topic:    
``` 
'autopilotServiceDemo/ORIGEN/telemetryInfo'
```
#### 4.2.2 Dashboard global en Python    
 
Este dashboard es un cliente que interacciona con el autopilotService. Tiene una interfaz gráfica prácticamente igual al dashboard local. Al iniciar la ejecución se conecta al bróker Hivemq y se suscribe a todos los mensajes cuyo topic sea:    
```
'autopilotServiceDemo/interfazGlobal/#'
```
Es decir, cualquier mensaje que venga del autopilotServiceDemo y tenga como destino “interfazGlobal” que es como se identifica el dashboard.    
 
Ahora al pulsar un botón no se usa la librería DronLink para ordenar la operación sino que se publica un mensaje en el borker para que lo reciba el servicio. Por ejemplo, cuando se pulsa el botón de despegue se publica un mensaje con topic:    
```
'interfazGlobal/autopilotServiceDemo/arm_takeOff'
```
Cuando el servicio reciba ese mensaje armará el dron y despegará. Al completar la operación publicará el mensaje de reconocimiento que hemos descrito antes. El dashboard recibirá ese mensaje y entonces cambiará el color del botón.   
 
Para poner en marcha esta aplicación es necesario tener funcionando el simulador SITL, poner en marcha el servicio y después poner en marcha el dashboard.    
 
Se proponen los siguientes ejercicios:    
  
1.	El botón de parar la recepción de datos de telemetría no está funcionando. Detectar el error y corregirlo.
2.	Los cambios de velocidad y de heading no están operativos en el dashboard. Introducir el código necesario para implementar estas funcionalidades.

#### 4.2.3 WebApp    
 
Una de las características de las aplicaciones de estación de tierra a las que nos hemos referido en los apartados anteriores es que deben ser instaladas en los dispositivos en las que se van a ejecutar (por ejemplo, un portátil). Eso no es un problema porque las aplicaciones están hechas para eso, para ser instaladas.    
 
No obstante, hay situaciones en las que puede ser interesante poder interactuar con el dron desde un dispositivo móvil sin tener que instalar ninguna aplicación específica para ello. Ese es el caso de demostraciones en el DronLab para que los visitantes puedan interactuar con el dron desde sus dispositivos móviles sin tener que pedirles que instalen cosas. Para este propósito las webapps son ideales.    
 
Una webapp es un servidor que sirve páginas web, igual que el servidor que sirve las páginas web de www.upc.edu. Pero las páginas web que sirve no tienen noticias o enlaces a documentos. Tienen botones de tal manera que cuando nos conectamos a la web desde el móvil lo que nos aparece es una página con botones, uno de los cuales, por ejemplo, nos permite hacer despegar el dron. Cuando el usuario pulsa ese botón en su móvil el navegador que se ha usado para acceder a la web hace una petición HTTP al servidor web (por ejemplo, un POST). El servidor detecta que ese POST indica que el usuario ha pulsado el botón y entonces envía al autopilotService la orden para que el dron despegue. La comunicación entre el servidor web y el servicio puede realizarse usando MQTT, tal y como hemos visto ya.     
 
Para implementar webapps usaremos el framework Flask. En su versión más básica, la webapp se compone de un servidor en Python que debe ejecutarse en una máquina con IP pública y un fichero HTML (cliente web) que contiene la página web que se enviará al dispositivo móvil que se conecte. En ese fichero se indican los elementos gráficos de la página codificados en HTML (botones, cuadros de texto, etc), los estilos gráficos codificados en CSS (colores, tamaños, etc.) y el código que debe ejecutar el navegador, escrito en Javascript (por ejemplo, lo que hay que hacer cuando el usuario pulse un botón).    

El fichero serverHTTP.py y el fichero indexHTTP que está en la carpeta templates es constituyen un ejemplo de una webapp muy sencilla, cuya interfaz gráfica se muestra en la imagen.    
<img width="343" height="558" alt="image" src="https://github.com/user-attachments/assets/c94439d8-8472-4cde-97ae-8c3bf1eb815f" />

Cuando se pulsa uno de los botones el código javascript realiza una operación HTTP de tipo post. Al recibir esa petición, el servidor hace la publicación correspondiente en el bróker para avisar al autopilotService.    
 
Puesto que el protocolo HTTP se basa en el mecanismo de petición/respuesta, la recepción de los datos de telemetría en el cliente web es un poco más compleja que en casos anteriores. Cuando el cliente se conecta (envía el POST correspondiente) el servidor publica la orden de conectarse y la de recibir datos de telemetría. A partir de ese momento recibirá del servicio los datos de telemetría (a través del bróker) y se irá guardando los valores recibidos en el ultimo paquete de telemetría (solo la altitud y el estado). Por su parte, el cliente web realizará un GET periódicamente solicitando al servidor los datos de telemetría, que recibirá como respuesta al GET (solo altitud y estado).   
 
Se proponen los siguientes ejercicios:    
 
1.	El botón de aterrizar tiene un comportamiento diferente al de despegar. Hacer los cambios necesarios para que el botón también se ponga en color amarillo cuando empiece el aterrizaje y se ponga en verde cuando el dron esté en tierra.
2.	Añadir un nuevo botón para realizar la operación RTL.
    
El mecanismo de petición/respuesta que caracteriza el protocolo HTTP entre el cliente web y el servidor web hace que el flujo de información no sea muy fluido en el caso de datos que viajan con frecuencia entre uno y otro, como es el caso de los datos de telemetría.    
 
Una mejora significativa se obtiene si el script del cliente web, en lugar de hacer peticiones HTTP, hace publicaciones y suscripciones directamente en el bróker que hace de intermediario en la comunicación por MQTT. De esta manera, los paquetes de telemetría que publica el autopilotService llegan también al navegador del móvil igual que a todos los demás dispositivos que se hubieran suscrito.   
 
Los ficheros serverMQTT.py y indexMQTT.html (en la carpeta templates) implementan esta segunda versión de la webapp, que tiene la misma interfaz gráfica. En este caso, el código del servidor es extraordinariamente simple, porque solo tiene que servir el código del cliente web (el fichero indexMQTT.html) a los clientes que se conectan. Es el cliente web el que se conecta al bróker, se suscribe a los mensajes del autopilotService y publica las ordenes según el botón que pulsa el usuario.    
 
Se proponen los siguientes ejercicios:    
 
1.	El botón de aterrizar tiene un comportamiento diferente al de despegar. Hacer los cambios necesarios para que el botón también se ponga en color amarillo cuando empiece el aterrizaje y se ponga en verde cuando el dron esté en tierra.
2.	Añadir un nuevo botón para realizar la operación RTL.
3.	Añadir los elementos necesarios para poder cambiar el heading del dron, igual que puede hacerse en las aplicaciones descritas en apartados anteriores.

### 4.3 Videostreaming   
 
Muchas de las aplicaciones de los drones requieren la captura y procesado de imágenes, como, por ejemplo, el stream de video. Naturalmente, esto requiere que el dron tenga instalada una cámara abordo y un trasmisor que envíe la señal de vídeo a la estación de tierra, en la que debe hacer un receptor que permita entregar ese stream de video a la aplicación que lo necesite.    
 
De nuevo, interesa que el stream de video sea capturado por un servicio (cameraService) que tendrá acceso al receptor y que luego pueda entregarlo al cliente que lo solicite (por ejemplo, un Dashboard como los descritos antes).    
 
Para implementar la comunicación entre el cameraService y el cliente teóricamente podría usarse MQTT, de manera que el servicio publicaría periódicamente los frames del stream de video que recibiría el cliente para mostrarlos al usuario. Sin embargo, MQTT no está pensado para transmitir datos voluminosos (como los frames) con mucha frecuencia (la necesaria en un stream de video en tiempo real).    
 
Una alternativa mucho mejor es enviar el stream de video usando WebRTC. Este mecanismo trabaja sobre UDP/IP y, por tanto, no necesita espera las  confirmaciones de paquetes típicas del protocolo TCP/IP, que es el que usa MQTT. El resultado es una mucho mayor fluidez en la transmisión del stream de video.    
 
Cuando se usa WebRTC, uno de los agentes implicados (emisor o receptor) debe actuar como servidor y el otro como cliente. El cliente se conecta al servidor usando la IP de éste. Para establecer la conexión el cliente y servidor intercambian algunos mensajes usando un websocket. Una vez establecida la conexión el emisor envía el stream de video que llegará al receptor con menor retraso y mejor fluidez, como corresponde al uso de UDP en vez de TCP, aunque con posibles pérdidas de paquetes que, si bien serían inadmisibles si se están enviando instrucciones, no van a afectar significativamente a la experiencia de usuario en el caso de video streaming.    
 
El fichero cameraService.py contiene el código necesario para capturar el stream de video usando la librería OpenCV y emitirlo por WebRTC.  El código captura el video de la webcam conectada al portátil en el que se ejecute, pero cambiando el valor de camera_id puede capturar el video que llega al receptor que tenga conectado. Al ponerse en marcha, el servicio queda a la espera de que algún cliente solicite el stream de video. Entonces se inicia un sencillo protocolo de coordinación a través de un web socket hasta que puestos de acuerdo se inicia la trasmisión del stream de video, frame a frame (en la función recv).    
 
El fichero DashboardLocalConVideoStream.py contiene el código de un dashboard que es básicamente igual que el descrito en el apartado x, al que se le ha añadido un botón para conectarse al CameraService y recibir el stream de video para mostrarlo al usuario. El código está preparado para el caso de que tanto el dashboard como el servicio se ejecuten en el mismo portátil (que debe tener una webcam). El sistema funcionaría igual si el servicio de cámara y el dashboard se ejecutan en portátiles diferentes pero conectados a la misma red de área local. En ese caso, hay que sustituir la palabra localhost en la función videoReceiver del Dashboard por la IP del servicio dentro de la red de área local.    
 
La transmisión de video por WebRTC puede funcionar también en el caso de que el servicio y el dashboard estén conectados a Internet pero no en la misma red de área local. Si el servicio no está conectado a una IP pública entonces la coordinación entre servicio y dashboard debe realizarse a través de un proxy que si tenga una IP pública conocida por ambos. Pero ese planteamiento se escapa del alcance de la versión 1 y puede quedar como objetivo en las siguientes versiones.

### 4.4 Reconocimiento de objetos    
 
Es habitual que el stream de video se requiera para reconocer objetos en la imagen. Para ello se utilizan redes neuronales convenientemente entrenadas.   
 
Es muy fácil experimentar con la tecnología del reconocimiento de objetos usando alguna red neuronal previamente entrenada y de libre acceso. Un ejemplo es la red neuronal capaz de reconocer cualquiera de los 80 tipos de objetos del data set COCO (Common Objects in Context). Entre esos objetos hay: banana, coche, perro, reloj, donut y así hasta 80.    
 
El fichero DashboardLocalConDeteccion.py contiene el código de un DashBoard que puede activar la detección de tres tipos de objetos: bananas, pizzas y relojes. El código es muy similar al Dashboard anterior, que mostraba el stream de video, pero se le ha añadido el código que usa la red neuronal para detectar los objetos en los frames que recibe. La mecánica es sencilla. El detector de objetos se ha implementado en la clase Detector, que usa la red neuronal pre-entrenada. Cada vez que se recibe un frame se llama a la función de detección indicándole el identificador del objeto que se quiere identificar (cada uno de los 80 objetos del data set de COCO tiene un identificador). El detector retorna una indicación de si lo ha detectado o no y en caso afirmativo las coordenadas del rectángulo dentro del frame en el que se ubica el objeto identificado. El dashboard usa esa información para añadir el rectángulo al frame y mostrarlo al usuario, tal y como muestra la figura.    

<img width="795" height="575" alt="image" src="https://github.com/user-attachments/assets/dce64e9a-1060-4112-817b-4df7874e2ff3" />

 
El proceso de detección se toma su tiempo. Si la detección se aplica a cada frame entonces la fluidez del stream de video va a verse muy afectada. El problema se reduce si aplicamos la detección solo a un frame de cada 100. Eso es justamente lo que hace el programa. Cuando detecta el objeto en un frame dibuja el rectángulo y lo añade a los 100 frames que vienen después antes de volver a intentar la detección.   
 
Se proponen los siguientes ejercicios:    
 
1.	Procesar 1 de cada 100 frames hace que el impacto en la fluidez sea despreciable, pero introduce un retardo en la detección del objeto. Experimentar con valores más bajos de ese periodo hasta encontrar un mejor compromiso entre fluidez y retardo en la detección.
2.	Añadir botones para reconocer otros objetos del data set de COCO.


## 5. Versión 2
Lo que hemos llamado versión 1 no es en realidad una versión de nada. Se trata de diferentes módulos desarrollados de manera independiente para aprender conmceptos y herramientas. Ahora ha llegado el momento de crear una verdadera versión de un sistema en el que los díferentes módulos estén interconectados y puedan colaborar en la tarea de controlar el dron.    

En la versión 2 habrá solo 3 modulos: el dashboard en python, el dashboard en C# y una webapp, todos ellos conectados a Internet. Además, ampliaremos las funcionalidades de todos ellos con, por ejemplo, mapas geolocalizados o control del dron por voz.    

Además, la vesión 2 va a estar mucho menos guiada. Será necesario buscar información, probar y buscar más. El uso de ChatGPT (o similar) será de mucha ayuda, aunque se espera que la versión 2 se construya sobre la base de lo aprendido en la versión 1, y no con códigos muy diferentes, proporcionados por la IA, que funcionas pero a penas se entienden. En cualquier caso, en el apartado 5.2 se proporcionan algunas pistas y se sugieren algunos recursos que pueden ser de ayuda.    
 
Será también muy adecuado repartir trabajo entre los miembros del equipo para poder cumplir con el plazo de entrega de esta versión.    

### 5.1 Requisitos específicos de esta versión    
 
Veamos los requisitos de cada uno de los tres módulos del sistema a desarrollar.    

#### 5.1.1 Dashboard en Python   

1.  El dashboard en Python debe integrar el servicio de autopiloto y el servicio de cámara. 
2. Debe poder trabajar en modo local o en modo global, según indique el usuario (quizá con un botón).
3. Si se pone marcha en modo local entonces debe activar el servicio de autopiloto y el servicio de cámara. 
4. Siempre tiene que haber una (y solo una) instancia del dashboard que se ponga en marcha en modo local, en el portátil que tenga la radio de telemetría y el receptor del vídeo del dron. 
5. Pueden ponerse en marcha una o varias instancias del dashboard en modo global que interactuaran con el servicio de autopiloto por MQTT y con el servicio de cámara por WebRTC.
6. Tanto en modo local como en modo global, el dashboard debe mostrar al usuario un mapa geolocalizado que muestre la posición en la que está el dron en cada momento, igual que lo hace Mission Planner.
7. El usuario de poder interactuar con el dron a través del mapa, por ejemplo clicando en un punto del mapa para que el dron se dirija a ese punto.
8. Tanto en modo local como en modo global el usuario debe poder solicitar el reconocimiento de objetos en el stream de video. Incluso debe poder solicitar que se reconozcan varios tipos de objetos simultaneamente, seleccionados de entre un subconjunto del data set de COCO.
9. El servicio de cámara debe suministrar el stream de video por WebRTC a todos los módulos que lo soliciten.

#### 5.1.2 Dashboard en C#   

1. Debe funcionar en modo global, es decir, haciendo peticiones al servicio de autopiloto por MQTT
2. Debe mostrar al usuario un mapa geolocalizado con la ubicación del dron en cada momento
3. El usuario debe poder clicar en el mapa para hacer que el dron se dirija a ese punto
4. Debe mostrar el stream de video que se recibe por WebRTC del servicio de cámara
5. El usuario debe poder solicitar el reconocimiento de uno o varios objetos de entre un subconjunto del data ser de COCO
6. Debe permitir capturar imagenes del stream de video (hacer fotos) y guardarlas, de manera que el usuario pueda verlas cuando quiera en un formulario que muestre una galería de las fotos tomadas

#### 5.1.3 WeApp   

1. Debe tener una pestaña que muestre los botones para controlar el dron, otra para mostrar un mapa geolocalizado con la posición del dron en cada momento y otra con el stream de video que se recibe del dron
2. Debe comunicarse con el servicio de autopiloto por MQTT y con el servicio de cámara por WebRTC
3. El usuario debe poder controlar el dron mediante la voz, diciendo palabras clave como: "Despega", "Aterriza", "Vuela hacia el Norte", etc.

## 5.2 Observaciones y recursos
Para muchos de los retos que se han planteado, la IA puede proporcionar soluciones fáciles de adaptar (por ejemplo, el tema de los mapas geolocalizados o en tema de captar la voz y convertirla en texto). Pero es posible que la IA no ayude mucho en los retos relacionados con la trasmisión del video por WebRTC.

El envío del stream de video por WebRTC a través de Internet no es trivial porque requiere de un proxy con IP pública a la que se conecten tanto el emisor como los diferentes clientes que soliciten el vídeo. Ese proxy también forma parte del sistema.    

Por otra parte, la recepción del vídeo por parte del Dashboard el C# tampoco es fáci. La codificación en C# de las operaciones para establecer la conexión son complejas y no hay buena información al respecto. Es más fácil que la conexión y recepción la realice un script de Python que activa el dashboard en C# y que facilite el stream recibido al dashboard para que éste lo muestre al usuario.   

Finalmente, tampoco es sencillo hacer que el stream de video se muestre en el cliente web de la WebApp.    

En todo caso, en este repositorio hay abundante material que puede resultar de ayuda para resolver estos retos.  

El uso del micrófono del dispositivo móvil para capturar la voz y controlar el dron con ella plantea el reto de que debe hacerse en modo seguro, es decir, con HTTPS y no con HTTP. Esto es así porque tratandose de información privada del usuario (su voz) los navegadores exigen que la información se transmita encriptada, lo cual requiere del uso de certificados que implementen claves públicas y privadas. Lo mismo pasaría si quisiésemos capturar información de otros sensores del movil, como por ejemplo, la imagen de la cámara o la geolocalización del móvil. Aunque resolver la cuestion solo requiere generar los certificados necesarios (cosa muy sencilla) y añadir unas pocas líneas de código los conceptos que hay detrás son complejos, aunque muy interesantes. En este repositorio hay material abundante que resultará de ayuda para aprender los conceptos clave y abordar el reto.








