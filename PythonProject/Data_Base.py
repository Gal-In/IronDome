import sqlite3
from Send_Gmail import first_email

# Working with sqlite3 module - creating and controlling the data base. Creating a class that connects to the
# data base. Can add new user, change password etc..


class DataBase:
    def __init__(self, file_name='users.db', table_name='users'):
        """
        This class is responsible for the users.db data base. This data base has all the information about the users.
        This class can create the table, add new users, change info.
        :param file_name: The name of the data base file (.db). This data base contains the information about the users.
        :param table_name: The name of the the table inside the data base file. This table contains the user_name,
        password, and email.
        """
        self.__file_name = file_name
        self.__table_name = table_name

    def connect(self):
        """
        This function connects to the data base file.
        """
        self.__conn = sqlite3.connect(self.__file_name)
        self.__c = self.__conn.cursor()

    def close(self):
        """
        Close the connection to the data base.
        """
        self.__conn.commit()
        self.__conn.close()

    def make_new_table(self):
        """
        Create the new table (if it doesnt exist).
        """
        self.connect()
        str = "CREATE TABLE IF NOT EXISTS" + " " + self.__table_name + \
              "(" + "User_Name TEXT PRIMARY KEY NOT NULL, " + \
                    "Password TEXT NOT NULL, " +\
                    "Email TEXT NOT NULL)"

        self.__c.execute(str)
        self.close()

    def new_user(self, user_name, password, email):
        """
        Get info about a new user and if the info about him is legal, adds him to the data base.
        :param user_name: The new user username.
        :param password: The new user password.
        :param email: The new user email.
        """
        self.connect()
        if self.is_valid_input2(user_name, password, email):
            try:
                first_email(user_name, email)
            except:
                print('problem')
                self.close()
                return 'email'
            str = "INSERT INTO " + self.__table_name + " (User_Name, Password, Email) VALUES ('" + user_name + "','" +\
                  password + "','" + email + "');"

            try:
                self.__c.execute('insert into users values (?,?,?)', (user_name, password, email))
                # self.__c.execute(str)
                print('added to the data base')
                self.close()
                return 'add'

            except sqlite3.IntegrityError:
                print('primary key is already taken')
                self.close()
                return 'already'
            except:
                self.close()
                print('There is a problem and it is not the primary key')

        else:
            self.close()
            return 'invalid'

    def is_valid_input2(self, user_name, password, email):
        """
        Check if the info that a new user is trying to add is legal.
        :param user_name: The new user username.
        :param password: The new user password.
        :param email: The new user email.
        :return: True / False. True if valid, False if not.
        """
        if len(user_name) > 3 and user_name.find(' ') == -1:
            if len(password) > 4 and password.find(' ') == -1:
                if email.find('@gmail.com') != -1 and len(email) - email.find('@gmail.com') == 10 and len(email) != 10\
                        and email.find(' ') == -1:
                    return True
                else:
                    print('email not good')
            else:
                print('password not good')
        else:
            print('user name not good')
        return False

    def forgot_password(self, user_name):
        """
        If exist, return this user name email.
        :param user_name: the username of this client.
        :return: If the user name exist, his email. If not False.
        """
        # get the user name, return (and print) email.
        self.connect()
        try:
            self.__c.execute('SELECT * FROM Users WHERE "User_Name" = ?', (user_name,))
            email = self.__c.fetchone()[2]  # email
            print(email)
            self.close()
            return email
            # print(self.__c.fetchone()), put the fetchone things inside a list and later print, return etc..
        except:
            print('data is incorrect, probably the user name is incorrect')
            self.close()
            return 'false'

    def check_password(self, user_name):
        """
        If exist, return this user name password.
        :param user_name: the username of this client.
        :return: If the user name exist, his email. If not False.
        """
        self.connect()
        try:
            self.__c.execute('SELECT * FROM Users WHERE "User_Name" = ?', (user_name,))
            password = self.__c.fetchone()[1]  # password
            print(password)
            self.close()
            return password
            # print(self.__c.fetchone()), put the fetchone things inside a list and later print, return etc..
        except:
            print('data is incorrect, probably the user name is incorrect')
            self.close()
            return 'false'

    def is_valid_input1(self, password):
        """
        Check if a password is valid.
        :param password: New password for a client who want to change his password.
        :return: True / False. True if its valid. False if not.
        """
        if len(password) > 4 and password.find(' ') == -1:
            return True
        else:
            return False

    def change_password(self, user_name, new_password):
        """
        If the new password is valid, change the password for this username to this new password.
        :param user_name: Existing user name.
        :param new_password: A new password for the user.
        :return: True / False. If the new password is valid, True. If not False.
        """
        if self.is_valid_input1(new_password):
            self.connect()
            str = """Update users set Password = ? where User_Name = ?"""
            data = (new_password, user_name)
            self.__c.execute(str, data)
            self.close()
            return True
        else:
            return False

