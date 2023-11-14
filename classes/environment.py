import tqdm
from classes.game_model import tic_tac_toe_model
from classes.Qlearningagent import QlearningAgent

class environment():
    def __init__(self, tic_tac_toe: tic_tac_toe_model, q_agent: QlearningAgent, train: bool):
        self.board = tic_tac_toe
        self.q_agent = q_agent
        self.train = train
    
    def play_one_game(self, piece):
        game_over = False
        win_piece = 0
        self.board.reset_matrix()
        if piece == 1:
            piece_enemy = 2
            states_x = []
            rewards_x = []
            while not game_over:
                w = self.board.check_win()
                if w != 4:
                    state = self.board.matriz.copy()
                    reward_x = self.board.reward_piece(piece)
                    state_x = (tuple(state.flatten()),-1,piece)# -1 for terminal state
                    states_x.append(state_x)
                    rewards_x.append(reward_x)
                    win_piece = w
                    break

                #x move and state/reward/move dynamic
                state = self.board.matriz.copy()
                avaible_moves = self.board.get_avaible_moves()
                action_x = self.q_agent.choose_move(state,avaible_moves,piece)
                i, j = self.board.number_ij(action_x)
                self.board.move(i,j,piece)
                reward_x = self.board.reward_piece(piece)
                state_x = (tuple(state.flatten()),action_x,piece)
                states_x.append(state_x)
                rewards_x.append(reward_x)
                w = self.board.check_win()
                if w != 4:
                    state = self.board.matriz.copy()
                    reward_x = self.board.reward_piece(piece)
                    state_x = (tuple(state.flatten()),-1,piece)# -1 for terminal state
                    states_x.append(state_x)
                    rewards_x.append(reward_x)
                    win_piece = w
                    break
                self.board.get_random_move(piece_enemy)
               
            self.q_agent.update_q_value(states_x,rewards_x)
                
            return win_piece
        else:
            piece_enemy = 1
            states_o = []
            rewards_o = []
            while not game_over:
                self.board.get_random_move(piece_enemy)
               
                w = self.board.check_win()  
                if w != 4:
                    state = self.board.matriz.copy()
                    reward_o = self.board.reward_piece(piece)
                    state_o = (tuple(state.flatten()),-1,piece)# -1 for terminal state
                    states_o.append(state_o)
                    rewards_o.append(reward_o)
                    win_piece = w
                    break
                state = self.board.matriz.copy()
                avaible_moves = self.board.get_avaible_moves()
                action_o = self.q_agent.choose_move(state,avaible_moves,piece)
                i, j = self.board.number_ij(action_o)
                self.board.move(i,j,piece)
                
                reward_o = self.board.reward_piece(piece)
                state_o = (tuple(state.flatten()), action_o, piece)
                states_o.append(state_o)
                rewards_o.append(reward_o)
                w = self.board.check_win()  
                if w != 4:
                    state = self.board.matriz.copy()
                    reward_o = self.board.reward_piece(piece)
                    state_o = (tuple(state.flatten()),-1,piece)# -1 for terminal state
                    states_o.append(state_o)
                    rewards_o.append(reward_o)
                    win_piece = w
                    break
                 
            self.q_agent.update_q_value(states_o,rewards_o)
                
            return win_piece
   
            
    def play_ia_vs_ia(self):
        game_over = False
        self.board.reset_matrix()
        ia_x = 1
        ia_o = 2
        states_x = []
        rewards_x = []
        states_o = []
        rewards_o = []
        while not game_over:
            w = self.board.check_win()
            if w != 4:
                win_piece = w
                break
            state_x = self.board.matriz.copy()
            avaible_moves_x = self.board.get_avaible_moves()
            action_x = self.q_agent.choose_move(state_x,avaible_moves_x,ia_x)
            i, j = self.board.number_ij(action_x)
            self.board.move(i,j,ia_x) # x play

            #x state/reward
            reward_x = self.board.reward_piece(ia_x)
            state_x = (tuple(state_x.flatten()),action_x,ia_x)
            states_x.append(state_x)
            rewards_x.append(reward_x)

            w = self.board.check_win()
            if w != 4:
                win_piece = w
                break

            state_o = self.board.matriz.copy()
            avaible_moves_o = self.board.get_avaible_moves()
            action_o = self.q_agent.choose_move(state_o,avaible_moves_o,ia_o)
            i, j = self.board.number_ij(action_o)
            self.board.move(i,j,ia_o) # o play

            reward_o = self.board.reward_piece(ia_o)
            state_o = (tuple(state_o.flatten()),action_o,ia_o)
            states_o.append(state_o)
            rewards_o.append(reward_o)
        
        if win_piece == 1:
            state = self.board.matriz.copy()
            reward_o = self.board.reward_piece(ia_o)
            state_o = (tuple(state.flatten()),-1,ia_o)# -1 for terminal state
            states_o.append(state_o)
            rewards_o.append(reward_o)     
        elif win_piece == 2:
            state = self.board.matriz.copy()
            reward_x = self.board.reward_piece(ia_x)
            state_x = (tuple(state.flatten()),-1,ia_x)# -1 for terminal state
            states_x.append(state_x)
            rewards_x.append(reward_x)

            
        self.q_agent.update_q_value(states_x,rewards_x)
        self.q_agent.update_q_value(states_o,rewards_o)

        return win_piece
    
    
    def run(self, n):
        wins_x = []
        wins_o = []
        wins_ia = []
        
        print(f'Playing {n} games with X')
        for i in tqdm.tqdm(range(0,n)):
            wins_x.append(self.play_one_game(piece=1))
        
        print(f'Playing {n} games with O')
        for i in tqdm.tqdm(range(0,n)):
            wins_o.append(self.play_one_game(piece=2))

        print(f'Playing {n} games ia vs ia')
        for i in tqdm.tqdm(range(0,n)):
            wins_ia.append(self.play_ia_vs_ia())
        
        return wins_x,wins_o, wins_ia