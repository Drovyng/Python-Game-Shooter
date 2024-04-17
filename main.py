import pygame, keyboard, math, random
from pygame import draw, display, mixer

pygame.init()
display.init()
mixer.init()
pygame.font.init()

sound_playerShoot = mixer.Sound("sounds/playerShoot.wav")
sound_playerReload = mixer.Sound("sounds/playerReload.wav")
sound_playerHurt = mixer.Sound("sounds/playerHurt.wav")
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
player_atkBullets = 0
player_atkReload = 180
player_shooting = False

player_bullets_pos = []
player_bullets_angle = []

playTime = 0
playTimeSec = 0

gameOver = False

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

                    playTime = 0
                    playTimeSec = 0
                else:
                    player_shooting = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                player_shooting = False
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and player_atkReload <= 0 and player_atkCd <= 0 and player_atkBullets < 12:
                player_atkReload = 180
            
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
            player_atkCd = 20
            player_atkBullets -= 1
            sound_playerShoot.play()
            if player_atkBullets <= 0:
                player_atkReload = 180
                
        if player_atkCd > 0: 
            player_atkCd -= enemy_speed / 2 + 0.75
            
        if player_atkReload > 0: 
            player_atkReload -= enemy_speed / 2 + 0.75
            if player_atkReload <= 0:
                sound_playerReload.play()
                player_atkBullets = int(12 * (enemy_speed / 2 + 0.75))
        
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
        draw.rect(surface, (255, 200, 50), (10, 4, int(640 * player_atkBullets / 12), 6))
        
        draw.rect(surface, (125, 125, 125), (10, 14, 640, 6))
        draw.rect(surface, (200, 200, 200), (10, 14, int(640 * player_atkCd / 20), 6))
        
        draw.rect(surface, (50, 125, 50), (10, 24, 640, 6))
        draw.rect(surface, (50, 200, 50), (10, 24, int(640 * player_atkReload / 180), 6))
        
        playTime += 1
        playTimeSec = playTime // 60
        
        sec = playTimeSec % 60
        secStr = str(sec)
        if sec < 10:
            secStr = f"0{secStr}"
        minutes = (playTimeSec - sec) // 60
        
        timefont = font.render(f"{minutes}:{secStr}", True, (250, 250, 250), None)
        
        surface.blit(timefont, (330 - timefont.get_width() // 2, 32))
    else:
        gameOverfont = font.render(f"Game Over!!!", True, (250, 250, 250), None)
        gameOverRestartfont = font.render(f"Click to restart!!!", True, (250, 250, 250), None)
        height = gameOverfont.get_height() + 50 + gameOverRestartfont.get_height()
        
        surface.blit(gameOverfont, (330 - gameOverfont.get_width() // 2, 330 - height // 2))
        surface.blit(gameOverRestartfont, (330 - gameOverRestartfont.get_width() // 2, 380 - height // 2))
    display.flip()
    clock.tick(60)