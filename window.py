import pygame
import pieces
import board

pygame.init()

WINDOWSIZE = 960
IMAGESIZE = 60
PIECESIZE = WINDOWSIZE // 8

clock = pygame.time.Clock()
fps = 60

class Window:

    def __init__(self) -> None:
        self.windowSize = WINDOWSIZE
        self.pieceSize = PIECESIZE

        self.team = "W"
        self.board = board.Board()
        self.screen = pygame.display.set_mode((self.windowSize, self.windowSize))
        self.whiteSquare = (230, 230, 230)
        self.blackSquare = (150, 150, 150)
        self.moveableWhiteSquare = (230, 255, 230)
        self.moveableBlackSquare = (150, 175, 150)
        self.selected = None
        self.selectedPossible = []
        self.running = False

    def getGridPosition(self, event):
        gridX = event.pos[0] // (self.pieceSize)
        gridY = event.pos[1] // (self.pieceSize)
        return gridX, gridY

    def resetSelectable(self):
        self.selected = None
        self.selectedPossible = []

    def onClick(self, event):
        if event.button == 1:
            gridX, gridY = self.getGridPosition(event)
            if self.selected:
                pos = self.selected.getPos()
                if pos == (gridX, gridY):
                    self.resetSelectable()

                else:
                    if self.selected.checkMove(self.board, self.selected.getPos(), (gridX, gridY)):
                        self.board.move(pos, (gridX, gridY))
                        self.selected.moveTo((gridX, gridY))
                        self.resetSelectable()
                        #if self.team == "W": self.team = "B"
                        #else: self.team = "W"

            elif self.board.grid[gridX, gridY]:
                piece = self.board.grid[gridX, gridY]
                if piece.team == self.team:
                    self.selected = piece

        elif event.button == 3:
            self.resetSelectable()

    def drawPattern(self):
        for x in range(8):
            for y in range(8):
                realX = x * self.pieceSize
                realY = y * self.pieceSize
                tot = x + y
                if tot % 2 == 0:
                    if (x, y) in self.selectedPossible:
                        pygame.draw.rect(self.screen, self.moveableWhiteSquare, (realX, realY, self.pieceSize, self.pieceSize))
                    
                    else:
                        pygame.draw.rect(self.screen, self.whiteSquare, (realX, realY, self.pieceSize, self.pieceSize))

                else:
                    if (x, y) in self.selectedPossible:
                        pygame.draw.rect(self.screen, self.moveableBlackSquare, (realX, realY, self.pieceSize, self.pieceSize))
                    
                    else:
                        pygame.draw.rect(self.screen, self.blackSquare, (realX, realY, self.pieceSize, self.pieceSize))

    def drawPieces(self):
        for x in range(8):
            for y in range(8):
                realX = x * self.pieceSize
                realY = y * self.pieceSize
                if self.board.grid[x, y]:
                    if not self.selected:
                        image = self.board.grid[x, y].image
                        scaledImage = pygame.transform.scale(image, (self.pieceSize, self.pieceSize))
                        self.screen.blit(scaledImage, (realX, realY))

                    else:
                        if self.selected.getPos() != (x, y):
                            image = self.board.grid[x, y].image
                            scaledImage = pygame.transform.scale(image, (self.pieceSize, self.pieceSize))
                            self.screen.blit(scaledImage, (realX, realY))

    def drawSelected(self):
        if self.selected:
            mousePos = pygame.mouse.get_pos()
            image = self.selected.image
            scaledImage = pygame.transform.scale(image, (self.pieceSize, self.pieceSize))
            self.selectedPossible = self.selected.getValid(self.board)
            self.screen.blit(scaledImage, (mousePos[0] - PIECESIZE // 2, mousePos[1] - PIECESIZE // 2))
        
    def update(self):
        self.screen.fill((255, 255, 255))
        self.drawPattern()
        self.drawPieces()
        self.drawSelected()
        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.onClick(event)

            self.update()
            clock.tick(fps)

        pygame.quit()

win = Window()
win.run()