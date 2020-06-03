from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from Client_Connection import Client
import random
import math
import winsound


place = ('172.19.226.31', 7777)


class Simulation:
    def __init__(self, where, x=0):
        """
        This class opens the different simulation pages using tkinter.
        :param where: where[0] - ip, where[1] - port.
        :param x: Type of screen. 0 - Shooter. 1 - Israel.
        """
        self.x = x

        self.root = Tk()
        self.where = where
        self.connection = Client(where[0], where[1], x)  # socket_connection_client
        self.root.iconbitmap('icon.ico')

        self.canvas = None
        self.frame = None
        self.button = None

        if self.x == 0:
            self.type = 1
            self.line = None
            self.entry01 = None
            self.entry02 = None
            self.entry03 = None
            self.combobox = None
            self.filename = 'Missile_Launch.wav'
            self.game()

        elif self.x == 1:
            self.last_one = 0
            self.alarm_arr = [[-1, -1, -1, -1, - 1], [-1, -1, -1, -1, - 1], [-1, -1, -1, -1, - 1], [-1, -1, -1, -1, - 1]]
            self.buttons = [-1, -1, -1, -1]  # array of buttons.
            self.dots = [-1, -1, -1, -1, -1]  # array of the dots.
            self.labels = [-1, -1, -1, -1]  # array of labels.
            self.lines = [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]]  # array of lines.
            self.colors = ['cornflowerblue', 'violetred', 'darkorchid', 'gray26']
            self.filename = 'Red_Color.wav'
            self.new_side()

    def stop_sound(self):
        """
        Stops the sound that is playing.
        """
        winsound.PlaySound(None, winsound.SND_FILENAME)

    def game(self):
        """
        Open the first page, shooter simulation.
        """
        self.root.title('Simulation - Gaza')  # Title
        self.root.geometry('800x740')  # Size of the screen
        # self.root.resizable(0, 0)

        self.canvas = Canvas(width=350, height=740)

        img = Image.open("IsMap.jpg")
        photo = ImageTk.PhotoImage(img)

        self.canvas.bind("<Button-1>", self.right_click)
        self.canvas.bind("<Button-2>", self.scroll)
        self.canvas.bind("<Button-3>", self.left_click)

        self.canvas.create_image(0, 0, image=photo, anchor=NW)
        self.canvas.grid(row=0, column=0)


        self.frame = Frame(self.root)
        self.frame.grid(row=0, column=1, sticky="n")

        Label(self.frame, text='Speed').grid(row=0, column=1)
        self.entry01 = Entry(self.frame)
        self.entry01.grid(row=0, column=2)

        Label(self.frame, text='Alpha α').grid(row=1, column=1)
        self.entry02 = Entry(self.frame)
        self.entry02.grid(row=1, column=2)

        Label(self.frame, text='Beta β').grid(row=2, column=1)
        self.entry03 = Entry(self.frame)
        self.entry03.grid(row=2, column=2)

        Label(self.frame, text='Type').grid(row=3, column=1)
        global types

        types = StringVar()
        self.combobox = ttk.Combobox(self.frame, width=17, textvariable=types, state='readonly')
        self.combobox['values'] = ("Qassam", "9M133", "M75", "M302")
        self.combobox.current(0)
        self.combobox.grid(row=3, column=2)

        Label(self.frame, text='', width=10).grid(row=5, column=2)
        Label(self.frame, text='', width=3).grid(row=0, column=3)
        Label(self.frame, text='Info: ', fg='blue').grid(row=0, column=4)

        self.button = Button(self.frame, text='Enter', command=lambda: self.input(types))

        self.button.grid(row=4, column=2)

        Label(self.frame, text='', width=5).grid(row=0, column=3)

        # switch side - first exit this window, then open new window, which is Israel side.
        b = Button(self.frame, text='Switch Side', command=lambda: self.switch_side(1))
        b.grid(row=4, column=5, sticky=W)

        self.canvas.create_oval(40, 386, 40, 386, fill='red', outline='red')

        self.root.protocol('WM_DELETE_WINDOW', self.exit_button)

        R1 = Radiobutton(self.frame, text='insert values', value=1, command=lambda: self.switch_way(1))
        R1.grid(row=6, column=2)

        R1.select()

        R2 = Radiobutton(self.frame, text='click on map', value=2,  command=lambda: self.switch_way(2))
        R2.grid(row=7, column=2)

        Label(self.frame, height=8).grid(row=8, column=2)  # space between the flag and info

        img2 = Image.open("PalFlag.jpg")
        photo2 = ImageTk.PhotoImage(img2)

        new_can = Canvas(self.frame, width=200, height=200)
        new_can.create_image(0, 0, image=photo2, anchor=NW)

        new_can.grid(row=9, column=2, sticky=NE, rowspan=2, columnspan=3)

        self.root.mainloop()

    def switch_way(self, num):
        """
        Switch between putting input (giving info) or point on map, using radiobutton.
        :param num: What button was pressed, 1 - insert values, 2 - click on map.
        """
        self.type = num
        Label(self.frame, text=' ', width=40).grid(row=1, column=5, sticky=W)
        Label(self.frame, text=' ', width=40).grid(row=2, column=5, sticky=W)
        Label(self.frame, text=' ', width=40).grid(row=3, column=5, sticky=W)
        Label(self.frame, text='    ', width=10).grid(row=5, column=2)
        self.button.configure(text='Enter')
        self.canvas.delete(self.line)
        if num == 1:
            self.entry01.config(state='normal')
            self.entry02.config(state='normal')
            self.entry03.config(state='normal')
            self.button.configure(state='normal')
            self.combobox.configure(state='normal')
        else:
            self.entry01.config(state='readonly')
            self.entry02.config(state='readonly')
            self.entry03.config(state='readonly')
            self.button.configure(state='disabled')
            # self.combobox.configure(state='disabled')

    def input(self, types):
        """
        Input was given about a new rocket going out, send it to the server.
        :param types: Type of rocket.
        """
        start_point_x = 40
        start_point_y = 386
        print("The speed is: {} and the type is: {} \n"
              "The α is: {} and the β is: {}".format(self.entry01.get(), types.get(), self.entry02.get(), self.entry03.get()))
        try:
            if 0 < int(self.entry02.get()) < 90 and \
                    -90 < int(self.entry03.get()) < 90 and 0 < int(self.entry01.get()) < 7000:
                send = 'd' + ' ' + types.get() + ' ' + str(int(self.entry02.get())) + ' ' +\
                       str(int(self.entry03.get())) + ' ' + str(int(self.entry01.get())) + ' ' +\
                       str(start_point_x) + ' ' + str(start_point_y)
                print(send)
                message = self.connection.send(send)
                if message == 'false':
                    Label(self.frame, text='out of range', fg='red').grid(row=5, column=2)
                else:
                    self.build_the_structure(message, types)
            else:
                Label(self.frame, text='invalid input', fg='red').grid(row=5, column=2)
        except:
            Label(self.frame, text='invalid input', fg='red').grid(row=5, column=2)

    def build_the_structure(self, message, types):
        """
        Show info about the rocket.
        :param message: Message from the server, contain info about the rocket.
        :param types: Type of rocket.
        """
        winsound.PlaySound(self.filename, winsound.SND_ASYNC | winsound.SND_ALIAS)
        arr = message.split(' ')
        Label(self.frame, text='', width=10).grid(row=5, column=2)
        Label(self.frame, text='', width=3).grid(row=0, column=3)
        self.button.configure(text='Back')
        self.entry01.config(state='readonly')
        self.entry02.config(state='readonly')
        self.entry03.config(state='readonly')

        self.combobox.configure(state='disabled')

        Label(self.frame, text='Rocket weight is: {}'.format(arr[0])).grid(row=1, column=5, sticky=W)
        Label(self.frame, text='Rocket total time in air is: {} sec'.format(arr[1])).grid(row=2, column=5, sticky=W)
        Label(self.frame, text='Rocket total destination is: {} km'.format(arr[2])).grid(row=3, column=5, sticky=W)
        self.line = self.canvas.create_line(40, 386, arr[3], arr[4], width=2, fill='black')

        print(arr[2])
        print(arr[5])
        print(arr[6])

        self.button.config(command=lambda: self.delete_can(types))

    def calc_line(self, x, y):
        """
        Trying to send a rocket with clicking on map.
        :param x: The x coordinate of the dot.
        :param y: The y coordinate of the dot.
        """
        self.canvas.delete(self.line)
        self.line = self.canvas.create_line(40, 386, x, y)
        Label(self.frame, text=' ', width=40).grid(row=1, column=5, sticky=W)
        Label(self.frame, text=' ', width=40).grid(row=2, column=5, sticky=W)
        Label(self.frame, text=' ', width=40).grid(row=3, column=5, sticky=W)
        Label(self.frame, text='    ', width=10).grid(row=5, column=2)
        if x != 40:
            beta = math.atan((386 - y) / (x - 40))
        else:
            beta = -90
        ratio = 1.724
        alpha = math.radians(25)
        try:
            v = math.sqrt(1000*(5*(x-40))/(math.sin(alpha)*math.cos(alpha)*math.cos(beta)*ratio))
        except:
            print('negative')
            v = math.sqrt(-1000 * (5 * (x - 40)) / (math.sin(alpha) * math.cos(alpha) * math.cos(beta) * ratio))
        t = v * math.sin(alpha) / 5
        beta = math.degrees(beta)
        alpha = 25
        print(alpha, beta, t, v)
        send = 'd' + ' ' + types.get() + ' ' + str(int(alpha)) + ' ' + \
               str(int(beta)) + ' ' + str(int(v)) + ' ' + \
               str(40) + ' ' + str(386)
        print(send)
        message = self.connection.send(send)
        if message == 'false':
            Label(self.frame, text='out of range', fg='red').grid(row=5, column=2)
        else:
            winsound.PlaySound(self.filename, winsound.SND_ASYNC | winsound.SND_ALIAS)
            arr = message.split(' ')
            self.entry01.config(state='normal')
            self.entry01.delete(0, 10)
            self.entry02.config(state='normal')
            self.entry02.delete(0, 10)
            self.entry03.config(state='normal')
            self.entry03.delete(0, 10)
            self.entry01.insert(0, int(v))
            self.entry02.insert(0, int(alpha))
            self.entry03.insert(0, int(beta))
            self.entry01.config(state='disabled')
            self.entry02.config(state='disabled')
            self.entry03.config(state='disabled')
            Label(self.frame, text='Rocket weight is: {}'.format(arr[0])).grid(row=1, column=5, sticky=W)
            Label(self.frame, text='Rocket total time in air is: {} sec'.format(arr[1])).grid(row=2, column=5, sticky=W)
            Label(self.frame, text='Rocket total destination is: {} km'.format(arr[2])).grid(row=3, column=5, sticky=W)

    def motion(self, event):
        """
        Click on map.
        :param event: Info about the click.
        """
        x, y = event.x, event.y
        print('{}, {}'.format(x, y))
        if self.x == 0:
            if self.type == 2:
                self.calc_line(x, y)

    def right_click(self, event):
        """
        Right click on map.
        :param event: Info about the click.
        """
        print('right')
        self.motion(event)

    def scroll(self, event):
        """
        Scroll on map.
        :param event: Info about the scroll.
        """
        print('Scroll')
        self.motion(event)

    def left_click(self, event):
        """
        Left click on map.
        :param event: Info about the click.
        """
        print('Left')
        self.motion(event)

    def delete_can(self, types):
        """
        Pressed the back button. Delete the line, clean the entries.
        :param types: Type of rocket.
        :return:
        """
        # delete the line:
        self.canvas.delete(self.line)
        # delete the typed entry info:
        self.entry01.config(state='normal')
        self.entry01.delete(0, 10)
        self.entry02.config(state='normal')
        self.entry02.delete(0, 10)
        self.entry03.config(state='normal')
        self.entry03.delete(0, 10)
        # rest the combobox:
        self.combobox.configure(state='readonly')
        # delete the info:
        Label(self.frame, text=' ', width=40).grid(row=1, column=5, sticky=W)
        Label(self.frame, text=' ', width=40).grid(row=2, column=5, sticky=W)
        Label(self.frame, text=' ', width=40).grid(row=3, column=5, sticky=W)
        # fix the button:
        self.button.configure(text='Enter', command=lambda: self.input(types))

    def exit_button(self):
        """
        Pressed the exit button of the window.
        """
        print('exit window')
        self.x = 0
        try:
            self.connection.send('exit')
        except:
            pass
        self.root.destroy()

    def switch_side(self, x):
        """
        Switch sides.
        :param x: New side num, 0 - Shooter, 1 - Israel
        """
        self.stop_sound()
        self.exit_button()
        self.__init__(self.where, x)

    def new_side(self):
        """
        Create the Israel side.
        """
        self.root.title('Simulation - Israel')  # Title
        self.root.geometry('800x740')  # Size of the screen

        self.canvas = Canvas(width=350, height=740)

        img = Image.open("IsMap.jpg")
        photo = ImageTk.PhotoImage(img)

        self.canvas.bind("<Button-1>", self.right_click)
        self.canvas.bind("<Button-2>", self.scroll)
        self.canvas.bind("<Button-3>", self.left_click)

        self.canvas.create_image(0, 0, image=photo, anchor=NW)
        self.canvas.grid(row=0, column=0)

        self.frame = Frame(self.root)
        self.frame.grid(row=0, column=1, sticky="n")

        Label(self.frame, text='Alarms: ').grid(row=0, column=0)

        for i in range(0, 4):
            Label(self.frame, text='', width=20).grid(row=i, column=1)
            # Label(self.frame, text='', width=25).grid(row=i, column=1)
        Label(self.frame, text='', width=5).grid(row=0, column=3)

        # switch side - first exit this window, then open new window, which is Israel side.
        b = Button(self.frame, text='Switch Side', command=lambda: self.switch_side(0))
        b.grid(row=0, column=3)

        for x in range(1, 5):
            Label(self.frame, text='').grid(row=str(x), column=1)

        Label(self.frame, text='amount of terrorists: ').grid(row=5, column=3)

        self.canvas.create_oval(40, 386, 40, 386, fill='red', outline='red')

        self.root.protocol('WM_DELETE_WINDOW', self.exit_button)


        img2 = Image.open("IsrFlag.jpg")
        photo2 = ImageTk.PhotoImage(img2)

        new_can = Canvas(self.frame, width=200, height=200)
        new_can.create_image(0, 0, image=photo2, anchor=NW)

        Label(self.frame, height=8).grid(row=6, column=0)  # space between the flag and info

        new_can.grid(row=7, column=0, sticky=NE, rowspan=2, columnspan=3)


        self.func()

        self.root.mainloop()

    def func(self):
        """
        Get info from the server about new rockets and more.
        """
        self.fix_places()

        count = 0
        position_of_empty = []

        for i in range(4):
            if self.alarm_arr[i][0] == -1 or self.alarm_arr[i][0] == 0:
                position_of_empty.append(i)
                count += 1
        count = str(count)
        print('count is: ', count)

        send = 'e' + ' ' + str(count) + ' ' + str(self.last_one)
        x = self.connection.send(send)
        print(x)
        arr = x.split(' ')  # arr[0] - amount of terrorist, ar[1] - amount of new rockets.
        Label(self.frame, text=arr[0]).grid(row=5, column=4, sticky=W)  # g_count
        amount_of_g = int(arr[1])
        # print(arr)
        print(arr[1])
        if arr[1] != '0':
            winsound.PlaySound(self.filename, winsound.SND_ASYNC | winsound.SND_ALIAS)
        del arr[0], arr[0]  # delete the original arr[0] arr[1]
        if amount_of_g != 0:
            self.put_info(amount_of_g, position_of_empty, arr)
        else:
            self.timer()
        # print(arr)

    def fix_places(self):
        """
        Check that there are no blanks.
        """
        numbers = [0, 0, 0, 0]
        arr = []

        for i in range(4):
            if self.alarm_arr[i][0] != -1 and self.alarm_arr[i][0] != 0:  # only one
                arr.append(i)

        if len(arr) == 4 or len(arr) == 0:
            pass
        else:
            for i in arr:
                numbers[i] = 1

            if numbers[3] == 1:
                if numbers[0] == 0:
                    self.change(3, 0)
                    numbers[0] = 1

                elif numbers[1] == 0:
                    self.change(3, 1)
                    numbers[1] = 1

                elif numbers[2] == 0:
                    self.change(3, 2)
                    numbers[2] = 1

            if numbers[2] == 1:
                if numbers[0] == 0:
                    self.change(2, 0)
                    numbers[0] = 1

                elif numbers[1] == 0:
                    self.change(2, 1)
                    numbers[1] = 1

            if numbers[1] == 1:
                if numbers[0] == 0:
                    self.change(1, 0)

    def change(self, i, j):
        """
        Change between the places of i and j.
        :param i: The place to move to (empty).
        :param j: The place to delete.
        """
        print('i am changing')
        print(i, j)
        self.labels[i].config(text=' ', width=25)
        self.buttons[i].destroy()
        self.alarm_arr[i], self.alarm_arr[j] = self.alarm_arr[j], self.alarm_arr[i]
        self.buttons[i], self.buttons[j] = self.buttons[j], self.buttons[i]
        self.dots[i], self.dots[j] = self.dots[j], self.dots[i]
        self.labels[i], self.labels[j] = self.labels[j], self.labels[i]
        self.lines[i], self.lines[j] = self.lines[j], self.lines[i]
        self.colors[i], self.colors[j] = self.colors[j], self.colors[i]
        self.buttons[j] = Button(self.frame, text='pull down', command=lambda j=j: self.button_press(j))
        # The j=j means that it will send to the button_press function the real amount of j.
        self.buttons[j].grid(row=j, column=2)

    def put_info(self, amount_of_g, position_of_empty, arr):
        """
        Organize new info from the server.
        :param amount_of_g: Amount of terrorists.
        :param position_of_empty: Where there are empty places.
        :param arr: Arr of rockets.
        :return:
        """
        x = 0
        for j in position_of_empty:
            if amount_of_g == 0:
                break
            else:
                self.alarm_arr[j][0] = int(arr[x])
                self.alarm_arr[j][1] = float(arr[x+1])
                self.alarm_arr[j][2] = float(arr[x+2])
                if arr[x+3] == 'nothing':
                    arr[x+3] = 'Small Villages'
                elif arr[x+3].find('_'):
                    arr[x+3] = arr[x+3].replace('_', ' ')
                self.alarm_arr[j][3] = arr[x+3]
                self.alarm_arr[j][4] = int(arr[x+4])
            x += 5
            amount_of_g -= 1
            x_pos = self.alarm_arr[j][1]
            y_pos = self.alarm_arr[j][2]
            self.dots[j] = self.canvas.create_oval(str(x_pos), str(y_pos), str(x_pos + 2), str(y_pos + 2), fill=self.colors[j],
                                                   outline=self.colors[j])
            self.buttons[j] = Button(self.frame, text='pull down', command=lambda j=j: self.button_press(j))
            # The j=j means that it will send to the button_press function the real amount of j.
            self.buttons[j].grid(row=j, column=2)
            self.lines[j][0] = self.alarm_arr[j][4]  # total time
            self.lines[j][1] = 40
            self.lines[j][2] = 386
            self.lines[j][3] = self.canvas.create_line(40, 386, 40, 386)


        print("The array: ", self.alarm_arr)
        self.last_one = max(int(self.alarm_arr[0][0]), int(self.alarm_arr[1][0]),
                            int(self.alarm_arr[2][0]), int(self.alarm_arr[3][0]))
        print("The last one is: ", self.last_one)
        self.timer()

    def timer(self):
        """
        Update info about rockets, like time.
        """
        for i in range(4):
            if self.alarm_arr[i][0] != -1:
                if self.alarm_arr[i][4] == -1:
                    self.finished(i)
                    self.buttons[i].destroy()
                elif self.alarm_arr[i][4] == -5:
                    self.button_press(i)
                elif self.alarm_arr[i][4] < -1:
                    self.alarm_arr[i][4] -= 1
                else:
                    text = self.alarm_arr[i][3]
                    text += ' Time remain: ' + str(self.alarm_arr[i][4])
                    self.labels[i] = Label(self.frame, text=text, fg=self.colors[i])
                    self.labels[i].grid(row=i, column=1)
                    self.alarm_arr[i][4] -= 1

                    self.canvas.delete(self.lines[i][3])
                    l = self.alarm_arr[i][4]
                    k = self.lines[i][0] - l
                    self.lines[i][1] = ((l*40 + k*self.alarm_arr[i][1]) / self.lines[i][0])
                    self.lines[i][2] = ((l*386 + k*self.alarm_arr[i][2]) / self.lines[i][0])
                    print(self.lines[i][1], self.lines[i][2])
                    self.lines[i][3] = self.canvas.create_line(40, 386, self.lines[i][1], self.lines[i][2],
                                                               fill=self.colors[i])

        try:
            self.root.after(1000, self.func)  # need to delete.
        except:
            print('why')

    def button_press(self, j):
        """
        Pull down button pressed.
        :param j: Line in which the button was pressed.
        """
        print('Num of the button: ', j)
        self.buttons[j].destroy()
        self.buttons[j] = -1
        self.canvas.delete(self.dots[j])
        self.dots[j] = -1
        self.labels[j].config(text=' ', width=25)
        self.labels[j] = -1
        self.canvas.delete(self.lines[j][3])
        for i in range(5):
            self.alarm_arr[j][i] = -1

    def finished(self, j):
        """
        Time was finished for this rocket.
        :param j: Line of rocket that hit the ground.
        """
        text = self.text_generator(j)
        self.labels[j].config(text=' ', width=25)
        self.labels[j].config(text=text, fg='red')
        self.canvas.delete(self.lines[j][3])
        self.alarm_arr[j][4] -= 1

    def text_generator(self, j):
        """
        Generate the amount of people injured.
        :param j: Line of rocket that hit the ground.
        """
        winsound.PlaySound('explosion.wav', winsound.SND_ASYNC | winsound.SND_ALIAS)
        if self.alarm_arr[j][3] == 'Small Villages':  # 30%
            arr = [0, 0, 0, 0, 0, 0, 0, 1, 2, 3]
        elif self.alarm_arr[j][3] == 'Settlements':  # 65%
            arr = [0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 4]
        else:  # city -- 95%
            arr = [0, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 20, 1, 2, 3, 4, 1, 2, 3, 4]
        hit = random.choice(arr)
        if hit == 0:
            return 'hit nobody'
        elif hit == 1:
            return 'hit one person'
        return 'hit ' + str(hit) + ' people'

