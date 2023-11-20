
import gradio as gr
import numpy as np
import time
from classes.game_model import tic_tac_toe_model
from classes.Qlearningagent import QlearningAgent


custom_css = """
.gradio-button {
  width: 75px; /* Defina a largura desejada */
  height: 75px; /* Defina a altura desejada */
  background-color: blue; /* Cor de fundo azul */
  color: white; /* Cor do texto (branco neste caso) */
  border: none; /* Remove a borda */
  text-align: center; /* Centraliza o texto horizontalmente */
  text-decoration: none; /* Remove a decoração do texto */
  display: inline-block; /* Permite definir largura e altura */
  font-size: 16px; /* Tamanho do texto */
  line-height: 75px; /* Centraliza o texto verticalmente */
}

"""

usr = -2
ia = -1

game_over = False
temp = -2

  
def usr_move(position,value):
    global game_over
    if value == '' and game_over == False:
      usr_piece = 'X' if usr == 1 else 'O'
      i,j = np.unravel_index(int(position)-1, shape=(3,3))
      board.move(i,j,usr) 
      board.print_game()
      w = board.check_win()

      global temp
      temp-=1
      return gr.update(size='lg', scale = 0, min_width = 100, value=usr_piece, interactive=True), gr.Number(value=temp, visible=False), gr.Number(value=w, visible=False)
    else:
      return gr.update(size='lg', scale = 0, min_width = 100, interactive=True), gr.update(value=temp, visible=False),gr.update(visible=False)
   
       
def ia_move():
    global game_over
    if game_over == False:
      state_board = board.matriz.copy()
      avaible_moves = board.get_avaible_moves()
      action = q_agent.choose_move(state_board,avaible_moves,ia)
      i, j = board.number_ij(action)
      ia_piece = 'X' if ia == 1 else 'O'
      board.move(i,j,ia)
      board.print_game()
      w = board.check_win()
      #buttons
      retornos_btn = [gr.Button(size='lg', scale = 0, min_width = 100, interactive=True)]*(action+1)
      retornos_btn[-1] = gr.Button(size='lg', scale = 0, min_width = 100, interactive=True, value=ia_piece)
      retornos_btn.extend([gr.Button(size='lg', scale = 0, min_width = 100,  interactive=True)]*(9 - action-1))
      retornos_btn.append(gr.Number(value=w, visible=False))
      return retornos_btn
    else:
      retornos_btn = [gr.Button(size='lg', scale = 0, min_width = 100, interactive=True)]*9
      retornos_btn.append(gr.Number(visible=False))
      return retornos_btn
       

def set_col_visible(selected):
    global usr
    global game_over
    game_over = False
    usr =  1 if selected  == 'X' else 2
    global ia
    ia = 2 if usr == 1 else 1
    retorn_buttons = [gr.Button(size='lg', scale = 0, min_width = 100,value='',elem_classes='gradio-button',interactive=True)]*9
    if selected == 'X':
      retorn_buttons.append(gr.Number(value=temp, visible=False))

    else:
      retorn_buttons = ia_move()

    return retorn_buttons
  
      
def reset():
  board.reset_matrix()
  buttons = [gr.Button(size='lg', scale = 0, min_width = 100,elem_classes='gradio-button',interactive=False)]*9
  return buttons


def check(n):
  msg = ''
  global game_over
  if n == 1:
    game_over = True
    msg = 'O jogador X ganhou'
    board.reset_matrix()

  elif n == 2:
    game_over = True
    msg = 'O jogador O ganhou'
    board.reset_matrix()

  elif n == 3 :
    game_over = True
    msg = 'VELHA'
    board.reset_matrix()
 
  print('check',game_over)
  return gr.update(value=msg, show_label=False)

with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:
    q_agent= QlearningAgent(epsilon=0,alpha=0,discount_factor=0, train=False)
    q_agent.load_agent_dict('models/q_agent-0.5ep-0.6ap-0.9-1000000r.json')
    board = tic_tac_toe_model(3)
    with gr.Row():
      with gr.Column() as x:
        title = gr.Text(value='Escolha uma peça', show_label=False)
        with gr.Row():
            p1 = gr.Button(size='lg', scale = 0, min_width = 100,value='',elem_classes='gradio-button',interactive=False)
            p2 = gr.Button(size='lg', scale = 0, min_width = 100,value='',elem_classes='gradio-button',interactive=False)
            p3 = gr.Button(size='lg', scale = 0, min_width = 100,value='',elem_classes='gradio-button',interactive=False)
        with gr.Row():
            p4 = gr.Button(size='lg', scale = 0, min_width = 100,value='',elem_classes='gradio-button',interactive=False)
            p5 = gr.Button(size='lg', scale = 0, min_width = 100,value='',elem_classes='gradio-button',interactive=False)
            p6 = gr.Button(size='lg', scale = 0, min_width = 100,value='',elem_classes='gradio-button',interactive=False)
        with gr.Row():
            p7 = gr.Button(size='lg', scale = 0, min_width = 100,value='',elem_classes='gradio-button',interactive=False)
            p8 = gr.Button(size='lg', scale = 0, min_width = 100,value='',elem_classes='gradio-button',interactive=False)
            p9 = gr.Button(size='lg', scale = 0, min_width = 100,value='',elem_classes='gradio-button',interactive=False)

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
      game_state = gr.Number(value="0", visible=False)

      with gr.Column():
        c1 = gr.Radio( ['X','O'],label='Jogar como')
        clear_button = gr.Button(value='Resetar')


    buttons = [p1, p2, p3, p4, p5, p6, p7, p8, p9,win_number]
    renders_components = [p1, p2, p3, p4, p5, p6, p7, p8, p9, win_number] 
    game_components = [p1, p2, p3, p4, p5, p6, p7, p8, p9, title,temp_number,win_number, c1]
    only_buttons = [p1, p2, p3, p4, p5, p6, p7, p8, p9]
    p1.click(fn=usr_move,inputs=[n1,p1], outputs = [p1,temp_number,win_number])
    p2.click(fn=usr_move,inputs=[n2,p2], outputs = [p2,temp_number,win_number])
    p3.click(fn=usr_move,inputs=[n3,p3], outputs = [p3,temp_number,win_number])
    p4.click(fn=usr_move,inputs=[n4,p4], outputs = [p4,temp_number,win_number])
    p5.click(fn=usr_move,inputs=[n5,p5], outputs = [p5,temp_number,win_number])
    p6.click(fn=usr_move,inputs=[n6,p6], outputs = [p6,temp_number,win_number])
    p7.click(fn=usr_move,inputs=[n7,p7], outputs = [p7,temp_number,win_number])
    p8.click(fn=usr_move,inputs=[n8,p8], outputs = [p8,temp_number,win_number])
    p9.click(fn=usr_move,inputs=[n9,p9], outputs = [p9,temp_number,win_number])


    def update_buttons():
      global game_over
      game_over = True
      return {p1: '', p2:'', p3:'', p4:'', p5:'', p6:'', p7:'', p8:'', p9:'', 
              title:'Escolha uma peça',temp_number:10, win_number:4, c1: ''}
    
   
          
    c1.select(fn=set_col_visible, inputs= c1, outputs=buttons)


    temp_number.change(fn=ia_move,outputs=renders_components)
    win_number.change(fn=check, inputs=win_number, outputs=title)
    clear_button.click(fn=update_buttons,outputs=game_components)
    clear_button.click(fn=reset,outputs=only_buttons)



demo.launch()


