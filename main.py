import pygame, keyboard, math, random
from pygame import draw, display, mixer

pygame.init()
display.init()
mixer.init()
pygame.font.init()

sound_playerShoot = mixer.Sound("sounds/playerShoot.mp3")
sound_playerReload = mixer.Sound("sounds/playerReload.wav")
sound_playerHurt = mixer.Sound("sounds/playerHurt.wav")
sound_playerWeaponChange = mixer.Sound("sounds/playerWeaponChange.mp3")
sound_gameOver = mixer.Sound("sounds/gameOver.wav")
font = pygame.font.Font(None, 64)

surface = display.set_mode((660, 660))
clock = pygame.time.Clock()

player_pos = (330, 330)
enemies_pos = []
enemies_see = []
enemies_angle = []
enemies_health = []
enemy_spawnRadius = 60

enemy_spawnTime = 0
enemy_spawnTimeRand = 5, 5

player_angle = 0
player_fov = 60 * math.pi / 180
player_fov_half = player_fov / 2
player_fov_details = 7
player_fog = 400
player_health = 100
player_healthCd = 0


player_atkCd = 0
player_atkReload = 130
player_shooting = False
player_gun = 0

player_guns = [
    [20, 12, 130, 1, 0], # [cd, bullets, reload, burst, curBUllets]
    [40, 7, 200, 3, 0]
]
player_guns_sprite:list[list[tuple[int, int]]] = [
    [(564, 599), (564, 597), (567, 597), (567, 599), (644, 599), (645, 596), (645, 596), (646, 599), (648, 599), (651, 596), (654, 599), (654, 600), (660, 612), (650, 622), (656, 657), (653, 658), (653, 660), (634, 660), (625, 632), (607, 631), (602, 618), (585, 617), (585, 615), (561, 615), (560, 607), (560, 599), (563, 599)],
    [(510, 611), (579, 610), (583, 607), (630, 607), (633, 610), (637, 613), (643, 612), (654, 616), (653, 620), (656, 622), (655, 628), (648, 632), (660, 652), (657, 656), (642, 660), (640, 658), (633, 635), (621, 633), (612, 626), (603, 627), (604, 636), (583, 633), (582, 628), (560, 627), (558, 629), (520, 629), (517, 626), (513, 626), (513, 621), (517, 617), (510, 617)]
]

player_bullets_pos = []
player_bullets_angle = []

playTime = 0
playTimeSec = 0

gameOver = False
timeStr = ""

def addEnemy():
    global enemies_angle, enemies_health, enemies_pos, enemies_see, player_pos, enemy_spawnRadius, player_fog
    
    angle = random.random() * math.pi * 2
    radius = player_fog + random.random() * enemy_spawnRadius
    
    x, y = player_pos
    
    enemies_pos.append((x + math.sin(angle) * radius, y + math.cos(angle) * radius))
    enemies_angle.append(0)
    enemies_health.append(100)
    enemies_see.append(False)

