"""Controlador de jogo de Othelo."""

import glob

from views.console_board_view import ConsoleBoardView
from models.board import Board

class BoardController(object):
    """Objeto do controlador de jogo de Othelo."""

    def __init__(self):
        self.board = Board(None)
        self.view = ConsoleBoardView(self, self.board)

        self.white_player = None
        self.black_player = None
        self.atual_player = None
        self.finish_game = 0

    def init_game(self):
        """Inicio o jogo Othelo."""
        self.view.carregar_jogadores_possiveis(self._possible_players_list())
        self.view.put_view_in_main_loop()

    def restart_game(self):
        """Reinicia o jogo Othelo."""
        self.board = Board(None)
        self.view.reiniciar_jogo(self.board)

        self.white_player = None
        self.black_player = None
        self.atual_player = None
        self.finish_game = 0

    def next_round(self):
        """Permite que a IA realize a jogada seguinte."""
        if self.finish_game == 3:
            self.restart_game()
            return

        atual_color = self.atual_player.color
        if self.board.valid_moves(atual_color).__len__() > 0:
            self.board.play(self.atual_player.play(self.board.get_clone()), atual_color)
            self.view.atualizar_discos()
            self.finish_game = 0
        else:
            self.finish_game += 1
        self.atual_player = self._opponent(self.atual_player)

        self.view.atualizar_jogador_atual(self.atual_player.color)

        if self.finish_game == 2:
            self._end_game()

    def _possible_players_list(self):
        return glob.glob('./models/players/*_player.py')

    def select_player(self, player, color):
        """Carrega o arquivo de um jogador para certa cor e retorna seu modulo."""
        module_globals = {}
        execfile(player, module_globals)
        return module_globals[module_globals.keys()[len(module_globals.keys()) - 1]](color)

    def _end_game(self):
        score = self.board.score()
        if score[0] > score[1]:
            self.view.anunciar_vitorioso(self.white_player.__class__.__name__,
                                         self.black_player.__class__.__name__,
                                         score[0], score[1])
        elif score[0] < score[1]:
            self.view.anunciar_vitorioso(self.black_player.__class__.__name__,
                                         self.white_player.__class__.__name__,
                                         score[1], score[0])

        self.finish_game = 3

    def _opponent(self, player):
        if player.color == Board.WHITE:
            return self.black_player

        return self.white_player
