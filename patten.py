import json
import map_loading
import collections
import time


class Patten:
    def __init__(patten ,patten_name):
        import real_game
        #패터 이름 받아오기
        patten.patten_name = patten_name
        patten.action_queue = collections.deque()
        patten.block_list = []
        #맵 josn 받아오기
        with open('./map/patten'+str(patten_name)+'.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        #블록의 x, y, z를 알아내기 위해 josn에서 x,y,z만 추출해서 blocklist에 넘
        for i in range(len(data["Blocks"]["x"])):
            tuple1= (data["Blocks"]["x"][i], data["Blocks"]["y"][i], data["Blocks"]["z"][i])
            patten.block_list.append(tuple1)

        #각 큐마다 고유한 정보를 저장하는 코드
        for i in range(len(patten.block_list)):
            patten.action_queue.append({
                "position": (patten.block_list[i][0], patten.block_list[i][1], patten.block_list[i][2]), 
                "status": patten.patten_name,
                "texture_num": 0,
                "last_update": real_game.nowtime  # 각 패턴마다 시간 생성
            })
    #디버그용 클래스를 프린트 할 때 이게 출력됨
    def __str__(patten):
        return f"{patten.patten_name}"       
    
     
def start_patten(patten):
    import real_game
    # real_game.pattens.remove(patten_loop[real_game.cur_patten][0])
    
    #각 큐마다의 정보를 알아내기 위한 for문
    for action in list(patten.action_queue):
        time_elapsed = real_game.nowtime - action["last_update"]
        #처음 빨간생 블록을 0.05가 지나면 생성하는 코드
        if action["status"] == patten.patten_name and time_elapsed >= 50:
            x, y, z = action["position"]
            
            map_loading.BLOCKS.append(map_loading.Block((x, y, z), 3))
            action["status"] = "block_origin_appear"
            action["last_update"] = real_game.nowtime
        #빨간색이였던 블록을 다시 0번째 블록으로 바꾸는 코드
        elif action["status"] == "block_origin_appear" and time_elapsed >= 450:
            x, y, z = action["position"]
            for block in list(map_loading.BLOCKS):
                if block.pos == (x, y, z):
                    map_loading.BLOCKS.remove(block)
            map_loading.BLOCKS.append(map_loading.Block((x, y, z), 0))
            action["status"] = "re_red_block"
            action["last_update"] = real_game.nowtime
        # 다시 2.5초 지나면 빨간색 블록으로 바뀜
        elif action["status"] == "re_red_block" and time_elapsed >= 2500:
            x, y, z = action["position"]
            map_loading.BLOCKS.append(map_loading.Block((x, y, z), 1))
            action["status"] = "disappear"
            action["last_update"] = real_game.nowtime
        # 그리고 소멸
        elif action["status"] == "disappear" and time_elapsed >= 500:
            x, y, z = action["position"]
            for block in list(map_loading.BLOCKS):
                if block.pos == (x, y, z):
                    map_loading.BLOCKS.remove(block)
            action["last_update"] = real_game.nowtime
            patten.action_queue.remove(action)
            # if patten.patten_name == 14:
            #     real_game.pattens = []
            
#패턴 초기화하는 함수
def reloadpatten():
    global patten_loop
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
