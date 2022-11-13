import pygame
import os

images = {}

colours = ["White", "Black"]
types = ["Bishop", "King", "Knight", "Pawn", "Queen", "Rook"]

kingPositions = [(1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1), (0,1), (1,1)]
knightPositions = [(-1, 2), (1, 2), (2, 1), (2,-1), (-1, -2), (1, -2), (-2, 1), (-2, -1)]


def getPieceImages():
    for col in colours:
        for piece in types:
            image = pygame.image.load(os.path.join("Pieces", f"{col} {piece}.png"))
            colID = col[0].upper()
            pieceID = piece[0].lower() if piece != "Knight" else "n"
            images[f"{colID}{pieceID}"] = image

def rookCheckMove(board, start, target, team):
    if (target[1] == start[1]):
        full_distance = (target[0]-1) - start[0]
        for i in range(abs(full_distance)):
            if full_distance > 0:
                if board[start[0]+(i+1), target[1]] != None:
                    return False

        full_distance = (target[0]+1) - start[0]
        for i in range(abs(full_distance)):
            if full_distance < 0:
                if board[start[0]-(i+1), target[1]] != None:
                    return False
        return True

    if (target[0] == start[0]):
        full_distance = (target[1]-1) - start[1]
        for i in range(abs(full_distance)):
            if full_distance > 0:
                if board[target[0], start[1]+(i+1)] != None:
                    return False

        full_distance = (target[1]+1) - start[1]
        for i in range(abs(full_distance)):
            if full_distance < 0:
                if board[target[0], start[1]-(i+1)] != None:
                    return False

        return True

def bishopCheckMove(board, start, target, team):
    if abs(start[0] - target[0]) != abs(start[1] - target[1]):
        return False

    x_pos =  1 if target[0] - start[0] > 0 else -1
    y_pos = 1 if target[1] - start[1] > 0 else -1

    i = start[0] + x_pos
    j = start[1] + y_pos
    while (i < target[0] if x_pos==1 else i > target[0]):
        if board[i, j] != None:
            return False

        i += x_pos
        j += y_pos

    return True
        
class Piece:

    def __init__(self, team, type_, pos) -> None:
        self.team = team
        self.type = type_
        self.validMoves = []
        self.hasMoved = False
        self.x, self.y = pos
        self.image = images[f"{team}{self.type}"]

    def moveTo(self, pos):
        self.x, self.y = pos    
        self.hasMoved = True

    def getPos(self):
        return self.x, self.y

    def checkAllspaces(self, board):
        self.validMoves = []
        for x in range(8):
            for y in range(8):
                if self.checkMove(board, (self.x, self.y), (x, y)):
                    self.validMoves.append((x, y))

    def getValid(self, board):
        self.checkAllspaces(board)
        return self.validMoves

    def checkMove(self, board, start, target):
        if start == target:
            return False

        if board[target] != None:
            if board[target].team == self.team:
                return False

        if board.checkedTeam == self.team:
            if target not in board.checkedPlaces:
                return False

        return True

    def __str__(self) -> str:
        return f"{self.team}{self.type}"

    def __repr__(self) -> str:
        return f"{self.team}{self.type}"

class Pawn(Piece):

    def __init__(self, team, pos) -> None:
        super().__init__(team, "p", pos)

    def checkMove(self, board, start, target):
        if super().checkMove(board, start, target):
            modifier = 1 if self.team == "B" else -1
            if (target[0] == start[0]) and board[target] == None:
                if target[1] == start[1] + modifier:
                    return True

                elif (target[1] == start[1] + (2 * modifier)) and not self.hasMoved:
                    if board[start[0], start[1] + modifier] == None:
                        return True
                
            elif ((target[0] == start[0] + 1) or (target[0] == start[0] - 1)) and board[target] != None:
                if target[1] == start[1] + modifier:
                    return True

        return False

class Rook(Piece):

    def __init__(self, team, pos) -> None:
        super().__init__(team, "r", pos)

    def checkMove(self, board, start, target):
        if super().checkMove(board, start, target):
            if (target[1] == start[1]):
                full_distance = (target[0]-1) - start[0]
                for i in range(abs(full_distance)):
                    if full_distance > 0:
                        if board[start[0]+(i+1), target[1]] != None:
                            return False
                full_distance = (target[0]+1) - start[0]
                for i in range(abs(full_distance)):
                    if full_distance < 0:
                        if board[start[0]-(i+1), target[1]] != None:
                            return False
                return True

            if (target[0] == start[0]):
                full_distance = (target[1]-1) - start[1]
                for i in range(abs(full_distance)):
                    if full_distance > 0:
                        if board[target[0], start[1]+(i+1)] != None:
                            return False
                full_distance = (target[1]+1) - start[1]
                for i in range(abs(full_distance)):
                    if full_distance < 0:
                        if board[target[0], start[1]-(i+1)] != None:
                            return False

                return True

        return False

class Knight(Piece):

    def __init__(self, team, pos) -> None:
        super().__init__(team, "n", pos)

    def checkMove(self, board, start, target):
        if super().checkMove(board, start, target):
            for offset in knightPositions:
                gridPos = (start[0] + offset[0], start[1] + offset[1])
                if gridPos == target:
                    return True
            
        return False

class Bishop(Piece):

    def __init__(self, team, pos) -> None:
        super().__init__(team, "b", pos)

    def checkMove(self, board, start, target):
        if super().checkMove(board, start, target):
            if abs(start[0] - target[0]) != abs(start[1] - target[1]):
                return False

            x_pos =  1 if target[0] - start[0] > 0 else -1
            y_pos = 1 if target[1] - start[1] > 0 else -1

            i = start[0] + x_pos
            j = start[1] + y_pos
            while (i < target[0] if x_pos==1 else i > target[0]):
                if board[i, j] != None:
                    return False

                i += x_pos
                j += y_pos

            return True

class Queen(Piece):

    def __init__(self, team, pos) -> None:
        super().__init__(team, "q", pos)

    def checkMove(self, board, start, target):
        if super().checkMove(board, start, target):
            bishop, rook = bishopCheckMove(board, start, target, self.team), rookCheckMove(board, start, target, self.team)
            if bishop or rook:
                return True

        return False

class King(Piece):

    def __init__(self, team, pos) -> None:
        super().__init__(team, "k", pos)

    def checkMove(self, board, start, target):
        if super().checkMove(board, start, target):
            for offset in kingPositions:
                gridPos = (start[0] + offset[0], start[1] + offset[1])
                if gridPos == target:
                    return True

getPieceImages()