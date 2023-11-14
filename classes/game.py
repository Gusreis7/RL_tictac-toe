import tqdm
import random
from classes.game_model import tic_tac_toe_model
from classes.Qlearningagent import QlearningAgent

class Game():
    def __init__(self, tic_tac_toe: tic_tac_toe_model, q_agent: QlearningAgent):
        self.board = tic_tac_toe
        self.q_agent = q_agent
    
    def ia_vs_ia(self):
        game_over = False
        self.board.reset_matrix()
        while not game_over:
            w = self.board.check_win()
            if w != 4:
                win_piece = w
                break
            state = self.board.matriz.copy()
            avaible_moves = self.board.get_avaible_moves()
            action = self.q_agent.choose_move(state,avaible_moves,1)
            i, j = self.board.number_ij(action)
            self.board.move(i,j,1)
            if w != 4:
                win_piece = w
                break

            state = self.board.matriz.copy()
            avaible_moves = self.board.get_avaible_moves()
            action = self.q_agent.choose_move(state,avaible_moves,2)
            i, j = self.board.number_ij(action)
            self.board.move(i,j,2)

            
        return win_piece
        
    def run_ia_vs_ia(self,n):
        games = []
        for i in tqdm.tqdm(range(0,n)):
            w = self.ia_vs_ia()
            games.append(w)
        return games
    
    def ia_vs_user(self):
        print('Menu')
        print("1 - Iniciar aleatorio")
        print("2 - Escolher peça [X-O]")
        m1 = int(input())
        while m1 != 1 and m1 !=2:
            print('Insira um valor valido 1-2')
            print("1 - Iniciar aleatorio")
            print("2 - Escolher peça [X-O]")
            m1 = int(input())

        game_over = False
        self.board.reset_matrix()
        pieces = [1,2]
        win_piece = 0
        if m1 == 1 :
            user = random.choice(pieces)    
        else:
            print('1 - X \n 2 - O')
            user = int(input())
            while user != 1 and user !=2:
                print("Insira um valor válido 1-2")
                print('1 - X\n2 - O')
                user = int(input())
                

        ia = 2 if user == 1 else 1
        print("Começo de jogo")
        self.board.print_game()
        if ia == 1:
            while not game_over:
                state = self.board.matriz.copy()
                avaible_moves = self.board.get_avaible_moves()
                action = self.q_agent.choose_move(state,avaible_moves,ia)
                i, j = self.board.number_ij(action)
                print('Jogada da IA - X')
                self.board.move(i,j,ia)
                self.board.print_game()
                w = self.board.check_win()
                if w != 4:
                    win_piece = w
                    break
                print("Jogue Usuario - O [Numero da linha][Numero da coluna]")
                ml,mv = int(input()), int(input())
                self.board.move(ml,mv,user)
                self.board.move(i,j,user)
                self.board.print_game()
                w = self.board.check_win()
                if w != 4:
                    win_piece = w
                    break

        else:
             while not game_over:
                print('Jogue Usuario - X [Numero da linha][Numero da coluna]')
                ml,mv = int(input()), int(input())

                self.board.move(ml,mv,user)
                self.board.print_game()
                w = self.board.check_win()
                if w != 4:
                    win_piece = w
                    break

                print('Jogada da IA - O')
                state = self.board.matriz.copy()
                avaible_moves = self.board.get_avaible_moves()
                action = self.q_agent.choose_move(state,avaible_moves,ia)
                i, j = self.board.number_ij(action)
                self.board.move(i,j,ia)
                w = self.board.check_win()

                self.board.print_game()

                if w != 4:
                    win_piece = w
                    break
               

        if win_piece == ia :
            print("IA venceu Humano Fraco")
        elif win_piece == user :
            print("Humano venceu, esta preparado para a revolução?")
        else:
            print('Deu velha, mas a I.A segue aprendendo e melhorando e você?')
        return win_piece
        