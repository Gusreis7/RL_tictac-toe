import tqdm
import random
import argparse
import numpy as np
from tictactoemodel import tic_tac_toe_model
from Qlearningagent import QlearningAgent
from environment import environment
from game import Game


def print_stats(games, piece, rounds):
    enemy_piece = 2 if piece == 1 else 1
    text_piece = 'X' if piece == 1 else 'O'
    text_enemy = 'O' if piece == 1 else 'X'
    print(f"wins_games[{text_piece}]: {np.where(games==piece)[0].shape[0]*100/rounds}%\n",
        f"losses_games[{text_enemy}]: {np.where(games==enemy_piece)[0].shape[0]*100/rounds}%\n",
        f"draw_games: {np.where(games==3)[0].shape[0]*100/rounds}%\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rounds', type=int, required=True)
    parser.add_argument('--epsilon', type=float, required=False, default=0.9)
    parser.add_argument('--alpha', type=float, required=False, default=0.6)
    parser.add_argument('--discount_factor', type=float, required=False, default=0.9)
    args = parser.parse_args()

    board = tic_tac_toe_model(3)
    rounds = args.rounds
    q_agent = QlearningAgent(epsilon=args.epsilon,alpha=args.alpha,discount_factor=args.discount_factor, train=True)
    print(f"Loaded Q-agent with:\n{args.epsilon:.2f} epsilon \n{args.alpha:.2f} alpha\n{args.discount_factor:.2f} discount factor\n")
    exp = environment(board,q_agent, train=True)
    print(f"Running Q-learning for {rounds} games")
    wins_x,wins_o, wins_ia = exp.run(rounds)
    print('Results training')

    print("IA VS IA")
    games = np.array(wins_ia)
    print_stats(games,1,rounds)
    print('IA[X] vs Random ')
    games = np.array(wins_x)
    print_stats(games,1,rounds)

    print('IA[0] vs Random ')
    games = np.array(wins_o)
    print_stats(games,2,rounds)
    
    print('Running 1000 test games without epsilon factor')
    q_agent.epsilon = 0
    q_agent.train = False

    rounds_test = 1000
    wins_x,wins_o, wins_ia = exp.run(rounds_test)
    print("Test results")
    print("IA VS IA")
    games = np.array(wins_ia)
    print_stats(games,1,rounds_test)
    print('IA[X] vs Random ')
    games = np.array(wins_x)
    print_stats(games,1,rounds_test)

    print('IA[0] vs Random ')
    games = np.array(wins_o)
    print_stats(games,2,rounds_test)
    
    print("Saving q agent as a json file")
    file_name = f"q_agent-{args.epsilon}ep-{args.alpha}ap-{args.discount_factor}-{rounds}r.json"
    q_agent.save_agent_dict(file_name)    
    print(f"Saved q_agent at: {file_name}")


if __name__ == '__main__':
    main()