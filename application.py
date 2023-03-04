import tkinter as tk
import numpy as np
import ant
import math

class Application(tk.Tk):
    NB_ANTS = 200
    CANVAS_WIDTH = 600
    CANVAS_HEIGHT = 400
    ANTHILL_XPOS = 100
    ANTHILL_YPOS = 100
    FOOD_XPOS = 200
    FOOD_YPOS = 200
    FOOD_PHEROMONE_DISTANCE = 50
    DISSOLVE_TIME = 50
    def __init__(self):
        tk.Tk.__init__(self)
        # GUI
        self.create_canvas()
        self.create_widget()
        # Ant world
        self.food_pheromone_map = np.zeros((self.CANVAS_WIDTH, self.CANVAS_HEIGHT), dtype=int)
        self.home_pheromone_map = np.zeros((self.CANVAS_WIDTH, self.CANVAS_HEIGHT), dtype=int)
        self.food_map = np.zeros((self.CANVAS_WIDTH, self.CANVAS_HEIGHT), dtype=int)
        self.init_food()
        self.home_map = np.zeros((self.CANVAS_WIDTH, self.CANVAS_HEIGHT), dtype=int)
        self.home_map[self.ANTHILL_XPOS, self.ANTHILL_YPOS] = 1
        self.ant_list = []
        for i in range(self.NB_ANTS):
                self.ant_list.append(ant.Ant(self.canvas, self.CANVAS_WIDTH, self.CANVAS_HEIGHT,
                                             self.food_pheromone_map, self.home_pheromone_map,\
                                             self.food_map, self.home_map,\
                                            (self.ANTHILL_XPOS, self.ANTHILL_YPOS)))
        self.time_to_dissolve = 10
        # Initial display
        self.display_anthill()
        self.display_food_pheromone()
        self.display_food()
  
    def create_canvas(self):
        self.canvas = tk.Canvas(self,bg="white", height=self.CANVAS_HEIGHT, width=self.CANVAS_WIDTH)
        self.canvas.pack(side = tk.LEFT)
        
    def create_widget(self):
        self.button_quit = tk.Button(self, text="close", command=self.quit)
        self.button_release = tk.Button(self, text="release ant", command=self.release_ant)
        self.button_release_ten = tk.Button(self, text="release 10 ants", command=self.release_ten_ants)
        self.button_release_all = tk.Button(self, text="release all ants", command=self.release_all_ants)
        self.button_animate = tk.Button(self, text="animate", command=self.animate)
        self.button_quit.pack(side=tk.TOP, fill = tk.X)
        self.button_release.pack(side=tk.TOP, fill = tk.X)
        self.button_release_ten.pack(side=tk.TOP, fill = tk.X)
        self.button_release_all.pack(side=tk.TOP, fill = tk.X)
        self.button_animate.pack(side=tk.TOP, fill = tk.X)

    def init_food(self):
        food_xpos = self.FOOD_XPOS
        food_ypos = self.FOOD_YPOS
        distance = self.FOOD_PHEROMONE_DISTANCE
        self.food_map[food_xpos, food_ypos] = 1
        for i in range(food_xpos - distance, food_xpos + distance):
            for j in range(food_ypos - distance, food_ypos + distance):
                dist = math.sqrt((i - food_xpos) **2 + (j - food_ypos) ** 2)
                if dist < distance:
                    intensity = int (255 - (255 / distance * dist))
                    self.food_pheromone_map[i % self.CANVAS_WIDTH][j % self.CANVAS_HEIGHT] = intensity

    def release_all_ants(self):
        for i in range(self.NB_ANTS):
            self.ant_list[i].status = self.ant_list[i].STATUS_SEARCHING

    def release_ant(self):
        change_made = False
        i = 0
        while change_made != True and i < self.NB_ANTS:
            if self.ant_list[i].status == self.ant_list[i].STATUS_INACTIVE:
                self.ant_list[i].status = self.ant_list[i].STATUS_SEARCHING
                change_made = True
            i += 1

    def release_n_ants(self, n):
        if n > self.NB_ANTS:
            n = self.NB_ANTS
        count = 0
        i = 0
        while i < self.NB_ANTS and count < n:
            if self.ant_list[i].status == self.ant_list[i].STATUS_INACTIVE:
                self.ant_list[i].status = self.ant_list[i].STATUS_SEARCHING
                count += 1
            i += 1

    def release_ten_ants(self):
        self.release_n_ants(10)

    def display_food_pheromone(self):
        for x in range(self.CANVAS_WIDTH):
            for y in range(self.CANVAS_HEIGHT):
                intensity = self.food_pheromone_map[x][y]
                if intensity != 0:
                    color = "#%02x%02x%02x" % tuple([255 - intensity, 255 - intensity, 255])
                    self.canvas.create_rectangle(x, y, x+1, y+1, outline=color, width=1, fill=color)

    def display_home_pheromone(self):
        for x in range(self.CANVAS_WIDTH):
            for y in range(self.CANVAS_HEIGHT):
                intensity = self.home_pheromone_map[x][y]
                if intensity != 0:
                    color = "#%02x%02x%02x" % tuple([255, 255 - intensity, 255 - intensity])
                    self.canvas.create_rectangle(x, y, x+1, y+1, outline=color, width=1, fill=color)

    def display_anthill(self):
        self.canvas.create_rectangle(self.ANTHILL_XPOS, self.ANTHILL_YPOS,\
             self.ANTHILL_XPOS+1, self.ANTHILL_YPOS+1, outline="green", width=1, fill="green")
        self.canvas.create_oval(self.ANTHILL_XPOS-2, self.ANTHILL_YPOS-2,\
             self.ANTHILL_XPOS+3, self.ANTHILL_YPOS+3, outline="green", width=1)

    def display_food(self):
        self.canvas.create_rectangle(self.FOOD_XPOS, self.FOOD_YPOS,\
             self.FOOD_XPOS+1, self.FOOD_YPOS+1, outline="grey", width=1, fill="grey")
        self.canvas.create_oval(self.FOOD_XPOS-2, self.FOOD_YPOS-2,\
             self.FOOD_XPOS+3, self.FOOD_YPOS+3, outline="grey", width=1)

    def dissolve(self):
        if self.time_to_dissolve == 0:
            for i in range(self.CANVAS_WIDTH):
                for j in range(self.CANVAS_HEIGHT):
                    if self.home_pheromone_map[i][j] > 0:
                        self.home_pheromone_map[i][j] -= 1
                    if self.food_pheromone_map[i][j] > 0:
                        self.food_pheromone_map[i][j] -= 1
            self.time_to_dissolve == self.DISSOLVE_TIME
        else:
            self.time_to_dissolve -= 1

    def animate(self):
        #self.dissolve()
        #self.display_food_pheromone()
        #self.display_home_pheromone()
        self.display_anthill()
        self.display_food()
        self.work()
        self.after(1, self.animate)

    def work(self):
        for i in range(self.NB_ANTS):
            ant = self.ant_list[i]
            if ant.status == ant.STATUS_SEARCHING:
                # In any case, put pheromone to find your way home (if any)
                ant.put_home_pheromone()
                # Erasing causes pheromone to be visible again so we call erase after put_home_ pheromone
                ant.erase()
                #if ant touches food, change status
                if ant.touch(self.food_map):
                    ant.status = ant.STATUS_GOING_HOME
                # If you can, follow the hunting trail
                direction = ant.detect(self.food_pheromone_map)
                if direction != -1:
                    coord = [(0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1)]
                    new_x = (ant.position[0] + coord[direction][0]) % self.CANVAS_WIDTH
                    new_y = (ant.position[1] + coord[direction][1]) % self.CANVAS_HEIGHT
                    ant.position = (new_x, new_y)
                # Otherwise go anywhere
                #else: !!!!!!!! AND is goood!
                ant.move_random()
                ant.display()
            elif ant.status == ant.STATUS_GOING_HOME:
                # In any case, put pheromone to help friends find the food
                ant.put_food_pheromone()
                # Erasing causes pheromone to be visible again so we call erase after put_home_ pheromone
                ant.erase()
                # If you're home you're done
                if ant.touch(self.home_map):
                    ant.status = ant.STATUS_INACTIVE
                # If you can, go home directly
                #direction = ant.detect(self.home_pheromone_map)
                #if direction != -1:
                #    coord = [(0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1)]
                #    new_x = (ant.position[0] + coord[direction][0]) % self.CANVAS_WIDTH
                #    new_y = (ant.position[1] + coord[direction][1]) % self.CANVAS_HEIGHT
                #    ant.position = (new_x, new_y)
                    # Otherwise go anywhere
                #else:
                ant.move_random()
                ant.display()
            elif ant.status == ant.STATUS_INACTIVE:
                ant.erase()



if __name__ == "__main__":
    application = Application()
    application.mainloop()
