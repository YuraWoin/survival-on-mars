import pygame
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
        self.current = 1
        self.distance = 0        
        self.in_house = False   

    def update(self, fon_x):
        self.distance = abs(fon_x)
        if self.distance >= 5000 and not self.in_house:
            self.in_house = True
            return True     
        return False

