import pygame
def init(chars,lines):
    global screen
    global myfont
    pygame.init()
    size = [24*chars,40*lines]
    screen= pygame.display.set_mode(size)
    pygame.display.set_caption("I am Gizmo!")
    myfont = pygame.font.SysFont("monospace", 40)

def draw(args):
    i=0;
    global screen
    global myfont
    screen.fill((0,0,0))#erase screen contents
    while(i < len(args)):
        line= myfont.render(args[i], 2, (255,255,0))
        screen.blit(line, (0, 20*i))
        i+=1
    pygame.display.flip()