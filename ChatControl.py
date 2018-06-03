from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication
from Chat import Ui_MainWindow
import sys
import os
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

class ChatControl(QtWidgets.QMainWindow, Ui_MainWindow):
    edit = None
    saveloc = ""
    def __init__(self):
        super(ChatControl, self).__init__()
        self.setupUi(self)
        self.send.clicked.connect(self.sendMsg)
        self.HOST = input('Enter host: ')
        self.PORT = input('Enter port: ')
        if not self.PORT:
            self.PORT = 33000
        else:
            self.PORT = int(self.PORT)

        self.BUFSIZ = 1024
        self.ADDR = (self.HOST, self.PORT)

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)

        self.receive_thread = Thread(target=self.receive)
        self.receive_thread.start()


    def sendMsg(self):
        msg = self.msg.toPlainText()
        self.msg.clear()  # Clears input field.
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            self.client_socket.close()
            self.top.quit()


    def receive(self):
        """Handles receiving of messages."""
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
                self.msgArea.append(msg)
            except OSError:  # Possibly client has left the chat.
                break



     

    #----Now comes the sockets part----
    



if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    form = ChatControl()
    form.show()
    sys.exit(app.exec_())