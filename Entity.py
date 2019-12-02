import socket, threading
#Tipo de queries
    #1 - Pedir datos(nombre,SO,Bytes recibidos)
    #2 - Apagar computadora
    #3 - Reiniciar
class Entity(object):
    def __init__(self,socket,address):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.data = self.request_data()

    #def run(self):
    #    while True:
    #        data = self.socket.recv(2048)
    #        msg = data.decode()
    #        self.socket.send(bytes(msg,'UTF-8'))
    def request_data(self):
        self.socket.send(bytes("1",'UTF-8'))
        data = self.socket.recv(4096)
        data = data.decode()
        data += "," + self.address
        return data.split(",")
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
    def getPackages(self):
        try:
            self.socket.send(bytes("3",'UTF-8'))
            data = self.socket.recv(4096)
        except:
            return 0
        else:
            return data
    def powerOff(self):
        self.socket.send(bytes("4",'UTF-8'))
        data = self.socket.recv(4096)
        if(data == "1"):
            self.socket.close()
    def reboot(self):
        self.socket.send(bytes("5",'UTF-8'))
        data = self.socket.recv(4096)
        if(data == "1"):
            self.socket.close()
