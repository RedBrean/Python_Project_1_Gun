import math
from random import choice
import random
import numpy as np

import pygame

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

ANGRYA = 0.7
ANGRYVK = 1
HITA = 0
JK = 0.02
HITK = 0.5

GUNV = 5

PROB0 = 0.003
PROB1 = 0.06
PROB2 = 0.01
PROB3 = 0.001

BOSSLIVE = 10
#Классы

class Moveble():
    """Класс фигни которая умеет двигаться. Задается до 3 производной координаты"""
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.vx1 = 0
        self.vy1 = 0
        self.vx2 = 0
        self.vy2 = 0
    def MoveUpdate(self):
        """Двигается исходядя из заданных параметров"""
        self.vx1 += self.vx2
        self.vx += self.vx1
        self.x += self.vx
        self.vy1 += self.vy2
        self.vy += self.vy1
        self.y += self.vy

class Drawable():
    def __init__(self, screen):
        self.screen = screen
        
    def Draw(self, x, y, angle = 0, sufrace : pygame.Surface = None):
        """Отрисовывает объект в нужных координатах"""
        if(sufrace == None):
            sufrace = self.__GetSufrace()
        newSufr = pygame.transform.rotate(sufrace, angle)
        rect = newSufr.get_rect()
        rect.center = (x, y)
        self.screen.blit(newSufr, rect)

    def __GetSufrace(self, width = 500, hight = 500):
        """Почти что декоратор. Обрабатывает спрайт"""
        surf = pygame.surface.Surface((width, hight))
        surf.fill(WHITE)
        surf.set_colorkey(WHITE)
        self.GetSprite(surf, width//2, hight//2)
        surf = surf.convert_alpha()
        return surf
    
    def GetSprite(self, surf, x = 50, y = 50):
        """В surf нужно нарисовать спрайт"""
        pygame.draw.polygon(surf, RED, [(x+50, y+50), 
                                        (x+50, y-50),
                                         (x-50, y-50),
                                          (x-50, y+50)])

class Entity(Moveble, Drawable):

    def __init__(self, screen, x = 50, y = 50, colisionR = 0):
        Moveble.__init__(self, x, y)
        Drawable.__init__(self, screen)
        self.__an = 0 
        self.dangerous = True
        self.colisionR = colisionR
        self.revives = 1

    @property
    def an(self):
        return self.__an
    @an.setter
    def an(self, an):
        self.__an = an
    @property
    def anDeg(self):
        return self.an * 180/math.pi
    @anDeg.setter
    def anDeg(self, anDeg):
        self.an = anDeg/180 * math.pi 

    def Update(self):
        self.MoveUpdate()
        self.Draw(self.x, self.y, self.anDeg)

    def HitTest(self, obj):
        if((self.x - obj.x)**2 + (self.y - obj.y)**2)**0.5 <= (self.colisionR + obj.colisionR):
            return True
        else:
            return False
        
#Игровые классы
class Ball(Entity):
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        Entity.__init__(self, screen, x, y)
        self.r = 10
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.vy1 = 0.5
        self.colisionR = self.r
    def Update(self):
        Entity.Update(self)
        if (self.x >= 800):
            self.vx = -0.6*self.vx
            self.x = 799
        elif (self.x <= 0):
            self.vx = -0.6*self.vx
            self.x = 1
        if (self.y >= 600):
            self.vy *= -0.6
            self.y = 600
        if (self.y < 0):
            self.vy = -0.6*self.vy
            self.y = 0
        if (self.y > 599 and abs(self.vy) < 5):
            self.y = 600
            self.vy = 0

    def GetSprite(self, surf, x=50, y=50):
        pygame.draw.circle(surf, self.color, (x, y), self.r)
    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        return self.HitTest(obj)
    
class Bullet(Ball):
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        super().__init__(screen, x, y)
        self.vy1 = 0.1
    def Update(self):
        Entity.Update(self)
        self.an = -math.atan2(self.vy, self.vx)
        if (self.x >= 800):
            self.vx = 0
            self.vy = 0
            self.vy1 = 0.5
            self.x = 799
        elif (self.x <= 0):
            self.vx = 0
            self.vy = 0
            self.vy1 = 0.5
            self.x = 1
        elif (self.y >= 600):
            self.vx = 0
            self.vy = 0
            self.vy1 = 0.5
            self.y = 600
        elif (self.y < 0):
            self.vx = 0
            self.vy = 0
            self.vy1 = 0.5
            self.y = 0
        elif (self.y > 599 and abs(self.vy) < 5):
            self.y = 600
            self.vy = 0
    def GetSprite(self, surf, x=50, y=50):
        pygame.draw.polygon(surf, YELLOW, (
            (x-10, y+3),(x-10, y-3),(x+10, y)
        ))
class Gun(Entity):
    def __init__(self, screen, x = 40, y = 450):
        Entity.__init__(self, screen, x, y)
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.lives = 5
        self.score = 0
        self.dangerous = False
        self.ballType = 0
    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event, listBalls = None):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        if(listBalls == None):
            global entities
            listBalls = entities
        if(self.ballType == 0):
            ballClass = Ball
        elif(self.ballType == 1):
            ballClass = Bullet
        else:
            ballClass = Ball
        ballx = self.x + math.cos(self.an) * (15 + self.f2_power)
        bally = self.y - math.sin(self.an)*(15 + self.f2_power)
        new_ball = ballClass(self.screen, ballx, bally)
        new_ball.r = 15
        new_ball.vx = self.f2_power * math.cos(self.an) * 0.5
        new_ball.vy = -self.f2_power * math.sin(self.an) * 0.5
        listBalls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 50:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY
    
    def hittest(self, obj):
        if((self.x - obj.x)**2 + (self.y - obj.y)**2)**0.5 <= (self.f2_power + obj.r):
            return True

        return False
    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if (event.pos[0] != self.x):
                self.an = -math.atan((event.pos[1]-self.y) / (event.pos[0]-self.x))
            else: 
                self.an = math.pi/2
            if(event.pos[0]<self.x):
                self.an += math.pi

    def GetSprite(self, surf, x=50, y=50):
        length = self.f2_power * 1.2
        width = 2
        pygame.draw.polygon(surf, self.color, [(x, y+width), (x, y-width), (x+length, y-width), (x+length, y+width)])
        pygame.draw.circle(surf, GREY, (x, y), 12)

    def Update(self):
        super().Update()
        self.drawingAn = self.an * 180 / math.pi
        self.power_up()
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

