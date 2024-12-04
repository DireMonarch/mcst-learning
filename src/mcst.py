import math
from tictactoe import Tic_Tac_Toe
import random
from typing import Self


UCT_WIN_VALUE = 25
UCT_LOSE_VALUE = 0
UCT_UNEXPLORED_VALUE = 5


class MCST_Node:
    def __init__(self, parent:Self, c : float, game : Tic_Tac_Toe, player : int, move : tuple[int, int]):
        self.w : float = 0.0
        self.n : int = 0
        self.c : float = c
        self.parent : MCST_Node = parent
        self.children : list[MCST_Node] = []
        self.game : Tic_Tac_Toe = game
        self.move : tuple[int, int] = move
        self.player : int = player  # Player who made THIS move
    
    
    def __str__(self):
        value = str(self.game)
        value += f'   w: {self.w}  /  n: {self.n}    move: {self.move}    p: {self.player}    children: {len(self.children)}\n\n'
        value += 'Parent:\n'
        value += 'None' if self.parent == None else str(self.parent)
        return value + '\n\n'
        
    def UCT(self) -> int:
        
        if self.game.winner == self.player:
            return UCT_WIN_VALUE
        
        if self.game.winner == -self.player:
            return UCT_LOSE_VALUE
        
        if self.n < 1:
            return UCT_UNEXPLORED_VALUE
        if self.parent == None:
            return -1
        
        win_rate : float = self.w / self.n
        exploration : float = self.c * math.sqrt(math.log(self.parent.n) / self.n)
        return win_rate + exploration
    
    def add_child(self, move : tuple[int, int], player:int):
        if move in self.game.valid_moves():
            new_game = self.game.deep_copy()
            new_game.move(move, player)
            child = MCST_Node(self, self.c, new_game, player, move)
            self.children.append(child)
    
class MCST:
    def __init__(self, c : float, game : Tic_Tac_Toe):
        # self.c : float = c
        self.root : MCST_Node = MCST_Node(None, c, game, 0, None)
        self.current : MCST_Node = self.root
        
    
    def __str__(self):
        value = f'{self.current.game}\nw: {self.current.w}  n: {self.current.n}  children: {len(self.current.children)}'
        return value
    
    def train(self, player:int, iterations:int):
        p = player
        for _ in range(iterations):
            self._train_step(p)
            p = -p
    
    
    def _train_step(self, player:int, debug=False) -> tuple[int, int]:
        if player not in [-1,1]:
            return None
        
        
        leaf:MCST_Node = self._selection(player)
        if leaf.game.winner == None:
        
            choice:MCST_Node = self._expansion(player, leaf)
            if choice is None:
                if debug: print('here')
                return None
            
            simulation_winner:int = self._simulation(player, choice)

        else:
            choice = leaf
            simulation_winner = leaf.game.winner
        
        self._backpropagation(simulation_winner, choice)
        
    def get_current_child(self, move:tuple[int,int]):
        for child in self.current.children:
            if child.move == move:
                return child
        return None
    
    def best_current_move(self, train_iterations:int = 1000):
        next_p = 1 if self.current.player == 0 else -self.current.player
        self.train(next_p,train_iterations)
        best = []
        best_value = -1.0        
        for child in self.current.children:
            win_ratio = 0 if child.n < 1 else child.w/child.n
            if win_ratio > best_value:
                best = [child]
                best_value = win_ratio
            elif win_ratio == best_value:
                best.append(child)            
        return random.choice(best).move
    
    
    def _selection(self, player:int) -> MCST_Node:
        if player not in [-1,1]:
            return None
        
        processing = self.current
        while len(processing.children) > 0:
            best = []
            best_value = -1.0
            for child in processing.children:
                if child.UCT() > best_value:
                    best = [child]
                    best_value = child.UCT()
                elif child.UCT() == best_value:
                    best.append(child)
            processing = random.choice(best)
        return processing
        
    def _expansion(self, player:int, leaf:MCST_Node) -> MCST_Node:
        for move in leaf.game.valid_moves():
            leaf.add_child(move, player if leaf.player == 0 else -leaf.player)
        if len(leaf.children) > 0:
            return random.choice(leaf.children)
        return None
    
    
    def _simulation(self, player:int, chosen:MCST_Node, debug=False) -> int:
        temp_game = chosen.game.deep_copy()
        temp_game.play_random(player)
        if debug: print(f'Player {player}, Winner {temp_game.winner}')
        return temp_game.winner
    
    def _backpropagation(self, winner:int, chosen:MCST_Node, debug=False):
        processing:MCST_Node = chosen
        if debug: print('\n\n')
        while processing != self.current.parent:
            processing.n += 1
            if winner != None:
                if winner == processing.player:
                    processing.w += 1
                elif winner == 0:
                    processing.w += 0.5
            processing = processing.parent
            
        if debug: print('After Backprop:')
        if debug: print(chosen)