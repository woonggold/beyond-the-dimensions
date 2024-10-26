import settings
class Block:
    def __init__(self, pos, texture_num):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.size = 50 #settings.py의 cube_size와 일치시켜야 됨.
        self.points = [
            [self.x - self.size, self.y - 50, self.z - self.size, self.z - self.size], [self.x + self.size, self.y - 50, self.z - self.size, self.z - self.size],
            [self.x + self.size, self.y + 50, self.z - self.size, self.z - self.size], [self.x - self.size, self.y + 50, self.z - self.size, self.z - self.size],
            [self.x - self.size, self.y - 50, self.z + self.size, self.z + self.size], [self.x + self.size, self.y - 50, self.z + self.size, self.z + self.size],
            [self.x + self.size, self.y + 50, self.z + self.size, self.z + self.size], [self.x - self.size, self.y + 50, self.z + self.size, self.z + self.size]
        ]
        self.texture_num = texture_num
        self.texture = settings.block_textures[texture_num]

BLOCKS = []

def load_map(map_name):
    global cube_size, BLOCKS
    if map_name == "test":
        

        for i in range(12):
            for j in range(10):
                BLOCKS.append(Block((i*100-500,500,j*100-500),0))
        BLOCKS.append(Block((300,400,-500),0))
        BLOCKS.append(Block((300,300,-500),0))
        
        return BLOCKS
class Map:
    def __init__(self, map):
        self.BLOCKS = load_map(map)

map_test = Map(settings.map_name)