class Target(Entity):
    def __init__(self, screen, revives = 1, score = 1):
        super().__init__(screen, 400, 500)
        self.new_target()
        self.colisionR = self.r
        self.revives = revives
        self.score = 1
    def new_target(self):
        """ Инициализация новой цели. """
        rnd = random.randint
        self.live = 1
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(2, 50)
        color = self.color = choice(GAME_COLORS)
    def GetSprite(self, surf, x=50, y=50):
        pygame.draw.circle(surf, self.color, (x, y), self.r)

class TargetRandom(Target):
    def new_target(self):
        Target.new_target(self)
        self.vx = 0
        self.vy = 0
        self.vx1 = 0
        self.vy1 = 0
    def Update(self):
        global HITA, HITK, JK

        self.vx2 = (random.random()-0.5)*JK 
        self.vy2 = (random.random()-0.5)*JK

        if (self.x >= 800):
            self.vx = -HITK*self.vx
            self.vx1 = -HITA
            self.x = 799
        elif (self.x <= 0):
            self.vx *= -HITK
            self.vx1 = HITA
            self.x = 1
        if (self.y >= 600):
            self.vy *= -HITK
            self.vy1 = -HITA
            self.y = 600
        if (self.y < 0):
            self.vy *= -HITK
            self.vy1 = HITA
            self.y = 0
        
        super().Update()

class TargetAngry(TargetRandom):
    def new_target(self):
        super().new_target()
        self.color = BLACK
    def Update(self):
        global HITA, HITK, JK, ANGRYA, ANGRYVK, gun
        dx = gun.x - self.x
        dy = gun.y - self.y
        dsum = (dx**2 + dy**2)**0.5
        self.an = -math.atan2(dy, dx)
        self.vx1 = ANGRYA*dx/dsum
        self.vy1 = ANGRYA*dy/dsum
        self.vx *= ANGRYVK
        self.vy *= ANGRYVK
        if (self.x >= 800):
            self.vx = -HITK*self.vx
            self.x = 799
        elif (self.x <= 0):
            self.vx *= -HITK
            self.x = 1
        if (self.y >= 600):
            self.vy *= -HITK
            self.y = 600
        if (self.y < 0):
            self.vy *= -HITK
            self.y = 0
        super().Update()
    def GetSprite(self, surf, x=50, y=50):
        pygame.draw.polygon(surf, YELLOW, (
            (x-2*self.r, y+self.r),(x-2*self.r, y-self.r),(x, y)))
        pygame.draw.circle(surf, self.color, (x, y), self.r)

