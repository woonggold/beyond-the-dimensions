import settings
import json
class Block:
    def __init__(self, pos, texture_num):
        self.pos = pos
        self.x = int(pos[0])
        self.y = int(pos[1])
        self.z = int(pos[2])
        self.original_z = self.z
        self.size = settings.cube_size
        self.points = [
            [self.x - self.size, self.y - 50, self.z - self.size, self.z - self.size], [self.x + self.size, self.y - 50, self.z - self.size, self.z - self.size],
            [self.x + self.size, self.y + 50, self.z - self.size, self.z - self.size], [self.x - self.size, self.y + 50, self.z - self.size, self.z - self.size],
            [self.x - self.size, self.y - 50, self.z + self.size, self.z + self.size], [self.x + self.size, self.y - 50, self.z + self.size, self.z + self.size],
            [self.x + self.size, self.y + 50, self.z + self.size, self.z + self.size], [self.x - self.size, self.y + 50, self.z + self.size, self.z + self.size]
        ]
        self.texture_num = texture_num
        self.texture = settings.block_textures[texture_num]

BLOCKS = []
warp_block_list = []

def load_map(map_name):
    global BLOCKS
    if map_name == "test":

        for i in range(1):
            for j in range(1):
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
    blocks_dict_warp_name = settings.warp_block_data
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
        "warp_blocks": blocks_dict_warp_name
    }
    mapname = input("저장할 맵 이름을 입력해 주세요: ")

    with open('./map/'+mapname+'.json', 'w', encoding='utf-8') as json_file:
        json.dump(final_data, json_file, ensure_ascii=False, indent=4)    
    print("저장됨")
        
def map_load(mapname):
    global BLOCKS, warp_block_list, stagename
    stagename = mapname
    if mapname == "":
        mapname = input("불러올 맵 이름을 입력해 주세요: ")
    else:
        pass
    with open('./map/'+mapname+'.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    BLOCKS = []
    warp_block_list = []
    for i in range(len(data["Blocks"]["x"])):
                
        BLOCKS.append(Block((data["Blocks"]["x"][i],data["Blocks"]["y"][i],data["Blocks"]["z"][i]),data["Blocks"]["texture"][i]))
        
    try:
        for i in range(0, len(data["warp_blocks"]["x"])):

            tuple1= (data["warp_blocks"]["x"][i], data["warp_blocks"]["y"][i], data["warp_blocks"]["z"][i], data["warp_blocks"]["warp_name"][i])
            warp_block_list.append(tuple1)
            BLOCKS.append(Block((data["warp_blocks"]["x"][i],data["warp_blocks"]["y"][i],data["warp_blocks"]["z"][i]),9))
    except:
        pass


    print("로드됨")
    
    
    