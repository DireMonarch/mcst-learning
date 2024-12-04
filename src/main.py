import mcst
from tictactoe import Tic_Tac_Toe
import random
import math
import visualize    

GLOBAL_C = math.sqrt(2)

def play_random(game:Tic_Tac_Toe):
    print(game)
    
    player = 1

    game.play_random(player)
    
    # while game.winner == None:
    #     move = random.choice(game.valid_moves())
    #     game.move(move, player)
    #     print(f'Player {player} move: {move}:')
    #     print(game)
    #     player = -player


def play_mcst(game:Tic_Tac_Toe):
    tree = mcst.MCST(GLOBAL_C,game)

    tree.train(1, 1000)

    while game.winner == None and len(game.valid_moves()) > 0:
        pick = -1
        while pick not in range(len(game.valid_moves())):
            print(game)
            print('\nValid moves: ')
            for i, move in enumerate(game.valid_moves()):
                print(f'{i}: {move}')
            pick = int(input('Pick a move:'))
        move = game.valid_moves()[pick]
        game.move(move,1)
        next = tree.get_current_child(move)
        if next == None:
            print("ERROR!!!")
            return
        tree.current = next
        
        print(game)

        if game.winner == None:
            pc_move = tree.best_current_move()
            game.move(pc_move,-1)
            next = tree.get_current_child(pc_move)
            if game.winner == None and next == None:
                print("ERROR!!!")
                return
            tree.current = next
            print(f"\nPC Move {pc_move}")
            print(game)
        
    

def auto_play(count):
    for _ in range(count):
        game = Tic_Tac_Toe()
        tree = mcst.MCST(GLOBAL_C, game)
        
        current_player = 1
        while game.winner == None:
            tree.train(current_player, 1000)
            move = tree.best_current_move()
            game.move(move, current_player)
            next = tree.get_current_child(move)
            tree.current = next
            current_player = -current_player
            
        print(game, game.winner)
            

def main():
    game = Tic_Tac_Toe()

    # play_random(game)
    # play_mcst(game)
    auto_play(100)
        
    print(f'Winner is {game.winner}')
    


if __name__ == "__main__":
    main()