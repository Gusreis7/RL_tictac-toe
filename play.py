import argparse
from tictactoemodel import tic_tac_toe_model
from Qlearningagent import QlearningAgent
from game import Game

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_name', type=str, required=True)
    args = parser.parse_args()
    q_agent= QlearningAgent(epsilon=0,alpha=0,discount_factor=0, train=False)
    q_agent.load_agent_dict(args.file_name)
    board = tic_tac_toe_model(3)
    game = Game(board,q_agent)
    game.ia_vs_user()


if __name__ == '__main__':
    main()