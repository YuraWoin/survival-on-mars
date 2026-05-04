from pygame import *
import random
from image import walk, fon, fon1, zombie1, icon, myfount, piv_pav, fon_sounds, fon_on_mars
from config_game import Player, Zombie, Strilba, Level




clock = time.Clock()
init() 
display.set_caption("zombie apokalipsis beta") 
display.set_icon(icon)
HEIGHT = 460
WIDTH = 630
sckrin = display.set_mode((WIDTH, HEIGHT))
zombie_timer = USEREVENT + 1
time.set_timer(zombie_timer, 5000) 
zombie_list_in_game = []
walk_left, walk_right = walk()
player_anim_count = 0

pulki = 10

fon_x = 0
fon1_x = 0

fon_sounds.play()

pivs_pavs = []
shoot_cooldown = 500
last_shot_time = 0
shoot = True

playerrr = Player(160, 310, sckrin, walk_right)

game_play = True
text_gameover = myfount.render('GAME OVER', False, 25)
text_restart = myfount.render('restart', False, 25)
restart_rect = text_restart.get_rect(topleft=(245, 300))

text_start = myfount.render('start', False, 25)
start_rect = text_restart.get_rect(topleft=(245, 300))

level = Level()



def pipipipapapa(e):  
            global pulki, shoot, last_shot_time  
            for i in range(len(pivs_pavs) - 1, -1, -1):
                b = pivs_pavs[i]
                b.update()
                b.draw()
                for j in range(len(zombie_list_in_game) - 1, -1, -1):
                    if b.collides_with(zombie_list_in_game[j].hitbox):
                        zombie_list_in_game.pop(j)
                        pivs_pavs.pop(i)
                        break
                if not b.active:
                    pivs_pavs.pop(i)
            if game_play and e.type == MOUSEBUTTONDOWN and e.button == 1 and pulki > 0 and shoot:
                # pivs_pavs.append(piv_pav.get_rect(topleft=(player_x + 30, player_y + 10)))
                pivs_pavs.append(Strilba(playerrr.hitbox.x + 30, playerrr.hitbox.y + 10, sckrin, piv_pav)) 
                pulki -= 1
                shoot = False
                last_shot_time = time.get_ticks()  

e_presed = False
game_started = False
ranning = True
dlyafonu = (5000 // 736) + 2
while ranning:
    for e in event.get():
        if e.type == QUIT:
            ranning = False
            quit()
        if e.type == zombie_timer:
            zombie_list_in_game.append(Zombie(740, 290, sckrin, zombie1)) 

    if level.in_house:
        sckrin.blit(fon_on_mars, (0, 0))          # фон хати
    else:
        for i in range(dlyafonu):
            sckrin.blit(fon_on_mars, (fon_x + i * 736, 0))
        
    if not game_started:
        sckrin.fill((255, 255, 255))
        text_start = myfount.render('START', True, (0, 0, 0))
        start_rect = text_start.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        sckrin.blit(text_start, start_rect)
        get_mouse = mouse.get_pos()
        if start_rect.collidepoint(get_mouse) and mouse.get_pressed()[0]:
            game_started = True
            zombie_list_in_game.clear()
            pivs_pavs.clear()
     
    elif game_started and game_play:
        keys = key.get_pressed()

        def zombie():
            global game_play
            for i in range(len(zombie_list_in_game) - 1, -1, -1):
                z = zombie_list_in_game[i]
                z.update()
                z.draw()
                if z.collides_with(playerrr.hitbox):
                    game_play = False
                if z.is_off_screen():
                    zombie_list_in_game.pop(i)
        zombie()
        current_time = time.get_ticks()

        def hodba():
            global player_anim_count, fon_x
            abc = False
            if keys[K_s or K_LEFT] and playerrr.hitbox.x > 50:
                playerrr.hitbox.x -= playerrr.speed
                sckrin.blit(walk_left[player_anim_count], (playerrr.hitbox.x, playerrr.hitbox.y))
                abc = True
            elif keys[K_w or K_RIGHT]:
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

        if level.update(fon_x):
            zombie_list_in_game.clear()
            pivs_pavs.clear()
            pulki = 15
            sckrin.blit(fon1, (0, 0))

        text_pulki = myfount.render(f'Bullets: {pulki}', True, (255, 255, 255))
        sckrin.blit(text_pulki, (2, 2))

        if current_time - last_shot_time > shoot_cooldown:
            shoot = True
        pipipipapapa(e)
         
    else:
        sckrin.fill((242, 4, 4))
        sckrin.blit(text_gameover, (245, 200))
        sckrin.blit(text_restart, restart_rect)
        get_mouse = mouse.get_pos()
        if restart_rect.collidepoint(get_mouse) and mouse.get_pressed()[0]:
            game_play = True
            player_x = 150
            zombie_list_in_game.clear()
            pivs_pavs.clear()
            shoot = True
            last_shot_time = 0
            fon_x = 0
            pulki = 10

    display.update() 
    clock.tick(30)
