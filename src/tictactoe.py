
from typing import Self
import random

class Tic_Tac_Toe:
    def __init__(self):
        self.SIZE = 3
        self.board = [[0 for i in range(self.SIZE)] for j in range(self.SIZE)]
        self.winner : int = None
    
    
    def __str__(self):
        
        y = 0
        h_div = '\n' + '-'.join(['----' for x in range(self.SIZE)]) + '\n'
        v = h_div.join(['|'.join([f' {self.board[y][x]:2} ' for x in range(self.SIZE)]) for y in range(self.SIZE)])
        return v

    def _check_for_winner(self):
        if self.winner != None:
            return
        
        # Check rows
        for row in self.board:
            if row[0] != 0:
                w = True
                for col in row[1:]:
                    if col != row[0]:
                        w = False
                        break
                if w:
                    self.winner = row[0]
                    # print(f'Row: {row}')
                    return

        # check columns
        for x in range(self.SIZE):
            if self.board[0][x] != 0:
                w = True
                for y in range(1,self.SIZE):
                    if self.board[y][x] != self.board[0][x]:
                        w = False
                        break
                if w:
                    self.winner = self.board[0][x]
                    # print(f'Column: {x}')
                    return
            
        # check diagonals
        if self.board[0][0] != 0:
            w = True
            for i in range(1,self.SIZE):
                if self.board[i][i] != self.board[0][0]:
                    w = False
                    break
            if w:
                self.winner = self.board[0][0]
                # print(f'Top Left Diagonal')
                return
            
        if self.board[0][self.SIZE-1] != 0:
            w = True
            for i in range(1,self.SIZE):
                if self.board[i][self.SIZE-1-i] != self.board[0][self.SIZE-1]:
                    w = False
                    break                    
            if w:
                self.winner = self.board[0][self.SIZE-1]
                # print(f'Top Right Diagonal')
                return
            
        if len(self.valid_moves()) < 1:
            self.winner = 0


    def move(self, position:tuple[int,int], value:int):
        y = position[0]
        x = position[1]
        if y < 0 or y >= self.SIZE or x < 0 or x > self.SIZE or value not in [-1,1] or self.winner != None:
            return False
        
        if self.board[y][x] == 0:
            self.board[y][x] = value
            self._check_for_winner()
            return True
        
        return False
    
    def valid_moves(self):
        moves = []
        for y in range(self.SIZE):
            for x in range(self.SIZE):
                if self.board[y][x] == 0:
                    moves.append((y, x))
        return moves
    
    def deep_copy(self) -> Self:
        new_game : Tic_Tac_Toe = Tic_Tac_Toe()
        
        new_game.SIZE = self.SIZE
        new_game.board = [[val for val in row] for row in self.board]
        new_game.winner = self.winner
        return new_game
        
    def compare_states(self, other:Self):
        if self.SIZE != other.SIZE:
            return False
        for y in range(self.SIZE):
            for x in range(self.SIZE):
                if self.board[y][x] != other.board[y][x]:
                    return False
        return True
    
    def play_random(self, player:int):
        p = player
        while self.winner == None:
            move = random.choice(self.valid_moves())
            self.move(move, p)
            # print(f'Player {p} move: {move}:')
            # print(self)
            p = -p        