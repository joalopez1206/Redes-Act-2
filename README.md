# Actividad 1
Hola este es el mini informe de esta actividad (Aun quedan refactorings xd).
La idea es que tenemos 3 modulos `http_parser, proxy_http_server y utils.py`
- El modulo `http_parser` se encarga de parsear los http messages para que despues
server pueda interpretarlos para hacer alguna accion!
- El modulo `proxy_http_server` es el que se encarga de interpertar los mensajes y tomar alguna accion!
- El modulo `utils` implementa las funciones `send_full_msg` y `recv_full_msg` y algunas
funciones de calidad de vida como `load_json`.

En palabras simples, lo que hace el servidor proxy es:
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
