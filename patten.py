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
    # 모든 action을 순회하며 업데이트
    for action in list(patten.action_queue):  # deque를 리스트로 복사하여 순회
        time_elapsed = real_game.nowtime - action["last_update"]
        
        if action["status"] == patten.patten_name and time_elapsed >= 50:
            # 패턴 2의 블록 생성
            x, y, z = action["position"]
            map_loading.BLOCKS.append(map_loading.Block((x, y, z), 1))  # 다른 색상 혹은 다른 동작
            action["status"] = "block_origin_appear"
            action["last_update"] = real_game.nowtime
            
        elif action["status"] == "block_origin_appear" and time_elapsed >= 450:
            # 기존 블록 제거하고 원래 블록 생성
            x, y, z = action["position"]
            for block in list(map_loading.BLOCKS):
                if block.pos == (x, y, z):
                    map_loading.BLOCKS.remove(block)
            map_loading.BLOCKS.append(map_loading.Block((x, y, z), 0))  # 원래 블록 생성
            action["status"] = "re_red_block"
            action["last_update"] = real_game.nowtime  # 상태가 변경되었으므로 시간 갱신

        elif action["status"] == "re_red_block" and time_elapsed >= 1500:
            # 빨간색 블록 다시 생성
            x, y, z = action["position"]
            map_loading.BLOCKS.append(map_loading.Block((x, y, z), 1))
            action["status"] = "disappear"
            action["last_update"] = real_game.nowtime  # 상태가 변경되었으므로 시간 갱신

        elif action["status"] == "disappear" and time_elapsed >= 500:
            # 블록 제거
            x, y, z = action["position"]
            for block in list(map_loading.BLOCKS):
                if block.pos == (x, y, z):
                    map_loading.BLOCKS.remove(block)
            # 액션을 완료했으므로 큐에서 제거
            patten.action_queue.remove(action)
