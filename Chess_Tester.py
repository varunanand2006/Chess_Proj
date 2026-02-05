from Pieces import *


# Create a 8x8 grid of boxes


def move_translate(move_string):
   move_string = move_string.lower()


   x = ord(move_string[0]) - ord('a')
   y = 8 - int(move_string[1])
   return (x, y)


def is_valid_move_string(move_string):
   if len(move_string) != 2:
       return False
   file = move_string[0].lower()
   rank = move_string[1]
   if file < 'a' or file > 'h':
       return False
   if rank < '1' or rank > '8':
       return False
   return True






class Board:
   def __init__(self):
       self.board = []
       for i in range(8):
           self.board.append([None] * 8)
       self.turn = "White"
       self.move_list = []
       self.taken_pieces = []


   def set_piece(self, piece, x, y):
       self.board[y][x] = piece


   def return_eval(self):
       total_eval = 0
       for row in self.board:
           for piece in row:
               if piece is None:
                   continue
               if piece.color == "White":
                   total_eval += piece.points
               else:
                   total_eval -= piece.points
       return total_eval


   def move_piece(self, from_str, to_str):
       if not is_valid_move_string(from_str) or not is_valid_move_string(to_str):
           print("Invalid move format.")
           return False


       from_x, from_y = move_translate(from_str)
       to_x, to_y = move_translate(to_str)


       piece = self.board[from_y][from_x]
       if piece is None:
           print(f"No piece at {from_str}.")
           return False


       # Enforce turn
       if piece.color != self.turn:
           print("Not your turn.")
           return False


       target = self.board[to_y][to_x]


       # Can't capture your own piece
       if target is not None and target.color == piece.color:
           print("Cannot capture your own piece.")
           return False


       # --- CAPTURE LOGIC ---
       if target is not None and is_enemy(piece, target):
           print(f"{piece.name} captures {target.name}!")
           self.taken_pieces.append(target)


       # Move piece
       self.board[to_y][to_x] = piece
       self.board[from_y][from_x] = None


       piece.x = to_x
       piece.y = to_y


       # Log it in move_list
       self.move_list.append(f"{str(piece)}:{from_str}->{to_str}")


       # Switch turn
       if self.turn == "White":
           self.turn = "Black"
       else:
           self.turn = "White"
       return True


   def in_bounds(self, x, y):
       return 0 <= x < 8 and 0 <= y < 8


   def find_king(self, color):
       for row in self.board:
           for piece in row:
               if piece is not None and piece.name == "King" and piece.color == color:
                   return piece
       return None


   def is_square_attacked(self, x, y, by_color):
       for row in self.board:
           for piece in row:
               if piece is None or piece.color != by_color:
                   continue


               if piece.name == "Pawn":
                   attacks = piece.get_attack_squares(self)
               else:
                   attacks = piece.get_pseudo_legal_moves(self)


               for ax, ay in attacks:
                   if ax == x and ay == y:
                       return True
       return False


   def get_legal_moves(self, piece):
       legal_moves = []


       for move in piece.get_pseudo_legal_moves(self):
           if self.is_legal_move(piece, move):
               legal_moves.append(move)


       return legal_moves


   def is_legal_move(self, piece, target):
       # 1. Save state
       from_x, from_y = piece.x, piece.y
       to_x, to_y = target
       captured = self.board[to_y][to_x]


       # 2. Make the move
       self.board[from_y][from_x] = None
       self.board[to_y][to_x] = piece
       piece.x, piece.y = to_x, to_y


       # 3. Check king safety
       in_check = self.is_in_check(piece.color)


       # 4. Undo move
       self.board[from_y][from_x] = piece
       self.board[to_y][to_x] = captured
       piece.x, piece.y = from_x, from_y


       return not in_check


   def is_in_check(self, color):
       king = self.find_king(color)
       if king is None:
           return False  # shouldn't happen


       enemy_color = "Black" if color == "White" else "White"
       return self.is_square_attacked(king.x, king.y, enemy_color)


   def get_all_legal_moves(self, color):
       moves = []
       for row in self.board:
           for piece in row:
               if piece and piece.color == color:
                   for move in self.get_legal_moves(piece):
                       moves.append((piece, move))
       return moves


   def is_empty(self, x, y):
       if not self.in_bounds(x, y):
           return False
       return self.board[y][x] is None


   def is_enemy_square(self, piece, x, y):
       if not self.in_bounds(x, y):
           return False
       target = self.board[y][x]
       return target is not None and target.color != piece.color


   def setup_starting_board(self):
       # Clear the board first
       for y in range(8):
           for x in range(8):
               self.board[y][x] = None


       # --- Pawns ---
       for x in range(8):
           self.board[6][x] = Pawn("White", x, 6)  # 2nd rank for White
           self.board[1][x] = Pawn("Black", x, 1)  # 7th rank for Black


       # --- Rooks ---
       self.board[7][0] = Rook("White", 0, 7)
       self.board[7][7] = Rook("White", 7, 7)
       self.board[0][0] = Rook("Black", 0, 0)
       self.board[0][7] = Rook("Black", 7, 0)


       # --- Knights ---
       self.board[7][1] = Knight("White", 1, 7)
       self.board[7][6] = Knight("White", 6, 7)
       self.board[0][1] = Knight("Black", 1, 0)
       self.board[0][6] = Knight("Black", 6, 0)


       # --- Bishops ---
       self.board[7][2] = Bishop("White", 2, 7)
       self.board[7][5] = Bishop("White", 5, 7)
       self.board[0][2] = Bishop("Black", 2, 0)
       self.board[0][5] = Bishop("Black", 5, 0)


       # --- Queens ---
       self.board[7][3] = Queen("White", 3, 7)
       self.board[0][3] = Queen("Black", 3, 0)


       # --- Kings ---
       self.board[7][4] = King("White", 4, 7)
       self.board[0][4] = King("Black", 4, 0)


       # Set starting turn
       self.turn = "White"


   def __str__(self):
       ret = "--------------------------\n"
       for i in range(8):
           ret += str(8 - i) + " "
           for j in range(8):
               piece = self.board[i][j]
               if piece is None:
                   if (j + i) % 2 == 0:
                       ret += "[ ]"
                   else:
                       ret += "| |"
               else:
                   if (j + i) % 2 == 0:
                       ret += "[" + str(piece) + "]"
                   else:
                       ret += "|" + str(piece) + "|"
           ret += "\n"
       ret += "   a  b  c  d  e  f  g  h "
       #ret += "\n--------------------------"
       return ret