from copy import copy
from random import choice, uniform
import sys
import pygame


def genparticle(x: float):
    return {
        'xvelocity': x,
        'yvelocity': uniform(5, 10)*choice([-1, 1]),
        'xacceleration': 0,
        'yacceleration': 0,
        'bounciness': 1,
        'pos': [0, (uniform(0, display[1])-(display[1]/2))/metersPerPixel],
        'radius': 15
    }


pygame.init()
terminalvelocity = float('inf')

defaultdisplay = (800, 600)
clock = pygame.time.Clock()
fps = 60
screen = pygame.display.set_mode(defaultdisplay)
display = defaultdisplay
metersPerPixel = 50
particleinit = genparticle(choice([-5, 5]))

particle = copy(particleinit)

player1 = 0
player1velocity = 0
player2 = 0
player2velocity = 0
player1score = 0
player2score = 0

player1Win = None


while True:
    screen.fill((0, 0, 0))
    if player1Win == None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player1velocity += 25
        if keys[pygame.K_s]:
            player1velocity -= 25
        if keys[pygame.K_UP]:
            player2velocity += 25
        if keys[pygame.K_DOWN]:
            player2velocity -= 25
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        UY = particle['yvelocity']
        T = (1/fps)

        particle['yvelocity'] = UY + particle['yacceleration'] * T
        particle['yvelocity'] = max(
            min(particle['yvelocity'], terminalvelocity), -terminalvelocity)
        particle['pos'][1] += UY * T + 0.5*particle['yacceleration']*T**2
        if particle['pos'][1]*metersPerPixel-particle['radius'] < -display[1]/2:
            particle['yvelocity'] = (
                abs(particle['yvelocity']))*particle['bounciness']
        elif particle['pos'][1]*metersPerPixel+particle['radius'] > display[1]/2:
            particle['yvelocity'] = (-abs(particle['yvelocity'])
                                     )*particle['bounciness']

        UX = particle['xvelocity']
        particle['xvelocity'] = UX + particle['xacceleration'] * T
        particle['xvelocity'] = max(
            min(particle['xvelocity'], terminalvelocity), -terminalvelocity)
        particle['pos'][0] += UX * T + 0.5 * particle['xacceleration']*T**2
        if particle['pos'][0]*metersPerPixel-particle['radius'] < -display[0]/2 + 10:
            particle['xvelocity'] = (
                abs(particle['xvelocity']))*particle['bounciness']
            particlepos = (particle['pos'][1]*metersPerPixel) + display[1]/2
            if not ((player2+display[1]/2)+50 >=
                    particlepos and (player2+display[1]/2)-50 <= particlepos):
                player1score += 1
                particle = genparticle(5)
                player1 = 0
                player1velocity = 0
                player2 = 0
                player2velocity = 0
        elif particle['pos'][0]*metersPerPixel+particle['radius'] > display[0]/2 - 10:
            particle['xvelocity'] = (-abs(particle['xvelocity'])
                                     )*particle['bounciness']
            particlepos = (particle['pos'][1]*metersPerPixel) + display[1]/2
            if not ((player1+display[1]/2)+50 >=
                    particlepos and (player1+display[1]/2)-50 <= particlepos):
                player2score += 1
                particle = genparticle(-5)
                player1 = 0
                player1velocity = 0
                player2 = 0
                player2velocity = 0

        UP1 = player1velocity
        AP1 = -player1velocity
        player1velocity = UP1 + AP1 * T
        player1velocity = max(
            min(player1velocity, terminalvelocity), -terminalvelocity)
        player1 += UP1 * T + 0.5 * AP1*T**2

        if player1+150 >= display[0]/2:
            player1 = display[0]/2 - 150
            player1velocity = 0
        elif player1-150 <= -display[0]/2:
            player1 = -display[0]/2 + 150
            player1velocity = 0

        UP2 = player2velocity
        AP2 = -player2velocity
        player2velocity = UP2 + AP2 * T
        player2velocity = max(
            min(player2velocity, terminalvelocity), -terminalvelocity)
        player2 += UP2 * T + 0.5 * AP2*T**2

        if player2+150 >= display[0]/2:
            player2 = display[0]/2 - 150
            player2velocity = 0
        elif player2-150 <= -display[0]/2:
            player2 = -display[0]/2 + 150
            player2velocity = 0

        pygame.draw.circle(
            screen, (255, 255, 255), (display[0]/2-particle['pos'][0]*metersPerPixel, display[1]/2-particle['pos'][1]*metersPerPixel), particle['radius'], 0)
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(
            0, (display[1]-100)/2-player1, 10, 100))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(
            display[0]-10, (display[1]-100)/2-player2, 10, 100))
        pygame.draw.line(screen, (255, 255, 255),
                         (display[0]/2, 0), (display[0]/2, display[1]), 1)
        font = pygame.font.SysFont(None, 100)
        img = font.render(str(player1score), True, (255, 255, 255))
        screen.blit(img, (75, 20))
        img = font.render(str(player2score), True, (255, 255, 255))
        screen.blit(img, (display[0]-(50*(len(str(player2score))+1)), 20))

    clock.tick(fps)
    pygame.display.update()
