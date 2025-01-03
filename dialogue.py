import pygame
from map_loading import *
import time
import piece

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100,100,255)
DIALOGUE_BOX_COLOR = (50, 50, 50)
current_dialogue_key = None
target_bar_height = 50
animation_speed = target_bar_height / (0.5 * 12) 
inform_space = False
inform_R = False
inform_boss = False
top_bar_height = 0
bottom_bar_height = 0
last_dialogue_key = None
start_time = None
fade_opacity = None
fadestart = None
talkstart = None
fade_duration = 3 #페이드 초를 이걸로 바꾸기
text_duration = 0.025
text_ended = False
once = False
esc_timer = 0
esc_start = 0


# Font
font = pygame.font.Font('fonts/BMDOHYEON_otf.otf', 36)
smallfont = pygame.font.Font('fonts/BMDOHYEON_otf.otf', 12)
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
            "막혀있는데..?"
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
        "position": (1250, 1350, -2350, -2250),
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
                "[blue]일단 아마 차원 이동이 더 쉬워졌을 거야..!",
                "뭐..?", 
                "여보세요….?", 
                "…", 
                "..일단 할 수 있는 걸 하자"
            ],
        "position": (750, 850, 50, 150),
        "stage": "stage5"
    },
    "5-2": {
        "lines": [
                "(다른 길을 찾아봐야 할 것 같다)"],
        "position": (5000, 5050, 50, 250),
        "stage": "stage5"
    },
    "6-1": {
        "lines": [
                "(사실 2D로도 지나갈 수 있어 보인다...)"],
        "position": (550, 650, -50, 50),
        "stage": "stage6"
    },
    "6-2": {
        "lines": [
                "[blue]파란색 블록을 밟으면 우리가 넘어가도록 블록을 생성시킬 수 있어",
                "좋아 저 위에 있는 파란 블록을 밟아야겠군"],
        "position": (550, 650, 50, 150),
        "stage": "stage6"
    },
    "6-3": {
        "lines": [
                "차원 붕괴라기에 걱정했는데..",
                "생각보다 별일은 없네"],
        "position": (150, 250, 50, 150),
        "stage": "stage6"
    },
    "6-4": {
        "lines": [
                "어…",
                "어라...?",
                "[blue]뛰어!!!!"],
        "position": (-650, -550, 50, 150),
        "stage": "stage6"
    },
    "6-5": {
        "lines": [
                "헉…",
                "헉…",
                "죽는줄 알았네…",
                "이젠.. 끝난건가…?",
                "...",
                "잠깐… ",
                "좀 이상한데…?",
                "차원균열이 이렇게 컸었나…?"],
        "position": (-7550, -7350, 50, 150),
        "stage": "stage6"
    },
    "6-6": {
        "lines": [
                "어…",
                "어…!",
                "어...!?"],
        "position": (-7650, -7550, 50, 150),
        "stage": "stage6"
    },
    "7-1": {
        "lines": [
            "[blue]드디어..!!!", "[blue]우리가 차원 붕괴를 해결했어…!!!", "[blue]세계를 지켜낸 거라고!!",
            "드디어…..!!", "…", "그런데….", "나도 차원 붕괴의 산물…인 거 아니야..?", "차원 문제를 해결하면..", "……나는 어떻게 되는 거야..?"
        ],
        "position": (5000, 5000, 0, 0),
        "stage": "stage7"
    }
}

def check_player_position():
    import real_game, map_loading
    global is_talking, current_dialogue_key, stagename, piece, fade_opacity
    
    for key, dialogue in talking.items():
        x_min, x_max, z_min, z_max = dialogue["position"]
        
        if key == "7-1" and piece.core_hp >= 200:
            if dialogue.get("completed", False) is not True:  
                is_talking = True
                current_dialogue_key = key
                fade_opacity = 0
                return
        
        elif key == "5-2":
            if (x_min < real_game.player.x < x_max and
                z_min < real_game.player.z < z_max and
                dialogue["stage"] == map_loading.stagename and
                real_game.player.y == -1000):
                
                if dialogue.get("completed", False) is not True:
                    is_talking = True
                    current_dialogue_key = key
                    return

        elif key != "7-1":
            if (x_min < real_game.player.x < x_max and 
                z_min < real_game.player.z < z_max and 
                dialogue["stage"] == map_loading.stagename):
                
                if dialogue.get("completed", False) is not True:
                    is_talking = True
                    current_dialogue_key = key
                    return
            
