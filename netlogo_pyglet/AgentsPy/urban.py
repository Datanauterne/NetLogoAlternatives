import math
import agents as ag

class Seeker(ag.Agent):
    def setup(self, model):
        (w,h) = model.get_area_size()
        self.x = w//2
        self.y = h//2
        self.size=4
        self.speed=1
        self.direction = ag.RNG(360)
        self.search_angle = 45
        self.set_color(0,0,255)
        self.settle = 0
        self.settled = False
        self.desire = 100 + ag.RNG(100)

    def get_next_tile(self,model,d):
        next_x = round(self.x + math.cos(math.radians(d)) * self.speed)
        next_y = round(self.y + math.sin(math.radians(d)) * self.speed)
        return model.get_tile(next_x,next_y)

    def step(self, model):
        if not self.settled:
            t = self.current_tile()
            if ag.RNG(100) > 75:
                t.info["value"] = min(t.info["value"]+1,255)
            fwd_tile = self.get_next_tile(model, self.direction)
            l_tile = self.get_next_tile(model, self.direction+self.search_angle)
            r_tile = self.get_next_tile(model, self.direction-self.search_angle)
            best_tile = max(fwd_tile.info["value"],l_tile.info["value"],r_tile.info["value"])
            if best_tile == l_tile.info["value"]:
                self.direction += ag.RNG(self.search_angle)
            if best_tile == r_tile.info["value"]:
                self.direction -= ag.RNG(self.search_angle)
            self.forward()
            self.settle += 1
            c_tile = self.current_tile()
            if self.settle > self.desire:
                self.set_color(150,150,255)
                self.settled = True
                self.settle = 0
        else:
            self.desire -= 1
            t = self.current_tile()
            if ag.RNG(100) > 75:
                t.info["value"] = max(t.info["value"]-1,0)
            if self.desire <= 0 or model.get_tile(self.x,self.y).info["value"] < 10:
                self.settled = False
                self.set_color(0,0,255)
                self.desire = 100 + ag.RNG(100)

def setup(model):
    model.reset()
    model["invisible"] = False
    (tx,ty) = model.get_tiles_xy()
    init_tile = model.get_tile(0,0)
    model.get_tile_index(0,0).info["value"] = 150
    for x in range(tx):
        for y in range(ty):
            avg_value = 0
            neighbors = 0
            if y > 0:
                avg_value += model.get_tile_index(x,y-1).info["value"]
                neighbors += 1
            if x > 0:
                avg_value += model.get_tile_index(x-1,y).info["value"]
                neighbors += 1
            if neighbors > 0:
                model.get_tile_index(x,y).info["value"] = max(0,min(255,avg_value // neighbors - 15 + ag.RNG(30)))
    for tile in model.get_tiles():
        tile.set_color(tile.info["value"],tile.info["value"],0)
    seekers = set([Seeker() for i in range(200)])
    model.add_agents(seekers)
    for a in model.get_agents():
        a.setup(model)

def step(model):
    for tile in model.get_tiles():
        tile.set_color(tile.info["value"],tile.info["value"],0)
        if tile.info["value"] > 255:
            tile.info["value"] = 0
    for agent in model.get_agents():
        agent.step(model)

def invisible(model):
    model["invisible"] = not model["invisible"]
    if model["invisible"]:
        for a in model.get_agents():
            a.size = 0
    else:
        for a in model.get_agents():
            a.size = 4

urban_model = ag.Model(400,400,50,50)
urban_model.add_single_button("Setup", setup)
urban_model.add_toggle_button("Go", step)
urban_model.add_single_button("Invisible", invisible)
ag.Start()
