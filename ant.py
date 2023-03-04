import math
import random

class Ant():
    # Possible status
    STATUS_INACTIVE = 0
    STATUS_SEARCHING = 1
    STATUS_FOOD_TRACKING = 2
    STATUS_EATING = 3
    STATUS_GOING_HOME = 4
    # Possible direction
    DIR_N = 0
    DIR_NE = 1
    DIR_E = 2
    DIR_SE = 3
    DIR_S = 4
    DIR_SO = 5
    DIR_O = 6
    DIR_NO = 7
    # Pheromone release quantity
    PHEROMONE_RELEASE_QUANTITY = 30
    """This is the ant class"""
    def __init__(self, canvas, width, height, food_pheromone_map, home_pheromone_map, food_map, home_map, position=(0,0), color="black"):
        """Initializes an ant"""
        self.canvas = canvas
        self.canvas_width = width
        self.canvas_height = height
        self.food_pheromone_map = food_pheromone_map
        self.home_pheromone_map = home_pheromone_map
        self.food_map = food_map
        self.home_map = home_map
        self.position = position
        self.color = color
        # status = {inactive|searching|going_home|eating}
        self.status = self.STATUS_INACTIVE
        self.home_pheromone_stock = 200000
        self.food_pheromone_stock = 500000
        # old continuous direction
        #self.direction = random.random() * math.pi * 2
        self.direction = random.randint(0, 7)
        # rotation_sense is direct (1) or indirect (-1)
        self.rotation_sense = 1
        # inertia defines the probability of (no) direction change
        self.inertia = 0.6
        # rotation_velocity defines the amplitude of direction change (rad)
        self.rotation_velocity = 0.15
        # rotation_inertia defines the probability of change of sense of rotation 
        self.rotation_inertia = 0.8
        # amount of food the ant is carrying
        self.carried_food = 0

    def __str__(self):
        """This is overwriting method to 'write' an ant"""
        return f"fourmi| {self.color}\t| {self.status}\t|{self.position} "

    def display(self):
        x = int(self.position[0])
        y = int(self.position[1])
        if self.status == self.STATUS_GOING_HOME:
            self.canvas.create_rectangle(x, y, x+1, y+1, outline="green", width=1, fill="green")
        else:
            self.canvas.create_rectangle(x, y, x+1, y+1, outline=self.color, width=1, fill=self.color)

    def erase(self):
        x = self.position[0]
        y = self.position[1]
        color = "white"
        home_pheromone_intensity = self.home_pheromone_map[x][y]
        food_pheromone_intensity = self.food_pheromone_map[x][y]
        if food_pheromone_intensity > home_pheromone_intensity:
            color = "#%02x%02x%02x" % tuple([255 - food_pheromone_intensity, 255 - food_pheromone_intensity, 255])
        elif home_pheromone_intensity != 0:
            color = "#%02x%02x%02x" % tuple([255, 255 - home_pheromone_intensity, 255 - home_pheromone_intensity])
        self.canvas.create_rectangle(x, y, x+1, y+1, outline=color, width=1, fill=color)

    def put_home_pheromone(self):
        """put home pheromone as long as the ant get some"""
        x = self.position[0]
        y = self.position[1]
        quantity = self.PHEROMONE_RELEASE_QUANTITY
        if self.home_pheromone_stock > quantity and self.home_pheromone_map[x][y] < (255 - quantity):
            self.home_pheromone_stock -= quantity
            self.home_pheromone_map[x][y] += quantity

    def put_food_pheromone(self):
        """put food pheromone as long as the ant get some"""
        x = self.position[0]
        y = self.position[1]      
        quantity = self.PHEROMONE_RELEASE_QUANTITY
        if self.food_pheromone_stock > quantity and self.food_pheromone_map[x][y] < (255 - quantity):
            self.food_pheromone_stock -= quantity
            self.food_pheromone_map[x][y] += quantity

    def move_random_old(self):
        x = self.position[0]
        y = self.position[1]
        # does the direction change?
        if random.random() > self.inertia:
            # does the sense of rotation change?
            if random.random() > self.rotation_inertia:
                self.rotation_sense = - self.rotation_sense
            double_pi = math.pi * 2
            self.direction = (self.direction + (self.rotation_sense * self.rotation_velocity)) % double_pi
        # calculate the new position (cyclic world!)
        x = (x + math.cos(self.direction)) % self.canvas_width
        y = (y + math.sin(self.direction)) % self.canvas_height
        self.position = (x,y)

    def move_random(self):
        x = self.position[0]
        y = self.position[1]
        xmax = self.canvas_width
        ymax = self.canvas_height
        # does the direction change?
        if random.random() > self.inertia:
            self.direction = (self.direction + random.choice([-1,1])) % 8
        # go one step in the direction
        if self.direction == self.DIR_N:
            y = (y - 1) % ymax
        elif self.direction == self.DIR_NE:
            x = (x + 1) % xmax
            y = (y - 1) % ymax
        elif self.direction == self.DIR_E:
            x = (x + 1) % xmax
        elif self.direction == self.DIR_SE:
            x = (x + 1) % xmax
            y = (y + 1) % ymax
        elif self.direction == self.DIR_S:
            y = (y + 1) % ymax
        elif self.direction == self.DIR_SO:
            x = (x - 1) % xmax
            y = (y + 1) % ymax
        elif self.direction == self.DIR_O:
            x = (x - 1) % xmax
        elif self.direction == self.DIR_NO:
            x = (x - 1) % xmax
            y = (y - 1) % ymax
        self.position = (x, y)

    def touch(self, thing_map):
        """returns True if self is in contact (8pos) with something on map, False otherwise"""
        x = self.position[0]
        y = self.position[1]
        # respect directions order: N, NE, E ...etc
        coord = [(0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1)]
        for i, j in coord:
            if thing_map[(x + i) % self.canvas_width][(y + j) % self.canvas_height] != 0:
                print("yeah")
                return True
        return False

    def detect(self, pheromone_map):
        """detect the pheromone on the pheromone_map and returns the best direction or -1 if nothing detected"""
        x = self.position[0]
        y = self.position[1]
        xmax = self.canvas_width
        ymax = self.canvas_height
        #respect directions order: N, NE, E ...etc
        max_pheromone = []
        zone_pheromone = 0
        # north
        for i in range(x - 1, x + 2):
            for j in range(y - 3, y):
                zone_pheromone += pheromone_map[i % xmax][j % ymax]
        max_pheromone.append(zone_pheromone)
        zone_pheromone = 0
        # north east
        for i in range(x +1, x + 4):
            for j in range(y - 3, y):
                zone_pheromone += pheromone_map[i % xmax][j % ymax]
        max_pheromone.append(zone_pheromone)
        zone_pheromone = 0
        # east
        for i in range(x + 1, x + 4):
            for j in range(y - 1, y + 2):
                zone_pheromone += pheromone_map[i % xmax][j % ymax]
        max_pheromone.append(zone_pheromone)
        zone_pheromone = 0
        # south east
        for i in range(x + 1, x + 4):
            for j in range(y + 1, y + 4):
                zone_pheromone += pheromone_map[i % xmax][j % ymax]
        max_pheromone.append(zone_pheromone)
        zone_pheromone = 0
        # south
        for i in range(x - 1, x + 2):
            for j in range(y + 1, y + 4):
                zone_pheromone += pheromone_map[i % xmax][j % ymax]
        max_pheromone.append(zone_pheromone)
        zone_pheromone = 0
        # south west
        for i in range(x - 3, x):
            for j in range(y + 1, y + 4):
                zone_pheromone += pheromone_map[i % xmax][j % ymax]
        max_pheromone.append(zone_pheromone)
        zone_pheromone = 0
        # west
        for i in range(x - 3, x):
            for j in range(y - 1, y + 2):
                zone_pheromone += pheromone_map[i % xmax][j % ymax]
        max_pheromone.append(zone_pheromone)
        zone_pheromone = 0
        # north west
        for i in range(x - 3, x):
            for j in range(y - 3, y):
                zone_pheromone += pheromone_map[i % xmax][j % ymax]
        max_pheromone.append(zone_pheromone)
        # returns the best direction or -1 if nothing detected
        maximum = max(max_pheromone)
        if maximum != 0:
            return max_pheromone.index(maximum)
        else:
            return -1

    def detect_home(self):
        """detect food up to one pixel and returns this pixel"""
        x = int(self.position[0]) % self.canvas_width
        y = int(self.position[1]) % self.canvas_height
        if self.home_pheromone_map[x][y] > 200:
            return True
        if self.home_map[(x - 1) % self.canvas_width][(y - 1) % self.canvas_height] != 0 or \
            self.home_map[x][(y - 1) % self.canvas_height] != 0 or \
            self.home_map[(x + 1) % self.canvas_width][(y - 1) % self.canvas_height] != 0 or \
            self.home_map[(x - 1) % self.canvas_width][y] != 0 or \
            self.home_map[(x + 1) % self.canvas_width][y] != 0 or \
            self.home_map[(x - 1) % self.canvas_width][(y + 1) % self.canvas_height] != 0 or \
            self.home_map[x][(y + 1) % self.canvas_height] != 0 or \
            self.home_map[(x + 1) % self.canvas_width][(y + 1) % self.canvas_height] != 0:
            return True
        else : return False

    def detect_food_pheromone(self):
        x = int(self.position[0])
        y = int(self.position[1])
        max_pheromone = 0
        x_max = 0
        y_max = 0
        for i in range(-1,2):
            for j in range(-1,2):
                max_temp = self.food_pheromone_map[(x + i) % self.canvas_width][(y + j) % self.canvas_height]
                if max_temp > max_pheromone:
                    max_pheromone = max_temp
                    x_max = i
                    y_max = j
        if max_pheromone == 0:
            return (0, 0)
        return(x_max, y_max)

    def detect_home_pheromone(self):
        x = int(self.position[0])
        y = int(self.position[1])
        max_pheromone = 0
        x_max = 0
        y_max = 0
        for i in range(-1,2):
            for j in range(-1,2):
                max_temp = self.home_pheromone_map[(x + i) % self.canvas_width][(y + j) % self.canvas_height]
                if max_temp > max_pheromone:
                    max_pheromone = max_temp
                    x_max = i
                    y_max = j
        if max_pheromone == 0:
            return (0, 0)
        return(x_max, y_max)
