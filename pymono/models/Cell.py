class Cell:
    def __init__(self, name):
        self.name = name

    def on_step(self, board_ctrl, on_end):
        """
        :param board_ctrl: BoardCtrl
        :param on_end: Function
        """
        on_end()
