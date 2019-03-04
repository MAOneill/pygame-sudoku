import pygame
from upside_down_arrow_strings import upside_down_arrow_strings
from pencil_strings import pencil_strings

def main_menu():
    
    width = 400
    height = 400

    #set some colores
    background_color = (159,209,204)   #blue
    pitch_blue_color = (83,94,126)

    main_answer = False

    pygame.init()       #should this be in each module??
    font = pygame.font.Font('fonts/cmtt10.ttf', 22)    #must be after init   

    # pygame.mouse.set_cursor(compile(thickarrow_strings, black='X', white='.', xor='o'))
    # datatuple, masktuple = pygame.cursors.compile( upside_down_arrow_strings,
    #                               black='X', white='.', xor='o' )
    # pygame.mouse.set_cursor( (24,24), (0,0), datatuple, masktuple )

    datatuple, masktuple = pygame.cursors.compile( pencil_strings,
                                  black='.', white='X', xor='o' )
    pygame.mouse.set_cursor( (24,24), (0,0), datatuple, masktuple )

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Soduko - Choose game play mode')
    clock = pygame.time.Clock()

    while not main_answer:
        
        for event in pygame.event.get():
            # Event handling
            if event.type == pygame.QUIT:
                main_answer = True


        screen.fill(background_color)

        window_text = font.render('Enter A or B', True, (pitch_blue_color))
        
        screen.blit(window_text, (100,100))

        pygame.display.update()     #internal function

        clock.tick(60)  #600 makes the fan go crazy


    pygame.quit()   #change to return  #quit when you are out of while loop


if __name__ == '__main__':
    # main()
    main_menu()
