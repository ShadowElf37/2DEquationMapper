import pygame
from math import *

def clamp(x, mn=0, mx=255):
    if x < mn: x = mn
    elif x > mx: x = mx
    return x

def load_data():
    global equation, size, screensize, inputs, screen, vscreensize
    data = open('equation', 'r').read().split('\n')
    size = int(data[0])
    screensize = vscreensize = int(data[1])
    equation = data[2].replace('^', '**')

    inputs = []
    i = -1
    for j in range(-size // 2, size // 2 + 1):
        i += 1
        inputs.append([])
        for k in range(-size // 2, size // 2 + 1):
            x = j + k * 1j
            inputs[i].append(x)

    screen = pygame.display.set_mode((screensize, screensize))

load_data()

def pixel(surface, color, pos):
    surface.fill(color, (pos, (1, 1)))

def calc():
    global outputs, inputs
    outputs = {}
    for row in inputs:
        for x in row:
            r = eval(equation)
            r = round(r.real)%(screensize) + round(r.imag)%(screensize)*1j
            if outputs.get(r) is None:
                outputs[r] = 1
            else:
                outputs[r] += 1

def draw():
    screen.fill((0, 0, 0))
    for k in outputs.keys():
        # Color calculation
        c = round(outputs[k]**2*10 % 255)
        b = clamp(abs(c-255//3), mx=255//3)*3
        g = clamp(abs(c-255*2//3)-b, mx=255//3)*3
        r = clamp(abs(c-255)-g-b, mx=255//3)*3
        #print(r,g,b)
        cl = pygame.Color(r, g, b, 255)

        s = screensize/2
        pixel(screen, cl, (round((k.real-s)*scale+s), round((k.imag-s)*scale+s)))

pygame.init()

screen = pygame.display.set_mode((screensize, screensize))
clock = pygame.time.Clock()
done = False
scale = 1

calc()
draw()

print('Entering loop...')
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                screen.fill((0, 0, 0))
                pygame.display.flip()
                load_data()
                print('Inputs reloaded.')
                calc()
                print('Output recalculated.')
                scale = 1
                draw()
            elif event.key == pygame.K_UP:
                print('Scale up.')
                scale *= 1.1
                draw()
            elif event.key == pygame.K_DOWN:
                print('Scale down.')
                scale *= 0.9
                draw()
        clock.tick(10)
    pygame.display.flip()
