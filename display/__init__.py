import pygame
import textwrap

def init():
    global screen
    global myfont
    global terminalfont
    pygame.init()
    info_object = pygame.display.Info()
    screen_width = info_object.current_w
    screen_height = info_object.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("I am Gizmo!")
    myfont = pygame.font.SysFont("monospace", min(screen_width, screen_height) // 4)
    terminalfont = pygame.font.SysFont("monospace", min(screen_width, screen_height) // 16)
    

def update_eyes(eyes_state):
    global screen
    global myfont

    screen.fill((0, 0, 0))  # Fill the screen with black color

    total_text_height = len(eyes_state) * myfont.get_height()
    y_offset = (screen.get_height() - total_text_height) // 2  # Center vertically

    for i, line_str in enumerate(eyes_state):
        line = myfont.render(line_str, True, (255, 255, 0))
        line_rect = line.get_rect(center=(screen.get_width() // 2, y_offset + i * myfont.get_height()))
        screen.blit(line, line_rect)

def update_terminal_line(terminal_line):
    global screen
    global terminalfont

    wrapper = textwrap.TextWrapper(width=int(screen.get_width()/terminalfont.size(' ')[0]))
    wrapped_lines = wrapper.wrap(terminal_line)

    for i, line in enumerate(wrapped_lines):
        terminal_line_rendered = terminalfont.render(line, True, (255, 255, 0))
        terminal_line_rect = terminal_line_rendered.get_rect(center=(screen.get_width() // 2, screen.get_height() - terminalfont.get_height() * (len(wrapped_lines) - i)))
        screen.blit(terminal_line_rendered, terminal_line_rect)