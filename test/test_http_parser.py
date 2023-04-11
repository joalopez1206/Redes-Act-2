import unittest
import src.http_parser as htp

testmsg = """GET / undefined
Host: localhost:8000
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1""".replace("\n", "\r\n") + htp.END_HEAD_SEQUENCE


class MyTestCase(unittest.TestCase):
    def test_idempotency(self):
        struct_http = htp.parse_http(testmsg)
        self.assertEqual(htp.to_http(struct_http), testmsg)


if __name__ == '__main__':
    unittest.main()