def inRange(pos1:tuple[float, float], pos2:tuple[float, float], radius:float) -> bool:
    x1, y1 = pos1
    x2, y2 = pos2
    return (x1 - x2) ** 2 + (y1 - y2) ** 2 < radius ** 2

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if gameOver:
                    gameOver = False
                    player_pos = (330, 330)
                    enemies_pos = [(10, 10)]
                    enemies_see = [False]
                    enemies_angle = [0]
                    enemies_health = [100]
                    enemy_spawnRadius = 100

                    enemy_spawnTime = 0
                    enemy_spawnTimeRand = 5, 5

                    player_angle = 0
                    player_fov = 60 * math.pi / 180
                    player_fov_half = player_fov / 2
                    player_fov_details = 7
                    player_fog = 400
                    player_health = 100
                    player_healthCd = 0

                    player_atkCd = 0
                    player_atkBullets = 0
                    player_atkReload = 180
                    player_shooting = False

                    player_bullets_pos = []
                    player_bullets_angle = []
                    player_gun = 0
                    playTime = 0
                    playTimeSec = 0
                else:
                    player_shooting = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                player_shooting = False
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and player_atkReload <= 0 and player_atkCd <= 0:
                player_gun += 1
                player_gun %= len(player_guns)
                if player_guns[player_gun][4] <= 0:
                    player_atkReload = player_guns[player_gun][2]
                sound_playerWeaponChange.play()
            if event.key == pygame.K_q and player_atkReload <= 0 and player_atkCd <= 0:
                player_gun -= 1
                if player_gun < 0:
                    player_gun = len(player_guns)-1
                player_atkCd = player_guns[player_gun][0]
                if player_guns[player_gun][4] <= 0:
                    player_atkReload = player_guns[player_gun][2]
                sound_playerWeaponChange.play()
            if event.key == pygame.K_r and player_atkReload <= 0 and player_atkCd <= 0 and player_guns[player_gun][4] < 12:
                player_atkReload = player_guns[player_gun][2]
                player_guns[player_gun]
                player_atkCd = player_guns[player_gun][0]
                
    cur_gun = player_guns[player_gun]
            
    surface.fill((50, 50, 50))
    
    if not gameOver:
        
        enemy_speed = playTimeSec / 120 + 0.5
        
        mouse_pos = pygame.mouse.get_pos()
        
        player_x, player_y = player_pos
        
        if keyboard.is_pressed("w"):
            player_y -= 3
        if keyboard.is_pressed("s"):
            player_y += 3
        if keyboard.is_pressed("a"):
            player_x -= 3
        if keyboard.is_pressed("d"):
            player_x += 3
            
        player_x = min(player_x, 650)
        player_y = min(player_y, 650)
        player_x = max(player_x, 10)
        player_y = max(player_y, 10)
            
        player_pos = player_x, player_y
        player_angle = math.atan2(mouse_pos[0] - player_pos[0], mouse_pos[1] - player_pos[1])
        
        enemy_spawnTime -= enemy_speed * 2
        if enemy_spawnTime <= 0:
            offset, rang = enemy_spawnTimeRand
            enemy_spawnTime = (offset + random.random() * rang) * 60
            addEnemy()
        
        if player_shooting and player_atkCd <= 0 and player_atkReload <= 0:
            player_bullets_pos.append(player_pos)
            player_bullets_angle.append(player_angle)
            bullets_fov = 20 * math.pi / 180
            burst = cur_gun[3]-1
            for i in range(cur_gun[3]):
                angle = player_angle
                if burst > 0:
                    angle = player_angle - bullets_fov / 2 + bullets_fov / burst * i
                player_bullets_pos.append(player_pos)
                player_bullets_angle.append(angle)
            player_atkCd = cur_gun[0]
            cur_gun[4] -= 1
            sound_playerShoot.play()
            if cur_gun[4] <= 0:
                player_atkReload = cur_gun[2]
                
        if player_atkCd > 0: 
            player_atkCd -= 1
            
        if player_atkReload > 0: 
            player_atkReload -= 1
            if player_atkReload <= 0:
                sound_playerReload.play()
                cur_gun[4] = cur_gun[1]
        
        if player_healthCd > 0: player_healthCd -= 1
        
        for i in range(len(enemies_pos)):
            enemy_pos = enemies_pos[i]
            enemy_angle = math.atan2(enemy_pos[0] - player_pos[0], enemy_pos[1] - player_pos[1])
            
            x, y = enemy_pos
            
            x -= math.sin(enemy_angle) * enemy_speed
            y -= math.cos(enemy_angle) * enemy_speed
            
            enemy_pos = x, y
            
            if inRange((x, y), player_pos, 40) and player_healthCd <= 0:
                player_health -= 15
                player_healthCd = 30 * (enemy_speed / 2 + 0.75)
                if player_health > 0:
                    sound_playerHurt.play()
                else:
                    sound_gameOver.play()
                    gameOver = True
            
            enemies_pos[i] = enemy_pos
            enemies_angle[i] = enemy_angle
            enemies_see[i] = inRange(enemy_pos, player_pos, player_fog) and player_angle - player_fov_half < enemy_angle and player_angle + player_fov_half > enemy_angle
        
        i = 0
        while i < len(player_bullets_pos):
            x, y = player_bullets_pos[i]
            angle = player_bullets_angle[i]
            
            x += math.sin(angle) * 12.5
            y += math.cos(angle) * 12.5
            
            kill = False
            
            for j in range(len(enemies_pos)):
                if inRange((x, y), enemies_pos[j], 20):
                    enemies_health[j] -= 35
                    if enemies_health[j] <= 0:
                        enemies_pos.pop(j)
                        enemies_angle.pop(j)
                        enemies_see.pop(j)
                        enemies_health.pop(j)
                    kill = True
                    break
                
            if kill or (x < 5 or y < 5 or x > 665 or y > 665):
                player_bullets_pos.pop(i)
                player_bullets_angle.pop(i)
                continue
            
            player_bullets_pos[i] = x, y
            i += 1
        

            
        points = [player_pos]
        for i in range(player_fov_details+1):
            angle = player_angle - player_fov_half + i * player_fov / player_fov_details
            points.append((player_pos[0] + math.sin(angle) * player_fog, player_pos[1] + math.cos(angle) * player_fog))
        draw.polygon(surface, (60, 60, 60), points)
        
        
        
        for i in range(len(enemies_pos)):
            if enemies_see[i]:
                x, y = enemies_pos[i]
                draw.circle(surface, (255, 50, 50), (x, y), 15)
                draw.rect(surface, (75, 75, 75), (x - 23, y - 23, 46, 9))
                draw.rect(surface, (75, 200, 75), (x - 20, y - 20, int(40 * enemies_health[i] / 100), 3))
                
        for i in range(len(player_bullets_pos)):
            draw.circle(surface, (150, 150, 150), player_bullets_pos[i], 5)
        
        
        draw.rect(surface, (75, 75, 75), (player_x - 23, player_y - 23, 46, 9))
        draw.rect(surface, (255, 25, 25), (player_x - 20, player_y - 20, int(40 * player_health / 100), 3))
        draw.circle(surface, (200, 200, 200), player_pos, 10)
        
        
        draw.rect(surface, (75, 75, 75), (0, 0, 660, 32))
        
        draw.rect(surface, (150, 125, 50), (10, 4, 640, 6))
        draw.rect(surface, (255, 200, 50), (10, 4, int(640 * cur_gun[4] / cur_gun[1]), 6))
        
        draw.rect(surface, (125, 125, 125), (10, 14, 640, 6))
        draw.rect(surface, (200, 200, 200), (10, 14, int(640 * player_atkCd / cur_gun[0]), 6))
        
        draw.rect(surface, (50, 125, 50), (10, 24, 640, 6))
        draw.rect(surface, (50, 200, 50), (10, 24, int(640 * player_atkReload / cur_gun[2]), 6))
        
        playTime += 1
        playTimeSec = playTime // 60
        
        sec = playTimeSec % 60
        secStr = str(sec)
        if sec < 10:
            secStr = f"0{secStr}"
        minutes = (playTimeSec - sec) // 60
        timeStr = f"{minutes}:{secStr}"
        timefont = font.render(f"{timeStr}", True, (250, 250, 250), None)
        
        surface.blit(timefont, (330 - timefont.get_width() // 2, 32))
        
        draw.lines(surface, (100, 255, 255), True, player_guns_sprite[player_gun], 5)
    else:
        gameOverfont = font.render(f"Game Over!!!", True, (250, 250, 250), None)
        gameOverRestartfont = font.render(f"Click to restart!!!", True, (250, 250, 250), None)
        timeSurvfont = font.render(f"Your time: {timeStr}", True, (250, 250, 250), None)
        height = gameOverfont.get_height() + 50 + gameOverRestartfont.get_height() + 50 + timeSurvfont.get_height()
        
        surface.blit(gameOverfont, (330 - gameOverfont.get_width() // 2, 330 - height // 2))
        surface.blit(gameOverRestartfont, (330 - gameOverRestartfont.get_width() // 2, 380 - height // 2))
        surface.blit(timeSurvfont, (330 - timeSurvfont.get_width() // 2, 430 - height // 2))
    display.flip()
    clock.tick(60)