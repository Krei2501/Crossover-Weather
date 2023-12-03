import pygame

import ValueManager

pygame.init()
font = pygame.font.Font(ValueManager.font, 50)

def report(info, x = 625, y = 325):
    screen = pygame.display.get_surface()
    report_surf = font.render(str(info), True, 'Red')
    report_rect = report_surf.get_rect(center = (x, y))
    screen.blit(report_surf, report_rect)
    