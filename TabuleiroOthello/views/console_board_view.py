"""View do jogo de Othelo."""

import Tkinter as Tkinter
import tkMessageBox as Alert
import ttk as Ttk

from models.board import Board

# Constantes mutaveis; podem ser mudadas para melhor visualizacao do tabuleiro
WINDOW_NAME = 'Othelo'
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 400

TABULEIRO_X = 20
TABULEIRO_Y = 20
TABULEIRO_SIDE = 396.0
TABULEIRO_COLOR = '#CCC'
TABULEIRO_DISCO_MARGEM = 10

# Constantes imutaveis; necessarias deste jeito para o funcionamento do app
TABULEIRO_CASA_NUM = 9
TABULEIRO_CASA_SIDE = TABULEIRO_SIDE/TABULEIRO_CASA_NUM

class ConsoleBoardView(object):
    """Objeto de view do jogo de Othelo."""

    def __init__(self, controller, board):
        self.controller = controller
        self.board = board
        self.jogadores = None

        # Variavel que define se a partida ja comecou ou nao
        self.partida_iniciada = 0

        # Inicia a janela do programa
        self.master = Tkinter.Tk()
        self.master.title(WINDOW_NAME)
        self.master.minsize(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.master.maxsize(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)

        # Inicia o canvas usado para desenhar o tabuleiro
        self.canvas = Tkinter.Canvas(self.master, width=TABULEIRO_SIDE + TABULEIRO_X*2,
                                     height=TABULEIRO_SIDE + TABULEIRO_Y*2)
        self.canvas.grid(row=0, rowspan=16, column=0, columnspan=6)

        # Desenhando as casas do tabuleiro
        for i in range(0, TABULEIRO_CASA_NUM-1):
            for j in range(0, TABULEIRO_CASA_NUM-1):
                self.canvas.create_rectangle(TABULEIRO_X + TABULEIRO_CASA_SIDE*i,
                                             TABULEIRO_Y + TABULEIRO_CASA_SIDE*j,
                                             TABULEIRO_X + TABULEIRO_CASA_SIDE*(i+1),
                                             TABULEIRO_Y + TABULEIRO_CASA_SIDE*(j+1),
                                             fill=TABULEIRO_COLOR, outline='#000', tag='tabuleiro')

        # Label de "Escolha os jogadores"
        self.escolha_label = Tkinter.Label(self.master, text="Escolha os jogadores",
                                           font=("Helvetica", 16))
        self.escolha_label.grid(row=1, column=7, columnspan=4)

        # Label "Black Player:"
        self.black_label = Tkinter.Label(self.master, text="Black player:")
        self.black_label.grid(row=2, column=7, columnspan=1)

        # Combobox de "Black Player"
        self.black_box_value = None
        self.black_box = Ttk.Combobox(self.master, textvariable=self.black_box_value)
        self.black_box.grid(row=2, column=8, columnspan=2)

        # Label "White Player:"
        self.white_label = Tkinter.Label(self.master, text="White player:")
        self.white_label.grid(row=3, column=7, columnspan=1)

        # Combobox de "White Player"
        self.white_box_value = None
        self.white_box = Ttk.Combobox(self.master, textvariable=self.white_box_value)
        self.white_box.grid(row=3, column=8, columnspan=2)

        # Label de estado atual da partida
        self.status_label = Tkinter.Label(self.master, text="",
                                          font=("Helvetica", 14))
        self.status_label.grid(row=8, column=7, columnspan=4)

        # Label de jogador atual da partida
        self.player_label = Tkinter.Label(self.master, text="",
                                          font=("Helvetica-Bold", 14))
        self.player_label.grid(row=9, column=7, columnspan=4)

        # Botao de Avancar
        self.action_button = Tkinter.Button(self.master, text="Avancar",
                                            command=self.realizar_proxima_jogada)
        self.action_button.grid(row=12, column=7, columnspan=3)
        self.master.bind('<Return>', self.realizar_proxima_jogada)

    def reiniciar_jogo(self, board):
        """Permite reiniciar o tabuleiro depois do fim de uma partida."""
        self.board = board
        self.partida_iniciada = 0
        self.status_label['text'] = ''
        self.player_label['text'] = ''
        self.canvas.delete('discos')

    def realizar_proxima_jogada(self, event=None):
        """Permitir que a proxima jogada seja executada."""

        if self.partida_iniciada == 0:
            white_box_value = self.jogadores[int(self.white_box.current())]
            black_box_value = self.jogadores[int(self.black_box.current())]

            self.controller.white_player = self.controller.select_player(white_box_value, Board.WHITE)
            self.controller.black_player = self.controller.select_player(black_box_value, Board.BLACK)
            self.controller.atual_player = self.controller.black_player

            self.partida_iniciada = 1
            self.atualizar_discos()
            self.atualizar_jogador_atual(self.controller.atual_player.color)
        else:
            self.controller.next_round()

    def carregar_jogadores_possiveis(self, jogadores):
        """Carrega os nomes dos jogadores possiveis nos ComboBoxes."""
        self.jogadores = jogadores

        self.black_box['values'] = jogadores
        self.black_box.current(0)
        self.black_box_value = jogadores[0]

        self.white_box['values'] = jogadores
        self.white_box.current(0)
        self.white_box_value = jogadores[0]

    def put_view_in_main_loop(self):
        """Coloca a view em loop principal quando o terminal para de ser usado."""
        self.master.mainloop()

    def atualizar_estado(self, estado):
        """Atualiza a label de estado com o valor fornecido."""
        self.status_label['text'] = estado

    def atualizar_jogador_atual(self, jogador):
        """Informa ao jogador por meio de uma label qual sera o proximo jogador."""
        if jogador == '@':
            self.player_label['text'] = 'Proxima jogada: Black'
        if jogador == 'o':
            self.player_label['text'] = 'Proxima jogada: White'

    def anunciar_vitorioso(self, vencedor, perdedor, pontos_vencedor, pontos_perdedor):
        """Anuncia caso alguem venca a partida."""
        self.status_label['text'] = (vencedor + ' venceu!')
        self.player_label['text'] = 'Fim de jogo'

        Alert.showinfo('Fim de jogo', vencedor + ' venceu a partida contra ' + perdedor +
                       ' (' + str(pontos_vencedor) + ' - ' + str(pontos_perdedor) + ')!')

    def _desenhar_disco(self, i, j, color):
        margem = TABULEIRO_DISCO_MARGEM
        pos_x0 = TABULEIRO_X + TABULEIRO_CASA_SIDE*(j-1) + margem
        pos_y0 = TABULEIRO_Y + TABULEIRO_CASA_SIDE*(i-1) + margem
        pos_x1 = TABULEIRO_X + TABULEIRO_CASA_SIDE*j - margem
        pos_y1 = TABULEIRO_Y + TABULEIRO_CASA_SIDE*i - margem

        if color == '@':
            self.canvas.create_oval(pos_x0, pos_y0, pos_x1, pos_y1,
                                    fill='#000', outline='#000', tag='discos')
        if color == 'o':
            self.canvas.create_oval(pos_x0, pos_y0, pos_x1, pos_y1,
                                    fill='#FFF', outline='#000', tag='discos')

    def atualizar_discos(self):
        """Atualiza a view do jogo."""
        self.canvas.delete('discos')

        for i in range(1, TABULEIRO_CASA_NUM):
            for j in range(1, TABULEIRO_CASA_NUM):
                self._desenhar_disco(i, j, self.board.get_square_color(i, j))

        self.atualizar_estado(self.board)
