import socket
import json

BUFFSIZE = 10000
JSON_PATH_DEFAULT = "files/json_actividad_http.json"


def load_json(path: str) -> dict:
    if path == "":
        path = JSON_PATH_DEFAULT
    with open(path) as fd:
        mapeo = json.load(fd)
    return mapeo


def receive_full_msg(reciver_socket: socket.socket, buf_size: int) -> bytes:
    return reciver_socket.recv(buf_size)


def send_full_msg(sender_socket: socket.socket, msg: bytes) -> int:
    return sender_socket.send(msg)
