from utils import *
import http_parser as hpar

LISTEN_Q_LEN = 3
ADDRESS = ('localhost', 8000)

# Config PATH
instr = ("Before initializing the server, i need a config file in the format '.json', give me a path: (by default is "
         "the hardcoded path)")
PATH: str = input(instr)
configuration = load_json(PATH)

httpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Initializing server")
httpServer.bind(ADDRESS)
httpServer.listen(LISTEN_Q_LEN)

while True:
    print("Waiting for clients")
    receiverSocket, addr = httpServer.accept()

    print("A Message has been recived, establishing communication channel")
    received_msg = receive_full_msg(receiverSocket, BUFFSIZE)

    print("parsing message...")
    parsed_received_message = hpar.parse_http(received_msg.decode())
    print(f"==\n{received_msg.decode().strip()}\n==")

    # print("The http message is a:", hpar.is_response_or_request(parsed_received_message))
    request_head: dict = parsed_received_message[hpar.HEAD]

    if hpar.get_url(request_head) in configuration["blocked"]:
        send_full_msg(receiverSocket, "HTTP/1.1 403 Forbidden\r\n\r\n".encode())
        receiverSocket.close()
        print("Forbidden page!")
        continue

    print("And is not forbidden!")
    print("Creating proxy socket!")
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_addr = (parsed_received_message[hpar.HEAD]["Host"], 80)

    parsed_received_message[hpar.HEAD].update({"X-ElQuePregunta": "Joaquin"})
    print("Connecting to", proxy_addr, "\n")
    sender_socket.connect(proxy_addr)

    print("Sending request message to", proxy_addr[0], "@ port", proxy_addr[1])
    sender_msg = hpar.to_http(parsed_received_message)
    send_full_msg(sender_socket, sender_msg.encode())
    proxy_message = receive_full_msg(sender_socket, BUFFSIZE)

    print("Message received! re-sending to client and ending sender_socket.")
    sender_socket.close()
    parsed_message = hpar.parse_http(proxy_message.decode())

    print("Censoring the message!")
    parsed_message[hpar.BODY] = censor_body(parsed_message[hpar.BODY], configuration["forbidden_words"])
    new_c_len = len(parsed_message[hpar.BODY].encode())
    parsed_message[hpar.HEAD]["Content-Length"] = str(new_c_len)

    send_full_msg(receiverSocket, hpar.to_http(parsed_message).encode())

    print("Message sent! ending receiver socket")
    receiverSocket.close()
