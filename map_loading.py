class Block:
    def __init__(self, pos, size):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.size = size
        self.points = [
            [self.x - self.size, self.y - 50, self.z - self.size, self.z - self.size], [self.x + self.size, self.y - 50, self.z - self.size, self.z - self.size],
            [self.x + self.size, self.y + 50, self.z - self.size, self.z - self.size], [self.x - self.size, self.y + 50, self.z - self.size, self.z - self.size],
            [self.x - self.size, self.y - 50, self.z + self.size, self.z + self.size], [self.x + self.size, self.y - 50, self.z + self.size, self.z + self.size],
            [self.x + self.size, self.y + 50, self.z + self.size, self.z + self.size], [self.x - self.size, self.y + 50, self.z + self.size, self.z + self.size]
        ]
        #self.squares = []


def load_map(map_name):
    global cube_size, BLOCKS
    if map_name == "test":
        BLOCKS = []

        

        BLOCKS.append(Block((0,500,0),500))
        BLOCKS.append(Block((300,400,-500),50))
        BLOCKS.append(Block((300,300,-500),50))
        
        return BLOCKS
class Map:
    def __init__(self, map):
        self.BLOCKS = load_map(map)