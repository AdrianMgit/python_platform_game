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
blockAmount=2
#rozmiar siatki
cellSize = 50
#grawitacja
gravity = 3

# kolor siatki
meshColor = (255, 255, 255)
# flaga dla myszy
clicked = False


# tworzenie listy siatki
if path.exists('data'):
    pickle_in = open('data', 'rb')
    meshList = pickle.load(pickle_in)


columnAmount=len(meshList[0])
rowAmount = len(meshList)
# rozmiary okno, wymiary musza byc podzielne przez rozmiar siatki
screenWidth = columnAmount*cellSize
screenHeight = rowAmount*cellSize

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Gierka")

# ---------------- WCZYTANIE OBRAZOW -----------------------
backgroundImg = pygame.image.load('img/background.png')
blockImg = pygame.image.load('img/grassCenter.png')
blockImg2 = pygame.image.load('img/grass.png')
playerImg = pygame.image.load('img/p1_walk01.png')



# ----------------- FUNKCJA RYSUJACA OBRAZY ------
def drawBlocks():
    for row in range(rowAmount):
        for col in range(columnAmount):
            if meshList[row][col] > 0:
                # jedno klikniecie = ziemia
                if meshList[row][col] == 1:
                    img = pygame.transform.scale(blockImg, (cellSize, cellSize))
                    screen.blit(img, (col * cellSize, row * cellSize))
                if meshList[row][col] == 2:
                    img = pygame.transform.scale(blockImg2, (cellSize, cellSize))
                    screen.blit(img, (col * cellSize, row * cellSize))

                rect= Rect(col * cellSize, row * cellSize,cellSize,cellSize)
                pygame.draw.rect(screen,(255,255,255),rect,1)


print(meshList)

# ---------------------------------- KLASA PLAYER ------------------------
class Player:
    def __init__(self,x,y,image, strength):
        self.image = pygame.transform.scale(image,(cellSize,cellSize))
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.strength = strength


    def move(self):

        moveX=0
        moveY=0

        key=pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            moveX-= self.strength
            if self.rect.x+moveX >=0:
                leftUpCell=meshList[int(self.rect.y/cellSize)][int((self.rect.x+moveX)/cellSize)]
                leftDownCell=meshList[int((self.rect.y+cellSize)/cellSize)][int((self.rect.x+moveX)/cellSize)]
                if leftUpCell!=0 or leftDownCell != 0:
                    moveX=int(self.rect.x/cellSize)*cellSize - self.rect.x
            else:
                moveX=-self.rect.x

        elif key[pygame.K_RIGHT]:
            moveX += self.strength
            if self.rect.x+cellSize+moveX < screenWidth:
                rightUpCell = meshList[int(self.rect.y/cellSize)][int((self.rect.x+cellSize+moveX)/cellSize)]
                rightDownCell=meshList[int((self.rect.y+cellSize)/cellSize)][int((self.rect.x+cellSize+moveX)/cellSize)]
                if rightUpCell!=0 or rightDownCell != 0:
                    int((self.rect.x+moveX)/cellSize)*cellSize
                    moveX=int((self.rect.x+moveX)/cellSize)*cellSize - self.rect.x -1
            else:
                moveX=screenWidth-(self.rect.x+cellSize)



        elif key[pygame.K_UP]:
            moveY -= self.strength
            if self.rect.y+moveY >=0 :
                upLeftCell = meshList[int((self.rect.y+moveY)/cellSize)][int(self.rect.x/cellSize)]
                upRightCell=meshList[int((self.rect.y+moveY)/cellSize)][int((self.rect.x+cellSize-1)/cellSize)]
                if upLeftCell!=0 or upRightCell != 0:
                    moveY=0
            else:
                moveY=0


        # grawitacja
        moveY+=gravity
        if self.rect.y+moveY <screenHeight :
            downLeftCell = meshList[int((self.rect.y+cellSize+moveY)/cellSize)][int((self.rect.x+1)/cellSize)]
            downRightCell=meshList[int((self.rect.y+cellSize+moveY)/cellSize)][int((self.rect.x-1+cellSize)/cellSize)]
            if downLeftCell!=0 or downRightCell != 0:
                moveY= (int((self.rect.y+cellSize+moveY)/cellSize)*cellSize)-(self.rect.y+cellSize) -1
        else:
            moveY=0


        # if self.rect.y + moveY >(screenHeight - self.image.get_height()):
        #     self.rect.y = screenHeight- self.image.get_height()
        # elif self.rect.y + moveY <0:
        #     self.rect.y = 0
        # if self.rect.x + moveX > (screenWidth - self.image.get_width()):
        #     self.rect.x = screenWidth - self.image.get_width()
        # elif self.rect.x + moveX <0:
        #     self.rect.x = 0


        self.rect.x +=moveX
        self.rect.y +=moveY



        screen.blit(self.image,self.rect)
        pygame.draw.rect(screen,(0,0,0),self.rect,1)








player= Player(0,screenHeight-(cellSize*3),playerImg,10)

















# flaga do uruchomionego okna
run = True
# -------------------------------- GLOWNA PETLA OKNA ---------------------------
while run:
    clock.tick(fps)
    screen.blit(backgroundImg, (0, 0))
    # rysowanie siatki i obrazow
    drawBlocks()
    player.move()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False




    pygame.display.update()

pygame.quit()
