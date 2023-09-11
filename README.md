# HTTP server

## Resumen y Instrucciones

Hay 3 modulos `http_parser, proxy_http_server y utils.py`

- El modulo `http_parser`: se encarga de parsear los http messages para que despues
server pueda interpretarlos para hacer alguna accion!

- El modulo `proxy_http_server`: es el que se encarga de interpertar los mensajes y tomar alguna accion!
En resumen lo que hace es: 
  1. Recibe un request de un cliente y crea un canal de comuniacion con el cliente
  2. Lo parsea
  3. Verifica si cumple las condiciones pedidas, como por ejemplo
     - Verifica si es alguna de las paginas "forbidden" o no, si es así, envia el error forbidden y termina la conexion!
     - Si no es así entonces, se crea un nuevo socket para establecer comuniacion con la pagina que pide el cliente
     - Recibe el mensaje del server, y al head le añade mi nombre (Joaquin).
     - Verifica que en el body no hayan palabras "forbidden".
  4. Finalmente cierra el socket de comunicacion con el server
  5. El proxy envia devuelta el mensaje al cliente
  6. Cierre de socket de comuniacion con el cliente

- El modulo `utils`: implementa las funciones `send_full_msg` y `recv_full_msg` y algunas
funciones de calidad de vida como `load_json`, la cual carga las configuraciones de la carpeta `src/files/`

Notar que en todo este codigo se asume un flujo de informacion, de esta manera:

```txt
1. Envia un mensaje el cliente por el proxy
    cliente ---> proxy ----> server 
2. El server envia la respuesta al cliente y le llega al proxy
    cliente <--- proxy <--- server
```

Para correr el codigo basta con:

```bash
python3 src/proxy_http_server.py 
```

A este punto del commit pasan todos los tests! 
Para probarlos, active el proxy en su navegador y acceda a los dominios provistos por la profesora en EOL.

## Experimentos

1. **Página forbidden**:
Basta con ver que en esta [pagina](http://cc4303.bachmann.cl/secret), sin el proxy muestra los contenidos,
en cambio, si usamos el proxy, no obtenemos nada, y si vemos las herramientas de desarrolladores obtenemos la respuesta

```txt
403 Forbidden
```

2. **Cambios en la pagina inicial**:
Si vemos esta [página](http://cc4303.bachmann.cl) Se añade el header X-ElQueResponde y tambien como side-effect 
se cambiaron las palabras prohibidas.

3. **Cambios en 2 páginas**:
Como se comentó antes, se cambió las palabras prohibidas en http://cc4303.bachmann.cl y tambien en 
http://cc4303.bachmann.cl/replace

4. **Tamaño del buffer**:
En el modulo [utils](src/utils.py) hay una variable que se llama `BUFFSIZE` que setea el tamaño del buffer.
Notemos que para el ejemplo de entrar a http://cc4303.bachmann.cl el tamaño del header son de 195 bytes.
   - Para un tamaño más grande que los headers pero menor que el mensaje
   basta tomar `BUFFSIZE=210`.
   - Para el otro caso basta con usar un `BUFFSIZE=30` ya que ahi estamos entre el tamaño del head y 
   el tamaño del startline.

Reemplazando esa variable, podemos ver que en ambos casos funcionan todos los tests.
