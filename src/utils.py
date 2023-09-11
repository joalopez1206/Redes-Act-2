import socket
import json
from http_parser import parse_head

BUFFSIZE=210
JSON_PATH_DEFAULT = "files/json_actividad_http.json"


def load_json(path: str) -> dict:
    if path == "":
        path = JSON_PATH_DEFAULT
    with open(path) as fd:
        mapeo = json.load(fd)
    return mapeo


def receive_full_msg(reciver_socket: socket.socket, buff_size: int) -> bytes:
    recv_message = reciver_socket.recv(buff_size)
    full_message: bytes = recv_message

    # verificamos si llegó el head completo o si aún faltan partes del mensaje
    is_end_of_head = "\r\n\r\n" in full_message.decode()

    while not is_end_of_head:
        recv_message = reciver_socket.recv(buff_size)
        full_message += recv_message

        is_end_of_head = "\r\n\r\n" in full_message.decode()

    head, body = full_message.split(b"\r\n\r\n")
    cnt_len = parse_head(head.decode()).get("Content-Length")
    if cnt_len is None:
        return full_message
    cnt_len = int(cnt_len)
    len_body = len(body)

    while len_body < cnt_len:
        recv_message = reciver_socket.recv(buff_size)
        body += recv_message
        len_body += min(buff_size, len(recv_message))

    retbyte = (head+b"\r\n\r\n"+body)
    return retbyte


def send_full_msg(sender_socket: socket.socket, msg: bytes) -> int:
    return sender_socket.send(msg)


def censor_body(http_body: str, forbidden_words: dict, ) -> str:
    for dictionary in forbidden_words:
        old_word = list(dictionary.keys())[0]
        new_word = dictionary[old_word]
        http_body = http_body.replace(old_word, new_word)
    return http_body
