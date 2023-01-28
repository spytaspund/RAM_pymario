import pygame
from time import sleep

WIN_WIDTH = 640
WIN_HEIGHT = 480
class Player(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos):
        super().__init__()
        self.image = pygame.image.load("mariosprites\mario32x32.png")
        self.x = xPos
        self.y = yPos
        self.xvel = 0
        self.mleft = False
        self.mright = False
        self.jmp = False
        self.yvel = 0
        self.onGround = False
        self.animLeft = False
        self.animRight = True
        self.rect = pygame.Rect(self.x, self.y, 32, 32)

    def update(self, left, right, up, platforms):
        if left:
            self.xvel = -speed
        if right:
            #self.xvel = speed
            self.xvel = speed
        if up:
            if self.onGround:
                self.yvel = -JUMP_POWER
        if not(left or right):
            self.xvel = 0
        if not self.onGround:
            self.yvel += gravity
        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = pygame.image.load("mariosprites/brick.png")
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

#функция движения платформ (когда игрок выбрался за пределы карты)
def movelevel():
    platformsmoved = 0
    for i in platforms:
        if Figure.rect.x > WIN_WIDTH:
            i.rect.x = i.rect.x - WIN_WIDTH
            window.blit(i.image, (i.rect.x, i.rect.y))
            platformsmoved = platformsmoved + 1
        if platformsmoved >= len(platforms):
            Figure.rect.x = 0

#цвета
Green = (0, 255, 0)
BGColor = (52, 174, 235)

#всякие вспомогательные функции и переменные
pygame.init()
pygame.key.set_repeat(20, 20)
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
Figure = Player(0, 150)
clock = pygame.time.Clock()

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"

entities = pygame.sprite.Group()
platforms = []
entities.add(Figure)

#первый уровень
level1 = [
    "--------------------------------------",
    "                    ",
    "                    ",
    " ---               ",
    "  ----             ",
    "                    ",
    "--------   ---------",
    "                    ",
    "                    ",
    "   ---              ",
    "   - -              ",
    "   ---     --         ",
    "   - -              ",
    "                    ",
    "----------------------------------------"
    ]
#переменные игрока
running = True
speed = 3
JUMP_POWER = 10
gravity = 0.35
plx = ply = 0
#================
#генератор уровня (считывает двумерный массив и отрисовывает платформы в соответствии с ним)
for row in level1:
    for col in row:
        if col == "-":
            #pf = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
            pf = Platform(plx, ply)
            #pf.fill(pygame.Color(PLATFORM_COLOR))
            pf.image = pygame.image.load("mariosprites/brick.png")
            entities.add(pf)
            platforms.append(pf)
        plx += PLATFORM_WIDTH
    ply += PLATFORM_HEIGHT
    plx = 0
#фон
bg = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
bg.fill(pygame.Color(BGColor))
#=========
#основной цикл
while running:
    #window.fill(BGColor)
    #обработка нажатий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not Figure.animLeft:
                    Figure.image = pygame.transform.flip(Figure.image, True, False)
                    Figure.animLeft = True
                    Figure.animRight = False
                #Figure.image = pygame.transform.flip(Figure.image, True, False)
                Figure.mleft = True
            if event.key == pygame.K_RIGHT:
                if not Figure.animRight:
                    Figure.image = pygame.transform.flip(Figure.image, True, False)
                    Figure.animRight = True
                    Figure.animLeft = False
                #Figure.image = pygame.transform.flip(Figure.image, True, False)
                Figure.mright = True
            if event.key == pygame.K_SPACE:
                Figure.jmp = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                Figure.mleft = False
            if event.key == pygame.K_RIGHT:
                Figure.mright = False
            if event.key == pygame.K_SPACE:
                Figure.jmp = False
    #=================================
    movelevel() #двигаем платформы
    
    #window.blit(Figure.image, (Figure.x, Figure.y))
    #=================================
    #отрисовка
    window.blit(bg, (0, 0))
    Figure.update(Figure.mleft, Figure.mright, Figure.jmp, platforms)
    entities.draw(window)

    #конечные функции
    clock.tick(60)
    pygame.display.update()
pygame.quit() #ФИНАЛ
