from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Global variables
player_pos = [0, 0, 0]
gun_angle = 0
camera_mode = "third"
camera_distance = 500
camera_height = 500
camera_angle = 0
cheat_mode = False
auto_camera = False
bullets = []
enemies = []
life = 5
missed_bullets = 0
score = 0
game_over = False
enemy_speed = 0.1
bullet_speed = 5
GRID_LENGTH = 600
step_toggle = False
# prothome enemy kivabe show hobe ta dekhte hobe
def initial_enemies():
    global enemies
    enemies = []
    for _ in range(5):
        enemies.append({
            'pos': [random.randint(-400, 400), 0, random.randint(-400, 400)],
            'scale': 1.0, 
            'scale_dir': 0.01 
        })
 
initial_enemies() 

def draw_text(x, y, text):
    glColor3f(1, 1, 1)
    glWindowPos2f(x, y)
    for character in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(character))
#player er drawing shuru 
def draw_player():
    global step_toggle
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    
    glPushMatrix()
    glRotatef(gun_angle, 0, 1, 0)

    # body
    glPushMatrix()
    glTranslatef(0, 30, 0)
    glColor3f(0, 0.3, 0)
    glScalef(30, 20, 15)
    glutSolidCube(1)
    glPopMatrix()

    # Head
    glPushMatrix()
    glTranslatef(0, 55, 0)
    glColor3f(0, 0, 0)
    glutSolidSphere(12, 20, 20)
    glPopMatrix()

    # Arms & Gun
    glPushMatrix()
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * 10, 40, 5)
        glColor3f(0.9, 0.75, 0.65)
        glutSolidSphere(4, 10, 10)
        gluCylinder(gluNewQuadric(), 3, 3, 35, 10, 10)
        glPopMatrix()
    
    # Gun
    glPushMatrix()
    glTranslatef(0, 40, 20)
    glColor3f(0.5, 0.5, 0.5)
    gluCylinder(gluNewQuadric(), 2.5, 2.5, 40, 10, 10)
    glPopMatrix()
    glPopMatrix()

    # Legs
    leg_tilt_angle = 15
    leg_length = 20 / math.cos(math.radians(leg_tilt_angle))
    leg_positions = [(-10, 20, 0), (10, 20, 0)]
    glColor3f(0, 0, 0.5)
    for i, pos in enumerate(leg_positions):
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        tilt_dir = leg_tilt_angle if (i == 0 and step_toggle) or (i == 1 and not step_toggle) else -leg_tilt_angle
        glRotatef(90 + tilt_dir, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 3, 3, leg_length, 10, 10)
        glPopMatrix()
    
    glPopMatrix()
    glPopMatrix()

#Enemy er drawing
def draw_enemy(enemy):
    glPushMatrix()
    glTranslatef(enemy['pos'][0], 30, enemy['pos'][2])
    glScalef(enemy['scale'], enemy['scale'], enemy['scale'])
    
    glColor3f(1, 0, 0)
    glutSolidSphere(30, 20, 20)
    
    glTranslatef(0, 40, 0)
    glColor3f(0, 0, 0)
    glutSolidSphere(15, 20, 20)
    glPopMatrix()

#Bullet er drawing(square)
def draw_bullet(bullet):
    glPushMatrix()
    glTranslatef(bullet['pos'][0], bullet['pos'][1], bullet['pos'][2])
    glColor3f(1, 0, 0)
    glutSolidCube(7)
    glPopMatrix()
