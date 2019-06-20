import pygame
import rockpaper.startscene
import rockpaper.mainscene

def main():
    pygame.init()
    pygame.display.set_caption("Super Rock Paper Scissors")

    surface = pygame.display.set_mode((800,600))

    pygame.key.set_repeat(1, 25)
    clock = pygame.time.Clock()

    running = True

    start = rockpaper.startscene.StartScene()
    smain  = rockpaper.mainscene.MainScene()
    scenes = {
        start.name: start,
        smain.name: smain
    }
    current_scene = start

    while running:
        # limit 30fps
        clock.tick(30)

        if current_scene is not None:
            current_scene.run(pygame.event.get())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == rockpaper.SCENE_CHANGE:
                try:
                    next_scene = scenes[event.newscene]
                    current_scene = next_scene
                    print("Changed to scene: {}".format(event.newscene))
                except KeyError:
                    print("ERROR: {} scene not found!".format(event.newscene))
                    current_scene = None

##################### :)
main()
