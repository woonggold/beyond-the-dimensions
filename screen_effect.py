import pygame

def screen_effect(effect):
    if effect == "normal":
        pass 
    if effect == "rotate": 
        screen_surface = pygame.display.get_surface()
        screen_copy = screen_surface.copy()  # 원본을 복사해 둡니다.

        # 회전 적용하기
        rotated_surface = pygame.transform.rotate(screen_copy, 180)

        # 화면을 채우고 변형된 Surface 그리기
        screen_surface.fill((0, 0, 0))  # 기존 화면 지우기
        screen_surface.blit(rotated_surface, (0, 0))  # 변형된 화면 그리기