# Imports:
from tkinter import *
from Client_Connection import Client
from Game import Simulation

WHERE = ('172.19.226.31', 7777)


class Windows:
    def __init__(self, where):
        """
        This class is responsible for the opening of the first windows using tkinter, like the login, register, and
        forgot password windows.
        :param where: Where[0] = ip, Where[1] = port
        """
        root = Tk()
        self.where = where
        self.connection = Client(where[0], where[1])
        self.root = root
        self.root.iconbitmap('icon.ico')
        self.open_page()

    def new_page(self):
        """
        Opening a new page (pressed a new button in the login page).
        """
        self.root.destroy()
        self.root = Tk()
        self.root.resizable(0, 0)
        self.root.protocol('WM_DELETE_WINDOW', self.exit_button)
        self.root.iconbitmap('icon.ico')

    def open_page(self):
        """
        Opening the first page.
        """
        self.root.geometry("400x400")  # set the configuration of GUI window
        self.root.title("Open Page")  # set the title of GUI window
        self.root.resizable(0, 0)
        self.root.protocol('WM_DELETE_WINDOW', self.exit_button)

        # create a Form label
        Label(text="Iron Dome\nSimulation", fg="royal blue", width="300", height="2",
              font=("Ink Free", 32)).pack()  # Header

        Label(text="").pack()  # Space

        # create Login Button
        main_login_button = Button(text="Login", bg="royal blue", fg="white", height="2", width="30",
                                   command=lambda: self.login_page())  # Login Button
        main_login_button.pack()

        # Button(text="Login", bg="pink", height="2", width="30").pack()
        Label(text="").pack()  # Space

        # create a register button
        Button(text="Register", bg="LightBlue3", fg="white", height="2", width="30",
               command=lambda: self.register_page()).pack()  # Register Button
        Label(text="").pack()  # Space

        # Quit Button:
        Button(text='Forgot Password', bg="DeepSkyBlue1", fg="white", height="2", width="30",
               command=lambda: self.reset_pass_page()).pack()
        # forgot password window
        self.root.protocol('WM_DELETE_WINDOW', self.exit_button)
        self.root.mainloop()  # start the GUI

    def login_page(self):
        """
        Opening the login page.
        """
        self.new_page()

        self.root.geometry("400x400")  # set the configuration of GUI wind
        self.root.title("Login Page")  # set the title of GUI window

        Label(self.root, text="User Name").grid(row=0)
        Label(self.root, text="Password").grid(row=1)

        e1 = Entry(self.root, width=25)
        e2 = Entry(self.root, width=25)
        e1.grid(row=0, column=170)
        e2.grid(row=1, column=170)

        space = Label(self.root, height="1", width="19")
        login_button = Button(self.root, text="Login", bg="Royal Blue", fg="white", height="1", width="15",
                              command=lambda: self.try_to_log(e1.get(), e2.get()))
        back_button = Button(self.root, text="back", bg="white", height="1", width="5",
                             command=lambda: self.go_back())
        login_button.grid(row=4, column=170)
        Label(text="", fg="red").grid(row=3, column=170)
        space.grid(row=0, column=200)
        back_button.grid(row=0, column=300)

    def try_to_log(self, e1, e2):
        """
        Pressed the login button in the login page. The user entered his details, username and password, checking if
        they are correct. Entering the simulation if they exist or putting an error message if not.
        :param e1: User name.
        :param e2: Password.
        """
        self.print_info(e1, e2)
        if e1.find(' ') == -1 and e2.find(' ') == -1:
            str = 'a' + ' ' + e1 + ' ' + e2
            message = self.connection.send(str)
            print('the message is:', message)
            if message == 'True':
                print('new screen')
                self.root.destroy()
                try:
                    self.connection.send('exit')
                except:
                    pass
                Simulation(self.where)
            else:
                Label(text='input is wrong', fg="red").grid(row=3, column=170)
        else:
            Label(text='input is wrong', fg="red").grid(row=3, column=170)

    def go_back(self):
        """
        Go back to the opening page (back button pressed).
        """
        self.root.destroy()
        self.__init__(self.where)

    def print_info(self, e1, e2):
        """
        Print information got from the user.
        :param e1: Username.
        :param e2: Password.
        """
        print("User Name: %s\nPassword: %s" % (e1, e2))

    def register_page(self):
        """
        Open the registration page (Pressed the register button in the first page).
        """
        self.new_page()

        self.root.geometry("400x400")  # set the configuration of GUI wind
        self.root.title("Register Page")  # set the title of GUI window

        Label(self.root, text="User Name:").grid(row=0)
        Label(self.root, height="1", width='19').grid(row=0, column=300)  # space
        Label(self.root, text="Password:").grid(row=1)
        Label(self.root, text="Email:").grid(row=2)
        Button(self.root, text="back", bg="white", height="1", width="5",
               command=lambda: self.go_back()).grid(row=0, column=400)

        e1 = Entry(self.root, width=25)
        e2 = Entry(self.root, width=25)
        e3 = Entry(self.root, width=25)

        e1.grid(row=0, column=170)
        e2.grid(row=1, column=170)
        e3.grid(row=2, column=170)

        x = Button(self.root, text="Register", bg="Royal Blue", fg="white", height="1", width="15",
                   command=lambda: self.try_to_register(e1.get(), e2.get(), e3.get()))
        Label(self.root, text='', fg="red").grid(row=3, column=170)
        x.grid(row=4, column=170)
        self.root.mainloop()

    def try_to_register(self, user_name, password, email):
        """
        Trying to register, checking if those details are legal for new registration, if they are open a simulation
        page, if not put an error message.
        :param user_name: The username the client put.
        :param password: The password the client put.
        :param email: The email.
        """
        str = 'c' + ' ' + user_name + ' ' + password + ' ' + email
        if user_name.find(' ') == -1 and password.find(' ') == -1 and email.find(' ') == -1:
            message = self.connection.send(str)
            print(message)
            if message == 'add':
                print('new screen')
                self.root.destroy()
                try:
                    self.connection('exit')
                except:
                    pass
                Simulation(self.where)
            else:
                if message == 'email':
                    Label(self.root, text="invalid email", fg="red").grid(row=3, column=170)
                elif message == 'already':
                    Label(self.root, text="user name exists", fg="red").grid(row=3, column=170)
                else:
                    Label(self.root, text="invalid input", fg="red").grid(row=3, column=170)
        else:
            Label(self.root, text="invalid input", fg="red").grid(row=3, column=170)

    def reset_pass_page(self):
        """
        Open reset password page.
        """
        self.new_page()

        self.root.geometry("400x400")  # set the configuration of GUI wind
        self.root.title("Reset Password Page")  # set the title of GUI window

        Label(self.root, text="User Name").grid(row=0)
        Label(self.root, text="Email").grid(row=1)

        e1 = Entry(self.root, width=25)
        e2 = Entry(self.root, width=25)

        e1.grid(row=0, column=170)
        e2.grid(row=1, column=170)

        space = Label(self.root, height="1", width='19')
        login_button = Button(self.root, text="Reset Password", bg="Royal Blue", fg="white", height="1", width="15",
                              command=lambda: self.try_to_change(e1.get(), e2.get()))

        back_button = Button(self.root, text="back", bg="white", height="1", width="5",
                             command=lambda: self.go_back())

        login_button.grid(row=4, column=170)
        Label(text="", fg="red").grid(row=3, column=200)
        space.grid(row=0, column=200)
        back_button.grid(row=0, column=300)

    def try_to_change(self, user_name, email):
        """
        Try to change the password, check if the username and email are connected using the server.
        :param user_name: The username.
        :param email: The gmail.
        """
        str = 'b' + ' ' + user_name + ' ' + email
        if user_name.find(' ') == -1 and email.find(' ') == -1:
            message = self.connection.send(str)
            print(message)
            if message == 'True':
                login_button = Button(self.root, text="Reset Password", bg="Royal Blue", fg="white", height="1",
                                      width="15", state=DISABLED)
                login_button.grid(row=4, column=170)

                Label(self.root, height='1').grid(row=6)
                Label(self.root, text="Temp Password").grid(row=7)
                Label(self.root, text="New Password").grid(row=8)

                e1 = Entry(self.root)
                e2 = Entry(self.root)

                e1.grid(row=7, column=170)
                e2.grid(row=8, column=170)

                Button(self.root, text="Change Password", bg="Royal Blue", fg="white", height="1", width="15",
                       command=lambda: self.change_pass(e1.get(), e2.get())).grid(row=10, column=170)
            else:
                Label(self.root, text="invalid input", fg="red").grid(row=3, column=170)
        else:
            Label(self.root, text="invalid input", fg="red").grid(row=3, column=170)

    def change_pass(self, old_pass, new_pass):
        """
        Check if the temporary password is correct and try to change to the new password.
        :param old_pass: The temporary password.
        :param new_pass: The new password.
        """
        str = old_pass + ' ' + new_pass
        print(str)
        message = self.connection.send(str)
        if message == 'True':
            self.root.quit()
            print('changed password')
            print('new screen')
        else:
            Label(self.root, text="invalid input", fg="red").grid(row=9)
            print('Something is incorrect')

    def exit_button(self):
        """
        The exit button in the screen is pressed.
        """
        print('exit window')
        try:
            self.connection.send('exit')
            print('exit..')
        except:
            pass
        self.root.destroy()


obj01 = Windows(WHERE)
