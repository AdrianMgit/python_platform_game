import pygame
import pickle
from os import path
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()

# ---------------------------------------- Stałe wartosci ----------------------------------------
#ilosc fps
fps = 60
#ilosc obiektow
blockAmount=3
#rozmiar siatki
cellSize = 50
#sila grawitacji
gravity = 6
#ilosc obrazow playera
playerImgAmount=10
# kolor siatki
meshColor = (255, 255, 255)
# flaga dla myszy
clicked = False
# flaga do konca gry
stillPlayFlag = True
# ---------------------------  WCZYTANIE PLANSZY ----------------
# tworzenie listy siatki
if path.exists('data'):
    pickle_in = open('data', 'rb')
    meshList = pickle.load(pickle_in)
columnAmount=len(meshList[0])
rowAmount = len(meshList)
# rozmiary okna
screenWidth = columnAmount*cellSize
screenHeight = rowAmount*cellSize
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Gierka")


# --------------------- WCZYTANIE OBRAZOW -----------------------
backgroundImg = pygame.image.load('img/background.png')
blockImg = pygame.image.load('img/grassCenter.png')
blockImg2 = pygame.image.load('img/grass.png')
finishImg = pygame.image.load('img/signExit.png')
endImg=pygame.image.load('img/endImg.png')
playerWalkImg = []
for i in range (0,playerImgAmount) :
    img=pygame.image.load(f'img/p1_walk0{i}.png')
    playerWalkImg.append(pygame.transform.scale(img,(cellSize,cellSize)))



# ------------------------------------ FUNKCJA RYSUJACA OBRAZY ------
def drawBlocks():
    for row in range(rowAmount):
        for col in range(columnAmount):
            if meshList[row][col] > 0:
                if meshList[row][col] == 1:
                    img = pygame.transform.scale(blockImg, (cellSize, cellSize))
                    screen.blit(img, (col * cellSize, row * cellSize))
                if meshList[row][col] == 2:
                    img = pygame.transform.scale(blockImg2, (cellSize, cellSize))
                    screen.blit(img, (col * cellSize, row * cellSize))
                if meshList[row][col] == 3:
                    img = pygame.transform.scale(finishImg, (cellSize, cellSize))
                    screen.blit(img, (col * cellSize, row * cellSize))

                rect= Rect(col * cellSize, row * cellSize,cellSize,cellSize)
                pygame.draw.rect(screen,(255,255,255),rect,1)



# ---------------------------------- KLASA PLAYER ------------------------
class Player:
    def __init__(self,x,y,images, strength):
        self.images = images
        self.rect = self.images[0].get_rect()
        self.rect.x=x
        self.rect.y=y
        self.strength = strength
        self.canJump= True
        self.imgNumber=0

    def move(self):
        #ustawienie danego obrazu z listy obrazow
        img=self.images[self.imgNumber]
        # presuniecia playera w lewo i w prawo
        moveX=0
        moveY=0
        # obsluga klawiszy
        key=pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.imgNumber+=1  #kolejny obraz
            moveX-= self.strength  #przesuniecie
            # detekcja kolizji
            if self.rect.x+moveX >=0:       # jesli po przesunieciu plaer jest dalej w planszy
                #wartosc komorki na lewo od lewego gornego boku playera
                leftUpCell=meshList[int((self.rect.y+2)/cellSize)][int((self.rect.x+moveX)/cellSize)]
                #wartosc komorki na lewo od lewego dolnego boku playera
                leftDownCell=meshList[int(((self.rect.y-2)+cellSize)/cellSize)][int((self.rect.x+moveX)/cellSize)]
                #jesli w ktorejs z tych komorek jest przeszkoda
                if (leftUpCell!=0 and leftUpCell!=3) or (leftDownCell != 0 and leftDownCell != 3):
                    #obliczam nowe przesuniecie tak aby player znajdowal sie zaraz przy przeszkodzie
                    moveX=int(self.rect.x/cellSize)*cellSize - self.rect.x
            else:
                #gdy player wychodzi poza plansze obliczam przesuniecie tak aby byl zaraz na skraju planszy
                moveX=-self.rect.x

        elif key[pygame.K_RIGHT]:
            self.imgNumber+=1
            moveX += self.strength
            if self.rect.x+cellSize+moveX < screenWidth:
                rightUpCell = meshList[int((self.rect.y+2)/cellSize)][int((self.rect.x+cellSize+moveX)/cellSize)]
                rightDownCell=meshList[int(((self.rect.y-2)+cellSize)/cellSize)][int((self.rect.x+cellSize+moveX)/cellSize)]
                if rightUpCell!=0 or rightDownCell != 0:
                    int((self.rect.x+moveX)/cellSize)*cellSize
                    moveX=int((self.rect.x+moveX)/cellSize)*cellSize - self.rect.x -1
            else:
                moveX=screenWidth-(self.rect.x+cellSize)

        elif key[pygame.K_UP] and self.canJump:
            self.canJump=False
            moveY -= cellSize*2
            if self.rect.y+moveY >=0 :
                upLeftCell = meshList[int((self.rect.y+moveY)/cellSize)][int((self.rect.x+2)/cellSize)]
                upRightCell=meshList[int((self.rect.y+moveY)/cellSize)][int((self.rect.x+cellSize-2)/cellSize)]
                if upLeftCell!=0 or upRightCell != 0:
                    moveY=int((self.rect.y+moveY)/cellSize)*cellSize +cellSize - self.rect.y
            else:
                moveY=0 - self.rect.y

        # grawitacja
        moveY+=gravity
        if self.rect.y+moveY <screenHeight :
            downLeftCell = meshList[int((self.rect.y+cellSize+moveY)/cellSize)][int((self.rect.x+2)/cellSize)]
            downRightCell=meshList[int((self.rect.y+cellSize+moveY)/cellSize)][int(((self.rect.x-2)+cellSize)/cellSize)]
            if downLeftCell!=0 or downRightCell != 0:
                self.canJump=True
                moveY= (int((self.rect.y+cellSize+moveY)/cellSize)*cellSize)-(self.rect.y+cellSize) -1
        else:
            moveY=0
            self.canJump=True

        # obliczzenie wspolrzednych x y playera po przesunieciu
        self.rect.x +=moveX
        self.rect.y +=moveY
        # rysowanie playera
        screen.blit(img,self.rect)
        # rysowanie siatki na playerze
        pygame.draw.rect(screen,(0,0,0),self.rect,1)
        # powrot do poczatku listy obrazow playera
        if self.imgNumber == (playerImgAmount-1):
            self.imgNumber=0

        # gdy player swoim srodkiem wejdzie na element nr 3 to koniec gry
        if meshList[int((self.rect.y+(cellSize/2))/cellSize)][int((self.rect.x+(cellSize/2))/cellSize)]==3:
            return False
        else:
            return True




# Tworzenie playera
player= Player(0,screenHeight-(cellSize*3),playerWalkImg,10)



# flaga do uruchomionego okna
run = True
# -------------------------------- GLOWNA PETLA OKNA ---------------------------
while run:
    clock.tick(fps)
    screen.blit(backgroundImg, (0, 0))
    # rysowanie siatki i obrazow

    if stillPlayFlag:
        drawBlocks()
        stillPlayFlag = player.move()
    else:
        screen.blit(pygame.transform.scale(endImg,(screenWidth,screenHeight)),(0,0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
