import pygame
import random

pygame.init()

win = pygame.display.set_mode((600, 570))
pygame.display.set_caption('My Mario Game')

bg = pygame.image.load('mariobg.png').convert()
bgX = 0
bgX2 = bg.get_width()

walkRight = [pygame.image.load('mario1.png'), pygame.image.load('mario2.png'), pygame.image.load('mario3.png'),
             pygame.image.load('mario4.png')]
walkLeft = [pygame.image.load('mario5.png'), pygame.image.load('mario6.png'), pygame.image.load('mario7.png'),
            pygame.image.load('mario8.png')]
jump = [pygame.image.load('jump1.png'), pygame.image.load('jump2.png'), pygame.image.load('jump3.png'),
            pygame.image.load('jump4.png'), pygame.image.load('jump5.png'), pygame.image.load('jump6.png'),
            pygame.image.load('jump7.png')]
jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,
            -2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,
            -4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]
home = pygame.image.load('homescreen.png').convert()
clock = pygame.time.Clock()

class player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 0.01
        self.isJump = False
        self.jumpCount = 10
        self.walkCount = 0
        self.standing = True
        self.left = False
        self.right = False
        #self.hitbox = (self.x + 13, self.y + 9, 29, 52)
        self.hitbox = (self.x, self.y, 29, 52)

    def draw(self, win):
        if self.isJump:
            self.y -= jumpList[self.jumpCount] * 1.2
            win.blit(pygame.transform.scale(jump[self.jumpCount//18], (64,64)), (self.x,self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.isJump = False
                self.runCount = 0

        if self.walkCount >= 32:
           self.walkCount = 0

        if not self.standing:
            if self.left:
                win.blit(pygame.transform.scale(walkLeft[self.walkCount//8], (64, 64)), (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(pygame.transform.scale(walkRight[self.walkCount//8], (64, 64)), (self.x, self.y))
                self.walkCount += 1
        else:
            if self.left:
                win.blit(pygame.transform.scale(walkLeft[0], (64, 64)), (self.x, self.y))
            else:
                win.blit(pygame.transform.scale(walkRight[0], (64, 64)), (self.x, self.y))
        self.hitbox = (self.x, self.y, 29, 52)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('Game Over', 1, (255, 0, 0))
        win.blit(text, (250 - (text.get_width() / 2), 200))
        pygame.display.update()
        global gameover
        gameover = True
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

class obstacle:
    ob1 = pygame.image.load('obstacle1.png')

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x + 5, self.y + 3, 32, 52)

    def draw(self, win):
        self.hitbox = (self.x + 5, self.y + 3, 32, 52)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        win.blit(pygame.transform.scale(self.ob1, (44, 44)), (self.x, self.y))

class obstacle1(obstacle):
    ob2 = pygame.image.load('obstacle2.png')

    def draw(self, win):
        self.hitbox = (self.x + 5, self.y + 3, 32, 52)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        win.blit(pygame.transform.scale(self.ob2, (44, 44)), (self.x, self.y))

class obstacle3(obstacle):
    ob3 = pygame.image.load('brick.png')

    def draw(self, win):
        self.hitbox = (self.x + 5, self.y + 3, 32, 52)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        win.blit(pygame.transform.scale(self.ob3, (44, 44)), (self.x, self.y))

class brick:
    b1 = pygame.image.load('brick.png')

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x + 5, self.y + 3, 32, 52)

    def draw(self, win):
        self.hitbox = (self.x + 5, self.y + 3, 32, 52)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        win.blit(pygame.transform.scale(self.b1, (44, 44)), (self.x, self.y))

class enemy:
    e = pygame.image.load('enemy2.png')

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 0.5
        self.visible = True
        self.hitbox = (self.x + 10, self.y + 4, 32, 52)

    def draw(self, win):
        if self.visible:
            self.move()
            win.blit(pygame.transform.scale(self.e, (44, 44)), (self.x, self.y))
            self.hitbox = (self.x + 7, self.y + 4, 32, 52)
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
     self.x -= self.velocity

    def hit(self):
        self.visible = False

class enemy1(enemy):
    e1 = pygame.image.load('enemy1.png')

    def draw(self, win):
        if self.visible:
            self.move()
            win.blit(pygame.transform.scale(self.e1, (44, 44)), (self.x, self.y))
            self.hitbox = (self.x + 7, self.y + 4, 32, 52)
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

class projectile:
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.velocity = 1*facing

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

def redraw():
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2, 0))
    man.draw(win)
    for obj in objects:
        obj.draw(win)
    for b in bricks:
        b.draw(win)
    for ene in enemies:
        ene.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

def home_screen():
    run = True
    while run:
        win.blit(pygame.transform.scale(home, (600, 570)), (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            run = False
        pygame.display.update()
        clock.tick(30)

home_screen()

man = player(100, 390, 64, 64)
objects = []
bullets = []
enemies = []
bricks = []
shootLoop = 0
pygame.time.set_timer(pygame.USEREVENT+2, random.randrange(2000, 4000))
pygame.time.set_timer(pygame.USEREVENT+3, random.randrange(2000, 4000))

#mainloop
gameover = False
run = True
while run:

    if gameover == True:
        win.blit(pygame.transform.scale(home, (600, 570)), (0, 0))
        #font1 = pygame.font.SysFont(None, 40)
        #text = font1.render('Press Enter to Play', 1, (255, 255, 255))
        #win.blit(text, (180, 425))
        pygame.display.update()
        man.__init__(100, 390, 64, 64)
        for obj in objects:
            obj.__init__(810, 410, 44, 44)
        for b in bricks:
            b.__init__(810, 410, 44, 44)
        for ene in enemies:
            ene.__init__(810, 410, 44, 44)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            gameover = False

    else:
        redraw()
        clock.tick(100)

        for obj in objects:
            if man.hitbox[1] < obj.hitbox[1] + obj.hitbox[3] and man.hitbox[1] + man.hitbox[3] > obj.hitbox[1]:
                if man.hitbox[0] < obj.hitbox[0] + obj.hitbox[2] and man.hitbox[0] + man.hitbox[3] > obj.hitbox[0]:
                    man.hit()

        for ene in enemies:
            if ene.visible:
                if man.hitbox[1] < ene.hitbox[1] + ene.hitbox[3] and man.hitbox[1] + man.hitbox[3] > ene.hitbox[1]:
                    if man.hitbox[0] < ene.hitbox[0] + ene.hitbox[2] and man.hitbox[0] + man.hitbox[3] > ene.hitbox[0]:
                        man.hit()

        for bullet in bullets:
            for ene in enemies:
                if bullet.y - bullet.radius < ene.hitbox[1] + ene.hitbox[3] and bullet.y + bullet.radius > ene.hitbox[1]:
                    if bullet.x - bullet.radius < ene.hitbox[0] + ene.hitbox[2] and bullet.x + bullet.radius > ene.hitbox[0]:
                        if ene.visible:
                            ene.hit()
                            bullets.remove(bullet)
                if bullet.x < 500 and bullet.x > 0:
                    bullet.x += bullet.velocity
                else:
                    if bullet in bullets:
                        bullets.remove(bullet)

        if shootLoop > 0:
            shootLoop += 1
        if shootLoop > 3:
            shootLoop = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.USEREVENT+2:
                r = random.randrange(0, 2)
                if r == 0:
                    objects.append(obstacle(810, 410, 44, 44))
                elif r == 1:
                    objects.append(obstacle(810, 410, 44, 44))
                else:
                    objects.append(obstacle1(810, 410, 44, 44))

            if event.type == pygame.USEREVENT+4:
                r = random.randrange(0, 2)
                if r == 0:
                    bricks.append(brick(810, 410, 44, 44))
                else:
                    bricks.append(brick(810, 410, 44, 44))

            if event.type == pygame.USEREVENT+3:
                r = random.randrange(0, 2)
                if r == 0:
                    enemies.append(enemy(810, 410, 44, 44))
                else:
                    enemies.append(enemy1(810, 410, 44, 44))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and shootLoop == 0:
            if man.left:
                facing = -1
            else:
                facing = 1
            if len(bullets) < 5:
                bullets.append(projectile(round(man.x + man.width//2), round(man.y + man.height//2), 6, (0, 0 ,0), facing))
                shootLoop = 1

        if keys[pygame.K_RIGHT]:
            bgX -= 1.4
            bgX2 -= 1.4
            if bgX < bg.get_width() * -1:
                bgX = bg.get_width()
            if bgX2 < bg.get_width() * -1:
                bgX2 = bg.get_width()

            for obj in objects:
                obj.x -= 1.4
                if obj.x < obj.width * -1:
                    objects.remove(obj)

            for b in bricks:
                b.x -= 1.4
                if b.x < b.width * -1:
                    bricks.remove(b)

            for ene in enemies:
                ene.x -= 1.4
                if ene.x < ene.width * -1:
                    enemies.remove(ene)

            man.x += man.velocity
            man.left = False
            man.right = True
            man.standing = False

        elif keys[pygame.K_LEFT]:
            man.x -= man.velocity
            man.left = True
            man.right = False
            man.standing = False

        else:
            man.standing = True
            man.walkCount = 0

        if man.isJump == False:
            if keys[pygame.K_UP]:
                    man.isJump = True
                    man.walkCount = 0
        '''else:
            if man.jumpCount >= -10:
                neg = 1
                if man.jumpCount < 0:
                    neg = -1
                man.y -= (man.jumpCount ** 2) * 0.5 * neg
                man.jumpCount -= 1

            else:
                man.isJump = False
                man.jumpCount = 10'''
