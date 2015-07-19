from SocketServer import ThreadingMixIn
from Queue import Queue
import time
import socket
import logging
import threading
import SocketServer

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s '
                    '[%(levelname)s] (%(threadName)-10s) %(message)s',)


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        file = open('test.log', 'wb')
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        response = "{} {}: {}\n".format(time.ctime(), cur_thread.name, data)
        file.write(response)
        self.request.sendall(response)
        file.close()


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    # use a thread pool instead of a new thread on every request
    numThreads = 50
    allow_reuse_address = True

    def serve_forever(self):
        # Handle one request at a time until doomsday.
        self.requests = Queue(self.numThreads)

        for x in range(self.numThreads):
            t = threading.Thread(target=self.process_request_thread)
            t.setDaemon(1)
            t.start()

        # server main loop
        while True:
            self.handle_request()

        self.server_close()

    def process_request_thread(self):
        # obtain request from queue instead of directly from server socket
        while True:
            ThreadingMixIn.process_request_thread(self, *self.requests.get())

    def handle_request(self):
        # simply collect requests and put them on the queue for the workers.
        try:
            request, client_address = self.get_request()
        except socket.error:
            return
        if self.verify_request(request, client_address):
            self.requests.put((request, client_address))

if __name__ == "__main__":
    HOST, PORT = "localhost", 12345

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    try:
        # logging.debug("server loop running in thread:", server_thread.name)
        server.serve_forever()
    except KeyboardInterrupt:
        pass
