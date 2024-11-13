import json
import map_loading
import collections
import time


class Patten:
    def __init__(patten ,patten_name):
        import real_game
        
        patten.patten_name = patten_name
        patten.action_queue = collections.deque()
        patten.block_list = []
        with open('./map/patten'+str(patten_name)+'.json', 'r', encoding='utf-8') as json_file:
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
    import real_game
    # 모든 action을 순회하며 업데이트
    # real_game.pattens.remove(patten_loop[real_game.cur_patten][0])
    
    for action in list(patten.action_queue):  # deque를 리스트로 복사하여 순회
        time_elapsed = real_game.nowtime - action["last_update"]
        print(patten.patten_name)
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

        elif action["status"] == "re_red_block" and time_elapsed >= 2500:
            x, y, z = action["position"]
            map_loading.BLOCKS.append(map_loading.Block((x, y, z), 1))
            action["status"] = "disappear"
            action["last_update"] = real_game.nowtime

        elif action["status"] == "disappear" and time_elapsed >= 500:
            x, y, z = action["position"]
            for block in list(map_loading.BLOCKS):
                if block.pos == (x, y, z):
                    map_loading.BLOCKS.remove(block)
            # 액션을 완료했으므로 큐에서 제거
            patten.action_queue.remove(action)
            # if patten.patten_name == 14:
            #     real_game.pattens = []
            

patten_loop = [
    [0, 1],#작동 안함
    [Patten(1), 2],
    [Patten(2), 2],
    [Patten(3), 2],
    [Patten(4), 2],
    [Patten(5), 2],
    [Patten(6), 2],
    [Patten(7), 2],
    [Patten(8), 2],
    [Patten(9), 2],
    [Patten(10), 2],
    [Patten(11), 2],
    [Patten(12), 2],
    [Patten(13), 2],
    [Patten(14), 2],
]
