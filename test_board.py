import pygame

#copied ball1.py from examples to begin
#copied draw_image from examples too

def main():
    # declare the size of the canvas
    width = 780
    height = 780
    blue_color = (97, 159, 182)

    pygame.init()
    screen = pygame.display.set_mode((width, height))

    pygame.display.set_caption('Can I display my image?')
    clock = pygame.time.Clock()

    # Game initialization
    hero_image = pygame.image.load('numbers/1_background_transparent.png').convert_alpha()
    pencil_image = pygame.image.load('numbers/2_pencil.png').convert_alpha()
    stop_game = False

    while not stop_game:
        for event in pygame.event.get():
            # Event handling
            if event.type == pygame.QUIT:
                stop_game = True

        # Game logic

        # Draw background
        screen.fill(blue_color)

        # Game display

        screen.blit(hero_image, (250, 250))
        screen.blit(pencil_image, (600,600))

        pygame.display.update()

        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
