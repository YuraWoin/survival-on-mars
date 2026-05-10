import pygame
import random

from image import walk, fon, fon1, zombie1, icon, myfount, piv_pav, fon_sounds, fon_on_mars, raketa, meteor, bida
from config_game import Player, Zombie, Strilba, Level, Meteor, RocketBullet, BioMaterial, Aptechka
from logik import *

clock = pygame.time.Clock()

pygame.init() 

pygame.display.set_caption("zombie apokalipsis beta") 
pygame.display.set_icon(icon)
HEIGHT = 460
WIDTH = 630
FPS = 30

sckrin = pygame.display.set_mode((WIDTH, HEIGHT))

zombie_timer = pygame.USEREVENT + 1
pygame.time.set_timer(zombie_timer, 5000) 

meteor_timer = pygame.USEREVENT + 2
pygame.time.set_timer(meteor_timer, 2000)

aptechka_timer = pygame.USEREVENT + 3
pygame.time.set_timer(aptechka_timer, 10000)

walk_left, walk_right = walk()

ending_lines = [
    "Біо матеріал зібрано...",
    "Але вчені не виходять на зв'язок...",
    "Продовження слідує... ",
    "(спойлер:до вчених дібрались...)",
    "Продовження в 2 частині"
]

mission_lines = [
    "Землі залишився менше одного року...",
    "Ваша місія — долетіти до Марсу...",
    "...та добути біо матеріал для вчених.",
    "щоб дізнатись що сталось з вченими",
    "пройдіть гру"
]

MISSION_LINE_DELAY = 2000

stars = [(random.randint(0, 630), random.randint(0, 460)) for _ in range(80)]

text_gameover = myfount.render('You Dead', False, 25)
text_restart = myfount.render('restart', False, 25)
text_start = myfount.render('start', False, 25)
restart_rect = text_restart.get_rect(topleft=(245, 300))
start_rect = text_restart.get_rect(topleft=(245, 300))

playerrr = Player(160, 337, sckrin, walk_right)
level = Level()
gs = GameState(sckrin)

def draw_space(sckrin, offset):
    sckrin.fill((0, 0, 0))
    for x, y in stars:
        draw_x = (x - offset) % 630
        pygame.draw.circle(sckrin, (255, 255, 255), (draw_x, y), 1)

keys = pygame.key.get_pressed()
current_time = pygame.time.get_ticks()

game_started = False
paused = False
ranning = True

