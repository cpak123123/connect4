# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 17:22:01 2021

@author: cpak1
"""
import sys
import copy
from collections import defaultdict
class State:
        def __init__(self, game, score = 0):
                #as to not touch the actual game
                self.game = game
                self.score= score
                pass
        def isTerm(self):
                #column checkk
                return self.game.running
        def sim_move(self, move_sim):
                temp_game = copy.copy(self.game)
                temp_game.move(move_sim)
                return temp_game
        #only done for p1, p2 can try to minimize this: heuristic is number of consecutive pieces in a row
        def eval_board(self, state, color = 'y'):
                col_state = []                        
                for cols in range(len(state)):
                        col_state.append([x[cols].color for x in state])
                value = 0
                for col in col_state:
                        ch = []
                        i = 0
                        while (col[i] == 'o' or col[i] == color) and i < len(col)-1:
                                ch.append(col[i])
                                i = i +1
                        if col[i] == 'o' or col[i] == color:
                                ch.append(col[i])
                        value += ch.count(color)**2
                row_state = []
                for rows in range(len(state[0])-1):
                        row_state.append([x.color for x in state[rows]])
                for row in row_state:
                        i = 0
                        ch = []
                        while (row[i] == 'o' or row[i] == color) and i < len(row)-1:
                                ch.append(row[i])
                                i+=1 
                        if row[i] == 'o' or row[i] == color:
                                ch.append(row[i])
                        value += ch.count(color)**2
                diag_state = []
                diag_lr = defaultdict(list)
                diag_rl = defaultdict(list)
                for i in range(len(state)):
                        for j in range(len(state[0])):
                                diag_lr[i-j].append(state[i][j].color)
                                diag_rl[i+j].append(state[i][j].color)
                for item in diag_lr.values():
                        if len(item) >= 4:
                                diag_state.append(item)
                for item in diag_rl.values():
                        if len(item) >= 4:
                                diag_state.append(item)
                for diag in diag_state:
                        i = 0
                        ch = []
                        while (diag[i] == 'o' or diag[i] == color) and i < len(diag)-1:
                                ch.append(diag[i])
                                i+= 1
                        if diag[i] == 'o' or diag[i] == color:
                                ch.append(diag[i])
                        value += ch.count(color)**2  

                return value
        
        def avalMoves(self):
                cols = []
                state = self.game.board.state
                for i in range(len(state)):
                        if 'o' in set([x.color for x in state[i]]):
                              cols.append(i)
                return cols
        def maxVal(self, game, depth):   
                v = -sys.maxsize+1
                if self.isTerm():
                   if self.game.winner == 'y':
                           return sys.maxsize-1
                   if self.game.winner == 'r':
                           return -sys.maxsize+1
                   return 0
                if depth == 0:
                        return self.eval_board(game.board.state)
                while depth > 0:
                        moves = self.avalMoves()
                        for move in moves:
                                result = self.sim_move(move)
                                v = min(v, self.minVal(game, depth-1))
                return v
        def minVal(self, game, depth):
                v = -sys.maxsize+1
                if self.isTerm():
                   if self.game.winner == 'y':
                           return sys.maxsize-1
                   if self.game.winner == 'r':
                           return -sys.maxsize+1
                   return 0
                if depth == 0:
                        return self.eval_board(game.board.state)
                while depth > 0:
                        moves = self.avalMoves()
                        for move in moves:
                                result = self.sim_move(move)
                                v = min(v, self.maxVal(game, depth-1))
                return v
                
                        
        
                
                
                        
                

        