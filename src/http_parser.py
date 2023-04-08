HEAD = "head"
BODY = "body"
METHOD = "method"
REQUEST_SEQUENCES = ("GET", "POST", "HEAD")
RESPONSE_SEQUENCE = "HTTP"
END_HEAD_SEQUENCE = '\r\n\r\n'
RESPONSE = 0
REQUEST  = 1
mapeo = {RESPONSE: "RESPONSE", REQUEST: "REQUEST"}


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
        retdict[line[0]] = line[1].strip()
    return retdict


def parse_body(body) -> str:
    return body


def head_to_http(head_struct_http: dict) -> str:
    retstr = ""
    retstr += head_struct_http[METHOD]
    retstr += "\r\n"
    for atribute in head_struct_http:
        if atribute == METHOD:
            continue
        string_to_add = ": ".join([atribute, head_struct_http[atribute]])
        retstr += string_to_add
        retstr += "\r\n"
    return retstr + "\r\n"


def to_http(parsed_msg: dict) -> str:
    return head_to_http(parsed_msg[HEAD]) + parsed_msg[BODY]


def is_response_or_request(parsed_msg: dict) -> str:
    head_line = parsed_msg[HEAD][METHOD]
    return mapeo[REQUEST] if head_line.startswith(REQUEST_SEQUENCES) else mapeo[RESPONSE]