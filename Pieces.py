

# Returns True if two pieces are opposite colors
def is_enemy(piece1, piece2):
   if piece1 is None or piece2 is None:
       return False
   return piece1.color != piece2.color

# General parent class for the pieces classes
class Piece:
   name = " "
   color = ""
   x = -1  # board column 0-7
   y = -1  # board row 0-7
   points = 0


   def __init__(self, name, color, x, y, points):
       self.name = name     # Piece name
       self.color = color   # Either black or white
       self.x = x           # Column position
       self.y = y           # Row position
       self.points = points # Points used for evaluation

    # Return list of legal moves without checks
   def get_pseudo_legal_moves(self, board):
       return []

    # String representation of a piece (based on color & piece type)
   def __str__(self):
       return " "



# Pieces

# Pawn
class Pawn(Piece):
   def __init__(self, color, x, y):
       super().__init__("Pawn", color, x, y, 1)

    # Only look at attacking moves (check purposes)
   def get_attack_squares(self, board):
       attacks = []
       # Set direction to check
       if self.color == "White":
           direction = -1
       else:
           direction = 1

        # Check left and right
       for dx in (-1, 1):
           x = self.x + dx
           y = self.y + direction
           if board.in_bounds(x, y):
               attacks.append((x, y))

       return attacks


   def get_pseudo_legal_moves(self, board):
       moves = []
       # Defining direction and start row
       if self.color == "White":
           direction = -1
           start_row = 6
       else:
           direction = 1
           start_row = 1

       # Forward 1
       nx, ny = self.x, self.y + direction
       if board.is_empty(nx, ny):
           moves.append((nx, ny))

           # Forward 2 from start  (pawn's very first move)
           if self.y == start_row:
               ny2 = ny + direction
               if board.is_empty(nx, ny2):
                   moves.append((nx, ny2))

       # Capturing moves
       for dx in [-1, 1]:
           cx, cy = self.x + dx, self.y + direction
           # Only append if there's an enemy occupying the square
           if board.is_enemy_square(self, cx, cy):
               moves.append((cx, cy))

       return moves


   def __str__(self):
       if self.color == "White":
           return "P"
       elif self.color == "Black":
           return "p"
       else:
           return " "

# Bishop
class Bishop(Piece):
   def __init__(self, color, x, y):
       super().__init__("Bishop", color, x, y, 3)

   def get_pseudo_legal_moves(self, board):
       moves = []
       # 4 diagonal directions
       directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]

       # Check all 4 directions
       for dx, dy in directions:
           x, y = self.x, self.y
           # Keep checking until end of board or a piece is hit
           while True:
               x += dx
               y += dy
               if not board.in_bounds(x, y):
                   # End of board
                   break
               if board.is_empty(x, y):
                   moves.append((x, y))
               else:
                   # Piece hit, append if enemy
                   if board.is_enemy_square(self, x, y):
                       moves.append((x, y))
                   break
       return moves

   def __str__(self):
       if self.color == "White":
           return "B"
       elif self.color == "Black":
           return "b"
       else:
           return " "

# Knight
class Knight(Piece):
   def __init__(self, color, x, y):
       super().__init__("Knight", color, x, y, 3)

   def get_pseudo_legal_moves(self, board):
       moves = []
       directions = [(2, 1), (1, 2), (-2, 1), (-1, 2), (-2, -1), (-1, -2), (2, -1), (1, -2)]
       # Check all 8 'L' shaped moves
       for dx, dy in directions:
           x = self.x + dx
           y = self.y + dy
           if board.in_bounds(x, y) and board.is_empty(x, y) or board.is_enemy_square(self, x, y):
                moves.append((x, y))
       return moves

   def __str__(self):
       if self.color == "White":
           return "N"
       elif self.color == "Black":
           return "n"
       else:
           return " "

# Rook
class Rook(Piece):
   def __init__(self, color, x, y):
       super().__init__("Rook", color, x, y, 5)

   def get_pseudo_legal_moves(self, board):
       moves = []

       # 4 cardinal directions
       directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
       # Check all 4 directions
       for dx, dy in directions:
           x, y = self.x, self.y
           # Keep going until end of board or a piece
           while True:
               x += dx
               y += dy
               if not board.in_bounds(x, y):
                   # End of board
                   break
               if board.is_empty(x, y):
                   moves.append((x, y))
               else:
                   # Piece hit, append if enemy
                   if board.is_enemy_square(self, x, y):
                       moves.append((x, y))
                   break
       return moves

   def __str__(self):
       if self.color == "White":
           return "R"
       elif self.color == "Black":
           return "r"
       else:
           return " "

# Queen
class Queen(Piece):
   def __init__(self, color, x, y):
       super().__init__("Queen", color, x, y, 9)

   def get_pseudo_legal_moves(self, board):
       moves = []

       # 4 diagonal and 4 cardinal directions
       directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
       # Check all 8 directions
       for dx, dy in directions:
           x, y = self.x, self.y
           # Keep going untol end of board or a piece
           while True:
               x += dx
               y += dy
               if not board.in_bounds(x, y):
                   # End of board
                   break
               if board.is_empty(x, y):
                   moves.append((x, y))
               else:
                   # Piece hit, append if enemy
                   if board.is_enemy_square(self, x, y):
                       moves.append((x, y))
                   break
       return moves

   def __str__(self):
       if self.color == "White":
           return "Q"
       elif self.color == "Black":
           return "q"
       else:
           return " "

# King
class King(Piece):
   def __init__(self, color, x, y):
       super().__init__("King", color, x, y, 10)

    # Doesn't consider moving into check
   def get_pseudo_legal_moves(self, board):
       moves = []
       # All 8 adjacent squares
       directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]

        # Check 8 adjacent squares
       for dx, dy in directions:
           x = self.x + dx
           y = self.y + dy
           if board.in_bounds(x, y) and (board.is_empty(x, y) or board.is_enemy_square(self, x, y)):
                moves.append((x, y))
       return moves


   def __str__(self):
       if self.color == "White":
           return "K"
       elif self.color == "Black":
           return "k"
       else:
           return " "