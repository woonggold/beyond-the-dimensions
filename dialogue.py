import pygame
from map_loading import *
import time

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100,100,255)
DIALOGUE_BOX_COLOR = (50, 50, 50)

target_bar_height = 50
animation_speed = target_bar_height / (0.5 * 12) 
inform_space = False
inform_R = False
top_bar_height = 0
bottom_bar_height = 0
last_dialogue_key = None
start_time = None

fadestart = None
fade_duration = 3 #페이드 초를 이걸로 바꾸기

# Font
font = pygame.font.Font('fonts/BMDOHYEON_otf.otf', 36)
blue_font = pygame.font.Font('fonts/BMEULJIRO.otf', 36)
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
        "position": (50, 150, 50, 150),
        "stage": "stage1"
    },
    "1-2": {
        "lines": [
            "(왜 이런 곳에 낭떠러지가 있는거지..?)", 
            "일단 넘어가보자"
        ],
        "position": (-350, -250, 50, 150),
        "stage": "stage1"
    },
    "1-3": {
        "lines": ["그래서 여기가 어디인거지.."],
        "position": (-4100, -4000, 50, 150),
        "stage": "stage1"
    },
    "1-4": {
        "lines": ["어", "저 블록은 뭐지"],
        "position": (-6800, -6700, 50, 150),
        "stage": "stage1"
    },
    "2-1": {
        "lines": [
            "뭐야?", "세상이 왜 이러지..!?", "[blue]ㅏㅏㅏ.. ", "[blue]들리니?", "어… 누가 말하는 거야?",
            "내가 왜 이런 곳에 있는 건데..!?", "[blue]안녕,", "[blue]난 너를 만든 과학자고",
            "[blue]다른 차원에서 너를 바라보고 있어.", "[blue]너를 만들어내면서 차원간의 균열이 일어났는데,",
            "[blue]방금 너가 그 균열을 지나온 거야.", "[blue]그니까 지금 더 높은 차원으로 넘어왔다고 생각하면 돼.",
            "[blue]그러니까…한마디로...", "[blue]너는 앞에 있는 벽을 지나갈 수 있을 거야.",
            "왜 딴소리야.. 내 목소리가 안 들리는 건가..?", "그나저나 내가 이 벽을 지나갈 수 있다고?",
            "막혀있는데..?", "...?"
        ],
        "position": (650, 750, 50, 150),
        "stage": "stage2"
    },
    "2-2": {
        "lines": ["이게 되네.."],
        "position": (-1450, -1350, -50, 250),
        "stage": "stage2"
    },
    "2-3": {
        "lines": ["일단.. 들어가 봐야겠지..?"],
        "position": (-2950, -2750, 50, 150),
        "stage": "stage2"
    },
    "2-4": {
        "lines": ["민준아 우흥~~~"],
        "position": (-950, -850, -50, 50),
        "stage": "stage2"
    },
    "3-1": {
        "lines": [
            "[blue]으아아악!", "무슨 일이야??", "[blue]으….", "[blue]지금 우리 차원에서도 균열이 발생하고 있어..",
            "[blue]당분간은 대화하기 힘들 것 같아….", "뭐..?", "여보세요….?", "…", 
            "..일단 할 수 있는 걸 하자"
        ],
        "position": (-2650, -2500, 50, 150),
        "stage": "stage3"
    },
    "4-1": {
        "lines": [
            "흠…. 뭔가 이상한 느낌이 드는데…", 
            "차원 균열이 점점 커지는 것 같기도 하고"
        ],
        "position": (-2200, -2100, 50, 150),
        "stage": "stage4"
    },
    "4-2": {
        "lines": ["어어…", "세상이..?"],
        "position": (-2700, -2600, -2100, -1900),
        "stage": "stage4"
    },
    "4-3": {
        "lines": [
            "어어...",
            "잠깐만… 왜 내가 천장에 있지…?", 
            "..아", 
            "내가 천장에 있는게 아니라", 
            "세상이 뒤바뀐거구나..", 
            "..젠장"
        ],
        "position": (-50, 50, -50, 50),
        "stage": "stage4"
    },
    "5-1": {
        "lines": [
                "[blue]ㅏㅏ", 
                "[blue]차원 붕괴 때문에 차원 간의 경계가 점점 줄어들고 있어..!!",
                "[blue]이러다간… 어떻게 될지…",
                "[blue]일단 아마 차원 이동이 더 쉬워졌을 거야..!"],
        "position": (750, 850, 50, 150),
        "stage": "stage5"
    },
    "6-1": {
        "lines": [
                "(사실 2D로도 지나갈 수 있게 보인다...)"],
        "position": (550, 650, -50, 50),
        "stage": "stage6"
    },
    "6-2": {
        "lines": [
                "[blue]파란색 블록을 밟으면 우리가 넘어가도록 블록을 생성시킬 수 있어",
                "좋아 저 위에 있는 파란 블록을 밟아야겠군"],
        "position": (550, 650, 50, 150),
        "stage": "stage6"
    }
}


