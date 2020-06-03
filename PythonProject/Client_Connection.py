import socket


class Client:
    def __init__(self, ip, port, x=2):
        """
        This class is the socket connection to the server.
        :param ip: The ip to connect to the server.
        :param port: The server port.
        :param x: Type of client (which side).
        """
        try:
            self.my_socket = socket.socket()
            self.my_socket.connect((ip, port))
            print('client x is: ', x)
            self.my_socket.send(bytes(str(x), 'utf-8'))
            print('s')
        except:
            print('f')

    def send(self, str):
        """
        Send a message to the server, and get his response.
        :param str: What the client went to send to the server.
        :return: If the server sent a message, his message. If not, nothing.
        """
        try:
            self.my_socket.send(bytes(str, 'utf-8'))
            if str == 'exit':
                print('get out of the client')
                self.my_socket.close()
            else:
                message = (self.my_socket.recv(1024)).decode('utf-8')
                return message
        except:
            pass

