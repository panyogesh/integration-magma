import socket

class eCONMGMT:
    server_ep_sock=0
    server_buffer=1024
    conn_addr=()

    @classmethod
    def create_server_endpoint(cls):
        cls.server_ep_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_ep=("127.0.0.1", 50001)
        print(server_ep)
        cls.server_ep_sock.bind(server_ep)
        cls.server_ep_sock.listen()
        conn, addr=cls.server_ep_sock.accept()
        cls.conn_addr=(conn, addr)
