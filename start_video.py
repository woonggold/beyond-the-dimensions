import pygame
from pygame.locals import *
from settings import *
from moviepy.editor import *
import map_loading

clip = VideoFileClip(f"{script_dir}//videos//start_video.mp4")

def run():
    for frame in clip.iter_frames(fps=24, dtype="uint8"):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 창 닫기 이벤트
                return "quit"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "quit"
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        frame_surface = pygame.transform.scale(frame_surface, (screen_width, screen_height))
        screen.blit(frame_surface, (0, 0))
        pygame.display.update()
        clock.tick(24)
    map_loading.map_load("stage1")
    return "real_game"