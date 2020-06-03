import socket
import threading
from Data_Base import DataBase
import random
import string
from Send_Gmail import send_email
from Rocket_Mode import Rocket
from Data_Points import DataBasePoints


class Server(object):

    def __init__(self, ip, port):
        """
        The server class. Open the socket connections to the different clients. Answer to the clients.
        :param ip: The server ip.
        :param port: The sever port.
        """
        self.ip = ip  # The server ip
        self.port = port  # The server port
        self.count = 0  # how many users at the same time.
        self.g_count = 0  # gaza count
        self.i_count = 0  # Israel count
        self.arr_hits = []  # an array of the hits.

        print('a -> the client gives the user name -> the server gives the password \n'
              'b -> the client gives the user name -> the server gives the email \n'
              'c -> the client gives the user name, password and the email')

        # Start socket connection
        self.my_socket = socket.socket()
        self.set_socket()
        self.accept_new_users()

    def set_socket(self):
        """
        This function builds the socket connection, bind it to the right ip and port.
        """
        self.my_socket.bind((self.ip, self.port))
        self.my_socket.listen(5)

    def accept_new_users(self):
        """
        If a new socket is trying to connect, it happens through this function. Accept the new connections from
        the different clients. Contains a loop that runs forever and listen.
        """
        while True:
            client_socket, address = self.my_socket.accept()  # block
            self.count += 1
            print('New client entered num: {} \n'
                  'In this address: {}'.format(self.count, address))
            # Main Program:
            self.handle_client(client_socket, address)

    def handle_client(self, client_socket, address):
        """
        Opens a new thread for a new connection, the thread is the main game function.
        :param client_socket: The client socket connection
        :param address: The client address
        """
        print("hello")
        new_client = threading.Thread(target=self.start, args=(client_socket, address,))
        new_client.start()

    def temp_password(self):
        """
        Generates the new temporary password - which includes both letters and numbers, in a random length.
        returns this password
        """
        string_length = random.randint(6, 9)  # The length of the new temporary password.
        letters_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_digits) for i in range(string_length))

    def start(self, client_socket, address):
        """
        This function is a forever loop (closes when the client quits), handles all of the requests of this client.
        :param client_socket: The client socket connection
        :param address: The client address
        """
        data_base = DataBase()
        city_data = DataBasePoints()
        client_name = client_socket.recv(1024).decode()
        print('The type is: ', client_name)
        type_client = int(client_name)
        if type_client == 0:
            self.g_count += 1
        elif type_client == 1:
            self.i_count += 1
        while client_name != 'exit':
            client_name = client_socket.recv(1024).decode()
            print(client_name)
            if client_name == '':
                break
            if client_name != 'exit':
                arr = client_name.split(' ')
                if arr[0] == 'a':
                    # Tries to login. arr[1] = username, arr[2] = password.
                    password = data_base.check_password(arr[1])
                    if arr[2] == password:
                        client_socket.send(bytes('True', 'utf-8'))
                        print('the password is correct!')
                    else:
                        client_socket.send(bytes('False', 'utf-8'))
                        print('the password is incorrect')

                elif arr[0] == 'b':
                    # Tries to change the password. arr[1] = username, arr[2] = email.
                    print('the user name is:', arr[1])
                    email = data_base.forgot_password(arr[1])
                    if email == arr[2]:
                        client_socket.send(bytes('True', 'utf-8'))
                        temporary_pass = self.temp_password()  # Generate the temporary password.
                        try:
                            send_email(arr[1], temporary_pass, arr[2])  # A new temporary password is sent to the email.
                            client_name = client_socket.recv(1024).decode()
                            print('Thr new str is: ', client_name)
                            print('The temp is: ', temporary_pass)
                            new_arr = client_name.split(' ')  # new_arr[0] = temp password, new_arr[1] = mew password.
                            if temporary_pass == new_arr[0] and data_base.change_password(arr[1], new_arr[1]):
                                client_socket.send(bytes('True', 'utf-8'))  # correct.
                            else:
                                client_socket.send(bytes('False', 'utf-8'))
                        except:
                            client_socket.send(bytes('False', 'utf-8'))

                elif arr[0] == 'c':
                    # Tries to register. arr[1] = username, arr[2] = password, arr[3] = email.
                    msg = data_base.new_user(arr[1], arr[2], arr[3])
                    client_socket.send(bytes(msg, 'utf-8'))

                elif arr[0] == 'd':
                    # Gets new rocket, arr[1] = type, ar[2] = alpha, arr[3] = beta, arr[4] = speed,
                    # arr[5] = start point x, arr[6] = start point y.
                    r = Rocket(arr[1], int(arr[2]), int(arr[3]), int(arr[4]))
                    x_point, y_point = r.point_on_map(int(arr[5]), int(arr[6]))  # Ending points.
                    print(x_point, y_point)
                    if x_point > 258 or x_point < 21:
                        client_socket.send(bytes('false', 'utf-8'))
                    elif y_point < 10:
                        client_socket.send(bytes('false', 'utf-8'))
                    else:
                        # Legal rocket:
                        msg = r.get_weight() + ' ' + str(r.t) + ' ' + str(r.total_destination) + ' ' + str(x_point) +\
                              ' ' + str(y_point) + ' ' + str(r.x_des) + ' ' + str(r.y_des)
                        print('i am the server: ' + msg)
                        client_socket.send(bytes(msg, 'utf-8'))  # Send details about the rocket.
                        time = r.get_time()
                        print('hey')
                        city = city_data.find_city(x_point, y_point)
                        print('bye')
                        info = (str(len(self.arr_hits) + 1), str(x_point), str(y_point), city, str(time))
                        self.arr_hits.append(info)  # Add rocket to the array.

                elif arr[0] == 'e':  # arr[1] = number of alarms you need, arr[2] = from which point (last alarm number
                    # given.
                    num = int(arr[1])
                    length = len(self.arr_hits)
                    mis = int(arr[2])
                    print('g count is: ', self.g_count)

                    msg = str(self.g_count) + ' '

                    if length == 0:  # No hits at all.
                        msg += '0'

                    elif mis >= length:  # If there are no new hits.
                        msg += '0'

                    elif length - mis >= num:
                        msg += str(num)
                        for i in range(num):
                            x = self.arr_hits[length - num + i]  # tuple
                            for j in x:
                                msg += ' ' + j

                    elif length - mis < num:
                        x = length - mis
                        msg += str(x)
                        for i in range(x):
                            x = self.arr_hits[mis+i]  # tuple
                            for j in x:
                                try:
                                    msg += ' ' + j
                                except:
                                    print('huge problem!', j)
                    print(msg)
                    client_socket.send(bytes(msg, 'utf-8'))

                print(self.arr_hits)

        if type_client == 0:
            print('bye G')
            self.g_count -= 1
            print(self.g_count)
        elif type_client == 1:
            print('bye I')
            self.i_count -= 1
        self.count -= 1
        # exit this specific connection.


ip = '0.0.0.0'
port = 7777
s = Server(ip, port)
