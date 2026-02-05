from Chess import *

board = Board()
print(board)
board.setup_starting_board()
print(board)


while True:
   inp = input("Input move: \nFormat: SquareFrom|SquareTo: ")
   if inp == "":
       print(board.move_list)
       break
   moves = inp.split("|")
   if len(moves) == 2:
       board.move_piece(moves[0], moves[1])
       print(board)
   else:
       print("Wrong move format!")


#  o
# /.\


# /->
# |\


#  ^
# /B\


# |||
# [R]


# \|/
# [Q]


# \+/
# |^|
