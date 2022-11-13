import pieces

class Board:

    def __init__(self) -> None:
        self.grid = {}
        self.resetBoard()
        self.normalLayout()

        self.checkedTeam = None
        self.checkedPlaces = []

    def normalLayout(self):
        for x in range(8):
            self.grid[(x, 1)] = pieces.Pawn("B", (x, 1))

        self.grid[(0, 0)] = pieces.Rook("B", (0, 0))
        self.grid[(1, 0)] = pieces.Knight("B", (1, 0))
        self.grid[(2, 0)] = pieces.Bishop("B", (2, 0))
        self.grid[(3, 0)] = pieces.Queen("B", (3, 0))
        self.grid[(4, 0)] = pieces.King("B", (4, 0))
        self.grid[(5, 0)] = pieces.Bishop("B", (5, 0))
        self.grid[(6, 0)] = pieces.Knight("B", (6, 0))
        self.grid[(7, 0)] = pieces.Rook("B", (7, 0))

        for x in range(8):
            self.grid[(x, 6)] = pieces.Pawn("W", (x, 6))

        self.grid[(0, 7)] = pieces.Rook("W", (0, 7))
        self.grid[(1, 7)] = pieces.Knight("W", (1, 7))
        self.grid[(2, 7)] = pieces.Bishop("W", (2, 7))
        self.grid[(3, 7)] = pieces.Queen("W", (3, 7))
        self.grid[(4, 7)] = pieces.King("W", (4, 7))
        self.grid[(5, 7)] = pieces.Bishop("W", (5, 7))
        self.grid[(6, 7)] = pieces.Knight("W", (6, 7))
        self.grid[(7, 7)] = pieces.Rook("W", (7, 7))

    def resetBoard(self):
        for x in range(8):
            for y in range(8):
                self.grid[(x, y)] = None

    def __getitem__(self, key):
        return self.grid[key]

    def __setitem__(self, key, value):
        self.grid[key] = value

    def display(self):
        pieceString = ""
        x = 0
        for key, value in self.grid.items():
            if key[0] == x:
                pieceString += f"{value}\t"

            else:
                print(pieceString)
                pieceString = ""
                pieceString += f"{value}\t"
                x = key[0]

    def move(self, pos1, pos2):
        first = self.grid[pos1]
        first.moveTo(pos2)
        self.grid[pos1] = None
        self.grid[pos2] = first

    def endOfMove(self):
        pass