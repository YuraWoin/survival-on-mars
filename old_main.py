import pygame
import random
from image import walk, fon, fon1, zombie1, icon, myfount, piv_pav, fon_sounds, fon_on_mars, raketa, meteor
from config_game import Player, Zombie, Strilba, Level, Meteor, RocketBullet, BioMaterial
clock = pygame.time.Clock()
pygame.init() 

pygame.display.set_caption("zombie apokalipsis beta") 
pygame.display.set_icon(icon)
HEIGHT = 460
WIDTH = 630
sckrin = pygame.display.set_mode((WIDTH, HEIGHT))
zombie_timer = pygame.USEREVENT + 1
pygame.time.set_timer(zombie_timer, 5000) 
zombie_list_in_game = []
walk_left, walk_right = walk()
player_anim_count = 0

meteor_timer = pygame.USEREVENT + 2
pygame.time.set_timer(meteor_timer, 2000)
meteor_list = []

paused = False

pulki = 10

bio_list = []
bio_zibrano = 0
BIO_NEEDED = 5

mars_start_time = 0

fon_x = 0
fon1_x = 0

game_state = "menu"
ending_lines = [
    "Біо матеріал зібрано...",
    "Але вчені не виходять на зв'язок...",
    "Продовження слідує...",
]
ending_index = 0
ending_timer = 0
mission_timer = 0
mission_lines = [
    "Землі залишився менше одного року...",
    "Ваша місія — долетіти до Марсу...",
    "...та добути біо матеріал для вчених.",
]
mission_line_index = 0
mission_line_timer = 0
MISSION_LINE_DELAY = 2000

pivs_pavs = []
shoot_cooldown = 500
last_shot_time = 0
shoot = True

star_offset = 0

playerrr = Player(160, 337, sckrin, walk_right)
stars = [(random.randint(0, 630), random.randint(0, 460)) for _ in range(80)]

game_play = True
text_gameover = myfount.render('GAME OVER', False, 25)
text_restart = myfount.render('restart', False, 25)
restart_rect = text_restart.get_rect(topleft=(245, 300))

text_start = myfount.render('start', False, 25)
start_rect = text_restart.get_rect(topleft=(245, 300))

level = Level()

hp = 100 

def pipipipapapa(e):
    global pulki, shoot, last_shot_time
    targets = meteor_list if level.current == "space" else zombie_list_in_game
    for i in range(len(pivs_pavs) - 1, -1, -1):
        b = pivs_pavs[i]
        b.update()
        b.draw()
        for j in range(len(targets) - 1, -1, -1):
            if b.collides_with(targets[j].hitbox):
                dead_z = targets.pop(j)
                if level.current == "mars":
                    bio_list.append(BioMaterial(dead_z.hitbox.x, dead_z.hitbox.y, sckrin))
                    pivs_pavs.pop(i)
                    break  
                pivs_pavs.pop(i)
                break
        else:
            if not b.active:
                pivs_pavs.pop(i)
    if game_play and e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and pulki > 0 and shoot:
        if level.current == "space":
            pivs_pavs.append(RocketBullet(playerrr.hitbox.x + 30, playerrr.hitbox.y + 10, sckrin))
        else:
            pivs_pavs.append(Strilba(playerrr.hitbox.x + 30, playerrr.hitbox.y + 10, sckrin, piv_pav))
        pulki -= 1
        shoot = False
        last_shot_time = pygame.time.get_ticks()
  
def draw_space(sckrin, offset):
    sckrin.fill((0, 0, 0))
    for x, y in stars:
        draw_x = (x - offset) % 630
        pygame.draw.circle(sckrin, (255, 255, 255), (draw_x, y), 1)

