import json
import sys
import time
from threading import Thread
from threading import Lock
import socket
import select


class Debugger(object):
    def __init__(self):
        self.server = None
        self.sockets = []
        self.queue = []
        self.running = True
        self.lock = Lock()
        t = Thread(target=self.server_thread)
        t.setDaemon(True)
        t.start()
        pass

    def send(self, msg):
        while len(self.sockets) < 1 or self.sockets[0] == self.server:
            time.sleep(0.1)
        self.sockets[0].send(msg + "\n")

    def wait_for(self, msg):
        line = ""
        while not line == msg:
            self.lock.acquire()
            if msg in self.queue:
                self.queue.remove(msg)
                line = msg
            self.lock.release()

    def server_thread(self):
        while self.running:
            line = self.server_styled_pull("localhost", 25923)
            self.lock.acquire()
            self.queue.append(line)
            self.lock.release()

    def close_sock(self, sock):
        sock.close()
        self.sockets.remove(sock)

    def server_styled_pull(self, host, port):
        line = None
        if self.server is None:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # bind the socket to a public host, and a well-known port
            self.server.bind((host, port))
            # become a server socket
            self.server.listen(5)
            self.sockets.append(self.server)
        sock = None
        sf = None
        while sock is None:
            ready_to_read, ready_to_write, in_error = select.select(self.sockets, [], [], 1)
            if len(ready_to_read) > 0:
                sock = ready_to_read[0]
                if sock == self.server:
                    sock, addr = self.server.accept()
                    self.sockets.append(sock)
                    self.close_sock(self.server)
                    sock = None
                    continue
                try:
                    sf = sock.makefile()
                except:
                    self.close_sock(sock)
                    sock = None
            else:
                time.sleep(0.001)
        line = sf.readline().rstrip('\n')
        return line
