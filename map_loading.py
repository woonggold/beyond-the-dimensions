import settings
import json
class Block:
    def __init__(self, pos, texture_num):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.original_z = self.z
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
    global BLOCKS
    if map_name == "test":
        

        for i in range(12):
            for j in range(10):
                BLOCKS.append(Block((i*100-500,500,j*100-500),0))
        BLOCKS.append(Block((100,400,100),0))

        
        return BLOCKS
class Map:
    def __init__(self, map):
        self.BLOCKS = load_map(map)

map_test = Map(settings.map_name)

def map_save():
    blocks_dict_x = []
    blocks_dict_y = []
    blocks_dict_z = []
    blocks_dict_texture = []
    for block in map_test.BLOCKS:
        blocks_dict_x.append(block.x)
        blocks_dict_y.append(block.y)
        blocks_dict_z.append(block.z)
        blocks_dict_texture.append(block.texture_num)
    
    separated_data = {
        "x": blocks_dict_x,
        "y": blocks_dict_y,
        "z": blocks_dict_z, 
        "texture": blocks_dict_texture, 
    }
    
    final_data = {
        "Blocks": separated_data, 
    }
    mapname = input("저장할 맵 이름을 입력해 주세요: ")

    with open(mapname+'.json', 'w', encoding='utf-8') as json_file:
        json.dump(final_data, json_file, ensure_ascii=False, indent=4)    
    print("저장됨")
        
def map_load():
    mapname = input("불러올 맵 이름을 입력해 주세요: ")
    with open(mapname+'.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    for block in map_test.BLOCKS:
        map_test.BLOCKS.remove(block)
    for i in range(len(data["Blocks"]["x"])):
                
        BLOCKS.append(Block((data["Blocks"]["x"][i],data["Blocks"]["y"][i],data["Blocks"]["z"][i]),data["Blocks"]["texture"][i]))

    print("로드됨")