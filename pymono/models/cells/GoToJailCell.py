from pymono.models.Cell import Cell

from pymono.models.cells.JailCell import JailCell


class GoToJailCell(Cell):
    def __init__(self):
        super().__init__("Go To Jail")

    def on_step(self, board_ctrl, on_end):

        current_player_observer = board_ctrl.players_ctrl.current_player

        jail_cell = None
        jail_cell_index = 0

        for i, cell in enumerate(board_ctrl.board.cells):
            if isinstance(cell, JailCell):
                jail_cell = cell
                jail_cell_index = i

        current_player_observer.get().cell_index = jail_cell_index
        current_player_observer.changed()

        jail_cell.on_step(board_ctrl, on_end)
