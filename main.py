import pygame
from threading import Timer
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
        self.gameover = False
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
        if self.gameover:
            self.yvel = 0
            self.xvel = 0
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
class LuckyBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        #========переменные только для lblock===============
        self.hitzonestart = x - PLATFORM_WIDTH/2
        self.hitzoneend = x+PLATFORM_WIDTH + PLATFORM_WIDTH/2
        self.hitzonebottom = y + PLATFORM_HEIGHT
        self.rooty = y
        self.isTouched = False
        #================debug======================
        if debug:
            print("[LB]Lucky Block spawned at " + str(self.hitzonestart) + ", " + str(self.hitzoneend))
            print("=============================")
        #==========переменные для платформ===============
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = pygame.image.load("mariosprites/lblock.png")
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    def touched(self, hero):
        #print("touched!")
        if hero.rect.x > self.hitzonestart and hero.rect.x < self.hitzoneend:
            if hero.rect.y == self.hitzonebottom or hero.rect.y == self.hitzonebottom+1:
                #self.rect.y = self.rect.y + 128
                self.isTouched = False
                new_gumba = Gumba(self.rect.x, self.rect.y - PLATFORM_HEIGHT)
                hero.rect.y = hero.rect.y + 6
                enemies.append(new_gumba)
                entities.add(new_gumba)
    def update(self):
        self.hitzonestart = self.rect.x - PLATFORM_WIDTH/2
        self.hitzoneend = self.rect.x+PLATFORM_WIDTH + PLATFORM_WIDTH/2
        self.hitzonebottom = self.rect.y + PLATFORM_HEIGHT

class Gumba(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos):
        super().__init__()
        self.image = pygame.image.load("mariosprites/gumba.png")
        self.xvel = 0
        self.yvel = 0
        self.rect = pygame.Rect(xPos, yPos, 32, 32)
        self.onGround = False
        self.animcounter = 0
    def collide(self, xvel, yvel, platforms, hero, window):
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
        if pygame.sprite.collide_rect(self, hero):
            if hero.rect.bottom != self.rect.top:
                hero.gameover = True
            if hero.rect.bottom == self.rect.top:
                pygame.transform.scale(self.image, (16, 32))
        
    def update(self, platforms, hero, window):
        self.animcounter += 1
        if self.animcounter == 60:
            self.image = pygame.transform.flip(self.image, True, False)
        if self.animcounter > 60:
            self.animcounter = 0
        if isMoving:
            self.xvel = speed
        else:
            self.xvel = speed/2
        if not self.onGround:
            self.yvel += gravity
        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, hero, window)
        self.rect.x -= self.xvel
        self.collide(self.xvel, 0, platforms, hero, window)
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        

#функция движения платформ (когда игрок выбрался за пределы карты)
def movelevel():
    if Figure.rect.x >= WIN_WIDTH / 2:
        for i in platforms:
            i.rect.x -= speed
            Figure.rect.x = WIN_WIDTH / 2 - 2
            isMoving = True
            window.blit(i.image, (i.rect.x, i.rect.y))
        for i in enemies:
            i.rect.x -= speed
            Figure.rect.x = WIN_WIDTH / 2 - 2
            isMoving = True
            window.blit(i.image, (i.rect.x, i.rect.y))
    if Figure.rect.x < 20:
        for i in platforms:
            i.rect.x += speed
            Figure.rect.x = 20 + 2
            isMoving = True
            window.blit(i.image, (i.rect.x, i.rect.y))
        for i in enemies:
            i.rect.x += speed
            Figure.rect.x = 20 + 2
            isMoving = True
            window.blit(i.image, (i.rect.x, i.rect.y))
    isMoving = False

def fileToConfig(file):
    f = open(file, "r")
    lines = f.readlines()
    configdict = {}
    for i in lines:
        values = i.split("=")
        key = values[0]
        if values[1].find('\n') == True:
            val = values[1][0:values[1].find('\n')]
        else:
            val = values[1]
        if key != "debug":
            val = float(val)
        else:
            if val == "True":
                val = True
            if val == "False":
                val = False
        if key != "gravity" and key != "debug":
            val = round(val)
            #print(val)
        configdict[key] = val
    return configdict
#цвета
Green = (0, 255, 0)
BGColor = (52, 174, 235)

#всякие вспомогательные функции и переменные
pygame.init()
pygame.key.set_repeat(20, 20)
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("RAM_PyMario")
Figure = Player(22, 150)
clock = pygame.time.Clock()

cfg = fileToConfig("game.cfg")

PLATFORM_WIDTH = cfg["PLATFORM_WIDTH"]
PLATFORM_HEIGHT = cfg["PLATFORM_HEIGHT"]
PLATFORM_COLOR = "#FF6262"

entities = pygame.sprite.Group()
platforms = []
lplatforms = []
enemies = []
entities.add(Figure)
gmcounter = 0

sysfont = pygame.font.Font("mariofont.ttf", 20)

#первый уровень
level1 = open("level1.txt", "r").readlines()
#переменные игрока
running = True
isMoving = False
debug = cfg["debug"]

speed = cfg["speed"]
JUMP_POWER = cfg["jump_power"]
gravity = cfg["gravity"]
plx = ply = 0
#================
if debug:
    print("\n==========RAM_PYMARIO==========")
    print("=============================")
    print("Current config:")
    print(cfg)
    print("=============================")
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
        if col == "?":
            lpf = LuckyBlock(plx, ply)
            lpf.image = pygame.image.load("mariosprites/lblock.png")
            entities.add(lpf)
            lplatforms.append(lpf)
            platforms.append(lpf)
        if col == ";":
            ngmb = Gumba(plx, ply)
            enemies.append(ngmb)
            entities.add(ngmb)
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
        if Figure.gameover == False:
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
    if debug:
        poslabel = sysfont.render(str(Figure.rect.x) + ", " + str(Figure.rect.y), False, (128, 0, 0))
    #=================================
    movelevel() #двигаем платформы
    #=================================
    for i in lplatforms:
        i.touched(Figure)
        i.update()
    for i in enemies:
        i.update(platforms, Figure, window)
    #window.blit(Figure.image, (Figure.x, Figure.y))
    #=================================
    #отрисовка
    window.blit(bg, (0, 0))
    if debug:
        window.blit(poslabel, (10, 32))
    Figure.update(Figure.mleft, Figure.mright, Figure.jmp, platforms)
    entities.draw(window)
    if Figure.gameover:
        gmcounter += 1
        gmlb_sur = sysfont.render("Game over!", False, (255, 0, 0))
        gmlb_sur_rect = gmlb_sur.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))
        window.fill((0, 0, 0))
        window.blit(gmlb_sur, gmlb_sur_rect)
        pygame.display.flip()
        if gmcounter == 60*5:
            running = False
    #конечные функции
    clock.tick(60)
    pygame.display.update()
pygame.quit() #ФИНАЛ
