"""Inicio da aplicacao."""

from controllers.board_controller import BoardController

CONTROLLER = BoardController()
CONTROLLER.init_game()
