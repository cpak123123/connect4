# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 22:31:23 2021

@author: cpak1
"""
from c4AI import State
from collections import defaultdict
class Tile():
        def __init__(self, x, y, color = "o"):
                self.color = color
                self.x = x
                self.y = y
                self.winner = None
        
class Board():
        def __init__(self):
                temp = []
                for i in range(6):
                        temp.append([])
                        for j in range(7):
                                temp[i].append(Tile(j,i))
                self.state = temp
                
        def print_board(self):
                for i in range(13):
                        if i % 2 == 0:
                                print("+--"*7, end = " ")
                                print("+", end = " ")
                        
                        for j in range(7):
                                if i % 2 !=0 and j != 6:
                                    print("|" + self.state[i//2][j].color, end = " ")
                                
                                if i% 2 != 0 and j == 6:
                                    print("|" + self.state[i//2][j].color, end = " ")
                        if i %2 != 0:
                                print("|", end = " ")
                        print()
class Game():
        def __init__(self, turn = 0, cc = "y", running = True):
                self.board = Board()
                self.turn = turn
                self.cc = cc
                self.running = running
                self.value = 0
                self.hist = []
        def chck_turn(self):
                if self.turn %2 == 0:
                        self.cc = "y"
                if self.turn %2 != 0:
                        self.cc = "r"
        def val_move(self, column):
                if 'o' not in [x[column].color for x in self.board.state]:
                        return False
                return True
        def move(self, column):
                col_stat = [x[column] for x in self.board.state]
                if not self.val_move(column):
                        print("try_again")
                        return
                        
                for i, tile in enumerate(col_stat):
                        if i < len(col_stat)-1:
                                if tile.color == "o" and col_stat[i+1].color == "o":
                                        continue
                                if tile.color =="o" and col_stat[i+1].color != "o":
                                        self.board.state[i][column] = Tile(i, column, color = self.cc)
                                        break
                        if i == len(col_stat)-1:
                                self.board.state[i][column] = Tile(i, column, color = self.cc)
                self.turn += 1
                self.hist.append(self.board.state)
                self.chck_go()
                self.chck_turn()
                return self.board.state
                                                    
        def chck_go(self, proofer = None):
                #column checkk
                r_win = ['r','r','r','r']
                y_win = ['y','y','y','y']
                col_state = []
                for cols in range(len(self.board.state)):
                        col_state.append([x[cols].color for x in self.board.state])
                for colsind in col_state:
                        n = len(r_win)
                        r_won = any(r_win == colsind[i:i + n] for i in range(len(colsind)-n + 1))
                        y_won = any(y_win == colsind[i:i + n] for i in range(len(colsind)-n + 1))
                        if y_won:
                                print("games over, yellow won lma")
                                self.board.print_board()
                                self.winner = 'y'
                                self.running = False
                                return
                        if r_won:
                                print("games over, red won")
                                self.board.print_board()
                                self.winner = 'r'
                                self.running = False
                                return
                #row checkkk
                row_state = []
                for rows in range(len(self.board.state[0])-1):
                        row_state.append([x.color for x in self.board.state[rows]])
                for rowsind in row_state:
                        n = len(r_win)
                        r_won = any(r_win == rowsind[i:i + n] for i in range(len(rowsind)-n + 1))
                        y_won = any(y_win == rowsind[i:i + n] for i in range(len(rowsind)-n + 1))
                        if y_won:
                                print("games over, yellow won lma")
                                self.board.print_board()
                                self.winner= 'y'
                                self.running = False
                                return
                        if r_won:
                                print("games over, red won")
                                self.board.print_board()
                                self.winner = 'w'
                                self.running = False
                                return
                #diag check:
                diag_state = []
                diag_lr = defaultdict(list)
                diag_rl = defaultdict(list)
                for i in range(len(self.board.state)):
                        for j in range(len(self.board.state[0])):
                                diag_lr[i-j].append(self.board.state[i][j].color)
                                diag_rl[i+j].append(self.board.state[i][j].color)
                for item in diag_lr.values():
                        if len(item) >= 4:
                                diag_state.append(item)
                for item in diag_rl.values():
                        if len(item) >= 4:
                                diag_state.append(item)
                for diagsind in diag_state:
                        n = len(r_win)
                        r_won = any(r_win == diagsind[i:i + n] for i in range(len(diagsind)-n + 1))
                        y_won = any(y_win == diagsind[i:i + n] for i in range(len(diagsind)-n + 1))
                        if y_won:
                                print("games over, yellow won ")
                                self.board.print_board()
                                self.winner = 'y'
                                self.running = False
                                return
                        if r_won:
                                print("games over, red won")
                                self.board.print_board()
                                self.winner = 'r'
                                self.running = False
                                return
                
                if 'o' not in set([i.color for j in game.board.state for i in j]):
                        print("its a draw")
                        self.running = False
                        return
                return "cont"
                        
game = Game()
ai = State(game)
print("welcome to connect four!")
while game.running:
        game.board.print_board()
        move = input("pick a column to place your tile!")
        game.move(int(move)-1)
        ai.game = game
        print("current eval of yellow: ", ai.eval_board())