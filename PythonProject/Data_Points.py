import sqlite3


class DataBasePoints:
    def __init__(self, file_name='city_points.db', table_name='points'):
        """
        This class is responsible for the city_points.db data base. This data base has all the information about the
        different areas in the map. This class can create the table, add a new city, find for a given coordinates in
        which area they are.
        :param file_name: The name of the data base file (.db). This data base contains information about the cities.
        :param table_name: The name of the the table inside the data base file. This table contains the x and y
        coordination's and the name of the city.
        """
        self.__file_name = file_name  # 'test_me.db'
        self.__table_name = table_name
        self.make_new_table()

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
              "(" + "x_cord_start INTEGER NOT NULL, " + \
                    "x_cord_end INTEGER NOT NULL, " + \
                    "y_cord_start INTEGER NOT NULL, " + \
                    "y_cord_end INTEGER NOT NULL, " +\
                    "Name TEXT NOT NULL)"
        self.__c.execute(str)
        self.close()

    def add_points(self, x_point_start, x_point_end, y_point_start, y_point_end, city):
        """
        Add a new row in the table, a new city.
        :param x_point_start: The left x coordinate of the city.
        :param x_point_end: The right x coordinate of the city.
        :param y_point_start: The left y coordinate of the city.
        :param y_point_end: The right y coordinate of the city.
        :param city: The name of the city.
        """
        self.connect()
        try:
            self.__c.execute('insert into points values (?,?,?,?,?)', (x_point_start, x_point_end, y_point_start, y_point_end, city))
            print('added to the data base')
        except:
            print('There is a problem and it is not the primary key')
        self.close()

    def find_if_in_city(self, x_point, y_point, x_start, x_end, y_start, y_end):
        """
        Find if a set of coordinate's are inside a city, given the city coordinates.
        :param x_point: X coordinate of the dot.
        :param y_point: Y coordinate of the dot.
        :param x_start: Left x coordinate of the city.
        :param x_end: Right x coordinate of the city.
        :param y_start: Left y coordinate of the city.
        :param y_end: Right y coordinate of the city.
        :return: True / False. If inside the city returns True, else False.
        """
        if x_point >= x_start and x_point <= x_end and y_point >= y_start and y_point<=y_end:
            return True
        else:
            return False

    def find_city(self, x_point, y_point):
        """
        Find for a dot if its inside any city from the data base.
        :param x_point: The dot x coordinate.
        :param y_point: The dot y coordinate.
        :return: nothing if its not inside any city. The name of the city if it does belong to any area.
        """
        self.connect()

        self.__c.execute("""SELECT * from points""")
        for row in self.__c.fetchall():
            if self.find_if_in_city(x_point, y_point, row[0], row[1], row[2], row[3]):
                self.close()
                return row[4]

        self.close()
        return 'nothing'
