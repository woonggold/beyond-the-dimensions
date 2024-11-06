import settings
import json
import piece
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

def map_save():
    blocks_dict_x = []
    blocks_dict_y = []
    blocks_dict_z = []
    blocks_dict_texture = []
    blocks_dict_warp_name = settings.warp_block_data
    blocks_dict_event_name = settings.event_block_data
    for block in BLOCKS:
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
        "warp_blocks": blocks_dict_warp_name,
        "event_blocks": blocks_dict_event_name
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
    warp_name_list = []
    warp_block_x_list = []
    warp_block_y_list = []
    warp_block_z_list = []
    event_name_list = []
    event_block_x_list = []
    event_block_y_list = []
    event_block_z_list = []


    for i in range(len(data["Blocks"]["x"])):
                
        BLOCKS.append(Block((data["Blocks"]["x"][i],data["Blocks"]["y"][i],data["Blocks"]["z"][i]),data["Blocks"]["texture"][i]))
        
    try:
        for i in range(0, len(data["warp_blocks"]["x"])):

            tuple1= (data["warp_blocks"]["x"][i], data["warp_blocks"]["y"][i], data["warp_blocks"]["z"][i], data["warp_blocks"]["warp_name"][i])
            warp_block_list.append(tuple1)
            BLOCKS.append(Block((data["warp_blocks"]["x"][i],data["warp_blocks"]["y"][i],data["warp_blocks"]["z"][i]),9))
            warp_block_x_list.append(data["warp_blocks"]["x"][i])
            warp_block_y_list.append(data["warp_blocks"]["y"][i])
            warp_block_z_list.append(data["warp_blocks"]["z"][i])
            warp_name_list.append(data["warp_blocks"]["warp_name"][i])



            
    except:
        pass
    try:
        for i in range(0, len(data["event_blocks"]["x"])):
            piece.Pieces.append(piece.MakePiece((data["event_blocks"]["x"][i],data["event_blocks"]["y"][i],data["event_blocks"]["z"][i]),data["event_blocks"]["event_name"][i]))
            event_block_x_list.append(data["warp_blocks"]["x"][i])
            event_block_y_list.append(data["warp_blocks"]["y"][i])
            event_block_z_list.append(data["warp_blocks"]["z"][i])
            event_name_list.append(data["warp_blocks"]["warp_name"][i])
    
    except:
        pass
    settings.warp_block_data = {
            "x": warp_block_x_list,
            "y": warp_block_y_list,
            "z": warp_block_z_list, 
            "warp_name": warp_name_list, 
        }
    
    settings.event_block_data = {
        "x": event_block_x_list,
        "y": event_block_y_list,
        "z": event_block_z_list, 
        "event_name": event_name_list, 
    }

    print("로드됨")
    
    
    