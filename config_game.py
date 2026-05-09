import pygame
import random
from image import * 

class Player:
    def __init__(self, x, y, sckrin, walk_right):
        self.sckrin = sckrin
        self.image = walk_right[0]
        self.max_y = y
        self.hitbox = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.velocity = 0
        self.gravity = 0.7
        self.in_air = False
        self.speed = 5
        

    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE] and not self.in_air:
            self.velocity = 15
            self.in_air = True
        if self.in_air:
            self.hitbox.y -= self.velocity
            self.velocity -= self.gravity
            if self.hitbox.y >= self.max_y:
                self.in_air = False
                self.hitbox.y = self.max_y
    def draw(self):
        self.sckrin.blit(self.image, (self.hitbox.x, self.hitbox.y))

class Zombie:
    def __init__(self, x, y, sckrin, zombie_image):
        self.sckrin = sckrin
        self.image = zombie_image
        self.hitbox = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.speed = 10
        

    def update(self):
        self.hitbox.x -= self.speed
    def draw(self):
        self.sckrin.blit(self.image, (self.hitbox.x, self.hitbox.y))

    def is_off_screen(self):
        return self.hitbox.x < -10

    def collides_with(self, other_rect):
        return self.hitbox.colliderect(other_rect)



class Strilba:
    def __init__(self, x, y, sckrin, image):
        self.sckrin = sckrin
        self.image = image
        self.hitbox = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.speed = 10
        self.active = True
        

    def update(self):
        self.hitbox.x += self.speed
        if self.hitbox.x > 736:
            self.active = False

    def draw(self):
        self.sckrin.blit(self.image, (self.hitbox.x, self.hitbox.y))

    def collides_with(self, other_rect):
        return self.hitbox.colliderect(other_rect)



class Level:
    def __init__(self):
        #ПОТІМ ПОМІНЯТИ НА "space"
        self.current = "space"
        #ПОТІМ ПОМІНЯТИ НА "space"
        self.flight_progress = 0

    def update(self, fon_x=0):
        if self.current == "space":
            self.flight_progress += 1
            if self.flight_progress >= 1800:
                self.current = "mars"
                return True
        return False






class Meteor:
    def __init__(self, x, y, sckrin, image):
        self.sckrin = sckrin
        self.image = image
        self.hitbox = pygame.Rect(x, y, 15, 15)
        self.speed = random.randint(3, 7)
        self.active = True

    def update(self):
        self.hitbox.y += self.speed
        if self.hitbox.y > 500:
            self.active = False

    def draw(self):
        self.sckrin.blit(self.image, (self.hitbox.x, self.hitbox.y))

    def collides_with(self, other_rect):
        return self.hitbox.colliderect(other_rect)
    


class RocketBullet:
    def __init__(self, x, y, sckrin):
        self.sckrin = sckrin
        self.hitbox = pygame.Rect(x + 15, y + 10, 20, 50)
        self.speed = 12
        self.active = True

    def update(self):
        self.hitbox.y -= self.speed
        if self.hitbox.y < -20:
            self.active = False

    def draw(self):
        pygame.draw.rect(self.sckrin, (255, 140, 0), self.hitbox)  # помаранчева

    def collides_with(self, other_rect):
        return self.hitbox.colliderect(other_rect)
    


class BioMaterial:
    def __init__(self, x, y, sckrin):
        self.sckrin = sckrin
        self.image = biomaterial
        self.hitbox = pygame.Rect(x, y, 20, 20)
        self.active = True

    def draw(self):
        self.sckrin.blit(self.image, (self.hitbox.x, self.hitbox.y))

    def collides_with(self, other_rect):
        return self.hitbox.colliderect(other_rect)
    
class Aptechka:
    def __init__(self, x, y, sckrin):
        self.sckrin = sckrin
        self.hitbox = pygame.Rect(x, y, 50, 50)
        self.active = True

    def draw(self):
        pygame.draw.rect(self.sckrin, (255, 50, 50), self.hitbox)
        pygame.draw.rect(self.sckrin, (255, 255, 255), (self.hitbox.x + 8, self.hitbox.y + 4, 4, 12))
        pygame.draw.rect(self.sckrin, (255, 255, 255), (self.hitbox.x + 4, self.hitbox.y + 8, 12, 4))

    def collides_with(self, other_rect):
        return self.hitbox.colliderect(other_rect)