class BOSS(TargetRandom):
    def __init__(self, screen):
        super().__init__(screen)
        self.live = 30
        self.r = 50
        self.colisionR = self.r
    def Update(self):
        global PROB0, PROB1, PROB2, entities
        shootProb = random.random()

        dx = gun.x - self.x
        dy = gun.y - self.y
        dsum = (dx**2 + dy**2)**0.5
        an = math.atan2(dy, dx)
        ballx = self.x + math.cos(an) * (15 + self.r)
        bally = self.y - math.sin(an)*(15 + self.r)

        if(shootProb<PROB0):
            ball = Ball(self.screen, ballx, bally)
            ball.vx = dx * 30 / dsum
            ball.vy = dy * 30 / dsum - dx/50
            entities.append(ball)
        elif(shootProb<(PROB1+PROB0)):
            ball = Bullet(self.screen, ballx, bally)
            ball.vx = dx * 30 / dsum
            ball.vy = dy * 30 / dsum - dx/500
            entities.append(ball)
        elif(shootProb<(PROB2+PROB1+PROB0)):
            newTarget = TargetAngry(self.screen, 1)
            newTarget.x = self.x
            newTarget.y = self.y
            entities.append(newTarget)
        elif(shootProb<(PROB3+PROB2+PROB1+PROB0)):
            ball = TargetRandom(self.screen, 1, 1)
            ball.x = ballx
            ball.y = bally
            ball.vx = dx * 30 / dsum
            ball.vy = dy * 30 / dsum 
            entities.append(ball)
        self.anDeg += 1
        super().Update()

    def GetSprite(self, surf, x=50, y=50):
        n = 7
        k = 1
        ls = list(np.linspace(0, 2*np.pi * (n-1)/n, n))
        angles = [(x+ self.r*k*math.cos(phi), y + self.r*k*math.sin(phi)) for phi in ls]
        pygame.draw.polygon(surf, (192, 251, 54), angles)
        n = 4
        k = 0.5
        ls = list(np.linspace(0, 2*np.pi * (n-1)/n, n))
        angles = [(x+ self.r*k*math.cos(phi), y + self.r*k*math.sin(phi)) for phi in ls]
        pygame.draw.polygon(surf, (13, 57, 12), angles)



def Main():
    balls = list(filter(lambda x: isinstance(x, Ball), entities))
    targets = list(filter(lambda x: isinstance(x, Target), entities))

    for b in balls:
        if(b.y > 590 and b.vy == 0):
            b.revives = 0

    for b in balls:
        for target in targets:
            if b.hittest(target) and target.live:
                target.live -= 1
                gun.score += 1
                if(target.live == 0):
                    target.new_target()
                    target.revives -= 1
    
    for entity in targets:
        if(gun.HitTest(entity) and entity.dangerous):
            gun.lives -= 1
            entity.new_target()

    for b in balls:
        if(gun.hittest(b)):
            gun.lives -= 1
            entities.remove(b)

    for entity in entities:
        if(gun.HitTest(entity) and entity.dangerous):
            gun.lives -= 1
            gun.x -= (entity.x > gun.x) * (entity.colisionR + gun.colisionR)
            gun.y -= (entity.y > gun.y) * (entity.colisionR + gun.colisionR)

    for entity in entities:
        if(entity.revives <= 0):
            entities.remove(entity)
    global win, finished
    if (len(targets) == 0):
        win = True
        finished = True

    if (gun.lives <= 0):
        win = False
        finished = True


    
    img = font.render(f"Балл: {gun.score} Жизни: {gun.lives} Тип снаряда: {gun.ballType}", True, 0)
    
    bossLineSurfB = pygame.Surface((300, 5))
    bossLineSurfR = pygame.Surface((boss.live/BOSSLIVE*300, 5))
    bossLineSurfR.fill(RED)
    bossLineRect = pygame.Rect((100, 100), (300, 100))
    
    screen.blit(bossLineSurfB, bossLineRect)
    if(boss.live > 1):
        screen.blit(bossLineSurfR, bossLineRect)
    elif(entities.__contains__(boss)):
        entities.remove(boss)
    screen.blit(img, (20, 20))
    
    reviveList = []
    for entity in entities:
        reviveList.append(entity.revives)

    for entity in entities:
        entity.Update()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()



entities = []

gun = Gun(screen, 40, 450)
entities.append(gun)
entities.append(Target(screen, 0))
entities.append(TargetRandom(screen, 0))
entities.append(TargetAngry(screen, 0))
boss = BOSS(screen)
boss.live = BOSSLIVE
entities.append(boss)
font = pygame.font.SysFont(None, 30)

finished = False
realyFinished = False
win = False

while not finished:
    screen.fill(WHITE)
    Main()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                gun.vx = -1 * GUNV
            elif event.key == pygame.K_d:
                gun.vx = 1 * GUNV
            elif event.key == pygame.K_w:
                gun.vy = -1 * GUNV
            elif event.key == pygame.K_s:
                gun.vy = 1 * GUNV
            elif event.key == pygame.K_1:
                gun.ballType = 0
            elif event.key == pygame.K_2:
                gun.ballType = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                gun.vx = 0
            elif event.key == pygame.K_d:
                gun.vx = 0
            elif event.key == pygame.K_w:
                gun.vy = 0
            elif event.key == pygame.K_s:
                gun.vy = 0

    clock.tick(FPS)
    pygame.display.update()

while not realyFinished:
    if (win):
        screen.fill(GREEN)
        text = font.render("ТЫ НЕ ПРОИГРАЛ!", True, 0)
    else:
        screen.fill(RED)
        text = font.render("СДОХ", True, 0)

    rect = text.get_rect()
    rect.center = (400,300)
    screen.blit(text, rect)

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            realyFinished = True
            pygame.quit()


pygame.quit()
