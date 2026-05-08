import pygame 
pygame.init()

fon_on_mars = pygame.image.load('images/geminifonresize.png')
fon = pygame.image.load('images/geminifonresize.png')
icon = pygame.image.load('images/gameone.jpg')
fon1 = pygame.image.load('images/home.png')
piv_pav = pygame.image.load('images/pulya.jpg')

biomaterial = pygame.image.load('images/biomaterial.png')

# fon_sounds = pygame.mixer.Sound('звуки/far-roket-rumble_fyzenym4u.mp3')
fon_sounds = pygame.mixer.Sound('sounds/raketa.mp3')

zombie1 = pygame.image.load('images/chasing.png')
pygame.font.init()
myfount = pygame.font.SysFont('Arial', 30)
meteor = pygame.image.load('images/pixil-frame-0.png')
raketa = pygame.image.load('images/raketa.png')

def walk():
    walk_left = [
        pygame.image.load('sprites/left/1.png'),
        pygame.image.load('sprites/left/2.png'),
        pygame.image.load('sprites/left/3.png'),
        pygame.image.load('sprites/left/4.png'),
    ]
    walk_right = [
        pygame.image.load('sprites/right/1.png'),
        pygame.image.load('sprites/right/2.png'),
        pygame.image.load('sprites/right/3.png'),
        pygame.image.load('sprites/right/4.png'),
    ]
    return walk_left, walk_right
walk()


