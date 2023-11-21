
import gradio as gr
import numpy as np
import time
import argparse
from classes.game_model import tic_tac_toe_model
from classes.Qlearningagent import QlearningAgent


def main():
  custom_css = """
    #color {background-color: #00BFFF}
    .gradio-button {
      width: 75px; /* Defina a largura desejada */
      height: 75px; /* Defina a altura desejada */
      background-color: #6495ED; /* Cor de fundo azul */
      color: black; /* Cor do texto (branco neste caso) */
      border: none; /* Remove a borda */
      text-align: center; /* Centraliza o texto horizontalmente */
      text-decoration: none; /* Remove a decoração do texto */
      display: inline-block; /* Permite definir largura e altura */
      font-size: 16px; /* Tamanho do texto */
      line-height: 75px; /* Centraliza o texto verticalmente */
    }

  """

  def usr_move(board,usr,game_over,temp,position,value):
      temp = int(temp)
      if value == '' and int(game_over) == -1:
        usr_piece = 'X' if int(usr) == 1 else 'O'
        i,j = np.unravel_index(int(position)-1, shape=(3,3))
        board.move(i,j,int(usr)) 
        w = board.check_win()
        temp-=1
        return gr.update(size='lg',elem_id='color', scale = 0, min_width = 100, value=usr_piece, interactive=True), gr.Number(value=temp, visible=False), gr.Number(value=w, visible=False), board
      else:
        return gr.update(size='lg',elem_id='color', scale = 0, min_width = 100, interactive=True), gr.update(value=temp, visible=False),gr.update(visible=False)
      
          
  def ia_move(board,game_over,ia):
      if int(game_over) == -1:
        state_board = board.matriz.copy()
        avaible_moves = board.get_avaible_moves()
        action = q_agent.choose_move(state_board,avaible_moves,int(ia))
        i, j = board.number_ij(action)
        ia_piece = 'X' if int(ia) == 1 else 'O'
        board.move(i,j,int(ia))
        w = board.check_win()
        #buttons
        retornos_btn = [gr.Button(size='lg',elem_id='color', scale = 0, min_width = 100, interactive=True)]*(action+1)
        retornos_btn[-1] = gr.Button(size='lg',elem_id='color', scale = 0, min_width = 100, interactive=True, value=ia_piece)
        retornos_btn.extend([gr.Button(size='lg',elem_id='color', scale = 0, min_width = 100,  interactive=True)]*(9 - action-1))
        retornos_btn.append(gr.Number(value=w, visible=False))
        retornos_btn.append(board)

        return retornos_btn
      else:
        retornos_btn = [gr.Button(size='lg',elem_id='color', scale = 0, min_width = 100, interactive=True)]*9
        retornos_btn.append(gr.Number(visible=False))
        retornos_btn.append(board)

        return retornos_btn
          
  def set_col_visible(board,game_over,temp,usr,ia,selected):
      usr =  1 if selected  == 'X' else 2
      ia = 2 if usr == 1 else 1
      game_over = -1
      retorn_buttons = [gr.Button(size='lg',elem_id='color', scale = 0, min_width = 100,value='',elem_classes='gradio-button',interactive=True)]*9
      if selected == 'X':
        retorn_buttons.append(gr.Number(value=temp, visible=False))
        retorn_buttons.append(gr.Number(value=-1, visible=False))
        retorn_buttons.append(gr.Number(value=ia, visible=False))
        retorn_buttons.append(gr.Number(value=usr, visible=False))
        
        retorn_buttons.append(board)

      else:
        retorn_buttons = ia_move(board,game_over,ia)
        retorn_buttons.insert(-1,gr.Number(value=-1, visible=False))
        retorn_buttons.insert(-1,gr.Number(value=ia, visible=False))
        retorn_buttons.insert(-1,gr.Number(value=usr, visible=False))
      

      return retorn_buttons
      
          
  def reset(board):
      board.reset_matrix()
      buttons = [gr.Button(size='lg',elem_id='color', scale = 0, min_width = 100,elem_classes='gradio-button',interactive=False)]*9
      buttons.append(board)
      return buttons


  def check(game_over,n):
      msg = ''
      if n == 1:
        game_over = 1
        msg = 'O jogador X ganhou'

      elif n == 2:
        game_over = 1
        msg = 'O jogador O ganhou'

      elif n == 3 :
        print('check',game_over)

        game_over = 1
        msg = 'VELHA'
    
      return gr.update(value=msg, show_label=False), gr.Number(value=int(game_over), visible=False)
  
  parser = argparse.ArgumentParser()
  parser.add_argument('--file_name', type=str, required=False, default='models/q_agent-0.9ep-0.6ap-0.9-1000r.json')
  args = parser.parse_args()
  q_agent= QlearningAgent(epsilon=0,alpha=0,discount_factor=0, train=False)
  q_agent.load_agent_dict(args.file_name)

  with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:
      with gr.Row():
        with gr.Column() as x:
          title = gr.Text(value='Escolha uma peça', show_label=False)
          with gr.Row():
              p1 = gr.Button(size='lg',elem_id='color', scale = 0, min_width = 100,value='',elem_classes='gradio-button',interactive=False)
              p2 = gr.Button(size='lg',elem_id='color', scale = 0, min_width = 100,value='',elem_classes='gradio-button',interactive=False)
              p3 = gr.Button(size='lg',elem_id='color', scale = 0, min_width = 100,value='',elem_classes='gradio-button',interactive=False)
          with gr.Row():
              p4 = gr.Button(size='lg',elem_id='color', scale = 0, min_width = 100,value='',elem_classes='gradio-button',interactive=False)
              p5 = gr.Button(size='lg',elem_id='color', scale = 0, min_width = 100,value='',elem_classes='gradio-button',interactive=False)
              p6 = gr.Button(size='lg',elem_id='color', scale = 0, min_width = 100,value='',elem_classes='gradio-button',interactive=False)
          with gr.Row():
              p7 = gr.Button(size='lg',elem_id='color', scale = 0, min_width = 100,value='',elem_classes='gradio-button',interactive=False)
              p8 = gr.Button(size='lg',elem_id='color', scale = 0, min_width = 100,value='',elem_classes='gradio-button',interactive=False)
              p9 = gr.Button(size='lg',elem_id='color', scale = 0, min_width = 100,value='',elem_classes='gradio-button',interactive=False)

        n1 = gr.Number(value="1", visible=False)
        n2 = gr.Number(value="2", visible=False)
        n3 = gr.Number(value="3", visible=False)
        n4 = gr.Number(value="4", visible=False)
        n5 = gr.Number(value="5", visible=False)
        n6 = gr.Number(value="6", visible=False)
        n7 = gr.Number(value="7", visible=False)
        n8 = gr.Number(value="8", visible=False)
        n9 = gr.Number(value="9", visible=False)
        temp_number = gr.Number(value="10", visible=False)
        win_number = gr.Number(value="4", visible=False)

        usr = gr.Number(value="-2", visible=False)
        ia = gr.Number(value="-1", visible=False)
        game_over = gr.Number(value="-1", visible=False)
        temp = gr.Number(value="-2", visible=False)

        with gr.Column():
          c1 = gr.Radio( ['X','O'],label='Jogar como')
          clear_button = gr.Button(value='Resetar')


      board = gr.State(tic_tac_toe_model(3))
      buttons = [p1, p2, p3, p4, p5, p6, p7, p8, p9,win_number, game_over,ia,usr,board]
      renders_components = [p1, p2, p3, p4, p5, p6, p7, p8, p9, win_number,board] 
      game_components = [p1, p2, p3, p4, p5, p6, p7, p8, p9, title,temp_number,win_number, c1,game_over]
      only_buttons = [p1, p2, p3, p4, p5, p6, p7, p8, p9,board]
      p1.click(fn=usr_move,inputs=[board,usr,game_over,temp_number,n1,p1], outputs = [p1,temp_number,win_number,board])
      p2.click(fn=usr_move,inputs=[board,usr,game_over,temp_number,n2,p2], outputs = [p2,temp_number,win_number,board])
      p3.click(fn=usr_move,inputs=[board,usr,game_over,temp_number,n3,p3], outputs = [p3,temp_number,win_number,board])
      p4.click(fn=usr_move,inputs=[board,usr,game_over,temp_number,n4,p4], outputs = [p4,temp_number,win_number,board])
      p5.click(fn=usr_move,inputs=[board,usr,game_over,temp_number,n5,p5], outputs = [p5,temp_number,win_number,board])
      p6.click(fn=usr_move,inputs=[board,usr,game_over,temp_number,n6,p6], outputs = [p6,temp_number,win_number,board])
      p7.click(fn=usr_move,inputs=[board,usr,game_over,temp_number,n7,p7], outputs = [p7,temp_number,win_number,board])
      p8.click(fn=usr_move,inputs=[board,usr,game_over,temp_number,n8,p8], outputs = [p8,temp_number,win_number,board])
      p9.click(fn=usr_move,inputs=[board,usr,game_over,temp_number,n9,p9], outputs = [p9,temp_number,win_number,board])


      def update_buttons():
        return {p1: '', p2:'', p3:'', p4:'', p5:'', p6:'', p7:'', p8:'', p9:'', 
                title:'Escolha uma peça',temp_number:10, win_number:4, c1: '', game_over: 1}
      
    
      c1.select(fn=set_col_visible, inputs= [board,game_over,temp,usr,ia,c1], outputs=buttons)
      temp_number.change(fn=ia_move,inputs=[board,game_over,ia],outputs=renders_components)
      win_number.change(fn=check, inputs=[game_over,win_number], outputs=[title, game_over])
      clear_button.click(fn=update_buttons,outputs=game_components)
      clear_button.click(fn=reset,inputs=board,outputs=only_buttons)



  demo.launch()

if __name__ == '__main__':
    main()

