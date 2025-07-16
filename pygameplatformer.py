import pygame
import random

pygame.init()
screen =pygame.display.set_mode((1290, 728))
clock = pygame.time.Clock()
running = True

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
PLAYER_SPEED = 400
vertical_velocity = 0
JUMP_VELOCITY = -30
GRAVITY = 1

PLAYER_RADIUS = 40
PLATFORM_HEIGHT = 50
PLATFORM_DELTA = 300

vert_offset = 0
SCROLL_BOUNDARY = 300

can_dash = True
DASH_DIST = 400


blocks = []
def add_block():
    global blocks
    width = random.randint(50,300)
    blocks.append((width,random.randint(0,screen.get_width()-width)))
def detect_collision(rect,pos):
    global vertical_velocity,can_jump,can_dash
    top = (pos.y+PLAYER_RADIUS)-rect.top
    bottom = (rect.top+rect.height)-(pos.y-PLAYER_RADIUS)
    left = (pos.x+PLAYER_RADIUS)-rect.left
    right = (rect.left+rect.width)-(pos.x-PLAYER_RADIUS)
    if top>0 and bottom>0 and right>0 and left>0:
        if top<bottom and top<right and top<left: # top collision
            pos.y -= top
            can_jump = True
            can_dash = True
            vertical_velocity = 0
        elif bottom<right and bottom<left: # bottom collision
            pos.y+=bottom
            vertical_velocity = 0
        elif left<right:          # left collision
            pos.x -= left
        else:   # right collision
            pos.x += right 
        return True
    return False

for i in range(100):
    add_block()

font = pygame.font.SysFont("Arial",40)
last_floor_touched = -1
while running:
    dt = clock.tick(60)/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("purple")

    
    color = "grey"
    if can_dash:
        color = "red"
    pygame.draw.circle(screen, color, player_pos, PLAYER_RADIUS)

    for i in range(len(blocks)):
        block = blocks[i]
        pos = block[1]
        width = block[0]
        height = screen.get_height()-((i+1)*PLATFORM_DELTA)+vert_offset
        rect = pygame.Rect(pos,height,width,PLATFORM_HEIGHT)
        color = "blue"
        if detect_collision(rect,player_pos):
            last_floor_touched = i
        # if detect_collision(rect,player_pos):
        #     color = "green"
        pygame.draw.rect(screen,color,rect)
        



    keys = pygame.key.get_pressed()
    if (keys[pygame.K_w] or keys[pygame.K_SPACE]) and can_jump:
        vertical_velocity = JUMP_VELOCITY
        can_jump = False
    if keys[pygame.K_a]:
        if keys[pygame.K_LSHIFT] and can_dash:
            player_pos.x -= DASH_DIST
            can_dash = False
        player_pos.x -= PLAYER_SPEED * dt
    if keys[pygame.K_d]:
        if keys[pygame.K_LSHIFT] and can_dash:
            player_pos.x += DASH_DIST
            can_dash = False
        player_pos.x += PLAYER_SPEED * dt

    player_pos.y += vertical_velocity
    vertical_velocity += GRAVITY

    if (player_pos.y > screen.get_height() - SCROLL_BOUNDARY) and vert_offset>0:
        vert_offset -= (player_pos.y-(screen.get_height()-SCROLL_BOUNDARY))
        player_pos.y = screen.get_height()-SCROLL_BOUNDARY
    
    if (player_pos.y<SCROLL_BOUNDARY):
        vert_offset += SCROLL_BOUNDARY-player_pos.y
        player_pos.y = SCROLL_BOUNDARY

    if player_pos.y > screen.get_height()-PLAYER_RADIUS:
        player_pos.y = screen.get_height()-PLAYER_RADIUS
        vertical_velocity = 0
        can_jump = True
        can_dash = True
        last_floor_touched = -1
    if player_pos.x > screen.get_width()+PLAYER_RADIUS:
        player_pos.x -= screen.get_width()+PLAYER_RADIUS*2
    if player_pos.x < -PLAYER_RADIUS:
        player_pos.x += screen.get_width()+PLAYER_RADIUS*2


    screen.blit(font.render("Block "+str(last_floor_touched +1),True,"white","purple"),(0,0))
    pygame.display.flip()
    

pygame.quit()