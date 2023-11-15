import tqdm
import random
import argparse
import numpy as np
from classes.game_model import tic_tac_toe_model
from classes.Qlearningagent import QlearningAgent
from classes.environment import environment
from classes.game import Game


def print_stats(games, piece, rounds):
    enemy_piece = 2 if piece == 1 else 1
    text_piece = 'X' if piece == 1 else 'O'
    print(f"wins_games[{text_piece}]: {np.where(games==piece)[0].shape[0]*100/rounds}%\n",
        f"losses_games[{text_piece}]: {np.where(games==enemy_piece)[0].shape[0]*100/rounds}%\n",
        f"draw_games: {np.where(games==3)[0].shape[0]*100/rounds}%\n")

def make_line(mode,games, rounds,eps,alpha,df, file):
    #mode, wins x , wins_o , draws, rounds, eps, alpha, df
    line = f'{mode},{np.where(games==1)[0].shape[0]*100/rounds},' \
       f'{np.where(games==2)[0].shape[0]*100/rounds},' \
       f'{np.where(games==3)[0].shape[0]*100/rounds},' \
       f'{rounds},{eps},{alpha},{df}\n'
    file.write(line)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rounds', type=int, required=False, default=1000)
    parser.add_argument('--epsilon', type=float, required=False, default=0.5)
    parser.add_argument('--alpha', type=float, required=False, default=0.6)
    parser.add_argument('--discount_factor', type=float, required=False, default=0.7)
    args = parser.parse_args()
    train_file = open('train_reports.csv','w') 
    train_file.write('mode,wins_x,wins_o,draws,rounds,eps,alpha,discount_factor\n')
    test_file = open('test_reports.csv','w') 
    test_file.write('mode,wins_x,wins_o,draws,rounds_train,eps,alpha,discount_factor\n')

    board = tic_tac_toe_model(3)
    rounds_test = 1000

    rounds_set= [10,100,1000,10000, 100000]
    alpha_set = [0.6]
    eps_set = [0.5]
    df_set = [0.7]
    for rounds in rounds_set:
        print(rounds)
        for alpha in alpha_set:
            for eps in eps_set:
                for df in df_set:
                    print(f"{rounds}R-{alpha}AP-{eps}EP-{df}DF")
                    q_agent = QlearningAgent(epsilon=eps,alpha=alpha,discount_factor=df, train=True)
                    exp = environment(board,q_agent, train=True, show_stats=False)

                    wins_x,wins_o, wins_ia = exp.run(rounds)

                    games = np.array(wins_ia)
                    make_line('ia_vs_ia',games,rounds,eps,alpha,df, train_file)

                    games = np.array(wins_x)
                    make_line('ia[x]_vs_random',games,rounds,eps,alpha,df, train_file)

                    games = np.array(wins_o)
                    make_line('ia[o]_vs_random',games,rounds,eps,alpha,df, train_file)
   
                    q_agent.epsilon = 0
                    q_agent.train = False
                    #test
                    wins_x,wins_o, wins_ia = exp.run(rounds_test)
                    
                    games = np.array(wins_ia)
                    make_line('ia_vs_ia',games,rounds_test,eps,alpha,df, test_file)

                    games = np.array(wins_x)
                    make_line('ia[x]_vs_random',games,rounds_test,eps,alpha,df, test_file)

                    games = np.array(wins_o)
                    make_line('ia[o]_vs_random',games,rounds_test,eps,alpha,df, test_file)
    
    

if __name__ == '__main__':
    main()