def extend_check():
    import real_game
    import piece
    import projection_3D
    global extend_piece_pos, extend_modified_size, once
    if current_dialogue_key == "6-6" and once == False:
        once = True
        real_game.extend_piece = True
        for piece1 in piece.Pieces:
            if piece1.event == "stage7":
                extend_piece_pos = projection_3D.project_3d_or_2d((piece1.x, piece1.y, piece1.z), real_game.camera_pos, real_game.angle_x, real_game.angle_y)
                extend_modified_size = int(piece1.size * 200 * piece1.width / (piece1.range**(1/2)))
def talkcheck():
    extend_check()
    import real_game
    global current_dialogue_index, is_talking, current_dialogue_key, blue_font, inform_space, inform_R, inform_boss, talkstart, smallfont, text_ended, talkstart, esc_start, esc_timer
    
    if is_talking and current_dialogue_key:
        real_game.player.jump_pressed = False
        real_game.prevent2 = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if text_ended:
                        current_dialogue_index += 1
                        talkstart = None
                    else:
                        talkstart = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if text_ended:
                        current_dialogue_index += 1
                        talkstart = None
                    else:
                        talkstart = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            if esc_timer == 0:
                esc_start = time.time()
            esc_timer = time.time() - esc_start + 0.01
            if esc_timer >= 1:
                return True
        else:
            esc_timer = 0


        dialogue_lines = talking[current_dialogue_key]["lines"]

        # 대화가 끝났을 때 조건문 추가
        if current_dialogue_index >= len(dialogue_lines): 
            real_game.prevent2 = False
            if current_dialogue_key == "1-2": 
                inform_space = True
            elif current_dialogue_key == "5-1": 
                inform_R = True
            elif current_dialogue_key == "6-6": 
                settings.start_looping_bool = True
                import player
                map_load("stage7")
                player.player.y = 0
                player.player.x = 100
                player.player.z = 100
                inform_boss = True
            current_dialogue_index = 0
            is_talking = False
            talking[current_dialogue_key]["completed"] = True
    return False

def draw_dialogue():
    import map_loading, real_game
    global top_bar_height, bottom_bar_height, last_dialogue_key, start_time, fadestart, inform_space, inform_R, inform_boss, talkstart, text_ended, stagename
    
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
        pygame.draw.rect(real_game.screen, DIALOGUE_BOX_COLOR, dialogue_box_rect, 0, 10)

        #대사 가져오고 dialogue_lines에 저장
        dialogue_lines = talking[current_dialogue_key]["lines"]
        if current_dialogue_index < len(dialogue_lines):
            if talkstart is None:
                talkstart = time.time()
            
            elapsed_time = time.time() - talkstart
            index = max(0, int(elapsed_time / text_duration))
            line = dialogue_lines[current_dialogue_index]

            #블루 태그 확인
            text_ended = False
            parts = line.split("[blue]")
            max_index0 = len(list(parts[0]))
            parts[0] = "".join(list(parts[0])[:index])
            if len(parts) > 1:
                max_index1 = len(list(parts[1]))
                parts[1] = "".join(list(parts[1])[:index])
                if index >= max_index1:
                    text_ended = True
            else:
                if index >= max_index0:
                    text_ended = True
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
            if text_ended and current_dialogue_index == 0 and map_loading.stagename == "stage1":
                next = smallfont.render("ENTER로 대사 넘기기", True, (128, 128, 128))
                real_game.screen.blit(next, (60, real_game.screen_height - bottom_bar_height - 140))


    if inform_space or inform_R or inform_boss:
        if fadestart is None:
            fadestart = time.time()  # 시작 시간 기록
        
        elapsed_time = time.time() - fadestart  # 경과 시간 계산
        alpha = max(0, 255 - int((elapsed_time / fade_duration) * 255))  # 알파 값 계산 (0 ~ 255)
        
        if alpha == 0:
            # 페이드아웃 완료 후 초기화
            fadestart = None
            inform_space = False
            inform_R = False
            inform_boss = False
            return

        if inform_space:
            instruction_text = font.render("SPACE키를 눌러 점프", True, (0, 0, 0))
        elif inform_R:
            instruction_text = font.render("좌클릭으로 차원변환", True, (0, 0, 0))
        elif inform_boss:
            instruction_text = font.render("좌클릭으로 에너지 코어 충전", True, (0, 0, 0))
        instruction_text.set_alpha(alpha)  # 알파 값 설정
        text_rect = instruction_text.get_rect(center=(real_game.screen_width // 2, real_game.screen_height - 50))

        # 텍스트 블리트 (화면에 그리기)
        real_game.screen.blit(instruction_text, text_rect)
