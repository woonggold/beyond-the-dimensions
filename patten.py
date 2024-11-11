import real_game
import json
import map_loading
import collections


class Patten:
    def __init__(patten ,patten_name):

        patten.patten_name = patten_name
        patten.action_queue = collections.deque()
        patten.block_list = []
        with open('./map/'+patten_name+'.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        for i in range(len(data["Blocks"]["x"])):
            tuple1= (data["Blocks"]["x"][i], data["Blocks"]["y"][i], data["Blocks"]["z"][i])
            patten.block_list.append(tuple1)

        for i in range(len(patten.block_list)):
            patten.action_queue.append({
                "position": (patten.block_list[i][0], patten.block_list[i][1], patten.block_list[i][2]), 
                "status": patten.patten_name,
                "texture_num": 0,
                "last_update": real_game.nowtime  # 각 액션의 시작 시간을 기록
            })
def start_patten(patten):
    for action in list(patten.action_queue):
        time_elapsed = real_game.nowtime - action["last_update"]

        if action["status"] == patten.patten_name and time_elapsed >= 50:
            x, y, z = action["position"]
            map_loading.BLOCKS.append(map_loading.Block((x, y, z), 1))
            action["status"] = "block_origin_appear"
            action["last_update"] = real_game.nowtime

        elif action["status"] == "block_origin_appear" and time_elapsed >= 450:
            x, y, z = action["position"]
            for block in list(map_loading.BLOCKS):
                if block.pos == (x, y, z):
                    map_loading.BLOCKS.remove(block)
            map_loading.BLOCKS.append(map_loading.Block((x, y, z), 0))
            action["status"] = "re_red_block"
            action["last_update"] = real_game.nowtime

        elif action["status"] == "re_red_block" and time_elapsed >= 1500:
            x, y, z = action["position"]
            map_loading.BLOCKS.append(map_loading.Block((x, y, z), 1))
            action["status"] = "disappear"
            action["last_update"] = real_game.nowtime

        elif action["status"] == "disappear" and time_elapsed >= 500:
            x, y, z = action["position"]
            for block in list(map_loading.BLOCKS):
                if block.pos == (x, y, z):
                    map_loading.BLOCKS.remove(block)
            patten.action_queue.remove(action)