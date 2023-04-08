# lets initialize a sever in port 8000
import socket

prefix_protocol = "http://"
from utils import *
import http_parser as hpar
import pprint

example = False
pprinter = pprint.PrettyPrinter(indent=4, sort_dicts=False)
ADDRESS = ('localhost', 8000)
PATH: str = input("Before initializing the server, i need a config file in the format '.json', give me a path: ")
configuration = load_json(PATH)
httpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Initializing server")
httpServer.bind(ADDRESS)
httpServer.listen(3)
while True:
    print("Waiting for clients")
    receiverSocket, addr = httpServer.accept()
    print("A Message has been recived, establishing communication channel")
    msg = receiverSocket.recv(BUFFSIZE)
    print("parsing message...")
    parsed_msg = hpar.parse_http(msg.decode())
    print(msg.decode().strip())
    print("The http message is a:", hpar.is_response_or_request(parsed_msg))
    if example:
        pprinter.pprint(parsed_msg)
        print("Answering The request:")
        content_type = "text/html"
        with open("files/hello-world.html") as fd:
            str_to_append = fd.read()
        cabezera = {hpar.METHOD: "HTTP/1.1 200 OK", 'Server': 'nginx', 'Content-Type': f'{content_type}',
                    'Content-Length': f'{len(str_to_append.encode())}'}
        cuerpo = str_to_append
        cabezera["X-El-Que-Pregunta"] = parsed_msg[hpar.HEAD]["User-Agent"]
        estrucutra_respuesta = {hpar.HEAD: cabezera, hpar.BODY: cuerpo}
        http_response = hpar.to_http(estrucutra_respuesta)
        print(http_response)
        receiverSocket.send(http_response.encode())
    request_head: dict = parsed_msg[hpar.HEAD]
    if hpar.get_url(request_head) in configuration["blocked"]:
        receiverSocket.send("HTTP/1.1 403 Forbidden\r\n\r\n".encode())
        receiverSocket.close()
        print("Forbidden page!")
        continue
    print("And is not forbidden!")
    print("Creating proxy socket!")
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_addr = (parsed_msg[hpar.HEAD]["Host"], 80)
    parsed_msg[hpar.HEAD].update({"X-ElQuePregunta": "Joaquin"})
    print("Connecting to", proxy_addr)
    sender_socket.connect(proxy_addr)
    print("Sending message")
    sender_msg = hpar.to_http(parsed_msg)
    sender_socket.send(sender_msg.encode())
    proxy_message = sender_socket.recv(BUFFSIZE)
    print("Message received! re-sending to client and ending sender_socket.")
    sender_socket.close()
    parsed_message = hpar.parse_http(proxy_message.decode())
    print("Censoring the message!")
    for dictionary in configuration["forbidden_words"]:
        old_word = list(dictionary.keys())[0]
        new_word = dictionary[old_word]
        parsed_message[hpar.BODY] = parsed_message[hpar.BODY].replace(old_word, new_word)
    new_c_len = len(parsed_message[hpar.BODY].encode())
    parsed_message[hpar.HEAD]["Content-Length"] = str(new_c_len)
    receiverSocket.send(hpar.to_http(parsed_message).encode())
    print("Message sent! ending receiver socket")
    receiverSocket.close()
