class Piece:
   name = " "
   color = ""
   x = -1  # board column 0-7
   y = -1  # board row 0-7
   points = 0


   def __init__(self, name, color, x, y, points):
       self.name = name
       self.color = color
       self.x = x
       self.y = y
       self.points = points


   def get_pseudo_legal_moves(self, board):
       return []


   def __str__(self):
       return " "