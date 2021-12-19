# Source Generated with Decompyle++
# File: typingv4.pyc (Python 3.9)

import pygame
import random
import time
import math
pygame.init()
pygame.mixer.init()
typeSound = pygame.mixer.Sound('type.mp3')
boomSound = pygame.mixer.Sound('boom.mp3')
bgm = pygame.mixer.Sound('RAIN.mp3')
start = False
over = False
numList = []
direction = [
    'top',
    'right',
    'bottom',
    'left']
win = pygame.display.set_mode((800, 600))
LETTER_FONT = pygame.font.SysFont('cosmicsans', 40)
a = 97
ltrId = 0

i = 0
FALL = pygame.USEREVENT
score = 0
life = 10
limit = 200
alphabet = [25]
for b in range(25):
    alphabet.append(b)
for i in range(1,6): #メニューのオプションの位置
    x = 120 + 90 * i#xの座標
    y = 250 #初めてのY座標はすべて同じだ。
    numList .append([x,y,i+48])
randarr = random.sample(alphabet, 26)
letters = []

class Letter:
    
    def __init__(self, ltrId, direction):
        self.x = 0
        self.y = 0
        self.ltrId = ltrId
        self.ltr = a + randarr[ltrId % 25]
        self.visible = True
        self.direction = direction
        self.speed = random.randrange(1, 3)
        self.color = 'white'
        self.init()

    
    def init(self):
        if self.direction == 'top':
            self.x = random.randrange(20, 750)
            self.y = 0
        elif self.direction == 'right':
            self.x = 750
            self.y = random.randrange(20, 550)
        elif self.direction == 'bottom':
            self.x = random.randrange(20, 750)
            self.y = 550
        elif self.direction == 'left':
            self.x = 0
            self.y = random.randrange(20, 550)
        randomNum = random.randrange(1, 101)
        if randomNum <= 10:
            self.color = 'blue'
        if randomNum <= 2:
            self.color = 'red'

    
    def move(self):
        if self.direction == 'top':
            self.y = self.y + self.speed
        elif self.direction == 'right':
            self.x = self.x - self.speed
        elif self.direction == 'bottom':
            self.y = self.y - self.speed
        elif self.direction == 'left':
            self.x = self.x + self.speed

    
    def draw(self, win):
        if self.visible == True:
            if self.color == 'blue':
                text = LETTER_FONT.render(chr(self.ltr - 32), 1, (0, 200, 255))
            elif self.color == 'red':
                text = LETTER_FONT.render(chr(self.ltr - 32), 1, (255, 100, 100))
            else:
                text = LETTER_FONT.render(chr(self.ltr - 32), 1, (255, 255, 255))
            win.blit(text, (self.x, self.y))

    
    def getSlow(self):
        self.speed = 0.3



def drawmenu():
    win.fill((0, 0, 0))
    for n in numList:
        x,y,num = n#x,y,numはそれぞれnの要素に対応する
        pygame.draw.circle(win,(255,255,255),(x,y),20,3)#オプションの円を見せる(どこにレンダー、色、座標、サイズ、重さ)
        levelnum = LETTER_FONT.render(chr(num),1,(255,255,255))#レベル数字のレンダリング
        win.blit(levelnum,(x-7,y-12))#レベル数字を見せる
    intro = LETTER_FONT.render("What's your level of typing?", 1, (255, 255, 255))
    win.blit(intro, (210, 100))
    pygame.display.update()


def draw():
    win.fill((0, 0, 0))
    lifeText = LETTER_FONT.render(str(life), 1, (255, 255, 255))
    scoreText = LETTER_FONT.render(str(score), 1, (255, 255, 255))
    restartText = LETTER_FONT.render('Play Again', 1, (255, 255, 255))
    win.blit(lifeText, (765, 10))
    win.blit(scoreText, (20, 10))
    for l in letters:#ローマ字を一つずづ生成する
        l.draw(win) 
    if over == True:
        text = LETTER_FONT.render('GAME OVER', 1, (255, 255, 255))
        text2 = LETTER_FONT.render('YOU GOT', 1, (255, 255, 255))
        win.blit(text, (315, 250))
        win.blit(text2, (290, 290))
        win.blit(scoreText, (450, 290))
        win.blit(restartText, (330, 380))
        pygame.draw.rect(win, (255, 255, 255), (300, 368, 200, 50), 1)
    pygame.display.update()

l = Letter(0, random.choice(direction))
run = True
bgm.set_volume(0.12)
bgm.play()
boomSound.set_volume(0.3)
typeSound.set_volume(1)


while run:
    pygame.time.delay(10)
    for event in pygame.event.get():#eventlistener
        if event.type == pygame.QUIT:#ウインドウを閉じると
            run = False
        if event.type == FALL:#落ちるイベントが起こると
            if(i >= 20):#もうすぐアルファベットを使い切ることになると。
                random.shuffle(randarr)
                i = 0#前回と違う順番にする#ゼロから始まる
            #最大限200文字は共存できる。
            letters.append(Letter(randarr[i],random.choice(direction)))
            i = i+1#次のローマ字を生成リストに入れる
        # if event.type == pygame.NOTHING:
        if event.type == pygame.MOUSEBUTTONDOWN:#マウスでレベルを選択
            m_x,m_y = pygame.mouse.get_pos()#カーソルの座標をゲット
            for n in numList:
                x,y,num= n   
                dis = math.sqrt((x-m_x)**2 + (y-m_y)**2)#カーソルと円の距離の計算
                if(dis < 20):#カーソルとオプションは十分近い場合
                    difficulty = 4000 - ((num-48)+1) * 630
                    tmp = difficulty#ローマ字生成頻度(難易度)の調整、任意の正整数である。
                    start = True#ゲームスタート
                    pygame.time.set_timer(FALL,difficulty)#difficultyごとにローマ字を生成するイベントを起こす。
            if(over == True):
                dis = math.sqrt((330-m_x)**2 + (380-m_y)**2)
                if(dis < 150):
                    start = False
                    over = False
                    letters.clear()
                    life = 10

    keys = pygame.key.get_pressed()
    for l in letters:
        l.move()
        if keys[l.ltr] and l.x >= 0 and l.x <= 800 and l.y >= 0 and l.y <= 600 and l.visible == True and over == False:
            typeSound.play()
            score = score + 10
            if difficulty > 100 :
                difficulty = difficulty - 30
            if l.color == 'blue':
                for blueLetter in letters:
                    blueLetter.getSlow()
                pygame.time.set_timer(FALL,999)
                l.visible = False
                letters.pop(letters.index(l))
            elif l.color == 'red':
                pygame.time.set_timer(FALL, difficulty)
                for ll in letters:
                    if ll.x >= 0 and ll.x <= 800 and ll.y >= 0 and ll.y <= 600 and ll.visible == True:
                        ll.visible = False
                        score = score + 10
                boomSound.play()
                score = score - 10
            else:
                pygame.time.set_timer(FALL, difficulty)
                letters.pop(letters.index(l))
        if (l.x < 0 or l.x >= 800 or l.y < 0 or l.y >= 600 ) and l.visible == True:
                life = life - 1
                letters.pop(letters.index(l))    
                if life <= 0:
                    life = 0
                    over = True
                    pygame.time.set_timer(FALL, 0)
                    score = 0
    if start == False :
        drawmenu()
    else:
        draw()
  
pygame.quit()
