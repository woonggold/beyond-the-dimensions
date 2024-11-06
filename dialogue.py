import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DIALOGUE_BOX_COLOR = (50, 50, 50)

# Font
font = pygame.font.Font('fonts/BMDOHYEON_otf.otf', 36)
current_dialogue_index = 0
is_talking = False

talking = {
    "1-1": {
        "lines": [
            "으..", 
            "으으…", 
            "여긴 대체 어디지..?", 
            "이 걸리적거리는 헤드셋은 대체 뭐야?…", 
            "일단.. 주변을 좀 둘러볼까…?"
        ],
        "position": (150, 250, 50, 150)
    },
    "1-2": {
        "lines": [
            "(왜 이런 곳에 낭떠러지가 있는거지..?)", 
            "일단 넘어가보자"
        ],
        "position": (-250, -150, 50, 150)
    },
    "1-3": {
        "lines": ["그래서 여기가 어디인거지.."],
        "position": (-2350, -2250, 50, 150)
    },
    "1-4": {
        "lines": ["어", "이건 뭐지"],
        "position": (-6350, -6250, 50, 150)
    },
    "1-5": {
        "lines": ["어…!!!!", "빨려들어간다"],
        "position": (-6950, -6850, 50, 250)
    },
    "2-1": {
        "lines": [
            "뭐야?", "세상이 왜 이러지..!?", "ㅏㅏㅏ.. ", "들리니?", "어… 누가 말하는 거야?",
            "내가 왜 이런 곳에 있는 건데..!?", "안녕,", "난 너를 만든 과학자고",
            "다른 차원에서 너를 바라보고 있어.", "너를 만들어내면서 차원간의 균열이 일어났는데,",
            "방금 너가 그 균열을 지나온 거야.", "그니까 지금 더 높은 차원으로 넘어왔다고 생각하면 돼.",
            "그러니까…한마디로...", "너는 앞에 있는 벽을 지나갈 수 있을 거야.",
            "왜 딴소리야.. 내 목소리가 안 들리는 건가..?", "그나저나 내가 이 벽을 지나갈 수 있다고?",
            "막혀있는데..?", "...?"
        ],
        "position": (-1000, -900, -1000, -900)
    },
    "2-2": {
        "lines": ["이게 되네.."],
        "position": (-1000, -900, -1000, -900)
    },
    "2-3": {
        "lines": ["일단.. 들어가 봐야겠지..?"],
        "position": (-1000, -900, -1000, -900)
    },
    "3-1": {
        "lines": [
            "으아아악!", "무슨 일이야??", "으….", "지금 우리 차원에서도 균열이 발생하고 있어..",
            "당분간은 대화하기 힘들 것 같아….", "뭐..?", "여보세요….?", "…", 
            "..일단 할 수 있는 걸 하자"
        ],
        "position": (-1000, -900, -1000, -900)
    },
    "4-1": {
        "lines": [
            "흠…. 뭔가 이상한 느낌이 드는데…", 
            "차원 균열이 점점 커지는 것 같기도 하고"
        ],
        "position": (-1000, -900, -1000, -900)
    },
    "4-2": {
        "lines": ["어어…", "세상이..?"],
        "position": (-1000, -900, -1000, -900)
    },
    "4-3": {
        "lines": [
            "잠깐만… 왜 내가 천장에 있지…?", 
            "..아", 
            "내가 천장에 있는게 아니라", 
            "세상이 뒤바뀐거구나..", 
            "..젠장"
        ],
        "position": (-1000, -900, -1000, -900)
    },
    "5-1": {
        "lines": ["ㅏㅏ", "일단 차원 붕괴를 안정시키고 왔어..!"],
        "position": (-1000, -900, -1000, -900)
    }
}

def check_player_position():
    import real_game
    global is_talking, current_dialogue_key

    is_talking = False
    for key, dialogue in talking.items():
        x_min, x_max, z_min, z_max = dialogue["position"]
        if x_min < real_game.player.x < x_max and z_min < real_game.player.z < z_max:
            if dialogue.get("completed", False) is not True:  # Run only if not completed
                is_talking = True
                current_dialogue_key = key
                return
            
def talkcheck():
    import real_game
    global current_dialogue_index, is_talking, current_dialogue_key
    
    if is_talking and current_dialogue_key:
        real_game.player.dx = 0
        real_game.player.dz = 0

        # Handle dialogue input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_dialogue_index += 1

        dialogue_lines = talking[current_dialogue_key]["lines"]
        #끝났을 때 if문
        if current_dialogue_index >= len(dialogue_lines): 
            current_dialogue_index = 0
            is_talking = False
            talking[current_dialogue_key]["completed"] = True

def draw_dialogue():
    import real_game
    if is_talking and current_dialogue_key:
        dialogue_box_rect = pygame.Rect(50, real_game.screen_height - 150, real_game.screen_width - 100, 100)
        pygame.draw.rect(real_game.screen, DIALOGUE_BOX_COLOR, dialogue_box_rect)

        # 
        dialogue_lines = talking[current_dialogue_key]["lines"]
        if current_dialogue_index < len(dialogue_lines):
            text_surface = font.render(dialogue_lines[current_dialogue_index], True, WHITE)
            text_rect = text_surface.get_rect(center=dialogue_box_rect.center)
            real_game.screen.blit(text_surface, text_rect)