#nicher floor
def draw_grid():
    tile_size = 50
    for x in range(-GRID_LENGTH, GRID_LENGTH, tile_size):
        for z in range(-GRID_LENGTH, GRID_LENGTH, tile_size):
            if ((x + z) // tile_size) % 2 == 0:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0.8, 0.6, 0.9)

            glBegin(GL_QUADS)
            glVertex3f(x, 0, z)
            glVertex3f(x + tile_size, 0, z)
            glVertex3f(x + tile_size, 0, z + tile_size)
            glVertex3f(x, 0, z + tile_size)
            glEnd()

def draw_boundaries():
    boundary_height = 100
    glColor3f(1, 1, 1) #white
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, 0, -GRID_LENGTH)
    glVertex3f(-GRID_LENGTH, boundary_height, -GRID_LENGTH)
    glVertex3f(-GRID_LENGTH, boundary_height, GRID_LENGTH)
    glVertex3f(-GRID_LENGTH, 0, GRID_LENGTH)
    glEnd()
    
    glColor3f(0, 1, 0) #green
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, 0, GRID_LENGTH)
    glVertex3f(-GRID_LENGTH, boundary_height, GRID_LENGTH)
    glVertex3f(GRID_LENGTH, boundary_height, GRID_LENGTH)
    glVertex3f(GRID_LENGTH, 0, GRID_LENGTH)
    glEnd()

    glColor3f(0, 0, 1) # blue
    glBegin(GL_QUADS)
    glVertex3f(GRID_LENGTH, 0, GRID_LENGTH)
    glVertex3f(GRID_LENGTH, boundary_height, GRID_LENGTH)
    glVertex3f(GRID_LENGTH, boundary_height, -GRID_LENGTH)
    glVertex3f(GRID_LENGTH, 0, -GRID_LENGTH)
    glEnd()
 
    glColor3f(0, 255, 255) #cyan
    glBegin(GL_QUADS) 
    glVertex3f(GRID_LENGTH, 0, -GRID_LENGTH)
    glVertex3f(GRID_LENGTH, boundary_height, -GRID_LENGTH)
    glVertex3f(-GRID_LENGTH, boundary_height, -GRID_LENGTH)
    glVertex3f(-GRID_LENGTH, 0, -GRID_LENGTH)
    glEnd()

# New global variables needed for smooth rotation
keys_pressed = set()

def keyboardListener(key, x, y):
    global gun_angle, cheat_mode, game_over, life, missed_bullets, score, step_toggle, player_pos, auto_camera
    key = key.decode('utf-8').lower()
    
    if key not in keys_pressed:
        keys_pressed.add(key)
    
    if game_over:
        if key == 'r':
            print("\n=== NEW GAME STARTED ===")
            game_over = False
            life = 5
            missed_bullets = 0
            score = 0
            player_pos = [0, 0, 0]
            initial_enemies()
            bullets.clear()
        return
    
    x_move = 0
    z_move = 0
    if key == 'w':
        if cheat_mode:
            z_move = 10 
        else:
            x_move = math.sin(math.radians(gun_angle)) * 10
            z_move = math.cos(math.radians(gun_angle)) * 10
    elif key == 's':
        if cheat_mode:
            z_move = -10
        else:
            x_move = -math.sin(math.radians(gun_angle)) * 10
            z_move = -math.cos(math.radians(gun_angle)) * 10
    elif key == 'a' and cheat_mode:
        x_move = -10
    elif key == 'd' and cheat_mode:
        x_move = 10
    elif key == 'c':
        cheat_mode = not cheat_mode
        print(f"Cheat Mode: {'ON' if cheat_mode else 'OFF'}")
    elif key == 'v' and cheat_mode and camera_mode == "first":
        auto_camera = not auto_camera
        print(f"Auto Camera: {'ON' if auto_camera else 'OFF'}")
    elif key == 'v':
        print("Auto Camera can only be toggled in Cheat Mode and First-Person view")

    if x_move != 0 or z_move != 0:
        new_x = player_pos[0] + x_move
        new_z = player_pos[2] + z_move
        
        safe_margin = 50
        max_limit = GRID_LENGTH - safe_margin
        new_x = max(-max_limit, min(new_x, max_limit))
        new_z = max(-max_limit, min(new_z, max_limit))
        
        player_pos[0] = new_x
        player_pos[2] = new_z
        step_toggle = not step_toggle

def keyUpListener(key, x, y):
    key = key.decode('utf-8').lower()
    if key in keys_pressed:
        keys_pressed.remove(key)

