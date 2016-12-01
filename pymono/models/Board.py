class Board:
    def __init__(self, bottom_right_cell, bottom_cells, bottom_left_cell, left_cells,
                 top_left_cell, top_cells, top_right_cells, right_cells):
        self.bottom_right_cell = bottom_right_cell
        self.bottom_cells = bottom_cells
        self.bottom_left_cell = bottom_left_cell
        self.left_cells = left_cells
        self.top_left_cell = top_left_cell
        self.top_cells = top_cells
        self.top_right_cell = top_right_cells
        self.right_cells = right_cells

    @property
    def cells(self):
        return [self.bottom_right_cell] + self.bottom_cells + [self.bottom_left_cell] + self.left_cells + \
               [self.top_left_cell] + self.top_cells + [self.top_right_cell] + self.right_cells
