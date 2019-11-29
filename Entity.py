import socket, threading
#Tipo de queries
    #1 - Pedir datos(nombre,SO,Bytes recividos)
    #2 - Apagar computadora
    #3 - Reiniciar
class Entity(object):
    def __init__(self,socket):
        threading.Thread.__init__(self)
        self.socket = socket
        self.data = self.request_data()

    #def run(self):
    #    while True:
    #        data = self.socket.recv(2048)
    #        msg = data.decode()
    #        self.socket.send(bytes(msg,'UTF-8'))
    def request_data(self):
        self.socket.send(bytes("1",'UTF-8'))
        data = self.socket.recv(4096)
        return data.decode().split(",")
    def getData(self):
        return self.data
    def isConn(self):
        try:
            self.socket.send(bytes("2",'UTF-8'))
            data = self.socket.recv(4096)
            if(data == ''):
                self.socket.close()
        except:
            return False
        else:
            return True
