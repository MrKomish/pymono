from pymono.models.Board import Board


class BoardLayout:
    # Each board has its own layout, we can see this layout in res/Monopoly-1000px.png.

    def __init__(self, width, height, cells):
        self.width = width
        self.height = height

        self.cells = cells

    def get_cell_at_position(self, board: Board, x, y):
        for i, cell in enumerate(self.cells):
            cell_x, cell_y, cell_width, cell_height = cell
            if cell_x <= x <= cell_x + cell_width and cell_y <= y <= cell_y + cell_height:
                return board.cells[i]
        return None


class BoardLayoutBuilder:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.bottom_cells = []
        self.left_cells = []
        self.top_cells = []
        self.right_cells = []

        self.bottom_right_cell = (0, 0, 0, 0)
        self.bottom_left_cell = (0, 0, 0, 0)
        self.top_left_cell = (0, 0, 0, 0)
        self.top_right_cell = (0, 0, 0, 0)

        self.corner_size = 0

    def config_corner_cells(self, corner_size):  # Has to be configured first!
        self.corner_size = corner_size

        self.bottom_right_cell = (self.width - corner_size, 0, corner_size, corner_size)
        self.bottom_left_cell = (0, 0, corner_size, corner_size)
        self.top_left_cell = (0, self.height - corner_size, corner_size, corner_size)
        self.top_right_cell = (self.width - corner_size, self.height - corner_size, corner_size, corner_size)

        return self

    def config_bottom_cells(self, width, height):
        self.bottom_cells = []

        for i in range((self.width - 2 * self.corner_size) // width + 1):
            self.bottom_cells.append((self.width - self.corner_size - width * (i + 1), 0, width, height))

        return self

    def config_left_cells(self, width, height):
        self.left_cells = []

        for i in range((self.height - 2 * self.corner_size) // height + 1):
            self.left_cells.append((0, self.corner_size + height * i, width, height))

        return self

    def config_top_cells(self, width, height):
        self.top_cells = []

        for i in range((self.width - 2 * self.corner_size) // width + 1):
            self.top_cells.append((self.corner_size + width * i, self.height - height, width, height))

        return self

    def config_right_cells(self, width, height):
        self.right_cells = []

        for i in range((self.height - 2 * self.corner_size) // height + 1):
            self.right_cells.append((self.width - width, self.height - self.corner_size - height * (i + 1), width, height))

        return self

    def build(self):
        cells = [self.bottom_right_cell] + self.bottom_cells + [self.bottom_left_cell] + self.left_cells + \
                [self.top_left_cell] + self.top_cells + [self.top_right_cell] + self.right_cells

        return BoardLayout(self.width, self.height, cells)
