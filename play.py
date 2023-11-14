import argparse
from classes.game_model import tic_tac_toe_model
from classes.Qlearningagent import QlearningAgent
from classes.game import Game

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_name', type=str, required=False, default='models/q_agent-0.9ep-0.6ap-0.9-1000r.json')
    args = parser.parse_args()
    q_agent= QlearningAgent(epsilon=0,alpha=0,discount_factor=0, train=False)
    q_agent.load_agent_dict(args.file_name)
    board = tic_tac_toe_model(3)
    game = Game(board,q_agent)
    game.ia_vs_user()


if __name__ == '__main__':
    main()