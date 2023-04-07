HEAD = "head"
BODY = "body"
METHOD = "method"
REQUEST_SEQUENCES = ("GET", "POST", "HEAD")
RESPONSE_SEQUENCE = "HTTP"
END_HEAD_SEQUENCE = '\r\n\r\n'


def parse_http(msg: str):
    head, body = msg.split(END_HEAD_SEQUENCE)
    return {HEAD: parse_head(head), BODY: parse_body(body)}


def parse_head(head: str):
    retdict = dict()
    # Primero separamos el head en \r\n
    lines = head.split("\r\n")
    # Extraemos el metodo
    retdict[METHOD] = lines[0]
    # y luego recorremos todos los atributos
    for line in lines[1:]:
        line = line.split(":", maxsplit=1)
        retdict[line[0]] = line[1]
    return retdict


def parse_body(body) -> str:
    return body


def to_http(parsed_msg: dict) -> str:
    ...
