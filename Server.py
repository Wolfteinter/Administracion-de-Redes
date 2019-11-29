from Entity import Entity
import socket, threading
class Server(object):
    def __init__(self):
        #Is the storage of the all dispositives in network
        self.dispositives = []
        #The port where will be listening
        self.PORT = 8080
        #The socket of the server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("",self.PORT))
        threading.Thread(target=self.listenDisp).start()
    def listenDisp(self):
        while True:
            self.socket.listen(1)
            clientsock, clientAddress = self.socket.accept()
            entity = Entity(clientsock)
            self.dispositives.append(entity)
    def getDispositives(self):
        return self.dispositives