def specialKeyListener(key, x, y):
    global camera_height, camera_angle
    if key == GLUT_KEY_UP:
        camera_height += 10
    elif key == GLUT_KEY_DOWN:
        camera_height -= 10
    elif key == GLUT_KEY_LEFT:
        camera_angle += 5
    elif key == GLUT_KEY_RIGHT:
        camera_angle -= 5

    camera_height = max(100, min(camera_height, 1500))
    camera_angle %= 360

def mouseListener(button, state, x, y):
    global camera_mode
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_over and not cheat_mode:
        bullets.append({
            'pos': [player_pos[0], player_pos[1], player_pos[2]],
            'dir': [math.sin(math.radians(gun_angle)), 0, math.cos(math.radians(gun_angle))],
            'active': True
        })
        print("Bullet Fired!")
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        camera_mode = "first" if camera_mode == "third" else "third"
        print(f"Camera mode switched to: {camera_mode}")

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect_ratio = glutGet(GLUT_WINDOW_WIDTH) / max(1, glutGet(GLUT_WINDOW_HEIGHT))
    gluPerspective(60, aspect_ratio, 0.1, 2500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if camera_mode == "third":
        cam_x = player_pos[0] + math.sin(math.radians(camera_angle)) * camera_distance
        cam_z = player_pos[2] + math.cos(math.radians(camera_angle)) * camera_distance
        gluLookAt(cam_x, camera_height, cam_z,
                  player_pos[0], player_pos[1] + 100, player_pos[2],
                  0, 1, 0)
    else:
        cam_x = player_pos[0] + math.sin(math.radians(gun_angle)) * 50
        cam_z = player_pos[2] + math.cos(math.radians(gun_angle)) * 50
        if cheat_mode and auto_camera:
            gluLookAt(cam_x, 50, cam_z,
                      cam_x + math.sin(math.radians(gun_angle)) * 100,
                      50,
                      cam_z + math.cos(math.radians(gun_angle)) * 100,
                      0, 1, 0)
        else:
            gluLookAt(cam_x, 50, cam_z,
                      cam_x + math.sin(math.radians(gun_angle)) * 100,
                      50,
                      cam_z + math.cos(math.radians(gun_angle)) * 100,
                      0, 1, 0)

def check_collisions():
    global score, life, missed_bullets, game_over
    for bullet in bullets[:]:
        if bullet.get('cheat'):
            enemy = bullet['target']
            dx = bullet['pos'][0] - enemy['pos'][0]
            dz = bullet['pos'][2] - enemy['pos'][2]
            if math.hypot(dx, dz) < 50:
                score += 1
                print(f"Target Hit! Current Score: {score}")
                enemy['pos'][0] = random.randint(-400, 400)
                enemy['pos'][2] = random.randint(-400, 400)
                bullets.remove(bullet)
            continue
        else:
            for enemy in enemies[:]:
                dx = bullet['pos'][0] - enemy['pos'][0]
                dz = bullet['pos'][2] - enemy['pos'][2]
                if math.hypot(dx, dz) < 50:
                    score += 1
                    print(f"Target Hit! Current Score: {score}")
                    enemy['pos'][0] = random.randint(-400, 400)
                    enemy['pos'][2] = random.randint(-400, 400)
                    bullets.remove(bullet)
                    break
 #bullet miss       
        if abs(bullet['pos'][0]) > GRID_LENGTH or abs(bullet['pos'][2]) > GRID_LENGTH:
            missed_bullets += 1
            bullets.remove(bullet)
            print(f"Bullet Missed: {missed_bullets}")
            if missed_bullets >= 10:
                print("\n=== GAME OVER: Too many missed bullets! ===")
                game_over = True
                bullets.clear()
                enemies.clear()
#enemy touch
    for enemy in enemies:
        dx = player_pos[0] - enemy['pos'][0]
        dz = player_pos[2] - enemy['pos'][2]
        if math.hypot(dx, dz) < 50:
            life -= 1
            print(f"\nPlayer Hit! Life Remaining: {life}")
            enemy['pos'][0] = random.randint(-400, 400)
            enemy['pos'][2] = random.randint(-400, 400)
            if life <= 0:
                print("\n=== GAME OVER: Player destroyed! ===")
                game_over = True
                bullets.clear()
                enemies.clear()

def update_enemies(): #enemy respawn
    for enemy in enemies:
        dx = player_pos[0] - enemy['pos'][0]
        dz = player_pos[2] - enemy['pos'][2]
        dist = math.hypot(dx, dz)
        if dist > 0:
            enemy['pos'][0] += (dx/dist) * enemy_speed
            enemy['pos'][2] += (dz/dist) * enemy_speed
        
        enemy['scale'] += enemy['scale_dir']
        if enemy['scale'] > 1.2 or enemy['scale'] < 0.8:
            enemy['scale_dir'] *= -1

def update_bullets(): 
    for bullet in bullets:
        bullet['pos'][0] += bullet['dir'][0] * bullet_speed
        bullet['pos'][2] +=bullet['dir'][2] * bullet_speed

def idle():
    global gun_angle
    if not game_over:
        # Smooth continuous rotation
        if 'a' in keys_pressed and not cheat_mode:
            gun_angle += 1.5
        if 'd' in keys_pressed and not cheat_mode:
            gun_angle -= 1.5

        if cheat_mode: 
            
            gun_angle += 2
            for enemy in enemies:
                dx = enemy['pos'][0] - player_pos[0]
                dz = enemy['pos'][2] - player_pos[2]
                dist = math.hypot(dx, dz)
                if dist > 0:
                    target_angle = math.degrees(math.atan2(dx, dz))
                    angle_diff = (target_angle - gun_angle) % 360
                    if angle_diff < 5 or angle_diff > 355: 
                        enemy_targeted = any(b.get('target') == enemy for b in bullets) 
                        if not enemy_targeted:
                            bullet = {
                                'pos': [player_pos[0], player_pos[1], player_pos[2]],
                                'dir': [dx/dist, 0, dz/dist],
                                'active': True,
                                'target': enemy,
                                'cheat': True
                            }
                            bullets.append(bullet)
                            print(f"Bullet Fired at Enemy! (Cheat Mode)")
        update_enemies()
        update_bullets()
        check_collisions()
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    win_width = glutGet(GLUT_WINDOW_WIDTH)
    win_height = glutGet(GLUT_WINDOW_HEIGHT)
    if win_width == 0 or win_height == 0:
        return
    
    glViewport(0, 0, win_width, win_height)
    
    setupCamera()
    draw_grid()
    draw_boundaries()
    draw_player()
    for enemy in enemies:
        draw_enemy(enemy)
    for bullet in bullets:
        draw_bullet(bullet)

    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, win_width, 0, win_height)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    if not game_over:
        draw_text(10, win_height - 30, f"Player Life Remaining: {life}")
        draw_text(10, win_height - 60, f"Game Score: {score}")
        draw_text(10, win_height - 90, f"Player Bullet Missed: {missed_bullets}")
    else:
        draw_text(10, win_height - 30, f"Game is over. Your score is {score}")
        draw_text(10, win_height - 60, "Press 'R' to RESTART the game")

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glEnable(GL_DEPTH_TEST)

    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(1000, 800)
glutCreateWindow(b"Bullet Frenzy")

glClearColor(0.0, 0.0, 0.0, 1.0)
glEnable(GL_DEPTH_TEST)

print("=== BULLET FRENZY ===")
print("Controls:")
print("WASD - Move/Rotate")
print("Left Click - Shoot")
print("Right Click - Toggle Camera")
print("Arrow Keys - Adjust Camera")
print("C - Toggle Cheat Mode (Auto-aim and fire)")
print("V - Toggle Auto Camera (in Cheat Mode, First-Person)")
print("R - Restart after Game Over")
print("\nGame Starting...\n")

glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_GLUTMAINLOOP_RETURNS)

glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboardListener)
glutKeyboardUpFunc(keyUpListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutIdleFunc(idle)

glutMainLoop()