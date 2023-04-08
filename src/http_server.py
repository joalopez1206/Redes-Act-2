# lets initialize a sever in port 8000
from utils import *
import http_parser as hpar
import pprint
pprinter = pprint.PrettyPrinter(indent=4, sort_dicts=False)
ADDRESS = ('localhost', 8000)
PATH: str = input("Before initializing the server, i need a config file in the format .json, give me a path: ")
configuration = load_json(PATH)
httpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pprinter.pprint(configuration)
exit(0)
print("Initializing server")
httpServer.bind(ADDRESS)
httpServer.listen(3)
while True:
    # la idea de este codigo es que
    # 1- Empiezo esperando un cliente
    # 2- Le digo que el mensaje fue recibio
    # 2- Decodifico si es un response o request
    # 4- y de ahí por el momento solo printeo.
    print("Waiting for clients")
    receiverSocket, addr = httpServer.accept()
    print("A Message has been recived, establishing communication channel")
    msg = receiverSocket.recv(BUFFSIZE)
    print("parsing message...")
    parsed_msg = hpar.parse_http(msg.decode())
    print("The http meesage is a:", hpar.is_response_or_request(parsed_msg))
    pprinter.pprint(parsed_msg)
    print("Answering The request:")
    content_type = "text/html"
    with open("files/hello-world.html") as fd:
        str_to_append = fd.read()
    cabezera = {hpar.METHOD:"HTTP/1.1 200 OK", 'Server':'nginx', 'Content-Type':f'{content_type}', 'Content-Length':f'{len(str_to_append.encode())}'}
    cuerpo = str_to_append
    cabezera["X-El-Que-Pregunta"] = parsed_msg[hpar.HEAD]["User-Agent"]
    estrucutra_respuesta = {hpar.HEAD: cabezera, hpar.BODY:cuerpo}
    http_response = hpar.to_http(estrucutra_respuesta)
    print(http_response)
    receiverSocket.send(http_response.encode())
    receiverSocket.close()
