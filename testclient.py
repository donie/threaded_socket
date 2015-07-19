import socket
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s '
                    '[%(levelname)s] (%(threadName)-10s) %(message)s',)


def client(string):
    HOST, PORT = 'localhost', 12345
    # SOCK_STREAM == a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.setblocking(0)  # optional non-blocking
    sock.connect((HOST, PORT))
    sock.send(string)
    reply = sock.recv(16384)  # limit reply to 16K
    logging.debug(reply)
    sock.close()
    return reply

if __name__ == "__main__":
    client("test bang #1")
    client("test bang #2")
    client("test bang #3")
    client("test bang #4")
    client("test bang #5")
    client("test bang #6")
