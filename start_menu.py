import pygame
from pygame.locals import *
from settings import *
import button
from moviepy.editor import *
import os
import time

clip = VideoFileClip(f"{script_dir}//videos//beyond_the_dimension.mp4")
pygame.mixer.init()
pygame.mixer.music.load(f"{script_dir}//music//noise_short.wav")
pygame.mixer.music.play()
start_button = button.button(screen_width/2-181,600,"시작1.png","시작2.png")

def run():
    pygame.display.set_caption('Beyond the Dimensions')
    for frame in clip.iter_frames(fps=24, dtype="uint8"):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return "quit"
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            if esc_timer == 0:
                esc_start = time.time()
            esc_timer = time.time() - esc_start + 0.01
            if esc_timer >= 1:
                pygame.mixer.music.stop()
                return "quit"
        else:
            esc_timer = 0
            
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        frame_surface = pygame.transform.scale(frame_surface, (screen_width, screen_height))
        screen.blit(frame_surface, (0, 0))
        
        if start_button.button_work() == True:
            pygame.mouse.set_visible(False)
            pygame.event.set_grab(True)
            pygame.mouse.get_rel()
            pygame.mixer.music.stop()
            return "start_video"
        pygame.display.flip()
    pygame.mixer.music.stop()
    return "start_menu"

