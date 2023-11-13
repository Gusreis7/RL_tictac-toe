import random

import json
import ast
class QlearningAgent():
    def __init__(self, epsilon,alpha ,discount_factor, train):
        self.q_table = {}
        self.q_table_values = {}
        self.q_table_qtd = {}
        self.epsilon = epsilon
        self.alpha = alpha
        self.discount_factor = discount_factor
        self.train = train

    def save_agent_dict(self, file_name):
         # Convert tuple keys to strings
        q_table_str_keys = {str(key): value for key, value in self.q_table.items()}

        with open(file_name, 'w') as file_json:
            json.dump(q_table_str_keys, file_json)

    def load_agent_dict(self, file_name):
        try:
            with open(file_name, 'r') as file_json:
                json_data = json.load(file_json)

            # Convert string keys back to tuples
            q_table = {ast.literal_eval(key): value for key, value in json_data.items()}
            
            self.q_table = q_table
            print("Q-table loaded successfully.")
        except FileNotFoundError:
            print(f"File '{file_name}' not found. Q-table not loaded.")

    def get_q_value(self, state, action, piece):
        state_tuple = tuple(state.flatten())

        if (state_tuple,action,piece) not in self.q_table:
            self.q_table[(state_tuple, action, piece)] = 0.0
            self.q_table_qtd[(state_tuple, action, piece)] = 0
            self.q_table_values[(state_tuple, action, piece)] = 0

        return self.q_table[(state_tuple, action, piece)]

    def choose_move(self, state, available_moves, piece):
        q_values = []
        for action in available_moves:
            q_values.append(self.get_q_value(state, action, piece))
            
        if random.uniform(0, 1) < self.epsilon and self.train:
            return random.choice(available_moves)
        else:
            max_q_value = max(q_values)
            if q_values.count(max_q_value) > 1:
                best_moves = [i for i in range(len(available_moves)) if q_values[i] == max_q_value]
                i = random.choice(best_moves)
            else:
                i = q_values.index(max_q_value)
            return available_moves[i]

    def update_q_value(self, states, rewards):
        #estado atual + alpha[retorno estado atual + ymax(proximo_estado) - estado atual]
        for i,state in enumerate(states):
            rt = 0
            if state not in self.q_table.keys():
                self.q_table[state] = 0.0
                self.q_table_qtd[state] = 0
                self.q_table_values[state] = 0

            for ii in range(0,len(rewards)):
                rt+= rewards[ii] * (self.discount_factor ** (ii-i))

            if i == len(states)-1:
                next_reward = 0
            else:
                next_reward = rewards[i+1]
           
            q_formula =  self.q_table[state] + (self.alpha*(rewards[i] + self.discount_factor*(next_reward) - self.q_table[state]))
            self.q_table[state] = q_formula
            #self.q_table_qtd[state] +=1 
            #self.q_table[state] = self.q_table_values[state] / self.q_table_qtd[state]
