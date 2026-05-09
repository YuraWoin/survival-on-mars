import pygame
import random
from config_game import BioMaterial, Aptechka, Strilba, RocketBullet

class GameState:
    def __init__(self, sckrin):
        self.sckrin = sckrin
        self.pivs_pavs = []
        self.zombie_list_in_game = []
        self.meteor_list = []
        self.bio_list = []
        self.aptechka_list = []
        self.bio_zibrano = 0
        self.BIO_NEEDED = 5
        self.hp = 100
        self.pulki = 10
        self.shoot = True
        self.last_shot_time = 0
        self.shoot_cooldown = 500
        self.fon_x = 0
        self.star_offset = 0
        self.mars_start_time = 0
        self.player_anim_count = 0
        self.game_play = True
        self.game_state = "menu"
        self.ending_index = 0
        self.ending_timer = 0
        self.mission_line_index = 0
        self.mission_line_timer = 0

    def reset(self, playerrr, level):
        self.pivs_pavs.clear()
        self.zombie_list_in_game.clear()
        self.meteor_list.clear()
        self.bio_list.clear()
        self.aptechka_list.clear()
        self.bio_zibrano = 0
        self.hp = 100
        self.pulki = 10
        self.shoot = True
        self.last_shot_time = 0
        self.fon_x = 0
        self.star_offset = 0
        self.game_play = True
        self.game_state = "playing"
        self.ending_index = 0
        self.ending_timer = 0 
        playerrr.hitbox.x = 160
        playerrr.hitbox.y = 337
        level.__init__()

    def pipipipapapa(self, targets, level):
        for i in range(len(self.pivs_pavs) - 1, -1, -1):
            b = self.pivs_pavs[i]
            b.update()
            b.draw()
            hit = False
            for j in range(len(targets) - 1, -1, -1):
                if b.collides_with(targets[j].hitbox):
                    dead = targets.pop(j)
                    if level.current == "mars":
                        self.bio_list.append(BioMaterial(dead.hitbox.x, dead.hitbox.y, self.sckrin))
                        if random.randint(1, 5) == 1:
                            self.aptechka_list.append(Aptechka(dead.hitbox.x, dead.hitbox.y, self.sckrin))
                    self.pivs_pavs.pop(i)
                    hit = True
                    break
            if not hit and not b.active:
                self.pivs_pavs.pop(i)

    def shoot_bullet(self, playerrr, level, piv_pav):
        if self.pulki > 0 and self.shoot:
            if level.current == "space":
                self.pivs_pavs.append(RocketBullet(playerrr.hitbox.x + 30, playerrr.hitbox.y + 10, self.sckrin))
            else:
                self.pivs_pavs.append(Strilba(playerrr.hitbox.x + 30, playerrr.hitbox.y + 10, self.sckrin, piv_pav))
            self.pulki -= 1
            self.shoot = False
            self.last_shot_time = pygame.time.get_ticks()

    def hodba(self, keys, walk_left, walk_right, sckrin, playerrr):
        sckrin.blit(walk_right[self.player_anim_count], (playerrr.hitbox.x, playerrr.hitbox.y))
        if keys[pygame.K_s] and playerrr.hitbox.x > 50:
            playerrr.hitbox.x -= playerrr.speed
            sckrin.blit(walk_left[self.player_anim_count], (playerrr.hitbox.x, playerrr.hitbox.y))
            self.player_anim_count += 1
            if self.player_anim_count >= len(walk_right):
                self.player_anim_count = 0
        elif keys[pygame.K_w]:
            if playerrr.hitbox.x >= 450 and self.fon_x > -5100:
                self.fon_x -= playerrr.speed
            elif playerrr.hitbox.x < 450:
                playerrr.hitbox.x += playerrr.speed
                sckrin.blit(walk_right[self.player_anim_count], (playerrr.hitbox.x, playerrr.hitbox.y))
            else:
                sckrin.blit(walk_right[0], (playerrr.hitbox.x, playerrr.hitbox.y))
                self.player_anim_count = 0
            self.player_anim_count += 1
            if self.player_anim_count >= len(walk_right):
                self.player_anim_count = 0

    def zombie(self, playerrr, level):
        if pygame.time.get_ticks() - self.mars_start_time < 10000:
            return
        for i in range(len(self.zombie_list_in_game) - 1, -1, -1):
            zombak = self.zombie_list_in_game[i]
            zombak.update()
            zombak.draw()
            if zombak.collides_with(playerrr.hitbox):
                self.hp -= 25
                self.zombie_list_in_game.pop(i)
                if self.hp <= 0:
                    self.game_play = False
                break
            if zombak.is_off_screen():
                self.zombie_list_in_game.pop(i)

    def biomaterial(self, playerrr, sckrin):
        for i in range(len(self.bio_list) - 1, -1, -1):
            b = self.bio_list[i]
            b.draw()
            if b.collides_with(playerrr.hitbox):
                self.bio_list.pop(i)
                self.bio_zibrano += 1
                if self.bio_zibrano >= self.BIO_NEEDED:
                    self.game_state = "ending"
                    self.ending_timer = pygame.time.get_ticks()
                    self.ending_index = 0

    def aptechka(self, playerrr):
        for i in range(len(self.aptechka_list) - 1, -1, -1):
            a = self.aptechka_list[i]
            a.draw()
            if a.collides_with(playerrr.hitbox):
                self.aptechka_list.pop(i)
                self.hp = min(100, self.hp + 30)