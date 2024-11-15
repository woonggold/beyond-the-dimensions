import pygame
from pygame.locals import *
from settings import *
from moviepy.editor import *
import map_loading

clip = VideoFileClip(f"{script_dir}//videos//start_video.mp4")


def run():
    pygame.mixer.music.load(f"{script_dir}//music//noise.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    for frame in clip.iter_frames(fps=24, dtype="uint8"):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return "quit"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                return "quit"
                
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        proportion = screen_width / frame_surface.get_rect().width
        modified_height = frame_surface.get_rect().height * screen_width / frame_surface.get_rect().width
        margin = (screen_height - modified_height) / 2
        frame_surface = pygame.transform.scale(frame_surface, (screen_width, int(modified_height)))
        screen.fill((0, 0, 0))
        screen.blit(frame_surface, (0, margin))
        pygame.display.update()
        clock.tick(24)
        
    pygame.mixer.music.stop()
    map_loading.map_load("stage1")
    return "real_game"