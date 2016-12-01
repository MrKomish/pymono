from pymono.lib.observable import Observable
from pymono.views.CellDetailsView import CellDetailsView


class CellDetailsCtrl:
    def __init__(self, board_ctrl):
        self.board_ctrl = board_ctrl

        self.view = CellDetailsView(self)
        
        self.current_cell = Observable()
