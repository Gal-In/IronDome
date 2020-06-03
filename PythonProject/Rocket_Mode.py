import math

# The rocket class, has the calculations of everything..


class Rocket:
    def __init__(self, name, alpha, beta, v_start):
        """
        This class represent a rocket and all of the info about this rocket.
        :param name: Type of the rocket.
        :param alpha: The alpha degree.
        :param beta: The beta degree.
        :param v_start: The speed at launch.
        """
        self.name = name
        self.alpha = alpha
        self.beta = beta
        self.v_start = v_start
        self.t = self.fix_num(self.calc_time())  # Total time until landing.
        self.speed_x, self.speed_y = self.calc_speed()
        self.total_destination, self.x_des, self.y_des = self.calc_destination()

    def calc_time(self):
        """
        Calculate the time until the rocket is reaching the ground.
        :return: The time.
        """
        return (self.v_start*math.sin(math.radians(self.alpha)))/5

    def calc_speed(self):
        """
        Calculate the different types of speeds.
        :return: The speeds.
        """
        return self.fix_num(self.v_start*math.cos(math.radians(self.alpha))),\
               self.fix_num(self.v_start*math.sin(math.radians(self.alpha)))

    def calc_destination(self):
        """
        Calculate the different types of distance.
        :return: The destinations.
        """
        d = self.speed_x*self.t / 1000
        return self.fix_num(d), self.fix_num(d*math.cos(math.radians(self.beta))),\
               self.fix_num(d*math.sin(math.radians(self.beta)))

    def get_weight(self):
        """
        By type of rocket, return her weight. If type doesnt exist return ''.
        :return: The weight.
        """
        info = {
            "Qassam": "90kg",
            "9M133": "27kg",
            "M75": "90kg",
            "M302": "524kg"
        }
        try:
            return info[self.name]
        except:
            print('rocket cant be found')
            return ''

    def point_on_map(self, start_point_x, start_point_y, ratio=1.724):
        """
        From all the information about the rocket, calculate where will it land.
        :param start_point_x: X coordinate of where the rocket launched.
        :param start_point_y: Y coordinate of where the rocket launched.
        :param ratio: Ratio between the map in the simulation and real life.
        :return: X coordinate and y coordinate of landing.
        """
        end_point_x = start_point_x + self.x_des*ratio
        end_point_y = start_point_y - self.y_des*ratio
        return end_point_x, end_point_y

    def fix_num(self, num):
        """
        Shorten a number with dot after it.
        :param num: The number.
        :return: Fixed number.
        """
        num = str(num)
        cut = num.find('.') + 3  # the dot plus two other numbers after it.
        if cut == 2:  # There is no dot.
            return int(num)
        num += '00'  # If for some reason there arent enough
        string = ''
        for i in range(cut):
            string += num[i]
        if float(string) == int(float(string)):
            return int(string.split('.')[0])
        else:
            return float(string)

    def get_time(self):
        """
        Calculate by the destination how much people have to go to the shelter.
        :return: The time in seconds.
        """
        des = int(self.total_destination)
        if des < 13.5:
            return 15
        elif des < 22:
            return 30
        elif des < 32:
            return 45
        elif des < 42:
            return 60
        else:
            return 90