def check_player_position():
    import real_game, map_loading
    global is_talking, current_dialogue_key, stagename

    is_talking = False
    for key, dialogue in talking.items():
        x_min, x_max, z_min, z_max = dialogue["position"]
        if x_min < real_game.player.x < x_max and z_min < real_game.player.z < z_max and dialogue["stage"] == map_loading.stagename:
            if dialogue.get("completed", False) is not True:  #이미 실행된 대본은 안나오게 하기
                is_talking = True
                current_dialogue_key = key
                return
            
def talkcheck():
    import real_game
    global current_dialogue_index, is_talking, current_dialogue_key, blue_font, inform_space, inform_R
    
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

        # 대화가 끝났을 때 조건문 추가
        if current_dialogue_index >= len(dialogue_lines): 
            if current_dialogue_key == "1-2": 
                inform_space = True
            elif current_dialogue_key == "5-1": 
                inform_R = True
            current_dialogue_index = 0
            is_talking = False
            talking[current_dialogue_key]["completed"] = True

def draw_dialogue():
    global top_bar_height, bottom_bar_height, last_dialogue_key, start_time, fadestart, inform_space, inform_R
    
    import real_game
    
    if is_talking and current_dialogue_key:
        if current_dialogue_key != last_dialogue_key:
            top_bar_height = 0
            bottom_bar_height = 0
            start_time = time.time()
            last_dialogue_key = current_dialogue_key

        if top_bar_height < target_bar_height:
            top_bar_height += animation_speed
        if bottom_bar_height < target_bar_height:
            bottom_bar_height += animation_speed

        #하이값 조절
        top_bar_height = min(top_bar_height, target_bar_height)
        bottom_bar_height = min(bottom_bar_height, target_bar_height)

        #블랙 바 생성 코드
        top_bar = pygame.Rect(0, 0, real_game.screen_width, int(top_bar_height))
        bottom_bar = pygame.Rect(0, real_game.screen_height - int(bottom_bar_height), real_game.screen_width, int(bottom_bar_height))
        pygame.draw.rect(real_game.screen, (0, 0, 0), top_bar)
        pygame.draw.rect(real_game.screen, (0, 0, 0), bottom_bar)

        # Adjust the dialogue box position based on bar heights
        dialogue_box_rect = pygame.Rect(
            50, real_game.screen_height - bottom_bar_height - 150, real_game.screen_width - 100, 100
        )
        pygame.draw.rect(real_game.screen, DIALOGUE_BOX_COLOR, dialogue_box_rect)

        #대사 가져오고 dialogue_lines에 저장
        dialogue_lines = talking[current_dialogue_key]["lines"]
        if current_dialogue_index < len(dialogue_lines):
            line = dialogue_lines[current_dialogue_index]

            #블루 태그 확인
            parts = line.split("[blue]")
            rendered_parts = []  # List to hold each rendered part

            for i, part in enumerate(parts):
                if i % 2 == 1:  
                    text_surface = blue_font.render(part, True, BLUE)
                else: 
                    text_surface = font.render(part, True, WHITE)
                
                rendered_parts.append(text_surface)

            # Calculate total width to center the entire line
            total_width = sum(part.get_width() for part in rendered_parts) + (len(rendered_parts) - 1) * 10  # Adding padding between parts
            x_offset = (real_game.screen_width - total_width) // 2  # Center line horizontally
            y_offset = dialogue_box_rect.centery - (rendered_parts[0].get_height() // 2)  # Center line vertically

            # Blit each part centered within the box
            for part in rendered_parts:
                text_rect = part.get_rect(topleft=(x_offset, y_offset))
                real_game.screen.blit(part, text_rect)
                x_offset += part.get_width() + 10
    if inform_space or inform_R:
        if fadestart is None:
            fadestart = time.time()  # 시작 시간 기록
        
        elapsed_time = time.time() - fadestart  # 경과 시간 계산
        alpha = max(0, 255 - int((elapsed_time / fade_duration) * 255))  # 알파 값 계산 (0 ~ 255)
        
        if alpha == 0:
            # 페이드아웃 완료 후 초기화
            fadestart = None
            inform_space = False
            inform_R = False
            return

        if inform_space:
            instruction_text = font.render("SPACE로 점프", True, (0, 0, 0))
        elif inform_R:
            instruction_text = font.render("R로 차원변환", True, (0, 0, 0))
        instruction_text.set_alpha(alpha)  # 알파 값 설정
        text_rect = instruction_text.get_rect(center=(real_game.screen_width // 2, real_game.screen_height - 50))

        # 텍스트 블리트 (화면에 그리기)
        real_game.screen.blit(instruction_text, text_rect)
