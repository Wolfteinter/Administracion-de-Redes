from sys import argv
import socket
import os
import platform
import time
import os
import psutil
#Tipo de queries
    #1 - Pedir datos constantes(nombre,SO)
    #2 - Pedir datos variables(numero de paketes,tipo de paquetes)
    #3 - Apagar computadora
    #4 - Reiniciar computadora
class Cliente(object):
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.cli = socket.socket()
        self.name = str(socket.gethostname())
        self.SO = str(platform.system())
    def conectar(self):
        self.cli.connect((self.host, self.port))
        while(True):
            opt = self.cli.recv(4096)
            opt = int(opt.decode())
            #send constant data of the dispositive
            if opt == 1 :
                data = self.name+","+self.SO
                self.cli.send(data.encode())
            if opt == 2:
                data = "1"
                self.cli.send(data.encode())
            if opt == 3: self.cli.send(str(psutil.net_io_counters(pernic=True)['lo'][1]).encode())
            if opt == 4:
                self.cli.send("1".encode())
                time.sleep(1)
                os.system("systemctl poweroff")
            if opt == 5:
                self.cli.send("1".encode())
                time.sleep(1)
                os.system("systemctl reboot")

        self.cli.close()

# Example: python3 Cliente.py serverHost
host = argv[1]
cli = Cliente(str(host),8080)
cli.conectar()
