import pygame
import pickle
from os import path
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()

# ---------------------------------------- Stałe wartosci ----------------------------------------
# ilosc fps
fps = 40
# ilosc obiektow
blockAmount = 5
# rozmiar siatki
cellSize = 30
# sila grawitacji
gravity = 6
# ilosc obrazow playera
playerImgAmount = 10
# kolor siatki
meshColor = (255, 255, 255)
# flaga dla myszy
clicked = False
# flaga do konca gry
stillPlayFlag = 0
# ---------------------------  WCZYTANIE PLANSZY ----------------
# tworzenie listy siatki
if path.exists('data'):
    pickle_in = open('data', 'rb')
    meshList = pickle.load(pickle_in)
columnAmount = len(meshList[0])
rowAmount = len(meshList)
# rozmiary okna
screenWidth = columnAmount * cellSize
screenHeight = rowAmount * cellSize
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Gierka")

# --------------------- WCZYTANIE OBRAZOW -----------------------

backgroundImg = pygame.transform.scale(pygame.image.load('img/background.png'), (screenWidth, screenHeight))
blockImg = pygame.transform.scale(pygame.image.load('img/grassCenter.png'), (cellSize, cellSize))
blockImg2 = pygame.transform.scale(pygame.image.load('img/grass.png'), (cellSize, cellSize))
finishBlockImg = pygame.transform.scale(pygame.image.load('img/signExit.png'), (cellSize, cellSize))
blockerMadImg = pygame.transform.scale(pygame.image.load('img/blockerMad.png'), (cellSize, cellSize))
wonImg = pygame.transform.scale(pygame.image.load('img/youWonImg.png'), (screenWidth, screenHeight))
lostImg = pygame.transform.scale(pygame.image.load('img/youLostImg.png'), (screenWidth, screenHeight))
enemyImg = pygame.transform.scale(pygame.image.load('img/mouse.png'), (cellSize, cellSize))


# wartosc komorki: [obraz, (0=pusta komorka -tlo, 1=przeszkoda, -1=zabicie, 2 = wygrana)]
blockDictionary = {
    0: [backgroundImg,0],
    1: [blockImg, 1],
    2: [blockImg2, 1],
    3: [finishBlockImg, 2],
    4: [blockerMadImg, -1],
    5: [enemyImg, -1]
}




playerWalkImg = []
for i in range(0, playerImgAmount):
    img = pygame.image.load(f'img/p1_walk0{i}.png')
    playerWalkImg.append(pygame.transform.scale(img, (cellSize, cellSize)))






# ------------------------------------ FUNKCJA RYSUJACA OBRAZY ------
def drawBlocks():
    for row in range(rowAmount):
        for col in range(columnAmount):
            if meshList[row][col] > 0 and meshList[row][col] !=5: # rysuje tylko te bloki w ktorych cos jest
                screen.blit(blockDictionary[meshList[row][col]][0], (col * cellSize, row * cellSize))
                rect = Rect(col * cellSize, row * cellSize, cellSize, cellSize)
                pygame.draw.rect(screen, (255, 255, 255), rect, 1)













