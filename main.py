#pgzero
import random

cell = Actor('spikey', size = (50, 50))
cell1 = Actor('ground', size = (50, 50))
cell2 = Actor("pointy", size = (50, 50))
cell3 = Actor("oooh", size = (50, 50))
cellborda = Actor("borda", size = (50, 50))
size_w = 11
size_h = 11
WIDTH = cell.width * size_w
HEIGHT = cell.height * size_h

win = 0
mode = "game"
colli = 0

TITLE = "Echoes of Void" 
FPS = 30
my_map = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
          [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1], 
          [-1, 0, 1, 1, 1, 1, 1, 1, 1, 0, -1], 
          [-1, 0, 1, 1, 2, 1, 3, 1, 1, 0, -1], 
          [-1, 0, 1, 1, 1, 2, 1, 1, 1, 0, -1], 
          [-1, 0, 1, 3, 2, 1, 1, 3, 1, 0, -1], 
          [-1, 0, 1, 1, 1, 1, 3, 1, 1, 0, -1], 
          [-1, 0, 1, 1, 3, 1, 1, 2, 1, 0, -1], 
          [-1, 0, 1, 1, 1, 1, 1, 1, 1, 0, -1],
          [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
          [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]

char = Actor('DaKnight',topleft = (150,150),size = (35, 35))

# char.top = cell.height
# char.left = cell.width
char.health = 100
char.attack = 5
level_completed = False

enemies = []

for i in range(5):
    x = random.randint(3, 8) * cell.width
    y = random.randint(3, 8) * cell.height
    enemy = Actor("skelly", topleft = (x, y), size = (35, 35))
    enemy.health = random.randint(10, 20)
    enemy.attack = random.randint(5, 10)
    enemy.bonus = random.randint(0, 3)
    enemies.append(enemy)
   

hearts = []
swords = []   
aces = []
clocks = []
def map_draw():
    for i in range(len(my_map)):
        for j in range(len(my_map[0])):
            if my_map[i][j] == 0:
                cell.left = cell.width*j
                cell.top = cell.height*i
                cell.draw()
            elif my_map[i][j] == 1:
                cell1.left = cell.width*j
                cell1.top = cell.height*i
                cell1.draw()
            elif my_map[i][j] == 2:
                cell2.left = cell.width*j
                cell2.top = cell.height*i
                cell2.draw()  
            elif my_map[i][j] == 3:
                cell3.left = cell.width*j
                cell3.top = cell.height*i
                cell3.draw() 
            elif my_map[i][j] == -1:
                cellborda.left = cell.width*j
                cellborda.top = cell.height*i
                cellborda.draw() 

def draw():
    if mode == 'game' or mode == 'level_2' or mode == 'level_3' or mode == 'level_4' or mode == 'level_5':
        screen.fill("#2f3542")
        map_draw()
        char.draw()
        screen.draw.text(char.health, topleft=(char.x + 5, char.y - 30), color = 'white', fontsize = 20)
        screen.draw.text(char.attack, topright=(char.x - 5, char.y - 30), color = 'white', fontsize = 20)
        for i in range(len(enemies)):
            enemies[i].draw()
            screen.draw.text(enemies[i].health, topleft=(enemies[i].x + 5, enemies[i].y - 30), color='white', fontsize=20)

        for i in range(len(hearts)):
            hearts[i].draw()
        for i in range(len(swords)):
            swords[i].draw()
        for i in range(len(aces)):
            aces[i].draw()
        for i in range(len(clocks)):
            clocks[i].draw()
    elif mode == "end":
        if win == 6:
            screen.fill("#000080")
            screen.draw.text("Você derrotou todos os monstros!", center=(WIDTH/2, HEIGHT/2), color = 'white', fontsize = 34)
        else:
            screen.fill("#FF0000")
            screen.draw.text("Você perdeu!", center=(WIDTH/2, HEIGHT/2), color = 'white', fontsize = 34)


def on_key_down(key):
    global colli
    old_x = char.x
    old_y = char.y
    if keyboard.right and char.x + cell.width*2 < WIDTH - cell.width:
        char.x += cell.width
    elif keyboard.left and char.x - cell.width*2 > cell.width:
        char.x -= cell.width
    elif keyboard.down and char.y + cell.height < HEIGHT - cell.height*2:
        char.y += cell.height
    elif keyboard.up and char.y - cell.height > cell.height * 2:
        char.y -= cell.height
        
    enemy_index = char.collidelist(enemies)
    if enemy_index != -1:
        char.x = old_x
        char.y = old_y
        colli = 1
        enemy = enemies[enemy_index]
        enemy.health -= char.attack
        char.health -= enemy.attack
        if enemy.health <= 0:
            if enemy.bonus == 1:
                heart = Actor('healthPoint', size = (35, 35))
                heart.pos = enemy.pos
                hearts.append(heart)
            elif enemy.bonus == 2:
                sword = Actor('sword', size = (35, 35))
                sword.pos = enemy.pos
                swords.append(sword)
            elif enemy.bonus == 3:
                ace = Actor('flowers', size = (35, 35))
                ace.pos = enemy.pos
                aces.append(ace)
            elif enemy.bonus == 4:
                clock = Actor('clock', size = (35, 35))
                clock.pos = enemy.pos
                clocks.append(clock)
            enemies.pop(enemy_index)     

def spawn_enemies(num, min_health, max_health, min_attack, max_attack):
    global enemies
    enemies = []
    for i in range(num):
        x = random.randint(2, 8) * cell.width
        y = random.randint(2, 8) * cell.height
        enemy = Actor("skelly", topleft=(x, y), size = (35, 35))
        enemy.health = random.randint(min_health, max_health)
        enemy.attack = random.randint(min_attack, max_attack)
        enemy.bonus = random.randint(0, 4)
        enemies.append(enemy)


def spawn_boss():
    global enemies
    boss = Actor("DaBlaKnight", topleft=(cell.width * 4, cell.height * 4),size = (35, 35))
    boss.health = 200
    boss.attack = random.randint(30, 40)
    boss.bonus = 0
    enemies.append(boss)

def victory():
    global mode, win, level_completed

    # Only check for victory if we’re not already processing a level-up
    if not level_completed and enemies == [] and char.health > 0:
        level_completed = True  # prevent running again
        win += 1
        char.health = 100

        if win == 1:
            mode = "level_2"
            spawn_enemies(5, 15, 25, 5, 10)
        elif win == 2:
            mode = "level_3"
            spawn_enemies(7, 25, 35, 10, 15)
        elif win == 3:
            mode = "level_4"
            spawn_enemies(10, 35, 45, 15, 20)
        elif win == 4:
            mode = "level_5"
            spawn_enemies(12, 45, 50, 20, 25)
            spawn_boss()
        elif win >= 5:
            mode = "end"

        # Once enemies are spawned, reset the flag so we can win again later
        level_completed = False

    elif char.health <= 0:
        mode = "end"
        win = -1

def update(dt):
    victory()
    for i in range(len(hearts)):
        if char.colliderect(hearts[i]):
            char.health += 5
            hearts.pop(i)
            break
        
    for i in range(len(swords)):
        if char.colliderect(swords[i]):
            char.attack += 5
            swords.pop(i)
            break
            
    for i in range(len(aces)):
        if char.colliderect(aces[i]):
            char.health *= 2
            aces.pop(i)
            break

    for i in range(len(clocks)):
        if char.colliderect(clocks[i]):
            char.attack += 10
            clocks.pop(i)
            break
