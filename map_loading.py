import settings
class Block:
    def __init__(self, pos):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.size = 50 #settings.py의 cube_size와 일치시켜야 됨.
        self.points = [
            [self.x - self.size, self.y - self.size, self.z - self.size, self.z - self.size], [self.x + self.size, self.y - self.size, self.z - self.size, self.z - self.size],
            [self.x + self.size, self.y + self.size, self.z - self.size, self.z - self.size], [self.x - self.size, self.y + self.size, self.z - self.size, self.z - self.size],
            [self.x - self.size, self.y - self.size, self.z + self.size, self.z + self.size], [self.x + self.size, self.y - self.size, self.z + self.size, self.z + self.size],
            [self.x + self.size, self.y + self.size, self.z + self.size, self.z + self.size], [self.x - self.size, self.y + self.size, self.z + self.size, self.z + self.size]
        ]
        self.texture = [(100,100,100),(255,255,255),(255,0,0),(0,0,0)]


def load_map(map_name):
    global cube_size, BLOCKS
    if map_name == "test":
        BLOCKS = []


        for i in range(10):
            for j in range(10):
                BLOCKS.append(Block((i*100-500,500,j*100-500)))
        BLOCKS.append(Block((300,400,-500)))
        BLOCKS.append(Block((300,300,-500)))
        
        return BLOCKS

class Map:
    def __init__(self, map):
        self.BLOCKS = load_map(map)

map_test = Map(settings.map_name)