e_presed = False
game_started = False
ranning = True
dlyafonu = (5000 // 736) + 2
while ranning:
    for e in pygame.event.get():
        if game_started and game_play and not paused:
            pipipipapapa(e)
        if e.type == meteor_timer and level.current == "space":
            meteor_list.append(Meteor(random.randint(20, 600), -50, sckrin, meteor))
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    paused = not paused
        if e.type == pygame.QUIT:
            ranning = False

        if game_started and game_play:
            pipipipapapa(e)


        if e.type == zombie_timer:
            zombie_list_in_game.append(Zombie(740, 337, sckrin, zombie1)) 

    if paused:
        text_pause = myfount.render('PAUSE', True, (255, 255, 255))
        sckrin.blit(text_pause, (WIDTH // 2 - 40, HEIGHT // 2))
        pygame.display.update()
        clock.tick(30)
        continue

    if level.current == "space":
        star_offset += 2
        draw_space(sckrin, star_offset) 
    elif level.current == "mars":
        fon_sounds.stop()
        for i in range(dlyafonu):
            sckrin.blit(fon_on_mars, (fon_x + i * 736, 0))
    else:
        for i in range(dlyafonu):
            sckrin.blit(fon, (fon_x + i * 736, 0))




    if game_state == "menu":
        sckrin.fill((0, 0, 0))
        text_start = myfount.render('START', True, (255, 255, 255))
        text_exit = myfount.render('EXIT', True, (255, 255, 255))
        exit_rect = text_exit.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        start_rect = text_start.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        sckrin.blit(text_start, start_rect)
        sckrin.blit(text_exit, exit_rect)
        get_mouse = pygame.mouse.get_pos()
        if start_rect.collidepoint(get_mouse) and pygame.mouse.get_pressed()[0]:
            game_state = "mission"
            game_started = True
            mission_line_timer = pygame.time.get_ticks()
            mission_line_index = 0
            zombie_list_in_game.clear()
            pivs_pavs.clear()
            fon_sounds.play(loops=-1)  # ← звук один раз тут
        if exit_rect.collidepoint(get_mouse) and pygame.mouse.get_pressed()[0]:
            ranning = False

    elif game_state == "mission":
        sckrin.fill((0, 0, 0))
        current_time = pygame.time.get_ticks()
        for i in range(mission_line_index + 1):
            text = myfount.render(mission_lines[i], True, (255, 255, 255))
            sckrin.blit(text, (40, 150 + i * 40))
        if current_time - mission_line_timer > MISSION_LINE_DELAY:
            mission_line_timer = current_time
            mission_line_index += 1
            if mission_line_index >= len(mission_lines):
                game_state = "playing"
                mission_line_index = 0

    elif game_state == "playing" and game_play:
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        
        if level.current == "space":
            # корабель
            sckrin.blit(raketa, (playerrr.hitbox.x, playerrr.hitbox.y))

            # метеорити
            for i in range(len(meteor_list) - 1, -1, -1):
                m = meteor_list[i]
                m.update()
                m.draw()
                if m.collides_with(playerrr.hitbox):
                    game_play = False
                if not m.active:
                    meteor_list.pop(i)

            # рух ракети
            if keys[pygame.K_a] and playerrr.hitbox.x > 20:
                playerrr.hitbox.x -= playerrr.speed
            if keys[pygame.K_d] and playerrr.hitbox.x < WIDTH - 80:
                playerrr.hitbox.x += playerrr.speed
            # прогрес
            level.update()
            progress = int((level.flight_progress / 1800) * 100)
            text_progress = myfount.render(f'До Марсу: {progress}%', True, (255, 255, 255))
            sckrin.blit(text_progress, (2, 2))

        elif level.current == "mars":
            mars_start_time = pygame.time.get_ticks()
            def zombie():
                global game_play
                if pygame.time.get_ticks() - mars_start_time < 10000: 
                    return 
                for i in range(len(zombie_list_in_game) - 1, -1, -1):
                    z = zombie_list_in_game[i]
                    z.update()
                    z.draw()
                    if z.collides_with(playerrr.hitbox):
                        game_play = False
                        hp -= 25
                        zombie_list_in_game.pop(i)
                        if hp <= 0:
                            game_play = False
                    if z.is_off_screen():
                        zombie_list_in_game.pop(i)
            zombie()

            def hodba():
                global player_anim_count, fon_x
                abc = False
                if keys[pygame.K_s] and playerrr.hitbox.x > 50:
                    playerrr.hitbox.x -= playerrr.speed
                    sckrin.blit(walk_left[player_anim_count], (playerrr.hitbox.x, playerrr.hitbox.y))
                    abc = True
                elif keys[pygame.K_w]:
                    if playerrr.hitbox.x >= 450 and fon_x > -5100:
                        fon_x -= playerrr.speed
                    elif playerrr.hitbox.x < 450:
                        playerrr.hitbox.x += playerrr.speed
                        sckrin.blit(walk_right[player_anim_count], (playerrr.hitbox.x, playerrr.hitbox.y))
                        abc = True
                    else:
                        sckrin.blit(walk_right[0], (playerrr.hitbox.x, playerrr.hitbox.y))
                        if not abc:
                            player_anim_count = 0
                    player_anim_count += 1
                    if player_anim_count >= len(walk_right):
                        player_anim_count = 0
            hodba()
            playerrr.update()

            text_pulki = myfount.render(f'Bullets: {pulki}', True, (255, 255, 255))
            pygame.draw.rect(sckrin, (255, 0, 0), (2, 60, hp * 1, 10))
            sckrin.blit(text_pulki, (2, 2))

            if current_time - last_shot_time > shoot_cooldown:
                shoot = True
            pipipipapapa(e)
       
    else:
        sckrin.fill((242, 4, 4))
        sckrin.blit(text_gameover, (245, 200))
        sckrin.blit(text_restart, restart_rect)
        get_mouse = pygame.mouse.get_pos()
        if restart_rect.collidepoint(get_mouse) and pygame.mouse.get_pressed()[0]:
            game_play = True
            game_started = False
            player_x = 150
            zombie_list_in_game.clear()
            pivs_pavs.clear()
            meteor_list.clear()
            shoot = True
            last_shot_time = 0
            fon_x = 0
            pulki = 10
            star_offset = 0
            level.__init__()
            playerrr.hitbox.x = 160
            playerrr.hitbox.y = 337
            hp = 100


    pygame.display.update() 
    clock.tick(30)

pygame.quit()












        
    # if not game_started:
    #     sckrin.fill((0, 0, 0))
    #     text_start = myfount.render('START', True, (255, 255, 255))
    #     text_exit = myfount.render('EXIT', True, (255, 255, 255))
    #     exit_rect = text_exit.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
    #     start_rect = text_start.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    #     sckrin.blit(text_start, start_rect)
    #     sckrin.blit(text_exit, exit_rect)

    #     get_mouse = pygame.mouse.get_pos()
    #     if start_rect.collidepoint(get_mouse) and pygame.mouse.get_pressed()[0]:
    #         game_started = True
    #         game_state = "mission"
    #         mission_line_timer = pygame.time.get_ticks()
    #         mission_line_index = 0
    #         zombie_list_in_game.clear()
    #         pivs_pavs.clear()

    #     if exit_rect.collidepoint(get_mouse) and pygame.mouse.get_pressed()[0]:
    #         ranning = False
            
     
    
    # # elif game_started and game_play:
    # #     keys = key.get_pressed()

    # #     def zombie():
    # #         global game_play
    # #         for i in range(len(zombie_list_in_game) - 1, -1, -1):
    # #             z = zombie_list_in_game[i]
    # #             z.update()
    # #             z.draw()
    # #             if z.collides_with(playerrr.hitbox):
    # #                 game_play = False
    # #             if z.is_off_screen():
    # #                 zombie_list_in_game.pop(i)
    # #     zombie()
    # #     current_time = time.get_ticks()

        # def hodba():
        #     global player_anim_count, fon_x
        #     abc = False
        #     if keys[K_s or K_LEFT] and playerrr.hitbox.x > 50:
        #         playerrr.hitbox.x -= playerrr.speed
        #         sckrin.blit(walk_left[player_anim_count], (playerrr.hitbox.x, playerrr.hitbox.y))
        #         abc = True
        #     elif keys[K_w or K_RIGHT]:
        #         if playerrr.hitbox.x >= 450 and fon_x > -5100:
        #             fon_x -= playerrr.speed
        #         elif playerrr.hitbox.x < 450:
        #             playerrr.hitbox.x += playerrr.speed
        #         sckrin.blit(walk_right[player_anim_count], (playerrr.hitbox.x, playerrr.hitbox.y))
        #         abc = True
        #     else:
        #         sckrin.blit(walk_right[0], (playerrr.hitbox.x, playerrr.hitbox.y))
        #         if not abc:
        #             player_anim_count = 0

    # #         player_anim_count += 1
    # #         if player_anim_count >= len(walk_right):
    # #             player_anim_count = 0
    # #     hodba()
    # #     playerrr.update()

    # #     if level.update(fon_x):
    # #         zombie_list_in_game.clear()
    # #         pivs_pavs.clear()
    # #         pulki = 15
    # #         sckrin.blit(fon1, (0, 0))

    # #     text_pulki = myfount.render(f'Bullets: {pulki}', True, (255, 255, 255))
    # #     sckrin.blit(text_pulki, (2, 2))

    # #     if current_time - last_shot_time > shoot_cooldown:
    # #         shoot = True
    # #     pipipipapapa(e)
        
    # if game_state == "mission":
    #     sckrin.fill((0, 0, 0))
    #     current_time = pygame.time.get_ticks()
    #         # показуємо рядки поступово
    #     for i in range(mission_line_index + 1):
    #         text = myfount.render(mission_lines[i], True, (255, 255, 255))
    #         sckrin.blit(text, (40, 150 + i * 40))
            
    #     if current_time - mission_line_timer > MISSION_LINE_DELAY:
    #         mission_line_timer = current_time
    #         mission_line_index += 1
    #         if mission_line_index >= len(mission_lines):
    #             game_state = "playing"
    #             game_started = True
    #             mission_line_index = 0



    # elif game_started and game_play:
    #     keys = pygame.key.get_pressed()
    #     current_time = pygame.time.get_ticks()

    #     if level.current == "space":
    #         # корабель
    #         sckrin.blit(raketa, (playerrr.hitbox.x, playerrr.hitbox.y))

    #         # метеорити
    #         for i in range(len(meteor_list) - 1, -1, -1):
    #             m = meteor_list[i]
    #             m.update()
    #             m.draw()
    #             if m.collides_with(playerrr.hitbox):
    #                 game_play = False
    #             if not m.active:
    #                 meteor_list.pop(i)

    #         # рух ракети вгору/вниз
    #         if keys[pygame.K_a] and playerrr.hitbox.x > 20:
    #             playerrr.hitbox.x -= playerrr.speed
    #         if keys[pygame.K_d] and playerrr.hitbox.x < WIDTH - 80:
    #             playerrr.hitbox.x += playerrr.speed

    #         # прогрес
    #         level.update()
    #         progress = int((level.flight_progress / 1800) * 100)
    #         text_progress = myfount.render(f'До Марсу: {progress}%', True, (255, 255, 255))
    #         sckrin.blit(text_progress, (2, 2))

    #         if level.current == "mars":
    #             meteor_list.clear()
    #             pivs_pavs.clear()
    #             pulki = 10