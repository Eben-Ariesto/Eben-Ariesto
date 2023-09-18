import pygame
import os
import matrix
import math
import colorsys

#--- enjoy the spaghetti code ------

os.environ["SDL_VIDEO_CENTERED"]='1'
width, height = 1920, 1080
size = (width, height)
white, black = (200, 200, 200), (0, 0, 0)
pygame.init()
pygame.display.set_caption("Lorenz Attractor")
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60

a = 0.95
b = 0.7
c = 0.6
d = 3.5
e = 0.25
f = 0.1
x, y, z = 0.1, 0.1, 0.1
dx, dy, dz = 0, 0, 0
points = []
colors = []
scale = 150
angle = 0
previous = None

def matrix_multiplication(a, b):
    columns_a = len(a[0])
    rows_a = len(a)
    columns_b = len(b[0])
    rows_b = len(b)

    result_matrix = [[j for j in range(columns_b)] for i in range(rows_a)]
    if columns_a == rows_b:
        for x in range(rows_a):
            for y in range(columns_b):
                sum = 0
                for k in range(columns_a):
                    sum += a[x][k] * b[k][y]
                result_matrix[x][y] = sum
        return result_matrix
    else:
        print("error! the columns of the first matrix must be equal with the rows of the second matrix")
        return None

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))
can_draw = False
run = True
while run:
    screen.fill(black)
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    rotation_x = [[1, 0, 0],
                  [0, math.cos(angle), -math.sin(angle)],
                  [0, math.sin(angle), math.cos(angle)]]

    rotation_y = [[math.cos(angle), 0, -math.sin(angle)],
                  [0, 1, 0],
                  [math.sin(angle), 0, math.cos(angle)]]

    rotation_z =[[math.cos(angle), -math.sin(angle), 0],
                 [math.sin(angle), math.cos(angle), 0 ],
                  [0, 0, 1]]
    
    rotation_xy = matrix_multiplication(rotation_x, rotation_y)
    rotation_all = matrix_multiplication(rotation_xy, rotation_z)
    
    time = 0.01
    dx = ((z - b) * x - d * y) * time
    dy = (d * x + (z - b) * y) * time
    dz = (c + a * z - ((z**3)/3) - (x*x + y*y)*(1+e*z) + f*z*(x**3)) * time

    x = x + dx
    y = y + dy
    z = z + dz
    hue = 0

    point = [[x], [y], [z]]
    points.append(point)
    for p in range(len(points)):

        rotated_2d = matrix_multiplication(rotation_all, points[p])
        distance = 5

        val = 1/(distance - rotated_2d[2][0])#z value
        projection_matrix = [[1, 0, 0],
                             [0, 1, 0]]

        projected2d = matrix_multiplication(projection_matrix, rotated_2d)
        x_pos = int(projected2d[0][0] * scale) + width//2 + 100
        y_pos = int(projected2d[1][0] * scale) + height//2
        if hue > 1:
            hue = 0
        #pygame.draw.circle(screen, (hsv2rgb(hue, 1, 1)) , (x_pos, y_pos), 3)
        if previous is not None:
            if hue > 0.:
                pygame.draw.line(screen, (hsv2rgb(hue, 1, 1)), (x_pos, y_pos), previous, 1 )


        previous = (x_pos, y_pos)
        hue += 0.01


    angle += 0.001

    pygame.display.update()
pygame.quit()