dlyafonu = (5000 // 736) + 2

while ranning:
    for e in pygame.event.get():
        if e.type == meteor_timer and level.current == "space":
            gs.meteor_list.append(Meteor(random.randint(20, 600), -50, sckrin, meteor))
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                paused = not paused
        if e.type == pygame.QUIT:
            ranning = False
        if e.type == zombie_timer:
            gs.zombie_list_in_game.append(Zombie(740, 337, sckrin, zombie1)) 
        if e.type == aptechka_timer and level.current == "mars":
            gs.aptechka_list.append(Aptechka(random.randint(50, 580), 337, sckrin))
            pygame.time.set_timer(aptechka_timer, random.randint(8000, 15000))
        if game_started and gs.game_play and not paused:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and gs.pulki > 0 and gs.shoot:
                if level.current == "space":
                    gs.pivs_pavs.append(RocketBullet(playerrr.hitbox.x + 30, playerrr.hitbox.y + 10, sckrin))
                else:
                    gs.pivs_pavs.append(Strilba(playerrr.hitbox.x + 30, playerrr.hitbox.y + 10, sckrin, piv_pav))
                gs.pulki -= 1
                gs.shoot = False
                gs.last_shot_time = pygame.time.get_ticks()

    if paused:
        text_pause = myfount.render('PAUSE', True, (255, 255, 255))
        sckrin.blit(text_pause, (WIDTH // 2 - 40, HEIGHT // 2))
        pygame.display.update()
        clock.tick(30)
        continue

    if gs.game_state == "menu":
        sckrin.fill((0, 0, 0))
        text_start = myfount.render('START', True, (255, 255, 255))
        text_exit = myfount.render('EXIT', True, (255, 255, 255))
        exit_rect = text_exit.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        start_rect = text_start.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        sckrin.blit(text_start, start_rect)
        sckrin.blit(text_exit, exit_rect)
        get_mouse = pygame.mouse.get_pos()
        if start_rect.collidepoint(get_mouse) and pygame.mouse.get_pressed()[0]:
            gs.game_state = "mission"
            game_started = True
            gs.mission_line_timer = pygame.time.get_ticks()
            gs.mission_line_index = 0
            gs.zombie_list_in_game.clear()
            gs.pivs_pavs.clear()
            fon_sounds.play(loops=-1)
        if exit_rect.collidepoint(get_mouse) and pygame.mouse.get_pressed()[0]:
            ranning = False

    elif gs.game_state == "mission":
        sckrin.fill((0, 0, 0))
        current_time = pygame.time.get_ticks()
        for i in range(gs.mission_line_index + 1):
            text = myfount.render(mission_lines[i], True, (255, 255, 255))
            sckrin.blit(text, (40, 150 + i * 40))
        if current_time - gs.mission_line_timer > MISSION_LINE_DELAY:
            bida.play()
            gs.mission_line_timer = current_time
            gs.mission_line_index += 1
            if gs.mission_line_index >= len(mission_lines):
                gs.game_state = "playing"
                gs.mission_line_index = 0

    elif gs.game_state in ("playing", "ending") and gs.game_play:
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        
        if level.current == "space":
            bida.stop()
            gs.star_offset += 2
            draw_space(sckrin, gs.star_offset)
            # корабель
            sckrin.blit(raketa, (playerrr.hitbox.x, playerrr.hitbox.y))

            # метеорити
            for i in range(len(gs.meteor_list) - 1, -1, -1):
                m = gs.meteor_list[i]
                m.update()
                m.draw()
                if m.collides_with(playerrr.hitbox):
                    gs.game_play = False
                if not m.active:
                    gs.meteor_list.pop(i)

            # рух ракети
            if keys[pygame.K_a] and playerrr.hitbox.x > 20:
                playerrr.hitbox.x -= playerrr.speed
            if keys[pygame.K_d] and playerrr.hitbox.x < WIDTH - 80:
                playerrr.hitbox.x += playerrr.speed
            # прогрес
            level.update()
            gs.mars_start_time = pygame.time.get_ticks()
            progress = int((level.flight_progress / 1800) * 100)
            text_progress = myfount.render(f'До Марсу: {progress}%', True, (255, 255, 255))
            sckrin.blit(text_progress, (2, 2))
            gs.pipipipapapa(gs.meteor_list, level)

        elif level.current == "mars":
            fon_sounds.stop()
            for i in range(dlyafonu):
                sckrin.blit(fon_on_mars, (gs.fon_x + i * 736, 0))
            gs.pipipipapapa(gs.zombie_list_in_game, level)
            gs.zombie(playerrr, level)
            gs.hodba(keys, walk_left, walk_right, sckrin,playerrr)
            playerrr.update()

            gs.biomaterial(playerrr, sckrin)
            gs.aptechka(playerrr)

            text_pulki = myfount.render(f'Bullets: {gs.pulki}', True, (255, 255, 255))
            pygame.draw.rect(sckrin, (255, 0, 0), (2, 60, gs.hp * 1, 10))
            sckrin.blit(text_pulki, (2, 2))

            if gs.game_state == "ending":
                sckrin.fill((0, 0, 0))
                current_time = pygame.time.get_ticks()
                for i in range(gs.ending_index + 1):
                    text = myfount.render(ending_lines[i], True, (255, 255, 255))
                    sckrin.blit(text, (40, 150 + i * 40))
                    if current_time - gs.ending_timer > 2000:
                        gs.ending_timer = current_time
                        gs.ending_index += 1
                        if gs.ending_index >= len(ending_lines):
                            gs.ending_index = len(ending_lines) - 1 

            text_bio = myfount.render(f'Біо: {gs.bio_zibrano}/{gs.BIO_NEEDED}', True, (0, 255, 0))
            sckrin.blit(text_bio, (2, 35))

            if current_time - gs.last_shot_time > gs.shoot_cooldown:
                gs.shoot = True
            

    else:
        sckrin.fill((242, 4, 4))
        sckrin.blit(text_gameover, (245, 200))
        sckrin.blit(text_restart, restart_rect)
        get_mouse = pygame.mouse.get_pos()
        if restart_rect.collidepoint(get_mouse) and pygame.mouse.get_pressed()[0]:
            game_started = False
            gs.reset(playerrr, level)

    pygame.display.update() 
    clock.tick(FPS)

pygame.quit()
