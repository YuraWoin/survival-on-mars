import pygame 
pygame.init()

fon_on_mars = pygame.image.load('images/namars')
fon = pygame.image.load(r'images/fonforgame.jpg')
icon = pygame.image.load(r'images/gameone.jpg')
fon1 = pygame.image.load(r'images/home.png')
piv_pav = pygame.image.load('/home/yurawoin/YuraWoin/game/images/pulya.jpg')
fon_sounds = pygame.mixer.Sound(r'/home/yurawoin/YuraWoin/game/звуки/horror-rumble-winds-253834.mp3')




def walk():
    walk_left = [
        pygame.image.load('sprites/left/1.png'),
        pygame.image.load(r'sprites/left/2.png'),
        pygame.image.load(r'sprites/left/3.png'),
        pygame.image.load(r'sprites/left/4.png'),
    ]
    walk_right = [
        pygame.image.load(r'sprites/right/1.png'),
        pygame.image.load(r'sprites/right/2.png'),
        pygame.image.load(r'sprites/right/3.png'),
        pygame.image.load(r'sprites/right/4.png'),
    ]
    return walk_left, walk_right
walk()


