import random
import numpy as np

class tic_tac_toe_model():
    def __init__(self, n):
        self.n = n
        self.matriz = np.full((n,n),0,dtype=int)
    
    def reset_matrix(self):
        self.matriz = np.full((self.n,self.n),0,dtype=int)

    def print_game(self):
        matriz = self.matriz
        substituicoes = {1: "X", 2: "O", 0:' '}
        
        cabecalho = [str(i) for i in range(0,self.n)]
        print(' ', ' | '.join(cabecalho))
        for i,linha in enumerate(matriz):
            linha_formatada = [str(substituicoes.get(valor, valor)) for valor in linha]
            print(i, " | ".join(linha_formatada))
            print("-" * 12)
    

    def number_ij(self, number):
        i,j = np.unravel_index(number, self.matriz.shape)
        return i,j
    
    
    def get_avaible_moves(self):
        avaible_moves = np.ravel_multi_index(np.where(self.matriz == 0), self.matriz.shape)
        return list(avaible_moves)

    def get_random_move(self, piece):
        possible_move_i, possible_move_j = np.where(self.matriz == 0)
        if possible_move_j.shape[0] > 0:  # Verifica se há movimentos possíveis
            index = random.randint(0, possible_move_j.shape[0] - 1)  # Correção aqui
            self.move(possible_move_i[index], possible_move_j[index], piece)



    def move(self,index_i,index_j,piece):
        if self.matriz[index_i][index_j] == 0:
            self.matriz[index_i][index_j] = piece
        
    
    def reward_piece(self,piece):
        w = self.check_win()
        if w != 4 :
            if w!=3:
                if w == piece:
                    return 1
                else:
                    return -1
            
        return 0
          
    def check_win(self):
        state = False
        win_piece = -1
        value_counts_diagonal = np.unique(self.matriz.diagonal())
        value_counts_diagonal2  = np.unique(np.fliplr(self.matriz).diagonal())
        if value_counts_diagonal.shape[0] == 1 and value_counts_diagonal[0] !=0:
            state=True     
            win_piece = value_counts_diagonal[0] 
            return win_piece          
        if value_counts_diagonal2.shape[0] == 1 and value_counts_diagonal2[0] !=0:
            state=True    
            win_piece = value_counts_diagonal2[0]   
            return win_piece         

        for i in range(0,self.n):
            value_counts_linha = np.unique(self.matriz[i,:])
            value_counts_coluna = np.unique(self.matriz[:,i])
            
            if value_counts_linha.shape[0] == 1 and value_counts_linha[0] != 0 :
                state=True
                win_piece = value_counts_linha[0]
                break
            if value_counts_coluna.shape[0] == 1 and value_counts_coluna[0] != 0:
                state=True
                win_piece = value_counts_coluna[0]
                break
            
        velha = np.where(self.matriz == 0)
        
        if state:
            return win_piece
        if velha[0].shape[0] == 0: 
            return 3
        else:
            return 4      