import pygame, time, piece, math, settings, dead
def screen_effect(effect):
    if effect == "normal":
        pass 
    if effect == "rotate": 
        screen_surface = pygame.display.get_surface()
        screen_copy = screen_surface.copy()  # 원본을 복사해 둡니다.

        # 회전 적용하기
        rotated_surface = pygame.transform.rotate(screen_copy, 180)

        # 화면을 채우고 변형된 Surface 그리기
        screen_surface.fill(dead.back_color)  # 기존 화면 지우기
        screen_surface.blit(rotated_surface, (0, 0))  # 변형된 화면 그리기
    if effect == "rotater": 
        screen_surface = pygame.display.get_surface()
        screen_copy = screen_surface.copy()  # 원본을 복사해 둡니다.

        # 회전 적용하기
        rotated_surface = pygame.transform.rotate(screen_copy, 90)

        # 화면을 채우고 변형된 Surface 그리기
        screen_surface.fill(dead.back_color)  # 기존 화면 지우기
        screen_surface.blit(rotated_surface, (200,-200))  # 변형된 화면 그리기
    if effect == "rotatel": 
        screen_surface = pygame.display.get_surface()
        screen_copy = screen_surface.copy()  # 원본을 복사해 둡니다.

        # 회전 적용하기
        rotated_surface = pygame.transform.rotate(screen_copy, 270)

        # 화면을 채우고 변형된 Surface 그리기
        screen_surface.fill(dead.back_color)  # 기존 화면 지우기
        screen_surface.blit(rotated_surface, (200,-200))  # 변형된 화면 그리기
    if effect == "rotating": 
        screen_surface = pygame.display.get_surface()
        screen_copy = screen_surface.copy().convert_alpha()  # 원본을 복사해 둡니다.

        # 회전 적용하기
        rotated_surface = pygame.transform.rotate(screen_copy, (((time.time()-piece.rotate_start)%360))*100).convert_alpha()
        surface_rect = rotated_surface.get_rect(center=(settings.screen_width / 2, settings.screen_height / 2))
        # 화면을 채우고 변형된 Surface 그리기
        screen_surface.fill(dead.back_color)  # 기존 화면 지우기
        screen_surface.blit(rotated_surface, surface_rect.topleft)  # 중심에 맞춰서 그리기