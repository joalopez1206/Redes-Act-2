# lets initialize a sever in port 8000
from utils import *
import http_parser as hpar

ADDRESS = ('localhost', 8000)
httpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
    print("A Message has been recived")
    msg = recive_full_msg(receiverSocket, BUFFSIZE)
    print("parsing message")
    parsed_msg = hpar.parse_http(msg)
    print("The http meesage is a:", parsed_msg["type"])
    print(parsed_msg["message"])
    print("translating back to http")
    other_msg = hpar.to_http(parsed_msg)
    if msg == other_msg:
        print("nais")
    else:
        print("na")
    receiverSocket.send(msg)
    receiverSocket.close()