# ---------------------------------- KLASA PLAYER ------------------------
class Player:
    def __init__(self, x, y, images, strength):
        self.images = images
        self.rect = self.images[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.strength = strength
        self.maxJumpCount = cellSize / 10
        self.jumpCount = 0
        self.imgNumber = 0

    def move(self):
        # ustawienie danego obrazu z listy obrazow
        img = self.images[self.imgNumber]
        # presuniecia playera w lewo i w prawo
        moveX = 0
        moveY = 0
        # obsluga klawiszy
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.imgNumber += 1  # kolejny obraz
            moveX -= self.strength  # przesuniecie
            # detekcja kolizji
            if self.rect.x + moveX >= 0:  # jesli po przesunieciu plaer jest dalej w planszy
                # wartosc komorki na lewo od lewego gornego boku playera
                leftUpCell = meshList[int((self.rect.y + 2) / cellSize)][int((self.rect.x + moveX) / cellSize)]
                # wartosc komorki na lewo od lewego dolnego boku playera
                leftDownCell = meshList[int(((self.rect.y - 2) + cellSize) / cellSize)][
                    int((self.rect.x + moveX) / cellSize)]
                # jesli w ktorejs z tych komorek jest przeszkoda
                if blockDictionary[leftUpCell][1] ==1 or blockDictionary[leftDownCell][1] ==1:
                    # obliczam nowe przesuniecie tak aby player znajdowal sie zaraz przy przeszkodzie
                    moveX = int((self.rect.x + 1) / cellSize) * cellSize - self.rect.x

            else:
                # gdy player wychodzi poza plansze obliczam przesuniecie tak aby byl zaraz na skraju planszy
                moveX = -self.rect.x

        elif key[pygame.K_RIGHT]:
            self.imgNumber += 1
            moveX += self.strength
            if self.rect.x + cellSize + moveX < screenWidth:
                rightUpCell = meshList[int((self.rect.y + 2) / cellSize)][
                    int((self.rect.x + cellSize + moveX) / cellSize)]
                rightDownCell = meshList[int(((self.rect.y - 2) + cellSize) / cellSize)][
                    int((self.rect.x + cellSize + moveX) / cellSize)]
                if blockDictionary[rightUpCell][1] ==1 or blockDictionary[rightDownCell][1] ==1:
                    moveX = int((self.rect.x + moveX) / cellSize) * cellSize - self.rect.x - 1
            else:
                moveX = screenWidth - (self.rect.x + cellSize)

        if key[pygame.K_UP]:
            if self.jumpCount < self.maxJumpCount:
                moveY -= cellSize - 1
                if self.rect.y + moveY >= 0:
                    upLeftCell = meshList[int((self.rect.y + moveY) / cellSize)][
                        int((self.rect.x + moveX + 2) / cellSize)]
                    upRightCell = meshList[int((self.rect.y + moveY) / cellSize)][
                        int((self.rect.x + moveX + cellSize - 2) / cellSize)]
                    if blockDictionary[upLeftCell][1] ==1 or blockDictionary[upRightCell][1] ==1:
                        moveY = int((self.rect.y + moveY) / cellSize) * cellSize + cellSize - self.rect.y
                else:
                    moveY = 0 - self.rect.y

                self.jumpCount += 1

        # grawitacja
        moveY += gravity
        if self.rect.y + moveY < screenHeight:
            downLeftCell = meshList[int((self.rect.y + cellSize + moveY) / cellSize)][int((self.rect.x + 2) / cellSize)]
            downRightCell = meshList[int((self.rect.y + cellSize + moveY) / cellSize)][
                int(((self.rect.x - 2) + cellSize) / cellSize)]
            if blockDictionary[downLeftCell][1] ==1 or blockDictionary[downRightCell][1] ==1:
                self.jumpCount = 0
                moveY = (int((self.rect.y + cellSize + moveY) / cellSize) * cellSize) - (self.rect.y + cellSize) - 1
        else:
            moveY = 0
            self.jumpCount = 0

        # obliczzenie wspolrzednych x y playera po przesunieciu
        self.rect.x += moveX
        self.rect.y += moveY
        # rysowanie playera
        screen.blit(img, self.rect)
        # rysowanie siatki na playerze
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)
        # powrot do poczatku listy obrazow playera
        if self.imgNumber == (playerImgAmount - 1):
            self.imgNumber = 0

        # wartosc komorki w ktorej znajduje sie srodek playera
        playerCellValue = meshList[int((self.rect.y + (cellSize / 2)) / cellSize)][
            int((self.rect.x + (cellSize / 2)) / cellSize)]

        if blockDictionary[playerCellValue][1] == 2:
            return 1
        elif blockDictionary[playerCellValue][1] == -1:
            return -1
        else:
            return 0


# ---------------------------------- KLASA ENEMY ------------------------
class Enemy:
    def __init__(self, x, y, image, strength,direction):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.strength = strength
        self.direction=direction

    def move(self):
        meshList[int(self.rect.y/cellSize)][int(self.rect.x/cellSize)]=0
        moveX=0
        moveY=0

        if self.direction == -1:
            moveX-=self.strength
            leftCell=meshList[int(self.rect.y / cellSize)][
                int((self.rect.x + moveX) / cellSize)]
            leftDownCell=meshList[int((self.rect.y+cellSize) / cellSize)][
                int((self.rect.x + moveX) / cellSize)]

            if blockDictionary[leftCell][1]!=0 or (blockDictionary[leftCell][1]==0 and blockDictionary[leftDownCell][1]==0):
                moveX = int(self.rect.x / cellSize) * cellSize - self.rect.x
                self.direction*=-1

        elif self.direction == 1:
            moveX+=self.strength
            rightCell=meshList[int(self.rect.y / cellSize)][
                int((self.rect.x +cellSize + moveX) / cellSize)]
            rightDownCell=meshList[int((self.rect.y+cellSize) / cellSize)][
                int((self.rect.x+cellSize + moveX) / cellSize)]

            if blockDictionary[rightCell][1]!=0 or (blockDictionary[rightCell][1]==0 and blockDictionary[rightDownCell][1]==0):
                moveX = int((self.rect.x + moveX) / cellSize) * cellSize - self.rect.x
                self.direction*=-1


        self.rect.x += moveX
        self.rect.y += moveY
        screen.blit(self.image, self.rect)
        meshList[int(self.rect.y/cellSize)][int(self.rect.x/cellSize)]=5





# Tworzenie playera
player = Player(0, screenHeight - (cellSize * 3), playerWalkImg, 10)


# lista poruszajacych sie wrogow
enemyMovingList =[]
#wczytanie poczatkowych pozycji wrogow do listy
for row in range(rowAmount):
    for col in range(columnAmount):
        if meshList[row][col] == 5:
            enemyMovingList.append(Enemy(col * cellSize,row * cellSize,enemyImg,4,-1))
            meshList[row][col] = 0

# flaga do uruchomionego okna
run = True

print(enemyMovingList)

# -------------------------------- GLOWNA PETLA OKNA ---------------------------
while run:
    clock.tick(fps)
    screen.blit(backgroundImg,(0,0))
     # rysowanie siatki i obrazow

    if stillPlayFlag == 0:
        drawBlocks()

        for enemy in enemyMovingList:
            enemy.move()

        stillPlayFlag = player.move()
    elif stillPlayFlag == 1:
        screen.blit(wonImg, (0, 0))
    else:
        screen.blit(lostImg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
