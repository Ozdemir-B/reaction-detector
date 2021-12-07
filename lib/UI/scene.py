import pygame
from pygame import display


def say_hello(asd = "sayed hello"):
    print(asd)

def start():
    print("UI initializing...")

def play(video_url = ""):
    FPS = 60

    pygame.init()
    clock = pygame.time.Clock()
    movie = pygame.movie.Movie(video_url)
    screen = pygame.display.set_mode(movie.get_size())
    movie_screen = pygame.Surface(movie.get_size()).convert()

    movie.set_display(movie_screen)
    movie.play()


    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                movie.stop()
                playing = False

        screen.blit(movie_screen,(0,0))
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()